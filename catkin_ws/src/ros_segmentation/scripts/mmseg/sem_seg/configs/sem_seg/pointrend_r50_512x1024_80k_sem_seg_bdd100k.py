"""PointRend with ResNet-50."""

_base_ = [
    "../_base_/models/pointrend_r50.py",
    "../_base_/datasets/bdd100k_512x1024.py",
    "../_base_/default_runtime.py",
    "../_base_/schedules/schedule_80k.py",
]
lr_config = dict(warmup="linear", warmup_iters=200)
load_from = "https://dl.cv.ethz.ch/bdd100k/sem_seg/models/pointrend_r50_512x1024_80k_sem_seg_bdd100k.pth"
