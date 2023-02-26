"""DeeplabV3 with ResNet-50-d8."""

_base_ = [
    "../_base_/models/deeplabv3_r50-d8.py",
    "../_base_/datasets/bdd100k_512x1024.py",
    "../_base_/default_runtime.py",
    "../_base_/schedules/schedule_80k.py",
]
load_from = "https://dl.cv.ethz.ch/bdd100k/sem_seg/models/deeplabv3_r50-d8_512x1024_80k_sem_seg_bdd100k.pth"
