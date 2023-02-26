#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import cv2
import os
import time
import json
import torch
import torchvision
from torchvision.ops import masks_to_boxes
from PIL import Image
from torchvision import transforms
from mask_to_bbox import mask_to_bbox
import numpy as np
import sys
import signal
from proc_util import get_proc_status
from timer_repeat import RepeatedTimer
from mmseg.apis import inference_segmentor, init_segmentor
import glob
from collections import defaultdict
from util import time_synchronized, mmdet_results, analyze_iou, get_iou, get_max_iou, img_diff, img_ssim

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
    print('stop drivable detection')
    sys.exit()

# 0: direct
# 1: alternative
# 2: background

def conver_to_box(img):
    object_set = {0,1}
    count = 0
    out_file = "./test_imgs/test.jpg"
    #mmcv.imwrite(img, out_file)
    for i,row in enumerate(img):
        for j,c in enumerate(row):
            if c == 2:
                img[i][j] = 0
            else:
                img[i][j] = 255
                count += 1
    
    # print(count)
    img_boxes = mask_to_bbox(img)
    # print(len(img_boxes))
    
    return img_boxes

class mmdrivable_node:
    
    def __init__(self):
        self.device = torch.device("cuda:2")
        # config_file = "/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/mmdrivable/drivable/configs/drivable/dnl_r50-d8_512x1024_80k_drivable_bdd100k.py"
        # checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/drivable/models/dnl_r50-d8_512x1024_80k_drivable_bdd100k.pth"
        config_file = "/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/mmdrivable/drivable/configs/drivable/dnl_r50-d8_512x1024_40k_drivable_bdd100k.py"
        checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/drivable/models/dnl_r50-d8_512x1024_40k_drivable_bdd100k.pth"
        self.model2 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:2"))

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        t2 = inference_segmentor(self.model2, img)

        self.count = 0
        self.runtime = 0
        self.detection_boxes = []
    
    def test(self,frame):
        t1 = time_synchronized()
        img = np.array(frame)

        result = inference_segmentor(self.model2, img)
        t2 = time_synchronized()
        lane_b = self.convert_to_box(result[0]).cpu().numpy()
        print(lane_b)
        self.detection_boxes.append(lane_b)
        del img

        self.count += 1
        t3 = time_synchronized()
        self.runtime = t3-t1
        print(t2-t1, t3-t2, t3-t1, self.count)
    
    def convert_to_box(self,img):
        res  = torch.from_numpy(img).float().to(self.device)
        obj_ids = torch.unique(res)
        obj_ids = obj_ids[:2]
        
        masks = res == obj_ids[:,None,None]
        boxes = masks_to_boxes(masks)
        
        return boxes.cpu()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']
    
    for i in a:
        ic = mmdrivable_node()
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