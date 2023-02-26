"""Mask RCNN with ResNet50-FPN, 1x schedule."""

_base_ = [
    "../_base_/models/mask_rcnn_r50_fpn.py",
    "../_base_/datasets/bdd100k.py",
    "../_base_/schedules/schedule_1x.py",
    "../_base_/default_runtime.py",
]
load_from = "https://dl.cv.ethz.ch/bdd100k/ins_seg/models/mask_rcnn_r50_fpn_1x_ins_seg_bdd100k.pth"
