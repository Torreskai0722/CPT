#!/usr/bin/env python3.6
import roslib

# roslib.load_manifest('video_stream_opencv')
import rospy
# import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import psutil
import os
from ros_referee.msg import ProcessStatus

def get_proc_status(pid):
    msg = ProcessStatus()
    ppid = os.getppid()
    proc = psutil.Process(pid)
    
    msg.pid = proc.pid
    msg.ppid = ppid
    msg.app = proc.name()
    msg.cpids = get_proc_children(proc)
    msg.scheduling_policy = sched_dict[os.sched_getscheduler(pid)]
    msg.priority = proc.nice()
    
    return msg

def get_proc_children(proc, r=True):
    a = proc.threads()
    id = []
    for i in a:
        id.append(i.id)
    # cmd = 'pstree -p 20026'
    # print(os.system(cmd))
    try:
		# return proc.children(recursive=r)
        # print(id)
        return id
    except AttributeError:
        # return proc.children(recursive=r)
        return []

#define SCHED_NORMAL		0
#define SCHED_FIFO		1
#define SCHED_RR		2
#define SCHED_BATCH		3
#define SCHED_IDLE		5
#define SCHED_DEADLINE		6
sched_dict = {0: "SCHED_OTHER", 
              1: "SCHED_FIFO", 
              2: "SCHED_RR", 
              3: "SCHED_BATCH", 
              5: "SCHED_IDLE", 
              6: "SCHED_DEADLINE"}



class image_converter:

    def __init__(self):
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('process_status', ProcessStatus, queue_size=10)
        # rospy.init_node('image_converter')
        # rospy.spin()

    def callback(self, data):
        t_curr = rospy.Time.now()
        # t = data.header.stamp
        # delay = t_curr.secs - t.secs + (t_curr.nsecs - t.nsecs) * 0.000000001
        # print(delay)
        
        pid = os.getpid()
        msg = get_proc_status(pid)
        msg.header.stamp = rospy.get_time()
            
        rospy.loginfo(msg)
        self.status_pub.publish(msg)


if __name__ == '__main__':
    ic = image_converter()
    rospy.init_node('image_converter')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()
