#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import roslib
roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
import os
from ros_referee.msg import ProcessStatus
from darknet_ros_msgs.msg import BoundingBoxes, BoundingBox
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

from util import time_synchronized, mmdet_results, analyze_iou, get_iou, get_max_iou, img_diff, img_ssim
import asyncio
from ssim import ssim
import os
import signal
import sys
from collections import defaultdict
# class_name = ["pedestrian", "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle", "traffic light", "traffic sign"]
from timer_repeat import RepeatedTimer
from time import sleep

# 1: pedestrian
# 2: rider
# 3: car
# 4: truck
# 5: bus
# 6: train
# 7: motorcycle
# 8: bicycle
# 9: traffic light
# 10: traffic sign

f_mmdet = []

def quit(signum, frame):
    print('stop detection')
    np.save('mmdet_boxes-referee-011123.npy', f_mmdet)
    sys.exit()

class mmdet_node:
    
    def __init__(self):
        # os.environ["CUDA_VISIBLE_DEVICES"]="0,1,2,3"
        config_file = "/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/mmdet/bdd100k-models/det/configs/det/faster_rcnn_r101_fpn_dconv_3x_det_bdd100k.py"
        checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/det/models/faster_rcnn_r101_fpn_dconv_3x_det_bdd100k.pth"
        # config_file = "/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/mmdet/bdd100k-models/det/configs/det/faster_rcnn_r50_fpn_1x_det_bdd100k.py"
        # checkpoint_file = "https://dl.cv.ethz.ch/bdd100k/det/models/faster_rcnn_r50_fpn_1x_det_bdd100k.pth"
        self.model0 = init_detector(config_file, checkpoint_file, torch.device("cuda:1"))
        # self.model1 = init_detector(config_file, checkpoint_file, torch.device("cuda:1"))
        # self.model2 = init_detector(config_file, checkpoint_file, torch.device("cuda:2"))
        # self.model3 = init_detector(config_file, checkpoint_file, torch.device("cuda:3"))
        

        #self.model = init_detector(rospy.get_param("mmdet_config"), rospy.get_param("mmdet_checkpoint"), self.device)

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)

        t0 = inference_detector(self.model0, img)
        # t1 = inference_detector(self.model1, img)
        # t2 = inference_detector(self.model2, img)
        # t3 = inference_detector(self.model3, img) 
        
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('mmdet_process_status', ProcessStatus, queue_size=1)
        self.track_sub = rospy.Subscriber("/object_tracker", BoundingBoxes, self.track_callback)

        self.count = 0
        tree = lambda: defaultdict(tree)
        self.former_res = []
        self.prev_frame = []
        self.frame_cache = Image()
        self.label_cache = []
        self.bboxes_cache = tree()
        self.tracks_cache = tree()
        self.stamp_cache = tree()
        # self.pid = os.getpid()
        self.runtime = 0

    def track_callback(self, tracks):
        seq = tracks.header.seq
        bboxes = tracks.bounding_boxes
        
        boxes_arr = []
        id_arr = []
        for t in bboxes:
            b = [t.xmin,t.ymin,t.xmax,t.ymax]
            id_arr.append(t.id)
            boxes_arr.append(b)
        #print(boxes_arr)

        self.tracks_cache[tracks.image_header.seq]=boxes_arr
        self.stamp_cache[tracks.image_header.seq]=tracks.image_header.stamp

    def callback(self, frame):
        self.frame_cache = frame
        frame_id = rospy.get_param("frame_id")
        frame_delay = frame_id - frame.header.seq
        
        ## DeepReferee keyframe check
        if rospy.get_param("testing_case") == 3 and frame_delay <= rospy.get_param("object_delay"):
            if rospy.get_param("no_keyframe"):
                self.run(frame, frame_id,frame_delay,3)
            else:
                deadline_delay = frame_id - rospy.get_param("object_last_keyframe")
                if frame.encoding == "key-ssim" or rospy.get_param("object_keyframe_detection") or deadline_delay > rospy.get_param("object_deadline") or rospy.get_param("traffic_scenario"):
                    # print("keyframe_mmdet")
                    rospy.set_param("object_last_keyframe", frame.header.seq)
                    self.run(frame, frame_id,frame_delay,3)

        ## Baseline check
        elif rospy.get_param("testing_case") == 1:
            self.run(frame, frame_id,frame_delay,1)

        ## MTC check
        elif rospy.get_param("testing_case") == 2 and frame_delay <= rospy.get_param("object_delay"):
            self.run(frame, frame_id,frame_delay,2)
    
    def run(self,frame,frame_id,frame_delay,case):
        # frame_id = rospy.get_param("frame_id")
        t1 = time_synchronized()
        img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
        t2 = time_synchronized()
        result = inference_detector(self.model0, img)
        bboxes, labels, names = mmdet_results(result)

        # f_mmdet.append([frame.header.seq,bboxes])

        ## define traffic scanerio based on detection
        ratio = (names.count('rider') + names.count('pedestrian')) / len(names)
        if ratio > 0.9:
            rospy.set_param("traffic_scenario", True)
            # print(ratio)
            # print(names.count('rider'), names.count('pedestrian'), len(names))
        
        self.labels_cache = labels
        self.bboxes_cache[frame.header.seq] = bboxes
        del img
        self.count += 1

        t3 = time_synchronized()
        self.runtime = t3-t1
        
        print(frame_id,frame.header.seq,frame_delay,t2-t1,t3-t2,t3-t1,self.count)

        if case != 3 or (case == 3 and rospy.get_param("prediction") == False):
            msg = ProcessStatus()
            msg.data = np.array(bboxes,dtype=np.uint32).flatten().tolist()
            msg.header.stamp = frame.header.stamp
            msg.imgseq = frame.header.seq
            msg.runtime = self.runtime
            msg.app = "mmdet"
            #msg.objects = len(self.labels_cache)
            # msg.probability = self.bboxes_cache[:,-1]
            self.status_pub.publish(msg)

    
    def mmdet_pub(self):
        if self.count != 0 and rospy.get_param("data_pub_finish") == False:
            # msg = get_proc_status(self.pid)
            msg = ProcessStatus()

            k,v = sorted(self.bboxes_cache.items())[-1]
            # k_, v_ = sorted(self.tracks_cache.items())[-1]
            # print(k,k_)
            bboxes = np.asarray(v[:,:-1],dtype=np.uint32)
            scores = np.asarray(v[:,-1])
            # for ki in range(k,k_):
            if self.tracks_cache[k]:
                track_boxes = np.asarray(self.tracks_cache[k])
                for index,box in enumerate(bboxes):
                    _,miou,nmax = get_max_iou(track_boxes,box)
                    # print(miou,nmax)
                    if miou > 0.5:
                        bboxes[index] = track_boxes[nmax]
            msg.data = bboxes.flatten().tolist()
            if self.stamp_cache[k]:
                msg.header.stamp = self.stamp_cache[k]
            else:
                msg.header.stamp = self.frame_cache.header.stamp
            msg.header.seq = k
            msg.imgseq = k
            msg.runtime = self.runtime
            msg.app = "mmdet"
            self.status_pub.publish(msg)
            frame_id = rospy.get_param("frame_id")
            f_mmdet.append([frame_id-1,bboxes])
            # print("Publishing detection results!")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    rospy.init_node('mmdet_node_0')
    ic = mmdet_node()

    print("timely function starting...")
    st = 1/rospy.get_param("image_fps")
    if rospy.get_param("testing_case") == 3 and rospy.get_param("prediction"):
        print("prediction starts")
        rt = RepeatedTimer(st, ic.mmdet_pub) # it auto-starts, no need of rt.start()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
