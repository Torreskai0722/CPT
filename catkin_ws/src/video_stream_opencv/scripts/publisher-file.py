#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""

Copyright (c) 2015 PAL Robotics SL.
Released under the BSD License.

Created on 7/14/15

@author: Sammy Pfeiffer

test_video_resource.py contains
a testing code to see if opencv can open a video stream
useful to debug if video_stream does not work
"""

import sys
import signal
import cv2
import rospy
# from cv_bridge import CvBridge, CvBridgeError
# from sensor_msgs.msg import Image
import glob
import os
import time
from PIL import Image
from sensor_msgs.msg import Image as SensorImage
import numpy as np
import yaml

keyframes = []

def load_yaml():
    with open("/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_referee/config/prophet.yaml", "r") as stream:
        try:
            yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def quit(signum, frame):
    print('')
    print('stop fusion')
    sys.exit()

def edgeperf_benchmark():
    IMAGE_FILE_road = '/home/mobilitylab/projects/PDNN/EdgePerf-benchmark/Road/10'
    IMAGE_FILE_resi = '/home/mobilitylab/projects/PDNN/EdgePerf-benchmark/Residential/10'
    IMAGE_FILE_city = '/home/mobilitylab/projects/PDNN/EdgePerf-benchmark/City/10'
    
    paths_road = glob.glob(os.path.join(IMAGE_FILE_road, '*.png'))
    paths_resi = glob.glob(os.path.join(IMAGE_FILE_resi, '*.png'))
    paths_city = glob.glob(os.path.join(IMAGE_FILE_city, '*.png'))
    
    paths_road.sort()
    paths_resi.sort()
    paths_city.sort()

    # paths = paths_road + paths_resi + paths_city
    paths = paths_road

    return paths

def is_keyframe(fframes, cframe, threshold):
    if len(fframes) == 0:
        return True
    else:
        if len(fframes) == 1:
            fframe = fframes
        else: 
            fframe = fframes[-1]
        diff = cv2.absdiff(fframe, cframe)
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count > threshold:
            return True
        else:
            return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    # bridge = CvBridge()
    # IMAGE_FILE = '/home/mobilitylab/projects/PDNN/data_odometry_color/dataset/sequences/09/image_2'
    # IMAGE_FILE = '/media/mobilitylab/6717202b-0641-47a2-87de-0a71081a1824/KITTI-ORB_SLAM2/dataset/sequences/00/image_0'
    # IMAGE_FILE = '/media/mobilitylab/6717202b-0641-47a2-87de-0a71081a1824/KITTI-ORB_SLAM2/dataset/sequences/02/image_0'
    IMAGE_FILE = '/home/mobilitylab/Downloads/image_0'
    # IMAGE_FILE = '/media/mobilitylab/6717202b-0641-47a2-87de-0a71081a1824/KITTI/2011_10_03/2011_10_03_drive_0047_sync/image_02/data'
    # IMAGE_FILE = '/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_object_detection/coco2017/train2017'
    #f = open('image-file-pub-yolov3.log','wt')
    paths = glob.glob(os.path.join(IMAGE_FILE, '*.png'))
    paths.sort()
    paths = paths[:1000]

    #paths = edgeperf_benchmark()

    # publisher = rospy.Publisher('/usb_cam/image_raw', SensorImage, queue_size=2)
    publisher = rospy.Publisher('/camera/image_raw', SensorImage, queue_size=1)
    # load_yaml()
    rospy.init_node('file_image')
    # print("Correctly opened resource, starting to show feed.")

    fframes = []
    #im = Image.open(paths[0]).convert('RGB')
    #fframes.append(im)
    
    for path in paths:
    # for i in range(10000):
        # path = "/home/nvidia/Downloads/EdgePerf-benchmark/Road/10/0000000" + str(i%599).zfill(3) + ".png"
        # print(path)
        st = 1/rospy.get_param("image_fps")
        # print(st)
        time.sleep(st)

        im = Image.open(path)
        im = im.convert('RGB')
        th = im.height * im.width * 0.5

        if iskeyframe(fframes, im, th):
            msg = SensorImage()
            msg.header.stamp = rospy.Time.now()
            msg.height = im.height
            msg.width = im.width
            msg.encoding = "rgb8"
            msg.is_bigendian = False
            msg.step = 3 * im.width
            msg.data = np.array(im).tobytes()
            publisher.publish(msg)
            keyframes.append(im)
            #print(len(keyframes))
            print(path)

        fframes.append(im)