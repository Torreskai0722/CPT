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
# from torchvision.io import read_image
# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

f_mmsem = []

def quit(signum, frame):
    print('stop segmentation node')
    np.save('mmsem_boxes-referee-011123.npy', f_mmsem)
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
        # self.model2 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:2"))
        # self.model3 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:3"))
        #self.model = init_detector(rospy.get_param("mmdet_config"), rospy.get_param("mmdet_checkpoint"), self.device)

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        # t0 = inference_segmentor(self.model0, img)
        t1 = inference_segmentor(self.model1, img)
        # t2 = inference_segmentor(self.model2, img)
        # t3 = inference_segmentor(self.model3, img)
        
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.track_sub = rospy.Subscriber("/object_tracker", BoundingBoxes, self.track_callback)
        self.status_pub = rospy.Publisher('mmsem_seg_process_status', ProcessStatus, queue_size=1)

        tree = lambda: defaultdict(tree)
        self.count = 0
        self.frame_cache = Image()
        #self.pid = os.getpid()
        self.runtime = 0
        self.seg_box = tree()
        self.stamp_cache = tree()
        self.prev_tracks = BoundingBoxes()
        self.track_cache = []
        self.results_cache = []
        
        self.velocity = tree()
        

    def track_callback(self, tracks):
        seq = tracks.header.seq
        bboxes = tracks.bounding_boxes
        prev_bboxes = self.prev_tracks.bounding_boxes
        # print(len(bboxes))
        # print(seq)
        self.stamp_cache[tracks.image_header.seq]=tracks.image_header.stamp
        
        boxes_arr = []
        id_arr = []
        for t in bboxes:
            b = [t.xmin,t.ymin,t.xmax,t.ymax]
            id_arr.append(t.id)
            boxes_arr.append(b)
        # print(id_arr)

        # velocity_one = {}

        if len(prev_bboxes) != 0:
            for i,track in enumerate(bboxes):
                for j,prev_track in enumerate(prev_bboxes):
                    if track.id == prev_track.id:
                        v = [track.xmin-prev_track.xmin, track.ymin-prev_track.ymin,track.xmax-prev_track.xmax,
                        track.ymax-prev_track.ymax]
                        self.velocity[seq][track.id] = v

        if self.seg_box.items():
            a = sorted(self.seg_box.items())[-1]
            k,v = a
            # print(type(v))
            v = v.numpy()
            # print(k, v)
            # print(self.velocity[k].items())
            for index, box in enumerate(v):
                if boxes_arr is [] or box is []:
                    print("None")
                    continue
                else:
                    _, maxiou,nmax = get_max_iou(np.asarray(boxes_arr),np.asarray(box))
                    # print(maxiou,nmax)
                    if maxiou > 0.4:
                        if self.velocity[k][id_arr[nmax]]:
                            v[index] = np.asarray(boxes_arr[nmax]) + np.asarray(self.velocity[k][id_arr[nmax]])
                            # print(v[index])
    
        self.prev_tracks = tracks

    def callback(self, frame):
        self.frame_cache = frame
        frame_id = rospy.get_param("frame_id")
        frame_delay = frame_id - frame.header.seq
        # print(rospy.get_param("frame_id"),frame.header.seq,frame_delay)

        ## DeepReferee keyframe check
        if rospy.get_param("testing_case") == 3 and frame_delay <= rospy.get_param("segmentation_delay"):
            if rospy.get_param("no_keyframe"):
                self.run(frame, frame_id,frame_delay,3)
            else:
                deadline_delay = frame_id - rospy.get_param("segmentation_last_keyframe")
                if frame.encoding == "key-ssim" or rospy.get_param("segmentation_keyframe_detection") or deadline_delay > rospy.get_param("segmentation_deadline") or rospy.get_param("traffic_scenario"):
                    # print("keyframe_mmsem_seg")
                    rospy.set_param("segmentation_last_keyframe",frame.header.seq)
                    self.run(frame, frame_id,frame_delay,3)

        ## Baseline check
        elif rospy.get_param("testing_case") == 1:
            self.run(frame,frame_id, frame_delay,1)

        ## MTC check
        elif rospy.get_param("testing_case") == 2 and frame_delay <= rospy.get_param("segmentation_delay"):
            self.run(frame,frame_id, frame_delay,2)
        
    def run(self,frame,frame_id, frame_delay,case):
        frame_id = rospy.get_param("frame_id")
        t1 = time_synchronized()
        img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
        result = inference_segmentor(self.model1,img)
        t2 = time_synchronized()
        seg_b = self.convert_to_box(result[0])
        self.seg_box[frame.header.seq] = seg_b
        # print(type(seg_b))

        # f_mmsem.append([frame.header.seq, seg_b.tolist()])
        # print(self.seg_box)
        # self.results_cache = result[0]
        del img
        self.count += 1
        t3 = time_synchronized()
        self.runtime = t2-t1
        
        print(frame_id,frame.header.seq,frame_delay, t2-t1, t3-t2,t3-t1, self.count)

        if case != 3 or (case == 3 and rospy.get_param("prediction") == False):
            msg = ProcessStatus()
            msg.imgseq = frame.header.seq
            msg.runtime = self.runtime
            msg.header.stamp = frame.header.stamp
            msg.data = np.array(seg_b,dtype=np.uint32).flatten().tolist()
            msg.app = "mmsem_seg"
            self.status_pub.publish(msg)
    
    def convert_to_box(self,img):
        res  = torch.from_numpy(img).float().to(self.device)
        obj_ids = torch.unique(res)
        obj_ids = obj_ids[6:]
        
        masks = res == obj_ids[:,None,None]
        boxes = masks_to_boxes(masks)
        
        return boxes.cpu()
    
    def mmseg_pub(self):
        if self.count != 0 and rospy.get_param("data_pub_finish") == False:
            # pid = os.getpid()
            # msg = get_proc_status(pid)
            msg = ProcessStatus()
            frame_id = rospy.get_param("frame_id")
            #msg.header.stamp = self.frame_cache.header.stamp
            msg.imgseq = self.frame_cache.header.seq
            msg.runtime = self.runtime
            k, v = sorted(self.seg_box.items())[-1]
            v_np = v.numpy()
            v = np.array(v_np,dtype=np.uint32).flatten().tolist()
            #print(type(v))
            # msg.data = self.results_cache
            if self.stamp_cache[k]:
                msg.header.stamp = self.stamp_cache[k]
            else:
                msg.header.stamp = self.frame_cache.header.stamp
            msg.data = v
            msg.app = "mmsem_seg"
            #print(v)
            #print(frame_id-k)
            self.status_pub.publish(msg)
            frame_id = rospy.get_param("frame_id")
            f_mmsem.append([frame_id-1, v_np])
            # print("Publishing detection results!")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    rospy.init_node('mmsem_seg_node')
    ic = mmsem_seg_node()

    print("timely function starting...")
    st = 1/rospy.get_param("image_fps")
    if rospy.get_param("testing_case") == 3 and rospy.get_param("prediction"):
        print("prediction starts")
        rt = RepeatedTimer(st, ic.mmseg_pub) # it auto-starts, no need of rt.start()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
