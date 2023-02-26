#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 19-5-16 下午6:26
# @Author  : MaybeShewill-CV
# @Site    : https://github.com/MaybeShewill-CV/lanenet-lane-detection
# @File    : evaluate_lanenet_on_tusimple.py
# @IDE: PyCharm
"""
Evaluate lanenet model on tusimple lane dataset
"""
import py_compile
import roslib
roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import psutil
from ros_referee.msg import ProcessStatus
import json
import sys
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post

import argparse
import glob
import os
import os.path as ops
import time
# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import tqdm
import matplotlib.pyplot as plt

from lanenet_model import lanenet
from lanenet_model import lanenet_postprocess
from local_utils.config_utils import parse_config_utils
from local_utils.log_util import init_logger
import torch

os.system("export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1")

# import cProfiler

CFG = parse_config_utils.lanenet_cfg
LOG = init_logger.get_logger(log_file_name_prefix='lanenet_eval')

def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

def init_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, help='The source tusimple lane test data dir')
    parser.add_argument('--weights_path', type=str, help='The model weights path')
    parser.add_argument('--save_dir', type=str, help='The test output save root dir')

    return parser.parse_args()

def minmax_scale(input_arr):
    """

    :param input_arr:
    :return:
    """
    min_val = np.min(input_arr)
    max_val = np.max(input_arr)

    output_arr = (input_arr - min_val) * 255.0 / (max_val - min_val)

    return output_arr

def eval_lanenet(src_dir, weights_path):
    """

    :param src_dir:
    :param weights_path:
    :param save_dir:
    :return:
    """
    #assert ops.exists(src_dir), '{:s} not exist'.format(src_dir)

    #os.makedirs(save_dir, exist_ok=True)

class lanenet_node:
    
    def __init__(self):
        
        weights_path = '/home/mobilitylab/projects/PDNN/catkin_ws/src/ros_lane_detection/scripts/lanenet-lane-detection/BiseNetV2_LaneNet_Tusimple_Model_Weights/tusimple_lanenet.ckpt'
        self.input_tensor = tf.placeholder(dtype=tf.float32, shape=[1, 256, 512, 3], name='input_tensor')
        
        self.net = lanenet.LaneNet(phase='test', cfg=CFG)
        self.binary_seg_ret, self.instance_seg_ret = self.net.inference(input_tensor=self.input_tensor, name='LaneNet')

        self.postprocessor = lanenet_postprocess.LaneNetPostProcessor(cfg=CFG)

        saver = tf.train.Saver()

        physical_devices = tf.config.list_physical_devices('GPU')
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        # Disable first three GPU
        # tf.config.set_visible_devices(physical_devices[3:], 'GPU')
        tf.config.set_visible_devices(physical_devices[3:], 'GPU')
        logical_devices = tf.config.list_logical_devices('GPU')

        # Set sess configuration
        # sess_config = tf.ConfigProto()
        # sess_config.gpu_options.per_process_gpu_memory_fraction = CFG.GPU.GPU_MEMORY_FRACTION
        # sess_config.gpu_options.allow_growth = CFG.GPU.TF_ALLOW_GROWTH
        # sess_config.gpu_options.allocator_type = 'BFC'

        # self.sess = tf.Session(config=sess_config)
        self.sess = tf.Session()

        # f = open('latency-agx-rt-lanenet-road10.log','wt')
        # fb = open('latency-agx-rt-lanenet-road10-postbreak.log','wt')
        # f_train = open('clustering-training-data.log','wt')
        
        path = '/home/mobilitylab/projects/PDNN/EdgePerf-benchmark/Road/10/0000000588.png'

        with self.sess.as_default():
            saver.restore(sess=self.sess, save_path=weights_path)
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            image_vis = image
            image = cv2.resize(image, (512, 256), interpolation=cv2.INTER_LINEAR)
            image = image / 127.5 - 1.0
            binary_seg_image, instance_seg_image = self.sess.run(
                [self.binary_seg_ret, self.instance_seg_ret],
                feed_dict={self.input_tensor: [image]}
            )

            # postprocess_result, td, fe, tc = self.postprocessor.postprocess(
            #     binary_seg_result=binary_seg_image[0],
            #     instance_seg_result=instance_seg_image[0],
            #     source_image=image_vis
            # )
            
        #self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('lanenet_process_status', ProcessStatus, queue_size=1)

        self.current_seq = 0
        
    def callback(self, frame):
        sf = rospy.get_param("lane_skip_frames")
        delay = frame.header.seq-self.current_seq
        print(delay)
        if sf == 0 and delay < rospy.get_param("delay_thresh"):
            t1 = time_synchronized()
            image = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
            t2 = time_synchronized()

            image_vis = image
            image = cv2.resize(image, (512, 256), interpolation=cv2.INTER_LINEAR)
            image = image / 127.5 - 1.0

            t3 = time_synchronized()

            binary_seg_image, instance_seg_image = self.sess.run(
                [self.binary_seg_ret, self.instance_seg_ret],
                feed_dict={self.input_tensor: [image]}
            )
            # print(binary_seg_image.size, instance_seg_image.size)

            t4 = time_synchronized()

            postprocess_result, td, fe, tc = self.postprocessor.postprocess(
                binary_seg_result=binary_seg_image[0],
                instance_seg_result=instance_seg_image[0],
                source_image=image_vis
            )
            
            # tm = time_synchronized()

            # mask_image = postprocess_result['mask_image']

            # for i in range(CFG.MODEL.EMBEDDING_FEATS_DIMS):
            #     instance_seg_image[0][:, :, i] = minmax_scale(instance_seg_image[0][:, :, i])
            # embedding_image = np.array(instance_seg_image[0], np.uint8)

            # plt.figure('mask_image')
            # plt.imshow(mask_image)
            # plt.figure('src_image')
            # plt.imshow(image_vis[:, :, (2, 1, 0)])
            # plt.figure('instance_image')
            # plt.imshow(embedding_image[:, :, (2, 1, 0)])
            # plt.figure('binary_image')
            # plt.imshow(binary_seg_image[0] * 255, cmap='gray')
            # plt.show(block=False)
            # plt.imshow(postprocess_result['source_image'])
            # plt.show()

            t5 = time_synchronized()
            # print(ds)
            # print(t2-t1,t3-t2,t4-t3,t5-t4,t5-t1)
            # print(frame.header.seq)

            pid = os.getpid()
            msg = get_proc_status(pid)
            # msg.header.stamp = rospy.Time.now()
            msg.header.stamp = frame.header.stamp 
            # msg.probability = 
            msg.runtime = t5-t1

            if td != None:
                msg.proposals = td[0]
                msg.objects = td[1]
                # rospy.loginfo(msg)
                self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("lane_skip_frames", 0)
        elif sf > 0:
            rospy.set_param("lane_skip_frames", sf-1)
        self.current_seq = frame.header.seq

if __name__ == '__main__':
    ic = lanenet_node()
    rospy.init_node('lanenet_node')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()