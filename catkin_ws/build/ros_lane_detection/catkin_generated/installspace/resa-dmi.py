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
import numpy as np
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post
import os.path as osp

import torch.nn.functional as F
from models.resa import RESANet
from utils.config import Config

from collections import OrderedDict

def probmap2lane(cfg,probmaps, exists, pts=18):
        ori_imgh = 590
        ori_imgw = 1640
        coords = []
        probmaps = probmaps[1:, ...]
        exists = exists > 0.5
        for probmap, exist in zip(probmaps, exists):
            if exist == 0:
                continue
            probmap = cv2.blur(probmap, (9, 9), borderType=cv2.BORDER_REPLICATE)
            thr = 0.3
            coordinate = np.zeros(pts)
            cut_height = cfg.cut_height
            for i in range(pts):
                line = probmap[round(
                    cfg.img_height-i*20/(ori_imgh-cut_height)*cfg.img_height)-1]

                if np.max(line) > thr:
                    coordinate[i] = np.argmax(line)+1
            if np.sum(coordinate > 0) < 2:
                continue
    
            img_coord = np.zeros((pts, 2))
            img_coord[:, :] = -1
            for idx, value in enumerate(coordinate):
                if value > 0:
                    img_coord[idx][0] = round(value*ori_imgw/cfg.img_width-1)
                    img_coord[idx][1] = round(ori_imgh-idx*20-1)
    
            img_coord = img_coord.astype(int)
            coords.append(img_coord)
    
        return coords

def view(img, coords, file_path=None):
        for coord in coords:
            for x, y in coord:
                if x <= 0 or y <= 0:
                    continue
                x, y = int(x), int(y)
                cv2.circle(img, (x, y), 4, (255, 0, 0), 2)

        if file_path is not None:
            if not os.path.exists(osp.dirname(file_path)):
                os.makedirs(osp.dirname(file_path))
            cv2.imwrite(file_path, img)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class resa_node:
    
    def __init__(self):

        self.cfg = Config.fromfile('/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/resa/configs/culane.py')
        self.model = RESANet(self.cfg)
        self.model = self.model.cuda()

        state_dict = torch.load('/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/resa/culane_resnet50.pth')
        new_state_dict = OrderedDict()
        for k, v in state_dict['net'].items():
            name = k[7:] # remove `module.`
            new_state_dict[name] = v
        # load params
        # model.load_state_dict(new_state_dict)
        self.model.load_state_dict(new_state_dict, strict=True)

        img_idx = 0
        # x = loader.dataset[img_idx]['img'].unsqueeze(0).cuda()
        # random init input tensor
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        mean=(0.3598, 0.3653, 0.3662) # CULane mean, std
        std=(0.2573, 0.2663, 0.2756)
        self.transform_img = transforms.Resize((288, 800))
        self.transform_to_net = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=mean, std=std)])

        img_path = "/home/mobilitylab/catkin_ws/src/ros_lane_detection/scripts/resa/demo.jpg"

        start = time_synchronized()
        img = pilim.open(img_path).convert('RGB')
        # print(img.size)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.transform_img(img)
        x = self.transform_to_net(img)
        x = x.unsqueeze_(0).to(self.device)        
        self.model.eval()  # 进入验证模式

        with torch.no_grad():
            img_height, img_width = x.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            self.model(init_img.to(self.device))

        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('resa_status', ProcessStatus, queue_size=1)
        print("ready")

    def callback(self, frame):
        # sf = rospy.get_param("lane_skip_frames")
        sf = 0
        if sf == 0:
            with torch.no_grad():
                t_1 = time_synchronized()
                # print(frame.width,frame.height,type(frame.width))
                img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
                img = pilim.fromarray(img)
                img = self.transform_img(img)
                x = self.transform_to_net(img)
                x = x.unsqueeze_(0).to(self.device)

                t_2 = time_synchronized()

                with torch.no_grad():
                    out = self.model(x)
                    t_3 = time_synchronized()
                    probmap, exist = out['seg'], out['exist']
                    probmap = F.softmax(probmap, dim=1).squeeze().cpu().numpy()
                    exist = exist.squeeze().cpu().numpy()
                    # print(probmap,exist)

                coords = probmap2lane(self.cfg,probmap, exist)
                # print(coords)
                # view(np.array(img), coords, './demo-results.png')
                t_4 = time_synchronized()

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
    rospy.init_node('resa_node')
    ic = resa_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
