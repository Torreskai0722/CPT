#!/usr/bin/env python3.6
import roslib

roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import psutil
import os
from ros_referee.msg import ProcessStatus
import time
import json
import io

import torch
import torchvision
from PIL import Image as pilim
import matplotlib.pyplot as plt

from torchvision import transforms
from network_files import FasterRCNN, FastRCNNPredictor, AnchorsGenerator
from backbone import resnet50_fpn_backbone, MobileNetV2
from draw_box_utils import draw_box

# from jetson_benchmarks import utilities, benchmark_argparser
import sys
import glob
import numpy as np

from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post
# from PIL import Image
from matplotlib import cm
# from ssim import compute_ssim

from skimage.metrics import structural_similarity as ssim

from network_files import MaskRCNN
from backbone import resnet50_fpn_backbone


def create_model(num_classes):
    backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d)
    model = MaskRCNN(backbone,
                     num_classes=num_classes,rpn_score_thresh=0.5)

    return model

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class maskrcnn_node:
    
    def __init__(self):
        
        # get devices
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # device = torch.device("cpu")
        print("using {} device.".format(self.device))
        # create model
        self.model = create_model(num_classes=21)
        # load train weights
        train_weights = "/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/faster_rcnn/model_25.pth"
        assert os.path.exists(train_weights), "{} file dose not exist.".format(train_weights)
        self.model.load_state_dict(torch.load(train_weights, map_location=self.device)["model"])
        self.model.to(self.device)

        # read class_indict
        # label_json_path = '/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/faster_rcnn/pascal_voc_classes.json'
        # assert os.path.exists(label_json_path), "json file {} dose not exist.".format(label_json_path)
        # json_file = open(label_json_path, 'r')
        # class_dict = json.load(json_file)
        # self.category_index = {v: k for k, v in class_dict.items()}

        # load image
        # original_img = cv2.imread("/home/nvidia/Downloads/data_odometry_color/dataset/sequences/02/image_2/000000.png", cv2.IMREAD_COLOR)
        original_img = cv2.imread("/home/mobilitylab/projects/PDNN/data_odometry_color/dataset/sequences/09/image_2/000000.png", cv2.IMREAD_COLOR)
        # print(original_img.shape)
        self.former_img = original_img
        original_img = pilim.fromarray(original_img)
        # print(original_img.shape)
        # self.shape = original_img.shape
        # original_img = cv2.imread("/home/nvidia/catkin_ws/src/video_stream_opencv/scripts/img.png",cv2.IMREAD_COLOR)

        # from pil image to tensor, do not normalize image
        self.data_transform = transforms.Compose([transforms.ToTensor()])
        img = self.data_transform(original_img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0)
        
        self.model.eval()  # 进入验证模式
        with torch.no_grad():
            # init
            img_height, img_width = img.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            self.model(init_img)
            
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('maskrcnn_process_status', ProcessStatus, queue_size=1)
        # rospy.init_node('fasterrcnn_node')
        # rospy.spin()

    def callback(self, frame):
        # t_curr = rospy.Time.now()
        # t = data.header.stamp
        # delay = t_curr.secs - t.secs + (t_curr.nsecs - t.nsecs) * 0.000000001
        # print(delay)
        
        # test_img = Image.open(path).convert('RGB')
        with torch.no_grad():
            t_1 = time_synchronized()
            # print(frame.width,frame.height,type(frame.width))
            # print(type(frame.data))
            test_img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
            # print(test_img.shape)

            # img_bwa = cv2.bitwise_and(self.former_img,test_img)
            # img_bwo = cv2.bitwise_or(self.former_img,test_img)
            # img_bwx = cv2.bitwise_xor(self.former_img,test_img)

            # cv2.imshow("Bitwise AND of Image 1 and 2", img_bwa)
            # cv2.imshow("Bitwise OR of Image 1 and 2", img_bwo)
            # cv2.imshow("Bitwise XOR of Image 1 and 2", img_bwx)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # print(ssim(test_img,test_img))
            test_img = pilim.fromarray(test_img)
            self.former_img = test_img

            # cv2.imwrite("test.png",test_img)
            tran_img = self.data_transform(test_img)
            tran_img = torch.unsqueeze(tran_img, dim=0)
            t_2 = time_synchronized()

            # res =  model(img.to(device))
            predictions = self.model(tran_img.to(self.device))[0]
            t_3 = time_synchronized()

            if predictions != [0]:
                pt = predictions["time"]
                midres = predictions["midres"]
                # print("inference+NMS time: {}".format(t_end - t_start))

                predict_boxes = predictions["boxes"].to("cpu").numpy()
                predict_classes = predictions["labels"].to("cpu").numpy()
                predict_scores = predictions["scores"].to("cpu").numpy()

                # if len(predict_boxes) == 0:
                #     print("No objects!")

                # draw_box(test_img,
                #     predict_boxes,
                #     predict_classes,
                #     predict_scores,
                #     self.category_index,
                #     thresh=0.05,
                #     line_thickness=3)
                # plt.imshow(test_img)
                # plt.show(block=False) 
            else:
                midres = [0, 0]
                pt = [0,0,0,0]
                predict_scores = [0]
                predict_boxes = [0]
                predict_classes = [0]

            t_4 = time_synchronized()

            # print(midres,predict_boxes,predict_classes,predict_scores)
            # print(t_2-t_1, t_3-t_2, t_4-t_3, t_4-t_1)
            # print(t_4-t_1)

            print(t_2-t_1, t_3-t_2, t_4-t_3, pt[0],pt[1],pt[2],pt[3], t_4-t_1,midres[0],midres[1])

            
            
        pid = os.getpid()
        msg = get_proc_status(pid)
        # msg.header.stamp = rospy.Time.now()
        msg.header.stamp = frame.header.stamp
        msg.proposals = midres[0]
        msg.objects = midres[1]
        msg.probability = predict_scores
        msg.runtime = t_4-t_1
            
        # rospy.loginfo(msg)
        self.status_pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('maskrcnn_node')
    ic = maskrcnn_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()
