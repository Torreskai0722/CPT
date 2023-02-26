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
from torchvision.ops import masks_to_boxes
from PIL import Image as pilim
from torchvision import transforms
from mask_to_bbox import mask_to_bbox
import numpy as np
import sys
import signal
from proc_util import get_proc_status
from timer_repeat import RepeatedTimer
from mmseg.apis import inference_segmentor, init_segmentor

from collections import defaultdict
from util import time_synchronized, mmdet_results, analyze_iou, get_iou, get_max_iou, img_diff, img_ssim

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

f_mmdrivable = []

def quit(signum, frame):
    print('stop drivable detection')
    np.save('mmdrivable_boxes-referee-011123.npy', f_mmdrivable)
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
        # self.model = init_segmentor(config_file, checkpoint_file, self.device)
        # self.model0 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:0"))
        # self.model1 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:1"))
        self.model2 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:2"))
        # self.model3 = init_segmentor(config_file, checkpoint_file, torch.device("cuda:3"))
        #self.model = init_segmentor(rospy.get_param("mmdet_config"), rospy.get_param("mmdet_checkpoint"), self.device)

        # initilization
        img = cv2.imread("/home/mobilitylab/catkin_ws/test.png", cv2.IMREAD_COLOR)
        # t0 = inference_segmentor(self.model0, img)
        # t1 = inference_segmentor(self.model1, img)
        t2 = inference_segmentor(self.model2, img)
        # t3 = inference_segmentor(self.model3, img)
        # print(t0 == t1, t1 == t2, t2 == t3)   
        
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.track_sub = rospy.Subscriber("/object_tracker", BoundingBoxes, self.track_callback)
        self.status_pub = rospy.Publisher('mmdrivable_process_status', ProcessStatus, queue_size=1)

        tree = lambda: defaultdict(tree)
        self.count = 0
        self.frame_cache = Image()
        self.lane_box = tree()
        self.stamp_cache = tree()
        self.tracks_cache = tree()
        self.results_cache = []
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
        if rospy.get_param("testing_case") == 3 and frame_delay <= rospy.get_param("lane_delay"):
            if rospy.get_param("no_keyframe"):
                self.run(frame, frame_id,frame_delay,3)
            else:
                deadline_delay = frame_id - rospy.get_param("lane_last_keyframe")
                if frame.encoding == "key-ssim" or rospy.get_param("lane_keyframe_detection") or deadline_delay > rospy.get_param("lane_deadline") or rospy.get_param("traffic_scenario"):
                    print("keyframe_mmdrivable")
                    rospy.set_param("lane_last_keyframe",frame.header.seq)
                    self.run(frame,frame_id,frame_delay, 3)
        ## Baseline check
        elif rospy.get_param("testing_case") == 1:
            self.run(frame,frame_id,frame_delay, 1)
        ## MTC check
        elif rospy.get_param("testing_case") == 2 and frame_delay <= rospy.get_param("lane_delay"):
            self.run(frame,frame_id,frame_delay, 2)
    
    def run(self,frame,frame_id,frame_delay,case):
        frame_id = rospy.get_param("frame_id")
        t1 = time_synchronized()
        img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)

        result = inference_segmentor(self.model2, img)
        self.results_cache = result[0]
        t2 = time_synchronized()
        lane_b = self.convert_to_box(result[0])
        # print(lane_b)
        self.lane_box[frame.header.seq] = lane_b
        # f_mmdrivable.append([frame.header.seq, lane_b.tolist()])
        del img

        self.count += 1
        t3 = time_synchronized()
        self.runtime = t3-t1
        print(frame_id,frame.header.seq,frame_delay, t2-t1, t3-t2, t3-t1, self.count)

        if case != 3 or (case == 3 and rospy.get_param("prediction") == False):
            msg = ProcessStatus()
            msg.imgseq = frame.header.seq
            msg.runtime = self.runtime
            msg.header.stamp = frame.header.stamp
            msg.data = np.array(lane_b,dtype=np.uint32).flatten().tolist()
            msg.app = "mmdrivable"
            self.status_pub.publish(msg)
    
    def convert_to_box(self,img):
        res  = torch.from_numpy(img).float().to(self.device)
        obj_ids = torch.unique(res)
        obj_ids = obj_ids[:2]
        # print(obj_ids)
        # obj_set = [6,7,11,12,13,14,15,16,17,18]
        
        masks = res == obj_ids[:,None,None]
        boxes = masks_to_boxes(masks)
        
        return boxes.cpu()

    def mmseg_pub(self):
        if self.count != 0 and rospy.get_param("data_pub_finish") == False:
            msg = ProcessStatus()
            # pid = os.getpid()
            # msg = get_proc_status(pid)
            # msg.header.stamp = self.frame_cache.header.stamp
            k, v = sorted(self.lane_box.items())[-1]
            v_np = v.numpy()
            if self.stamp_cache[k]:
                msg.header.stamp = self.stamp_cache[k]
            else:
                msg.header.stamp = self.frame_cache.header.stamp
            msg.imgseq = self.frame_cache.header.seq
            msg.runtime = self.runtime
            msg.app = "mmdrivable"
            v = np.array(v_np,dtype=np.uint32).flatten().tolist()
            # print(np.array(v,dtype=np.uint32).flatten().tolist())
            msg.data = v
            self.status_pub.publish(msg)
            frame_id = rospy.get_param("frame_id")
            f_mmdrivable.append([frame_id-1, v_np])
            # print("Publishing detection results!")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    rospy.init_node('mmdrivable_node')
    ic = mmdrivable_node()

    print("timely function starting...")
    st = 1/rospy.get_param("image_fps")
    if rospy.get_param("testing_case") == 3 and rospy.get_param("prediction"):
        print("prediction starts")
        rt = RepeatedTimer(st, ic.mmseg_pub) # it auto-starts, no need of rt.start()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
