#!/usr/bin/env python3.6
import roslib

roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import psutil
import os
from ros_referee.msg import ProcessStatus
import time
import json

import torch
# import torchvision
# from PIL import Image
import matplotlib.pyplot as plt

from torchvision import transforms
from draw_box_utils import draw_box

import sys
import glob
import numpy as np
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post, time_synchronized 
from build_utils import img_utils, torch_utils, utils
# from models import Darknet
    
class yolov3_node:
    
    def __init__(self):
        
        img_size = 512  # 必须是32的整数倍 [416, 512, 608]
        cfg = "/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/yolov3_spp/cfg/my_yolov3.cfg"  # 改成生成的.cfg文件
        weights = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_object_detection/yolov3_spp/weights/yolov3spp-29.pt"  # 改成自己训练好的权重文件
        json_path = "/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/yolov3_spp/data/pascal_voc_classes.json"  # json标签文件
        img_path = "/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_object_detection/scripts/yolov3_spp/example.png"
        # WSI_MASK_PATH = '/home/nvidia/Downloads/EdgePerf-benchmark/Road/10'
        # WSI_MASK_PATH  = '/run/user/1000/gvfs/afp-volume:host=Hydra-NAS.local,user=liangkai,volume=AVBench/cadc_dataset/cadcd/2018_03_06/0001/labeled/image_00/data'
        
        assert os.path.exists(cfg), "cfg file {} dose not exist.".format(cfg)
        assert os.path.exists(weights), "weights file {} dose not exist.".format(weights)
        assert os.path.exists(json_path), "json file {} dose not exist.".format(json_path)
        assert os.path.exists(img_path), "image file {} dose not exist.".format(img_path)

        json_file = open(json_path, 'r')
        class_dict = json.load(json_file)
        self.category_index = {v: k for k, v in class_dict.items()}

        self.input_size = (img_size, img_size)

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # self.model = Darknet(cfg, img_size)
        self.model = torch.hub.load('ultralytics/yolov3', 'yolov3')
        # self.model.load_state_dict(torch.load(weights, map_location=self.device)["model"])
        self.model.to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            # init
            img = torch.zeros((1, 3, img_size, img_size), device=self.device)
            self.model(img)
            
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('yolov3_process_status', ProcessStatus, queue_size=1)
        # rospy.init_node('fasterrcnn_node')
        # rospy.spin()

    def callback(self, frame):
        sf = rospy.get_param("object_skip_frames")
        if sf == 0:
            with torch.no_grad():
                t0 = time_synchronized()
                # img_o = cv2.imread(path)  # BGR
                img_o = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
                # assert img_o is not None, "Image Not Found " + img_path

                img = img_utils.letterbox(img_o, new_shape=self.input_size, auto=True, color=(0, 0, 0))[0]
                # Convert
                img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
                img = np.ascontiguousarray(img)

                img = torch.from_numpy(img).to(self.device).float()
                img /= 255.0  # scale (0, 255) to (0, 1)
                img = img.unsqueeze(0)  # add batch dimension

                t1 = time_synchronized()
                # pred, _, t = self.model(img)  # only get inference result
                pred, _ = self.model(img)  # only get inference result
                t2 = time_synchronized()
                # print(t2 - t1)

                pred = utils.non_max_suppression(pred, conf_thres=0.1, iou_thres=0.6, multi_label=True)[0]
                t3 = time_synchronized()
                # print(t3 - t2)

                # if pred is None:
                #     print("No target detected.")
                #     exit(0)

                # process detections
                if pred != None:
                    pred[:, :4] = utils.scale_coords(img.shape[2:], pred[:, :4], img_o.shape).round()
                    # print(pred.shape)

                    bboxes = pred[:, :4].detach().cpu().numpy()
                    scores = pred[:, 4].detach().cpu().numpy()
                    classes = pred[:, 5].detach().cpu().numpy().astype(np.int) + 1

                    # img_o = draw_box(img_o[:, :, ::-1], bboxes, classes, scores, self.category_index)
                else:
                    bboxes = [0]
                    scores = 0
                t4 = time_synchronized()
                # plt.imshow(img_o)
                # plt.show()

                # img_o.save("test_result.jpg")
                
                # line = '| %s | %s | %s | %s | %s |' % (t1-t0, t2-t1, t3-t2, t4-t3, t4-t0)
                # print(line)
                # print(t1-t0, t2-t1, t3-t2, t4-t3, t4-t0, t[0], t[1])
                print(t1-t0, t2-t1, t3-t2, t4-t3, t4-t0)
                
            pid = os.getpid()
            msg = get_proc_status(pid)
            msg.header.stamp = rospy.Time.now()
            # msg.proposals = 
            msg.objects = len(bboxes)
            msg.probability = scores
            msg.runtime = t4-t1
                
            # rospy.loginfo(msg)
            self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("object_skip_frames", 0)
        else:
            rospy.set_param("object_skip_frames", sf-1)


if __name__ == '__main__':
    rospy.init_node('yolov3_node')
    ic = yolov3_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()