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
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import time

def quit(signum, frame):
    print('')
    print('stop fusion')
    sys.exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    cap = cv2.VideoCapture('/dev/video1')
    cap.set(3,1920)
    cap.set(4,1080)
    f = open('usb_cam_read.log','wt')
    rval, frame = cap.read()

    while rval:

        t1 = time.perf_counter() * 1000
        rval, frame = cap.read()
        t2 = time.perf_counter() * 1000

        f.write(str(t2-t1)+'\n')
        print(t2-t1)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            f.close()
            cv2.destroyAllWindows()
            break
    f.close()
