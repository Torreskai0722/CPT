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

#from skimage.metrics import structural_similarity as ssim
from torch.profiler import profile, record_function, ProfilerActivity
import cProfile

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def create_model(num_classes):
    # mobileNetv2+faster_RCNN
    # backbone = MobileNetV2().features
    # backbone.out_channels = 1280
    #
    # anchor_generator = AnchorsGenerator(sizes=((32, 64, 128, 256, 512),),
    #                                     aspect_ratios=((0.5, 1.0, 2.0),))
    #
    # roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0'],
    #                                                 output_size=[7, 7],
    #                                                 sampling_ratio=2)
    #
    # model = FasterRCNN(backbone=backbone,
    #                    num_classes=num_classes,
    #                    rpn_anchor_generator=anchor_generator,
    #                    box_roi_pool=roi_pooler)

    # resNet50+fpn+faster_RCNN
    # 注意，这里的norm_layer要和训练脚本中保持一致
    backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d)
    model = FasterRCNN(backbone=backbone, num_classes=num_classes, rpn_score_thresh=0.2)

    return model

def time_synchronized():
    torch.cuda.synchronize(torch.device("cuda:0")) if torch.cuda.is_available() else None
    return time.time()


class fasterrcnn_node:
    
    def __init__(self):
        
        # get devices
        # os.environ["CUDA_AVAILABLE_DEVICES"] = "1"
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # device = torch.device("cpu")
        print("using {} device.".format(self.device))
        # create model
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        #self.model = create_model(num_classes=21)
        # load train weights
        #train_weights = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_object_detection/faster_rcnn/save_weights/resNetFpn-model-14.pth"
        # train_weights = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_object_detection/faster_rcnn/save_weights/fasterrcnn_voc2012.pth"
        #assert os.path.exists(train_weights), "{} file dose not exist.".format(train_weights)
        #self.model.load_state_dict(torch.load(train_weights, map_location=self.device)["model"])
        self.model.to(self.device)

        # read class_indict
        # label_json_path = '/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/faster_rcnn/pascal_voc_classes.json'
        # assert os.path.exists(label_json_path), "json file {} dose not exist.".format(label_json_path)
        # json_file = open(label_json_path, 'r')
        # class_dict = json.load(json_file)
        # self.category_index = {v: k for k, v in class_dict.items()}

        print(os.getpid())

        # load image
        # original_img = cv2.imread("/home/nvidia/Downloads/data_odometry_color/dataset/sequences/02/image_2/000000.png", cv2.IMREAD_COLOR)
        original_img = cv2.imread("/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/faster_rcnn/test.png", cv2.IMREAD_COLOR)
        # original_img = cv2.imread("test.jpeg", cv2.IMREAD_COLOR)
        # print(original_img.shape)
        self.former_img = original_img
        original_img = pilim.fromarray(original_img)
        # print(original_img.shape)
        # self.shape = original_img.shape
        # original_img = cv2.imread("/home/nvidia/catkin_ws/src/video_stream_opencv/scripts/img.png",cv2.IMREAD_COLOR)

        # from pil image to tensor, do not normalize image
        self.data_transform = transforms.Compose([transforms.ToTensor()])
        # self.data_transform = transforms.Compose([transforms.Resize(size = (50,30)),transforms.ToTensor()])
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
        self.status_pub = rospy.Publisher('fasterrcnn_process_status', ProcessStatus, queue_size=1)
        self.current_seq = 0
        # rospy.init_node('fasterrcnn_node')
        # rospy.spin()

    def callback(self, frame):
        # sf = rospy.get_param("object_skip_frames")
        sf = 0
        delay = frame.header.seq-self.current_seq
        # print(delay)
        # if sf == 0 and delay < rospy.get_param("delay_thresh"):
        if sf == 0:
            with torch.no_grad():
                with record_function("model_inference_"+str(frame.header.seq)):
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
                    # print(self.device)
                    t_3 = time_synchronized()

                    pid = os.getpid()
                    msg = get_proc_status(pid)
                    # msg.header.stamp = rospy.Time.now()
                    msg.header.stamp = frame.header.stamp
                    msg.imgseq = frame.header.seq
                    msg.runtime = t_3-t_1

                    if predictions != [0]:
                        #pt = predictions["time"]
                        #midres = predictions["midres"]
                        # print("inference+NMS time: {}".format(t_end - t_start))

                        predict_boxes = predictions["boxes"].to("cpu").numpy()
                        predict_classes = predictions["labels"].to("cpu").numpy()
                        predict_scores = predictions["scores"].to("cpu").numpy()

                        #msg.proposals = midres[0]
                        #msg.objects = midres[1]
                        msg.probability = predict_scores
                            
                        # rospy.loginfo(msg)
                    self.status_pub.publish(msg)
                    t_4 = time_synchronized()

                    # print(midres,predict_boxes,predict_classes,predict_scores)
                    # print(t_2-t_1, t_3-t_2, t_4-t_3, t_4-t_1)
                    # print(frame.header.seq)
                    print(frame.header.stamp,t_4-t_1)
                    # print(t_2-t_1, t_3-t_2, pt[0],pt[1],pt[2],pt[3], t_3-t_1,midres[0],midres[1])
                    #if msg.scheduling_policy == "SCHED_DEADLINE":
                        #print(1000*(t_3-t_1))
        elif sf < 0:
            rospy.set_param("object_skip_frames", 0)
        elif sf > 0:
            rospy.set_param("object_skip_frames", sf-1)
        self.current_seq = frame.header.seq


if __name__ == '__main__':
    rospy.init_node('fasterrcnn_node')
    ic = fasterrcnn_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()
