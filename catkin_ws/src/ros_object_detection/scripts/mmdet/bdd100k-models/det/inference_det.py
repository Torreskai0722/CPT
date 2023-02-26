from cgi import test
from mmdet.apis import init_detector, inference_detector
import mmcv
import time
import os
import glob
from bs4 import BeautifulSoup
import requests
import torch
import signal

class inference_test:
    def __init__(self):
        self.url = "https://dl.cv.ethz.ch/bdd100k/det/models/"
        self.ext = "pth"
        self.config_file_base = (
            "/home/mobilitylab/catkin_ws/src/ros_object_detection/scripts/mmdet/bdd100k-models/det/configs/det/"
        )
        # self.IMAGE_FILE = "/home/hydrapc/Downloads/EdgePerf-benchmark/Road/10"
        # self.IMAGE_FILE = '/home/hydrapc/projects/MTL/bdd100k-models/data/bdd100k/images/10k/test'
        # self.IMAGE_FILE = '/home/nvidia/Downloads/EdgePerf-benchmark/Road/10'

    def video_images_loader(self):
        
        VIDEO_FILE = '/home/mobilitylab/images/'
        # f = open('image-file-pub-yolov3.log','wt')

        # a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf', 
        # 'cac07407-ba37148a', 'cac07407-e969f06a', 'cac07407-bc0b048a', 'cac07407-15b814db', 
        # 'cac07407-76e4c968', 'cac07407-fe32e494']
        
        a = ['cac07407-0396e053', 'cac07407-196cd6f8', 'cac07407-951977c8', 'cac07407-0eb1c8bf']

        paths = []
        for i in a:
            print(i)
            pd = glob.glob(os.path.join(VIDEO_FILE + str(i) + "/", '*.jpg'))
            paths.extend(pd)
        paths = sorted(paths, key=os.path.getmtime)
        print(len(paths))

        self.paths = paths

    def listFD(self):
        page = requests.get(self.url).text
        # print(page)
        soup = BeautifulSoup(page, "html.parser")
        # print(soup)
        return [
            node.get("href")
            for node in soup.find_all("a")
            if node.get("href").endswith(self.ext)
        ]

    def inference_image(self, config_file, load_from):
        # build the model from a config file and a checkpoint file
        # torch.hub.set_dir("/media/hydrapc/hdd-drive/torch/hub")
        self.model = init_detector(config_file, load_from, device="cuda:0")

        # test a single image and show the results
        # img = 'test.jpg'  # or img = mmcv.imread(img), which will only load it once
        for img in self.paths:
            start = time.monotonic()
            result = inference_detector(self.model, img)
            # print(result)
            end = time.monotonic()
            print(end - start)
        # visualize the results in a new window
        # self.model.show_result(img, result)
        # or save the visualization results to image files
        # model.show_result(img, result, out_file='result.jpg')


def main():
    infer_test = inference_test()
    infer_test.video_images_loader()

    # test one model
    modelname = "cascade_rcnn_convnext-b_fpn_fp16_3x_det_bdd100k"
    config_file = infer_test.config_file_base + modelname + ".py"
    load_from = infer_test.url + modelname + ".pth"
    infer_test.inference_image(config_file, load_from)

    # # test on all models
    # checkfiles = infer_test.listFD()
    # print(checkfiles)
    # for checkfile in checkfiles:
    #     modelname = str(checkfile).split(".")[0]
    #     print(modelname)
    #     config_file = infer_test.config_file_base + modelname + ".py"
    #     load_from = infer_test.url + modelname + ".pth"
    #     print(load_from)
    #     print(config_file)
    #     infer_test.inference_image(config_file, load_from)

    # test a video and show the results
    # video_path = (
    #     "/home/hydrapc/Downloads/bdd100k_videos_test_00/bdd100k/videos/test/"
    # )
    # video = mmcv.VideoReader(video_path + "cc59b570-fa6f8d84.mov")
    # print("video detection started")
    # for frame in video:
    #     start = time.monotonic()
    #     result = inference_detector(infer_test.model, frame)
    #     end = time.monotonic()
    #     print(end - start)
    #     infer_test.model.show_result(frame, result, wait_time=1)


def test_multimodel_video():
    # video_path = (
    #     "/home/hydrapc/Downloads/bdd100k_videos_test_00/bdd100k/videos/test/"
    # )
    # video = mmcv.VideoReader(video_path + "cc59b570-fa6f8d84.mov")
    # print("video detection started")

    infer_test = inference_test()
    infer_test.video_images_loader()

    #checkfiles = infer_test.listFD()
    #print(checkfiles)
    # checkfiles = [ 'atss_r101_fpn_3x_det_bdd100k.pth', 
    # 'cascade_rcnn_r101_fpn_3x_det_bdd100k.pth', 
    # 'cascade_rcnn_swin-t_fpn_3x_det_bdd100k.pth',
    # 'faster_rcnn_r101_fpn_3x_det_bdd100k.pth', 
    # 'fcos_r101_fpn_3x_det_bdd100k.pth', 
    # 'libra_faster_rcnn_r101_fpn_3x_det_bdd100k.pth', 
    # 'retinanet_r101_fpn_3x_det_bdd100k.pth',  
    # 'sparse_rcnn_r101_fpn_3x_det_bdd100k.pth']
    checkfiles = ['cascade_rcnn_convnext-s_fpn_fp16_3x_det_bdd100k.pth']

    for checkfile in checkfiles:
        modelname = str(checkfile).split(".")[0]
        print(modelname)
        config_file = infer_test.config_file_base + modelname + ".py"
        load_from = infer_test.url + modelname + ".pth"

        model = init_detector(config_file, load_from, device="cuda:0")
        # print(load_from)
        # print(config_file)
        # print(len(video))
        file_name = modelname + ".log"
        f = open("logs/" + file_name, "w")

        for frame in infer_test.paths:
            start = time.monotonic()
            result = inference_detector(model, frame)
            end = time.monotonic()
            f.write(str(end - start) + "\n")
            # print(end - start)
        # print(s)
        # f.write(s)
        f.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    # main()
    test_multimodel_video()