#!/usr/bin/env python3
import rospy
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import Image
# from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import TransformStamped, PoseStamped
from ros_referee.msg import ProcessStatus
from tf2_msgs.msg import TFMessage

def object_callback(object):
    print("hello")

def lane_callback(object):
    print("hello")

def semantic_callback(object):
    print("hello")

def callback(object,semantic,lane):
    # f1 = open("./logs/04-21-sensor-fusion-system-1000-2-sleep0.05-gpu-allfour-earlyexit.log","a+")
    # f2 = open("./logs/04-21-sensor-fusion-runtime-1000-2-sleep0.05-gpu-09-allfour-earlyexit.log","a+")
    f1 = open("./logs/05-14-sensor-fusion-system-1000-2-sleep0.33-onegpu-baseline.log","a+")
    f2 = open("./logs/05-14-sensor-fusion-runtime-1000-2-sleep0.33-onegpu-baseline.log","a+")
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #print("hello")
    t1 = semantic.header.stamp.secs + semantic.header.stamp.nsecs * 0.000000001
    t2 = object.header.stamp.secs + object.header.stamp.nsecs * 0.000000001
    t3 = lane.header.stamp.secs + lane.header.stamp.nsecs * 0.000000001
    # t4 = orbslam.header.stamp.secs + orbslam.header.stamp.nsecs * 0.000000001
    
    print(object.runtime,semantic.runtime, lane.runtime)

    #print(orbslam.transforms[0])
    #print(t1, t2, t3)
    t = rospy.Time.now()
    t_current = t.secs + t.nsecs * 0.000000001
    print(t1,t2,t3,t_current)
    f1.write("%s,%s,%s,%s,%s" % (str(t1), str(t2), str(t3),str(t_current),str(t_current - t1))+"\n")
    f2.write("%s,%s,%s" % (str(object.runtime), str(semantic.runtime), str(lane.runtime))+"\n")
    f1.close()
    f2.close()
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('fusion', anonymous=True)

    #rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

    object_sub = rospy.Subscriber('fasterrcnn_process_status', ProcessStatus, object_callback)
    semantic_sub = rospy.Subscriber('deeplab_process_status', ProcessStatus)
    # orbslam_sub = rospy.Subscriber('/pose_timestamp', PoseStamped)
    # lane_sub = rospy.Subscriber('lanenet_process_status',ProcessStatus)
    lane_sub = rospy.Subscriber('pinet_process_status',ProcessStatus)
    # orbslam = rospy.Subscriber('orbslam_process_status',ProcessStatus)
    
    print("ready for subscribing!")
    rospy.spin()

if __name__ == '__main__':
    listener()
