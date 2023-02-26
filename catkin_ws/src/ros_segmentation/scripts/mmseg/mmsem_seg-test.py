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
from torchvision.ops import masks_to_boxes
import numpy as np
import random
from random import choice
from proc_util import get_proc_status
from timer_repeat import RepeatedTimer
from mmseg.apis import inference_segmentor, init_segmentor
import threading
import sys
import signal
from mask_to_bbox import mask_to_bbox
import collections
import mmcv
from collections import defaultdict
from util import time_synchronized, mmdet_results, analyze_iou, get_iou, get_max_iou, img_diff, img_ssim
import glob
# from torchvision.io import read_image
# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

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

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

def quit(signum, frame):
    print('stop segmentation node')
    sys.exit()

# 0:  road
# 1:  sidewalk
# 2:  building
# 3:  wall
# 4:  fence
# 5:  pole
# 6:  traffic light
# 7:  traffic sign
# 8:  vegetation
# 9:  terrain
# 10: sky
# 11: person
# 12: rider
# 13: car
# 14: truck
# 15: bus
# 16: train
# 17: motorcycle
# 18: bicycle

class mmsem_seg_node:
    
    def __init__(self):
        
        # get devices
        # self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cuda:3")
        # print("using {} device.".format(self.device))
        # create model
        config_file = "/home/mobilitylab/catkin_ws/src/ros_segmentation/scripts/mmseg/sem_seg/configs/sem_seg/deeplabv3+_r50-d8_769x769_40k_sem_seg_bdd100k.py"
        checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/sem_seg/models/deeplabv3+_r50-d8_769x769_40k_sem_seg_bdd100k.pth"
        # self.model0 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:0"))
        self.model1 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:3"))

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        t1 = inference_segmentor(self.model1, img)
        
        self.count = 0
        
        self.runtime = 0
        self.detection_boxes = []
        
    def test(self,frame):
        img = np.array(frame)
        t1 = time_synchronized()
        result = inference_segmentor(self.model1,img)
        t2 = time_synchronized()
        seg_b = self.convert_to_box(result[0]).cpu().numpy()
        self.detection_boxes.append(seg_b)

        del img
        self.count += 1
        t3 = time_synchronized()
        self.runtime = t2-t1
        
        print(t2-t1, t3-t2,t3-t1, self.count)
    
    def convert_to_box(self,img):
        res  = torch.from_numpy(img).float().to(self.device)
        obj_ids = torch.unique(res)
        obj_ids = obj_ids[6:]
        
        masks = res == obj_ids[:,None,None]
        boxes = masks_to_boxes(masks)
        
        return boxes.cpu()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']
    
    for i in a:
        ic = mmsem_seg_node()
        paths = image_paths(i)
        frame_count = []
        for count, path in enumerate(paths):
            img = Image.open(path)
            ic.test(np.asarray(img))
            frame_count.append(count)
            # print(count)

        np.save(i +'-detection_boxes.npy', ic.detection_boxes)
        # np.save(i + '-detection_labels.npy', ic.detection_labels)
        # np.save(i + '-frame_count.npy', frame_count)
