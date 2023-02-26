#!/usr/bin/env python3.6
import roslib
roslib.load_manifest('video_stream_opencv')
import requests
import matplotlib.pyplot as plt
# config InlineBackend.figure_format = 'retina'
import time
import torch
from torch import nn
import torchvision
from torchvision.models import resnet50
import torchvision.transforms as T
from zmq import device
torch.set_grad_enabled(False)
import glob
import os

import rospy
import cv2
from sensor_msgs.msg import Image
from ros_referee.msg import ProcessStatus
import json
from PIL import Image as pilim
from torchvision import transforms
import numpy as np
from proc_util import get_proc_status

# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
        [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

class detr_node:
    
    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = DETRdemo(num_classes=91)
        state_dict = torch.hub.load_state_dict_from_url(
            url='https://dl.fbaipublicfiles.com/detr/detr_demo-da2a99e9.pth',
            map_location='cpu', check_hash=True)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device).eval()

        # standard PyTorch mean-std input image normalization
        self.transform = T.Compose([
            T.Resize(400),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        # print("using {} device.".format(self.device))

        # load image
        # original_img = cv2.imread("/home/nvidia/Downloads/data_odometry_color/dataset/sequences/02/image_2/000000.png", cv2.IMREAD_COLOR)
        original_img = cv2.imread("/home/mobilitylab/projects/PDNN/data_odometry_color/dataset/sequences/09/image_2/000000.png", cv2.IMREAD_COLOR)
        # print(original_img.shape)
        self.former_img = original_img
        original_img = pilim.fromarray(original_img)

        # from pil image to tensor, do not normalize image
        
        img = self.transform(original_img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0).to(self.device)
        
        self.model.eval()  # 进入验证模式
        with torch.no_grad():
            # init
            # print(img.shape)
            img_height, img_width = img.shape[-2:]
            assert img.shape[-2] <= 1600 and img.shape[-1] <= 1600, 'demo model only supports images up to 1600 pixels on each side'
            init_img = torch.zeros((1, 3, img_height, img_width), device=self.device)
            # print(init_img.shape)
            self.model(init_img)
            
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('detr_process_status', ProcessStatus, queue_size=1)

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
                # self.former_img = test_img

                # cv2.imwrite("test.png",test_img)
                tran_img = self.transform(test_img)
                tran_img = torch.unsqueeze(tran_img, dim=0)
                t_2 = time_synchronized()

                # propagate through the model
                outputs = self.model(tran_img.to(self.device))
                # print(outputs)

                # keep only predictions with 0.7+ confidence
                probas = outputs['pred_logits'].to("cpu").softmax(-1)[0, :, :-1]
                keep = probas.max(-1).values > 0.7
                # print(outputs['pred_boxes'][0, keep])

                # convert boxes from [0; 1] to image scales
                bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep].to("cpu"),test_img.size)

                # res =  model(img.to(device))
                t_3 = time_synchronized()

                # if predictions != [0]:
                #     pt = predictions["time"]
                #     midres = predictions["midres"]
                #     # print("inference+NMS time: {}".format(t_end - t_start))

                #     predict_boxes = predictions["boxes"].to("cpu").numpy()
                #     predict_classes = predictions["labels"].to("cpu").numpy()
                #     predict_scores = predictions["scores"].to("cpu").numpy()

                #     # if len(predict_boxes) == 0:
                #     #     print("No objects!")

                #     # draw_box(test_img,
                #     #     predict_boxes,
                #     #     predict_classes,
                #     #     predict_scores,
                #     #     self.category_index,
                #     #     thresh=0.05,
                #     #     line_thickness=3)
                #     # plt.imshow(test_img)
                #     # plt.show(block=False) 
                # else:
                #     midres = [0, 0]
                #     predict_scores = [0]
                #     predict_boxes = [0]
                #     predict_classes = [0]

                # t_4 = time_synchronized()
                print(t_2-t_1, t_3-t_2, t_3-t_1)

                # print(midres,predict_boxes,predict_classes,predict_scores)

                # print(t_2-t_1, t_3-t_2, t_4-t_3, pt[1]-pt[0], pt[2]-pt[1], pt[3]-pt[2], pt[4]-pt[3], pt[5]-pt[4], pt[6]-pt[5])
                
            pid = os.getpid()
            msg = get_proc_status(pid)
            # msg.header.stamp = rospy.Time.now()
            msg.header.stamp = frame.header.stamp
            # msg.proposals = midres[0]
            # msg.objects = midres[1]
            # msg.probability = predict_scores
            msg.runtime = t_3-t_1
                
            # rospy.loginfo(msg)
            self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("object_skip_frames", 0)
        else:
            rospy.set_param("object_skip_frames", sf-1)

class DETRdemo(nn.Module):
    """
    Demo DETR implementation.

    Demo implementation of DETR in minimal number of lines, with the
    following differences wrt DETR in the paper:
    * learned positional encoding (instead of sine)
    * positional encoding is passed at input (instead of attention)
    * fc bbox predictor (instead of MLP)
    The model achieves ~40 AP on COCO val5k and runs at ~28 FPS on Tesla V100.
    Only batch size 1 supported.
    """
    def __init__(self, num_classes, hidden_dim=256, nheads=8,
                 num_encoder_layers=6, num_decoder_layers=6):
        super().__init__()

        # create ResNet-50 backbone
        self.backbone = resnet50()
        del self.backbone.fc

        # create conversion layer
        self.conv = nn.Conv2d(2048, hidden_dim, 1)

        # create a default PyTorch transformer
        self.transformer = nn.Transformer(
            hidden_dim, nheads, num_encoder_layers, num_decoder_layers)

        # prediction heads, one extra class for predicting non-empty slots
        # note that in baseline DETR linear_bbox layer is 3-layer MLP
        self.linear_class = nn.Linear(hidden_dim, num_classes + 1)
        self.linear_bbox = nn.Linear(hidden_dim, 4)

        # output positional encodings (object queries)
        self.query_pos = nn.Parameter(torch.rand(100, hidden_dim))

        # spatial positional encodings
        # note that in baseline DETR we use sine positional encodings
        self.row_embed = nn.Parameter(torch.rand(50, hidden_dim // 2))
        self.col_embed = nn.Parameter(torch.rand(50, hidden_dim // 2))

    def forward(self, inputs):
        # propagate inputs through ResNet-50 up to avg-pool layer
        x = self.backbone.conv1(inputs)
        x = self.backbone.bn1(x)
        x = self.backbone.relu(x)
        x = self.backbone.maxpool(x)

        x = self.backbone.layer1(x)
        x = self.backbone.layer2(x)
        x = self.backbone.layer3(x)
        x = self.backbone.layer4(x)

        # convert from 2048 to 256 feature planes for the transformer
        h = self.conv(x)

        # construct positional encodings
        H, W = h.shape[-2:]
        # print(W, H)
        pos = torch.cat([
            self.col_embed[:W].unsqueeze(0).repeat(H, 1, 1),
            self.row_embed[:H].unsqueeze(1).repeat(1, W, 1),
        ], dim=-1).flatten(0, 1).unsqueeze(1)

        # propagate through the transformer
        h = self.transformer(pos + 0.1 * h.flatten(2).permute(2, 0, 1),
                             self.query_pos.unsqueeze(1)).transpose(0, 1)
        
        # finally project transformer outputs to class labels and bounding boxes
        return {'pred_logits': self.linear_class(h), 
                'pred_boxes': self.linear_bbox(h).sigmoid()}

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def PIL_to_tensor(image,device):
    image = torchvision.transforms.ToTensor()(image).unsqueeze(0)
    return image.to(device, torch.float)

def detect(im, model, transform):
    # mean-std normalize the input image (batch-size: 1)
    # img = transform(im).unsqueeze(0)
    img = PIL_to_tensor(im, device)

    # demo model only support by default images with aspect ratio between 0.5 and 2
    # if you want to use images with an aspect ratio outside this range
    # rescale your image so that the maximum size is at most 1333 for best results
    assert img.shape[-2] <= 1600 and img.shape[-1] <= 1600, 'demo model only supports images up to 1600 pixels on each side'

    # propagate through the model
    outputs = model(img)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].to("cpu").softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > 0.7

    # convert boxes from [0; 1] to image scales
    bboxes_scaled = rescale_bboxes(outputs['pred_boxes'][0, keep].to("cpu"), im.size)
    return probas[keep], bboxes_scaled

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(16,10))
    plt.imshow(pil_img)
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), COLORS * 100):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    rospy.init_node('detr_node')
    ic = detr_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")