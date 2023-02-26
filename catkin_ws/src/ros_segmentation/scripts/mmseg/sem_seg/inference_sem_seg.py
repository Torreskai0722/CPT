from cgi import test
import mmcv
import time
import os
import glob
from bs4 import BeautifulSoup
import requests
import torch
from mmseg.apis import inference_segmentor, init_segmentor, show_result_pyplot
from mmseg.core.evaluation import get_palette
import numpy as np
from statistics import mean
import signal

class inference_test:
    def __init__(self):
        self.url = "https://dl.cv.ethz.ch/bdd100k/sem_seg/models/"
        self.ext = "pth"
        self.config_file_base = (
            "/home/mobilitylab/catkin_ws/src/ros_segmentation/scripts/mmseg/sem_seg/configs/sem_seg/"
        )

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
        self.model = init_segmentor(config_file, load_from, device="cuda:0")

        # test a single image and show the results
        # img = 'test.jpg'  # or img = mmcv.imread(img), which will only load it once
        for img in self.paths[:2]:
            start = time.monotonic()
            result = inference_segmentor(self.model, img)
            print(result)
            end = time.monotonic()
            print(end - start)
        # visualize the results in a new window
            self.model.show_result(img, result,out_file='result.jpg')
        # or save the visualization results to image files
        # model.show_result(img, result, out_file='result.jpg')


def main():
    torch.hub.set_dir("/media/hydrapc/hdd-drive/torch/hub")
    infer_test = inference_test()
    infer_test.image_loader()

    # test one model
    modelname = "apcnet_r50-d8_769x769_40k_drivable_bdd100k"
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
    # torch.hub.set_dir("/media/hydrapc/hdd-drive/torch/hub")

    infer_test = inference_test()
    infer_test.video_images_loader()

    #checkfiles = infer_test.listFD()
    #print(checkfiles)
    checkfiles = [ 'deeplabv3+_r50-d8_512x1024_80k_sem_seg_bdd100k.pth',  
    'emanet_r50-d8_769x769_80k_sem_seg_bdd100k.pth', 
    'fcn_hr48_512x1024_80k_sem_seg_bdd100k.pth', 
    'pspnet_r50-d8_512x1024_80k_sem_seg_bdd100k.pth',
    'upernet_convnext-b_fp16_512x1024_80k_sem_seg_bdd100k.pth', 
    'upernet_deit-s_512x1024_80k_sem_seg_bdd100k.pth', 
    'upernet_swin-b_fp16_512x1024_80k_sem_seg_bdd100k.pth',  
    'upernet_vit-b_512x1024_80k_sem_seg_bdd100k.pth']
    torch.cuda.set_device(1)
    for checkfile in checkfiles:
        modelname = str(checkfile).split(".")[0]
        # print(modelname)
        config_file = infer_test.config_file_base + modelname + ".py"
        load_from = infer_test.url + modelname + ".pth"

        print(modelname, config_file, load_from)

        model = init_segmentor(config_file, load_from, device="cuda:1")
        # print(load_from)
        # print(config_file)
        # print(len(video))
        file_name = modelname + ".log"
        f = open("logs/" + file_name, "w")

        for frame in infer_test.paths:
            start = time.monotonic()
            result = inference_segmentor(model, frame)
            end = time.monotonic()
            f.write(str(end - start) + "\n")
            # print(end - start)
        # print(s)
        # f.write(s)
        f.close()

def analyze_logs():
    for infile in sorted(glob.glob('logs/*.log')):
            with open(infile, 'r') as f: # open in readonly mode
                    # do your stuff
                    model_name = f.name[5:-4]
                    da = f.readlines()
                    da = [float(i.rstrip()) for i in da]
                    da = np.array(da)[1:]
                    # print(da)
                    # try:
                    #     re = dict[model_name]
                    # except:
                    #     re = 'NULL'
                    print(model_name, int(max(da)*1000), int(min(da)*1000),
                    int(mean(da)*1000), int((max(da)-min(da))*1000))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    # main()
    test_multimodel_video()
    # analyze_logs()