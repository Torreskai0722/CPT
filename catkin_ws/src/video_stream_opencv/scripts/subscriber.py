#!/usr/bin/env python3.6
import roslib

roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class image_converter:

    def __init__(self):
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        rospy.init_node('image_converter')
        rospy.spin()

    def callback(self, data):
        t_curr = rospy.Time.now()
        t = data.header.stamp
        delay = t_curr.secs - t.secs + (t_curr.nsecs - t.nsecs) * 0.000000001
        print(delay)


if __name__ == '__main__':
    ic = image_converter()
    #rospy.init_node('image_converter')
    #try:
    #rospy.spin()
    #except KeyboardInterrupt:
        #print("Shutting down")
    #cv2.destroyAllWindows()
