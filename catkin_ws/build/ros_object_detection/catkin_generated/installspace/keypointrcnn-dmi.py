#!/usr/bin/env python3.6
import roslib
roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
import os
from ros_referee.msg import ProcessStatus
import time
import json
import torch
import torchvision
from PIL import Image as pilim
from torchvision import transforms
import numpy as np

from proc_util import get_proc_status

# import nvidia_dlprof_pytorch_nvtx as nvtx
# nvtx.init(enable_function_stack=True)

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


class keypointrcnn_node:
    
    def __init__(self):
        
        # get devices
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # device = torch.device("cpu")
        print("using {} device.".format(self.device))
        # create model
        self.model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
        # self.model = torch.hub.load('ultralytics/yolov3', 'yolov3')
        self.model.to(self.device)

        # load image
        # original_img = cv2.imread("/home/nvidia/Downloads/data_odometry_color/dataset/sequences/02/image_2/000000.png", cv2.IMREAD_COLOR)
        original_img = cv2.imread("/home/mobilitylab/projects/PDNN/data_odometry_color/dataset/sequences/09/image_2/000000.png", cv2.IMREAD_COLOR)
        # print(original_img.shape)
        self.former_img = original_img
        original_img = pilim.fromarray(original_img)

        # from pil image to tensor, do not normalize image
        self.data_transform = transforms.Compose([transforms.ToTensor()])
        img = self.data_transform(original_img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0)
        
        self.model.eval()  # 进入验证模式
        with torch.no_grad():
            # init
            img_height, img_width = img.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            self.model(init_img)
            
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('keypointrcnn_process_status', ProcessStatus, queue_size=1)

    def callback(self, frame):
        sf = rospy.get_param("object_skip_frames")
        if sf == 0:
            with torch.no_grad():
                t_1 = time_synchronized()
                # print(frame.width,frame.height,type(frame.width))
                # print(type(frame.data))
                test_img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)

                # print(ssim(test_img,test_img))
                test_img = pilim.fromarray(test_img)
                self.former_img = test_img

                # cv2.imwrite("test.png",test_img)
                tran_img = self.data_transform(test_img)
                tran_img = torch.unsqueeze(tran_img, dim=0)
                t_2 = time_synchronized()

                # res =  model(img.to(device))
                predictions = self.model(tran_img.to(self.device))[0]
                t_3 = time_synchronized()

                # print(len(predictions['keypoints_scores']))

                if predictions != [0]:
                    pt = predictions["time"]
                    midres = predictions["midres"]

                    predict_boxes = predictions["boxes"].to("cpu").numpy()
                    predict_classes = predictions["labels"].to("cpu").numpy()
                    predict_scores = predictions["scores"].to("cpu").numpy()

                    # if len(predict_boxes) == 0:
                    #     print("No objects!")

                    # draw_box(test_img,
                    #     predict_boxes,
                    #     predict_classes,
                    #     predict_scores,
                    #     self.category_index,
                    #     thresh=0.05,
                    #     line_thickness=3)
                    # plt.imshow(test_img)
                    # plt.show(block=False) 
                else:
                    midres = [0, 0]
                    predict_scores = [0]
                    predict_boxes = [0]
                    predict_classes = [0]

                t_4 = time_synchronized()
                # print(t_2-t_1,t_3-t_2,t_4-t_3,t_4-t_1)
                # print(predictions["mid"])
                print(t_2-t_1, t_3-t_2, t_4-t_3, pt[0],pt[1],pt[2],pt[3], t_4-t_1,midres[0],midres[1])
                
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
            rospy.set_param("object_skip_frames", 0)
        else:
            rospy.set_param("object_skip_frames", sf-1)


if __name__ == '__main__':
    rospy.init_node('keypointrcnn_node')
    ic = keypointrcnn_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")