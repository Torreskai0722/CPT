#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import cv2
import os
import time
import json
import torch
import torchvision
from PIL import Image
from torchvision import transforms
import numpy as np
import random
from random import choice
# from proc_util import get_proc_status
from mmcv.parallel import MMDataParallel, MMDistributedDataParallel
from mmdet.apis import multi_gpu_test, single_gpu_test
from torch.nn import DataParallel
from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector, show_result_pyplot)

from util import time_synchronized, mmdet_results, analyze_iou, get_iou, get_max_iou, img_diff, img_ssim
import asyncio
from ssim import compute_ssim
import glob

# class_name = ["pedestrian", "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle", "traffic light", "traffic sign"]

def image_paths(folder_name):
    VIDEO_FILE = '/home/mobilitylab/dataset/bdd100k_videos_test_00/bdd100k/videos/images/'

    # a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf', 
    # 'cac07407-ba37148a', 'cac07407-e969f06a', 'cac07407-bc0b048a', 'cac07407-15b814db', 
    # 'cac07407-76e4c968', 'cac07407-fe32e494']
    
    # a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']

    # a = ['cac07407-0396e053']

    paths = []
    pd = glob.glob(os.path.join(VIDEO_FILE + str(folder_name) + "/", '*.jpg'))
    paths.extend(pd)
    paths = sorted(paths, key=os.path.getmtime)
    print(len(paths))

    return paths

def cv2_img_diff(prev_frame,curr_frame):
    diff = cv2.absdiff(curr_frame, prev_frame)
    non_zero_count = np.count_nonzero(diff)

    a = curr_frame.shape
    return non_zero_count / (a[0]*a[1]*a[2])

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
        
        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        t0 = inference_detector(self.model0, img)

        self.count = 0
        self.former_res = []
        self.prev_frame = []
        self.detection_boxes = []
        self.detection_labels = []

    def test(self, frame):
        t1 = time_synchronized()
        result = inference_detector(self.model0, frame)
        bboxes, labels, names = mmdet_results(result)
        self.detection_boxes.append(bboxes)
        self.detection_labels.append(labels)
        
        t3 = time_synchronized()
        print(t3-t1, self.count)
        del frame

if __name__ == '__main__':
    a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']
    
    for i in a:
        ic = mmdet_node()
        paths = image_paths(i)
        frame_count = []
        for count, path in enumerate(paths):
            img = Image.open(path)
            ic.test(np.asarray(img))
            frame_count.append(count)
            # print(count)

        np.save(i +'-detection_boxes.npy', ic.detection_boxes)
        np.save(i + '-detection_labels.npy', ic.detection_labels)
        # np.save(i + '-frame_count.npy', frame_count)