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
# from jetson_benchmarks import utilities, benchmark_argparser
import sys
import glob
import numpy as np
from proc_util import get_proc_status
from matplotlib import cm

# from PIL import Image

from network_files import RetinaNet
from backbone import resnet50_fpn_backbone, LastLevelP6P7
from draw_box_utils import draw_box

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)


def create_model(num_classes):
    # resNet50+fpn+retinanet
    # 注意，这里的norm_layer要和训练脚本中保持一致
    backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d,
                                     returned_layers=[2, 3, 4],
                                     extra_blocks=LastLevelP6P7(256, 256))
    model = RetinaNet(backbone, num_classes)

    return model

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class retinanet_node:
    
    def __init__(self):
        
        # get devices
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # device = torch.device("cpu")
        print("using {} device.".format(self.device))
        
        # create model
        # self.model = create_model(num_classes=20)
        self.model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
        # train_weights = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_object_detection/retinaNet/save_weights/resNetFpn-model-14.pth"
        # assert os.path.exists(train_weights), "{} file dose not exist.".format(train_weights)
        # self.model.load_state_dict(torch.load(train_weights, map_location=self.device)["model"])
        self.model.to(self.device)

        label_json_path = '/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/retinanet/pascal_voc_classes.json'
        assert os.path.exists(label_json_path), "json file {} dose not exist.".format(label_json_path)
        json_file = open(label_json_path, 'r')
        class_dict = json.load(json_file)
        json_file.close()
        category_index = {v: k for k, v in class_dict.items()}

        # load image
        # original_img = cv2.imread("/home/nvidia/Downloads/data_odometry_color/dataset/sequences/02/image_2/000000.png", cv2.IMREAD_COLOR)
        original_img = cv2.imread("/home/mobilitylab/projects/PDNN/data_odometry_color/dataset/sequences/09/image_2/000000.png", cv2.IMREAD_COLOR)
        # print(original_img.shape)
        self.former_img = original_img
        original_img = pilim.fromarray(original_img)

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
    
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('retinanet_process_status', ProcessStatus, queue_size=1)

    def callback(self, frame):
        sf = rospy.get_param("object_skip_frames")
        if sf == 0:
            with torch.no_grad():
                t_1 = time_synchronized()
                # print(frame.width,frame.height,type(frame.width))
                # print(type(frame.data))
                test_img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)

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

                predict_boxes = predictions["boxes"].to("cpu").numpy()
                predict_classes = predictions["labels"].to("cpu").numpy()
                predict_scores = predictions["scores"].to("cpu").numpy()
                # print(len(predict_scores))

                # if predictions != [0]:
                #     pt = predictions["time"]
                #     midres = predictions["midres"]
                    # print("inference+NMS time: {}".format(t_end - t_start))

                    # predict_boxes = predictions["boxes"].to("cpu").numpy()
                    # predict_classes = predictions["labels"].to("cpu").numpy()
                    # predict_scores = predictions["scores"].to("cpu").numpy()

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
                # else:
                #     midres = [0, 0]
                #     predict_scores = [0]
                #     predict_boxes = [0]
                #     predict_classes = [0]

                # t_4 = time_synchronized()
                print(t_2-t_1, t_3-t_2, t_3-t_1)

                # print(midres,predict_boxes,predict_classes,predict_scores)

                # print(t_2-t_1, t_3-t_2, t_4-t_3, pt[1]-pt[0], pt[2]-pt[1], pt[3]-pt[2], pt[4]-pt[3], pt[5]-pt[4], pt[6]-pt[5])
    
            pid = os.getpid()
            msg = get_proc_status(pid)
            # msg.header.stamp = rospy.Time.now()
            msg.header.stamp = frame.header.stamp
            # msg.proposals = midres[0]
            # msg.objects = midres[1]
            # msg.probability = predict_scores
            msg.runtime = t_3-t_1
                
            # rospy.loginfo(msg)
            self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("object_skip_frames", 0)
        else:
            rospy.set_param("object_skip_frames", sf-1)


if __name__ == '__main__':
    rospy.init_node('retinanet_node')
    ic = retinanet_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")