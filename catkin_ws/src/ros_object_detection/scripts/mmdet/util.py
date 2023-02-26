import time
import torch
import numpy as np
import cv2

from skimage.measure import compare_ssim
import argparse
import imutils

class_name = ["pedestrian", "rider", "car", "truck", "bus", "train", "motorcycle", "bicycle", "traffic light", "traffic sign"]

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

def mmdet_results(result, score_thr=0.5):
    bbox_result = result
    bboxes = np.vstack(bbox_result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bbox_result)
    ]
    labels = np.concatenate(labels)
    # print(labels)
    # print(bboxes[:,-1] > 0.5)

    scores = bboxes[:, -1]
    inds = scores > score_thr
    bboxes = bboxes[inds, :]
    labels = labels[inds]

    names = []
    for i in labels:
        names.append(class_name[i-1])

    return bboxes, labels, names

def analyze_iou(former_res, res):

    f_bboxes, f_labels, f_names = mmdet_results(former_res)
    bboxes, labels, names = mmdet_results(res)
    print(len(f_bboxes) == len(bboxes), f_labels == labels, f_names == names)

    l = len(bboxes)
    f_boxes = f_bboxes[:,:-1]
    f_scores = f_bboxes[:,-1]
    boxes = bboxes[:,:-1]
    scores = bboxes[:,-1]
    for i in range(l):
        iou, max_iou, nmax = get_max_iou(f_bboxes, boxes[i])
        print(max_iou, f_scores[nmax])

def get_iou(pred_box, gt_box):
    """
    pred_box : the coordinate for predict bounding box
    gt_box :   the coordinate for ground truth bounding box
    return :   the iou score
    the  left-down coordinate of  pred_box:(pred_box[0], pred_box[1])
    the  right-up coordinate of  pred_box:(pred_box[2], pred_box[3])
    """
    # 1.get the coordinate of inters
    ixmin = max(pred_box[0], gt_box[0])
    ixmax = min(pred_box[2], gt_box[2])
    iymin = max(pred_box[1], gt_box[1])
    iymax = min(pred_box[3], gt_box[3])

    iw = np.maximum(ixmax-ixmin+1., 0.)
    ih = np.maximum(iymax-iymin+1., 0.)

    # 2. calculate the area of inters
    inters = iw*ih

    # 3. calculate the area of union
    uni = ((pred_box[2]-pred_box[0]+1.) * (pred_box[3]-pred_box[1]+1.) +
           (gt_box[2] - gt_box[0] + 1.) * (gt_box[3] - gt_box[1] + 1.) -
           inters)

    # 4. calculate the overlaps between pred_box and gt_box
    iou = inters / uni

    return iou


def get_max_iou(pred_boxes, gt_box):
    """
    calculate the iou multiple pred_boxes and 1 gt_box (the same one)
    pred_boxes: multiple predict  boxes coordinate
    gt_box: ground truth bounding  box coordinate
    return: the max overlaps about pred_boxes and gt_box
    """
    # 1. calculate the inters coordinate
    if pred_boxes.shape[0] > 0:
        ixmin = np.maximum(pred_boxes[:, 0], gt_box[0])
        ixmax = np.minimum(pred_boxes[:, 2], gt_box[2])
        iymin = np.maximum(pred_boxes[:, 1], gt_box[1])
        iymax = np.minimum(pred_boxes[:, 3], gt_box[3])

        iw = np.maximum(ixmax - ixmin + 1., 0.)
        ih = np.maximum(iymax - iymin + 1., 0.)

    # 2.calculate the area of inters
        inters = iw * ih

    # 3.calculate the area of union
        uni = ((pred_boxes[:, 2] - pred_boxes[:, 0] + 1.) * (pred_boxes[:, 3] - pred_boxes[:, 1] + 1.) +
               (gt_box[2] - gt_box[0] + 1.) * (gt_box[3] - gt_box[1] + 1.) -
               inters)

    # 4.calculate the overlaps and find the max overlap ,the max overlaps index for pred_box
        iou = inters / uni
        iou_max = np.max(iou)
        nmax = np.argmax(iou)
        return iou, iou_max, nmax

def img_diff(prev_frame, curr_frame):
    diff = np.absolute(curr_frame - prev_frame)
    non_zero_count = np.count_nonzero(diff)
    a = curr_frame.shape
    print(non_zero_count, a[0]*a[1]*a[2], non_zero_count / (a[0]*a[1]*a[2]))

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def img_ssim(prev_frame, curr_frame):
    # convert the images to grayscale
    prev_gray = rgb2gray(prev_frame)
    curr_gray = rgb2gray(curr_frame)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(prev_gray, curr_gray, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))