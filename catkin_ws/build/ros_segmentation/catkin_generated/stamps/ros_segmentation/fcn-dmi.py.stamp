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
from src import fcn_resnet50
import json

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


class fcn_node:
    
    def __init__(self):
        aux = False  # inference time not need aux_classifier
        classes = 20
        weights_path = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_segmentation/fcn/fcn_resnet50_coco.pth"
        palette_path = "/home/mobilitylab/projects/deep-learning-for-image-processing/pytorch_segmentation/fcn/palette.json"
        img_path = "/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_segmentation/test.png"
        self.device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
        # self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
        self.model = fcn_resnet50(aux=aux, num_classes=classes+1)
        
        with open(palette_path, "rb") as f:
            pallette_dict = json.load(f)
            self.pallette = []
            for v in pallette_dict.values():
                self.pallette += v
        
        # delete weights about aux_classifier
        weights_dict = torch.load(weights_path, map_location='cpu')
        for k in list(weights_dict.keys()):
            if "aux" in k:
                del weights_dict[k]

        # load weights
        self.model.load_state_dict(weights_dict)
        self.model.to(self.device)

        # load image
        original_img = pilim.open(img_path)

        # from pil image to tensor and normalize
        self.data_transform = transforms.Compose([transforms.Resize(520),
                                            transforms.ToTensor(),
                                            transforms.Normalize(mean=(0.485, 0.456, 0.406),
                                                                std=(0.229, 0.224, 0.225))])
        img = self.data_transform(original_img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0)
        self.model.eval()  # 进入验证模式

        with torch.no_grad():
            img_height, img_width = img.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            self.model(init_img)

        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('fcn_status', ProcessStatus, queue_size=1)
        print("ready")

    def callback(self, frame):
        sf = rospy.get_param("semantic_skip_frames")
        if sf == 0:
            with torch.no_grad():
                t_1 = time_synchronized()
                # print(frame.width,frame.height,type(frame.width))
                test_img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
                # cv2.imwrite("test.png",test_img)
                test_img = pilim.fromarray(test_img)

                tran_img = self.data_transform(test_img)
                tran_img = torch.unsqueeze(tran_img, dim=0)
                t_2 = time_synchronized()

                output = self.model(tran_img.to(self.device))
                t_3 = time_synchronized()

                prediction = output['out'].argmax(1).squeeze(0)
                prediction = prediction.to("cpu").numpy().astype(np.uint8)
                # mask = pilim.fromarray(prediction)
                # mask.putpalette(self.pallette)
                # mask.save("test_result.png")
                
                t_4 = time_synchronized()
                print(t_2-t_1,t_3-t_2,t_4-t_3,t_4-t_1)
                
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
            rospy.set_param("semantic_skip_frames", 0)
        else:
            rospy.set_param("semantic_skip_frames", sf-1)

if __name__ == '__main__':
    rospy.init_node('fcn_node')
    ic = fcn_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")