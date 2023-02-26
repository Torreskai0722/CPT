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
from sensor_msgs.msg import Image
import time
import numpy as np

def quit(signum, frame):
    print('')
    print('stop fusion')
    sys.exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    
    # bridge = CvBridge()
    publisher = rospy.Publisher('/usb_cam/image_raw', Image, queue_size=1)
    rospy.init_node('web_cam')
    print("Correctly opened resource, starting to show feed.")
    cap = cv2.VideoCapture("/dev/video1")
    cap.set(3,1920)
    cap.set(4,1080)
    rval, frame = cap.read()
    #f = open('access_usbcam_cvbridge.log','wt')
    #image_message = Image()
    #img = np.random.randint(0,255,size=[1080,1920,3])
    #cv2.imwrite("img.png",img)
    #image_message.data = np.random.randint(0,255,size=[6220800]).tolist()

    while rval:
        # t1 = time.perf_counter() * 1000
        image_message = Image()
        # frame = cv2.imread('img.png')
        # print(frame.shape)
        # print(frame.tolist())
        size  = 1080*1920*3
        image_message.data = frame.reshape(size).tolist()
        # image_message = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        # im = np.frombuffer(frame, dtype=np.uint8).reshape(1080, 1920, -1)
        image_message.header.stamp = rospy.Time.now()
        # image_message.data = frame.reshape(size).tolist()
        #print(rospy.Time.now().secs)
        #f.write("%s" % rospy.Time.now().secs + "\n")
        #try:
        publisher.publish(image_message)
        #except CvBridgeError as e:
            #continue
            #print(e)
            #f.close()
        rval, frame = cap.read()
        # t2 = time.perf_counter() * 1000
        # print(t2-t1)

        #if cv2.waitKey(25) & 0xFF == ord('q'):
        #    f.close()
        #    cv2.destroyAllWindows()
        #    break
    #f.close()
