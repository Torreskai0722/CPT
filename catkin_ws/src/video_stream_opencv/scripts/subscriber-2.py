#!/usr/bin/env python3.6
import roslib

roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class image_converter:

    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            t = data.header.stamp
            t_curr = rospy.Time.now()
            delay = t_curr.secs - t.secs + (t_curr.nsecs - t.nsecs) * 0.000000001
            print(delay*1000)
        except CvBridgeError as e:
            print(e)

        #(rows, cols, channels) = cv_image.shape
        #if cols > 60 and rows > 60:
        #    cv2.circle(cv_image, (150, 150), 20, (30, 144, 255), -1)
        cv2.imshow("Image window", cv_image)
        #cv2.waitKey(3)


if __name__ == '__main__':
    ic = image_converter()
    rospy.init_node('image_converter_2')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
