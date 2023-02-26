#!/usr/bin/env python3.6
import roslib
import rospy
import cv2
from sensor_msgs.msg import Image
import os
from ros_referee.msg import ProcessStatus
import time
from torchvision import transforms
# import deeplab
import torch
from PIL import Image as pilim
import sys
import glob
import numpy as np
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post
import json
from model import SCNN
from utils.prob2lines import getLane
from utils.transforms import *

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class scnn_node:
    
    def __init__(self):

        self.model = SCNN(input_size=(800, 288), pretrained=False)
        mean=(0.3598, 0.3653, 0.3662) # CULane mean, std
        std=(0.2573, 0.2663, 0.2756)
        self.device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

        img_path = "/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/SCNN_Pytorch/demo/demo.jpg"
        weight_path = "/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/SCNN_Pytorch/vgg_SCNN_DULR_w9.pth"

        # from pil image to tensor and normalize
        self.transform_img = Resize((800, 288))
        self.transform_to_net = Compose(ToTensor(), Normalize(mean=mean, std=std))
        # self.data_transform = transforms.Compose([Resize((800, 288)),
        #                                     transforms.ToTensor(),
        #                                     transforms.Normalize(mean=mean,std=std)])

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = self.transform_img({'img': img})['img']
        x = self.transform_to_net({'img': img})['img']
        x.unsqueeze_(0)

        save_dict = torch.load(weight_path, map_location='cpu')
        self.model.load_state_dict(save_dict['net'])
        self.model.to(self.device)

        # # expand batch dimension
        # img = self.data_transform(img)
        # img = torch.unsqueeze(img, dim=0)
        self.model.eval()  # 进入验证模式

        with torch.no_grad():
            img_height, img_width = x.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            self.model(init_img.to(self.device))

        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('scnn_status', ProcessStatus, queue_size=1)
        print("ready")

    def callback(self, frame):
        #sf = rospy.get_param("lane_skip_frames")
        sf = 0
        if sf == 0:
            with torch.no_grad():
                t_1 = time_synchronized()
                # print(frame.width,frame.height,type(frame.width))
                img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)

                img = self.transform_img({'img': img})['img']
                x = self.transform_to_net({'img': img})['img']
                x.unsqueeze_(0)

                t_2 = time_synchronized()

                seg_pred, exist_pred = self.model(x.to(self.device))[:2]
                t_3 = time_synchronized()

                seg_pred = seg_pred.detach().cpu().numpy()
                exist_pred = exist_pred.detach().cpu().numpy()
                seg_pred = seg_pred[0]
                exist = [1 if exist_pred[0, i] > 0.5 else 0 for i in range(4)]

                # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                # lane_img = np.zeros_like(img)
                # color = np.array([[255, 125, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255]], dtype='uint8')
                # coord_mask = np.argmax(seg_pred, axis=0)
                # for i in range(0, 4):
                #     if exist_pred[0, i] > 0.5:
                #         lane_img[coord_mask == (i + 1)] = color[i]
                # img = cv2.addWeighted(src1=lane_img, alpha=0.8, src2=img, beta=1., gamma=0.)
                # cv2.imwrite("demo/demo_result.jpg", img)

                # for x in getLane.prob2lines_CULane(seg_pred, exist):
                #     print(x)
                t_4 = time_synchronized()

                # print([1 if exist_pred[0, i] > 0.5 else 0 for i in range(4)])
                # cv2.imshow("test", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                print(t_2-t_1,t_3-t_2,t_4-t_3,t_4-t_1,frame.header.seq)
                
            pid = os.getpid()
            msg = get_proc_status(pid)
            # msg.header.stamp = rospy.Time.now()
            msg.header.stamp = frame.header.stamp
            # msg.proposals = midres[0]
            # msg.objects = midres[1]
            # msg.probability = predict_scores
            msg.runtime = t_4-t_1
                
            # rospy.loginfo(msg)
            self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("lane_skip_frames", 0)
        else:
            rospy.set_param("lane_skip_frames", sf-1)

if __name__ == '__main__':
    rospy.init_node('scnn_node')
    ic = scnn_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
