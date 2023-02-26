#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import roslib
roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
import os
from ros_referee.msg import ProcessStatus
import time
import json
import torch
import torchvision
from PIL import Image as pilim
from torchvision import transforms
import numpy as np
import random
from random import choice
from proc_util import get_proc_status
from mmcv.parallel import MMDataParallel, MMDistributedDataParallel
from mmdet.apis import multi_gpu_test, single_gpu_test
from torch.nn import DataParallel

from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector, show_result_pyplot)

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


class mmdet_node:
    
    def __init__(self):
        
        # get devices
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # device = torch.device("cpu")
        print("using {} device.".format(self.device))
        # create model
        config_file = "/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/mmdet/bdd100k-models/det/configs/det/faster_rcnn_r101_fpn_dconv_3x_det_bdd100k.py"
        checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/det/models/faster_rcnn_r101_fpn_dconv_3x_det_bdd100k.pth"
        self.model0 = init_detector(config_file, checkpoint_file, torch.device("cuda:0"))
        self.model1 = init_detector(config_file, checkpoint_file, torch.device("cuda:1"))
        self.model2 = init_detector(config_file, checkpoint_file, torch.device("cuda:2"))
        self.model3 = init_detector(config_file, checkpoint_file, torch.device("cuda:3"))
        # self.model0 = DataParallel(self.model0)
        # self.model1 = DataParallel(self.model1)
        # self.model2 = DataParallel(self.model2)
        # self.model3 = DataParallel(self.model3)
        #self.model = init_detector(rospy.get_param("mmdet_config"), rospy.get_param("mmdet_checkpoint"), self.device)

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        # img = torch.from_numpy(img)
        # img = img.half()
        t0 = inference_detector(self.model0, img)
        t1 = inference_detector(self.model1, img)
        t2 = inference_detector(self.model2, img)
        t3 = inference_detector(self.model3, img) 
        
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('mmdet_process_status', ProcessStatus, queue_size=1)

        self.count = 0

    def callback(self, frame):
        if frame.header.seq % 3 == 1:
            # print(type(frame.data))
            # print(int.from_bytes(frame.data))
            t1 = time_synchronized()
            # t1 = time.time()
            img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
            t2 = time_synchronized()
            # t2 = time.time()
            # print(ssim(test_img,test_img))
            # print(img)
            # img = pilim.fromarray(img)
            # print(img)
            # img = cv2.imread(test_img, cv2.IMREAD_COLOR)
            # test a single image
            models = [self.model0, self.model1, self.model2, self.model3]
            model = models[frame.header.seq % 4]
            result = inference_detector(self.model1, img)
            # print(model)
            del img
            self.count += 1
            t3 = time_synchronized()
            # t3 = time.time()
            # print(result[-1])
            pid = os.getpid()
            print(pid, frame.header.seq, t2-t1, t3-t2, self.count)
            # show the results
            # show_result_pyplot(
            #     self.model,
            #     img,
            #     result,
            #     palette="coco",
            #     score_thr=0.5)


if __name__ == '__main__':
    rospy.init_node('mmdet_node_1')
    ic = mmdet_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
