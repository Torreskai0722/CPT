#!/usr/bin/env python3.6
# from ros_segmentation.scripts.deeplab import deeplabv3_resnet101
import roslib

import rospy
import cv2
from sensor_msgs.msg import Image
import psutil
import os
from ros_referee.msg import ProcessStatus
import time
import json
# from PIL import Image
import torchvision
from torchvision import transforms
# import deeplab
import torch
from PIL import Image as pilim

# from jetson_benchmarks import utilities, benchmark_argparser
import sys
import glob
import numpy as np
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post
from src import deeplabv3_resnet50
from torch.profiler import profile, record_function, ProfilerActivity

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


class deeplab_node:
    
    def __init__(self):
        aux = False  # inference time not need aux_classifier
        classes = 20
        # self.device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
        self.model = deeplabv3_resnet50(aux=aux, num_classes=classes+1)
        palette_path = "/home/mobilitylab/catkin_ws/src/ros_segmentation/scripts/deeplab_v3/palette.json"
        weights_path = "/home/mobilitylab/catkin_ws/src/ros_segmentation/scripts/deeplab_v3/deeplabv3_resnet50_coco.pth"

        weights_dict = torch.load(weights_path, map_location=self.device)
        for k in list(weights_dict.keys()):
            if "aux" in k:
                del weights_dict[k]
        
        with open(palette_path, "rb") as f:
            pallette_dict = json.load(f)
            self.pallette = []
            for v in pallette_dict.values():
                self.pallette += v

        # load weights
        self.model.load_state_dict(weights_dict)

        # or any of these variants
        # model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
        # model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_mobilenet_v3_large', pretrained=True)
        self.model.eval()
        
        input_image = cv2.imread("/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/faster_rcnn/test.png", cv2.IMREAD_COLOR)
        self.former_img = input_image
        self.shape = input_image.shape
        # input_image = input_image.convert("RGB")
        self.data_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = self.data_transform(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to(self.device)
            self.model.to(self.device)

        with torch.no_grad():
            output, _ = self.model(input_batch)
        # output_predictions = output.argmax(0)
            
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('deeplab_process_status', ProcessStatus, queue_size=1)
        self.current_seq = 0
        print("ready")
        # rospy.spin()

    def callback(self, frame):
        # sf = rospy.get_param("semantic_skip_frames")
        sf = 0
        delay = frame.header.seq-self.current_seq
        print(delay)
        # if sf == 0 and delay < rospy.get_param("delay_thresh"):
        if sf == 0:
            with torch.no_grad():
                with record_function("model_inference_"+str(frame.header.seq)):
                    t_1 = time_synchronized()
                    # print(frame.width,frame.height,type(frame.width))
                    test_img = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
                    # cv2.imwrite("test.png",test_img)
                    test_img = pilim.fromarray(test_img)
                    tran_img = self.data_transform(test_img)
                    tran_img = torch.unsqueeze(tran_img, dim=0)
                    t_2 = time_synchronized()

                    # res =  model(img.to(device))
                    res, t = self.model(tran_img.to(self.device))
                    t_3 = time_synchronized()

                    pid = os.getpid()
                    msg = get_proc_status(pid)
                    # msg.header.stamp = rospy.Time.now()
                    msg.header.stamp = frame.header.stamp
                    msg.imgseq = frame.header.seq
                    msg.runtime = t_3-t_1

                    if res != None and t != None:
                        predictions = res['out'][0]
                        predictions.to("cpu")
                        # rospy.loginfo(msg)
                    self.status_pub.publish(msg)

                    # prediction = res['out'].argmax(1).squeeze(0)
                    # prediction = prediction.to("cpu").numpy().astype(np.uint8)
                    # mask = pilim.fromarray(prediction)
                    # mask.putpalette(self.pallette)
                    
                    # mask.save("test_result.png")
                    
                    # profile_time = predictions["time"]
                    # midres = predictions["midres"]
                    # print("inference+NMS time: {}".format(t_end - t_start))

                    # predict_boxes = predictions["boxes"].to("cpu").numpy()
                    # predict_classes = predictions["labels"].to("cpu").numpy()
                    # predict_scores = predictions["scores"].to("cpu").numpy()
                    t_4 = time_synchronized()
                    print(t_2-t_1,t_3-t_2,t_4-t_3, t_4-t_1,frame.header.seq)
                    # print(frame.header.seq)
                
            
            # msg.proposals = midres[0]
            # msg.objects = midres[1]
            # msg.probability = predict_scores
            
        elif sf < 0:
            rospy.set_param("semantic_skip_frames", 0)
        elif sf > 0:
            rospy.set_param("semantic_skip_frames", sf-1)
        self.current_seq = frame.header.seq

if __name__ == '__main__':
    rospy.init_node('deeplab_node')
    ic = deeplab_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()
