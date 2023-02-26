#!/usr/bin/env python3
import rospy
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_msgs.msg import TFMessage

def callback(yolov3,semantic,orbslam):
    f = open("sensor-fusion-buffer-1000-2.log","a+")
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #print("hello")
    t1 = semantic.header.stamp.secs + semantic.header.stamp.nsecs * 0.000000001
    t2 = yolov3.header.stamp.secs + yolov3.header.stamp.nsecs * 0.000000001
    t3 = orbslam.header.stamp.secs + orbslam.header.stamp.nsecs * 0.000000001

    #print(orbslam.transforms[0])
    #print(t1, t2, t3)
    t = rospy.Time.now()
    t_current = t.secs + t.nsecs * 0.000000001
    print(t1,t2,t3,t_current)
    f.write("%s,%s,%s,%s" % (str(t1), str(t2), str(t3), str(t_current))+"\n")
    f.close()
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    #rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

    yolov3_sub = message_filters.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes)
    semantic_sub = message_filters.Subscriber('/semantic', Image)
    orbslam_sub = message_filters.Subscriber('/pose_timestamp', PoseStamped)
    
    #ts = message_filters.TimeSynchronizer([image_sub, info_sub], 10)
    ts = message_filters.ApproximateTimeSynchronizer([yolov3_sub, semantic_sub, orbslam_sub], 1000, 0.1, allow_headerless=False)
    ts.registerCallback(callback)
    print("ready for subscribing!")
    rospy.spin()

if __name__ == '__main__':
    listener()
