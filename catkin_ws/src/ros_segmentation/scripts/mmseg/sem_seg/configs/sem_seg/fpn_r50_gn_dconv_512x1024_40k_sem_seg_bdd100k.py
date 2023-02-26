"""FPN with ResNet-50."""

_base_ = [
    "../_base_/models/fpn_r50.py",
    "../_base_/datasets/bdd100k_512x1024.py",
    "../_base_/default_runtime.py",
    "../_base_/schedules/schedule_40k.py",
]
model = dict(
    decode_head=dict(
        norm_cfg=dict(type="GN", num_groups=32, requires_grad=True),
        conv_cfg=dict(type="DCNv2"),
    )
)
load_from = "https://dl.cv.ethz.ch/bdd100k/sem_seg/models/fpn_r50_gn_dconv_512x1024_40k_sem_seg_bdd100k.pth"
