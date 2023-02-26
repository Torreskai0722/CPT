#! /usr/bin/env python3.6
# coding=utf-8
#############################################################################################################
##
##  Source code for testing
##
#############################################################################################################

import roslib
roslib.load_manifest('video_stream_opencv')
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import psutil
from ros_referee.msg import ProcessStatus
import sys
from proc_util import get_proc_status, get_proc_children, benchmark_pre, benchmark_post

import cv2
import json
import torch
import agent
import numpy as np
from copy import deepcopy
from data_loader import Generator
import time
from parameters import Parameters
import util
import glob
import os
from sklearn.preprocessing import PolynomialFeatures
from torch.profiler import profile, record_function, ProfilerActivity
import proc_client as pc

def time_synchronized():
    torch.cuda.synchronize(torch.device("cuda:0")) if torch.cuda.is_available() else None
    return time.time()

# def predict_time(len_raw, len_mask):
#     a = [[len_raw, len_mask]]
#     poly = PolynomialFeatures(3)
#     b = poly.fit_transform(a)
#     # print(b)
#     eliminate_time = 0
#     w = [0,-1.67523118e-02,3.70423296e-03,3.41350306e-03,-5.36147603e-04,1.64606226e-05]
    
#     # eliminate_time_new = len_raw*w[1] + len_mask*w[2] + len_raw**2*w[3] + len_raw*len_mask*w[4] + w[5]*len_mask**2
    
#     for i in range(len(w)):
#         eliminate_time += b[0][i]*w[i]
    
#     # print(eliminate_time-eliminate_time_new)
#     ta = eliminate_time + 0.14083779674141497
    
#     return ta

# ############################################################################
# ## linear interpolation for fixed y value on the test dataset
# ############################################################################
# def find_target(x, y, target_h, ratio_w, ratio_h):
#     # find exact points on target_h
#     out_x = []
#     out_y = []
#     x_size = p.x_size/ratio_w
#     y_size = p.y_size/ratio_h
#     for i, j in zip(x,y):
#         min_y = min(j)
#         max_y = max(j)
#         temp_x = []
#         temp_y = []
#         for h in target_h:
#             temp_y.append(h)
#             if h < min_y:
#                 temp_x.append(-2)
#             elif min_y <= h and h <= max_y:
#                 for k in range(len(j)-1):
#                     if j[k] >= h and h >= j[k+1]:
#                         #linear regression
#                         if i[k] < i[k+1]:
#                             temp_x.append(int(i[k+1] - float(abs(j[k+1] - h))*abs(i[k+1]-i[k])/abs(j[k+1]+0.0001 - j[k])))
#                         else:
#                             temp_x.append(int(i[k+1] + float(abs(j[k+1] - h))*abs(i[k+1]-i[k])/abs(j[k+1]+0.0001 - j[k])))
#                         break
#             else:
#                 if i[0] < i[1]:
#                     l = int(i[1] - float(-j[1] + h)*abs(i[1]-i[0])/abs(j[1]+0.0001 - j[0]))
#                     if l > x_size or l < 0 :
#                         temp_x.append(-2)
#                     else:
#                         temp_x.append(l)
#                 else:
#                     l = int(i[1] + float(-j[1] + h)*abs(i[1]-i[0])/abs(j[1]+0.0001 - j[0]))
#                     if l > x_size or l < 0 :
#                         temp_x.append(-2)
#                     else:
#                         temp_x.append(l)
#         out_x.append(temp_x)
#         out_y.append(temp_y)
    
#     return out_x, out_y

# ############################################################################
# ## write result
# ############################################################################
# def write_result_json(result_data, x, y, testset_index):
#     for i in x:
#         result_data[testset_index]['lanes'].append(i)
#         result_data[testset_index]['run_time'] = 1
#     return result_data

# ############################################################################
# ## save result by json form
# ############################################################################
# def save_result(result_data, fname):
#     with open(fname, 'w') as make_file:
#         for i in result_data:
#             json.dump(i, make_file, separators=(',', ': '))
#             make_file.write("\n")

class pinet_node:
    
    def __init__(self):
        self.p = Parameters()
        os.environ["CUDA_AVAILABLE_DEVICES"] = "0"
        print('Get agent')
        if self.p.model_path == "":
            self.lane_agent = agent.Agent()
        else:
            self.lane_agent = agent.Agent()
            self.lane_agent.load_weights(804, "tensor(0.5786)")

        print('Setup GPU mode')
        if torch.cuda.is_available():
            print("use GPU")
            self.lane_agent.cuda()

        print('Testing loop')
        self.lane_agent.evaluate_mode()
        
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)
        self.status_pub = rospy.Publisher('pinet_process_status', ProcessStatus, queue_size=1)

        self.current_seq = 0

    def callback(self, frame):
        sf = rospy.get_param("lane_skip_frames")
        delay = frame.header.seq-self.current_seq
        # print(delay)
        if sf == 0 and delay < rospy.get_param("delay_thresh"):
            with record_function("model_inference_"+str(frame.header.seq)):
                t1 = time_synchronized()
                image = np.frombuffer(frame.data, dtype=np.uint8).reshape(frame.height, frame.width, -1)
                
                t2 = time_synchronized()
                test_image = cv2.resize(image, (512,256))/255.0
                # print(test_image.shape)
                # print(test_image)
                test_image = np.rollaxis(test_image, axis=2, start=0)
                # print(test_image.shape)
                # print(np.array([test_image]).shape)
                t3 = time_synchronized()
                _, _, ti, td = self.test(self.lane_agent, np.array([test_image]))
                t4 = time_synchronized()
                #print(t2-t1,t3-t2,t4-t3,t4-t1)
                # print(frame.header.seq)
            
            
            pid = os.getpid()
            msg = get_proc_status(pid)
            msg.header.stamp = frame.header.stamp
            msg.imgseq = frame.header.seq
            msg.runtime = t4-t1
            if td != [[0]]:
                msg.proposals = td[7]
                msg.objects = td[6]
            print(frame.header.stamp,t4-t1)
            # msg.probability
            # if msg.scheduling_policy == "SCHED_DEADLINE":
            #     print(1000*(t4-t1))

            # print(td[5],td[6],td[7],t4-t1)
                
            # rospy.loginfo(msg)
            self.status_pub.publish(msg)
        elif sf < 0:
            rospy.set_param("lane_skip_frames", 0)
        elif sf > 0:
            rospy.set_param("lane_skip_frames", sf-1)
        self.current_seq = frame.header.seq
    
    ############################################################################
    ## test on the input test image
    ############################################################################
    def test(self, lane_agent, test_images):
        
        thresh = self.p.threshold_point

        t0 = time_synchronized()
        result = lane_agent.predict_lanes_test(test_images)
        confidences, offsets, instances = result[-1]
        # print(confidences.shape)
        # print(offsets.shape)
        # print(instances.shape)
        
        t1 = time_synchronized()
        
        num_batch = len(test_images)
        # print(num_batch)

        out_x = []
        out_y = []
        out_images = []

        for i in range(num_batch):
            p0 = time_synchronized()
            
            # test on test data set
            image = deepcopy(test_images[i])
            image =  np.rollaxis(image, axis=2, start=0)
            image =  np.rollaxis(image, axis=2, start=0)*255.0
            image = image.astype(np.uint8).copy()
            # print(confidences[i].shape)

            confidence = confidences[i].view(self.p.grid_y, self.p.grid_x).cpu().data.numpy()
            # print(confidence.shape) # (32, 64)
            # print(offsets[i][0])

            offset = offsets[i].cpu().data.numpy()
            offset = np.rollaxis(offset, axis=2, start=0)
            offset = np.rollaxis(offset, axis=2, start=0)
            # print(offset.shape) # (32, 64, 2)
            
            instance = instances[i].cpu().data.numpy()
            instance = np.rollaxis(instance, axis=2, start=0)
            instance = np.rollaxis(instance, axis=2, start=0)
            # print(instance.shape) # (32, 64, 4)
            
            p1 = time_synchronized()

            # generate point and cluster
            raw_x, raw_y, len_mask = self.generate_result(confidence, offset, instance, thresh)

            if rospy.get_param("lane_gpu_yield") == True and len_mask > rospy.get_param("pinet_len_mask"):
                return out_x, out_y,  out_images, [[0]]
            
            p2 = time_synchronized()
            
            # print(raw_x.shape)
            # print(raw_y.shape)

            # eliminate fewer points
            in_x, in_y = self.eliminate_fewer_points(raw_x, raw_y)
            # print(in_x.shape)
            # print(in_y.shape)
                    
            # sort points along y 
            in_x, in_y = util.sort_along_y(in_x, in_y)
            # print(in_x.shape, in_y.shape)  
            in_x, in_y = self.eliminate_out(in_x, in_y, confidence, deepcopy(image))
            in_x, in_y = util.sort_along_y(in_x, in_y)
            in_x, in_y = self.eliminate_fewer_points(in_x, in_y)
            
            p3 = time_synchronized()
            # pm = time_synchronized()

            # result_image = util.draw_points(in_x, in_y, deepcopy(image))

            out_x.append(in_x)
            out_y.append(in_y)
            # out_images.append(result_image)
            
            p4 = time_synchronized()
        
        t2 = time_synchronized()
        
        # print(t1-t0, p1-p0, p2-p1, p3-p2, p4-p3, len(raw_x), len(raw_y))
        
        td = [t1-t0, p1-p0, p2-p1, p3-p2, p4-p3, len(raw_x), len(in_x), len_mask]
        # td=[]
        # print(td)
        # print(len_mask)
        # print("\n")
        return out_x, out_y,  out_images, td

    ############################################################################
    ## post processing for eliminating outliers
    ############################################################################
    def eliminate_out(self, sorted_x, sorted_y, confidence, image = None):
        out_x = []
        out_y = []

        for lane_x, lane_y in zip(sorted_x, sorted_y):
            
            # print("333333333333333333333333")
            # print(len(lane_x))
            # print(len(lane_y))

            lane_x_along_y = np.array(deepcopy(lane_x))
            lane_y_along_y = np.array(deepcopy(lane_y))

            ind = np.argsort(lane_x_along_y, axis=0)
            # print(ind)
            lane_x_along_x = np.take_along_axis(lane_x_along_y, ind, axis=0)
            lane_y_along_x = np.take_along_axis(lane_y_along_y, ind, axis=0)
            
            if lane_y_along_x[0] > lane_y_along_x[-1]: #if y of left-end point is higher than right-end
                starting_points = [(lane_x_along_y[0], lane_y_along_y[0]), (lane_x_along_y[1], lane_y_along_y[1]), (lane_x_along_y[2], lane_y_along_y[2]),
                                    (lane_x_along_x[0], lane_y_along_x[0]), (lane_x_along_x[1], lane_y_along_x[1]), (lane_x_along_x[2], lane_y_along_x[2])] # some low y, some left/right x
            else:
                starting_points = [(lane_x_along_y[0], lane_y_along_y[0]), (lane_x_along_y[1], lane_y_along_y[1]), (lane_x_along_y[2], lane_y_along_y[2]),
                                    (lane_x_along_x[-1], lane_y_along_x[-1]), (lane_x_along_x[-2], lane_y_along_x[-2]), (lane_x_along_x[-3], lane_y_along_x[-3])] # some low y, some left/right x            
        
            # print("starting points")
            # print(len(starting_points))
            temp_x = []
            temp_y = []
            # get lines for the same lane
            for start_point in starting_points:
                temp_lane_x, temp_lane_y = self.generate_cluster(start_point, lane_x, lane_y, image)
                temp_x.append(temp_lane_x)
                temp_y.append(temp_lane_y)
            
            max_lenght_x = None
            max_lenght_y = None
            max_lenght = 0
            # print("lane points")
            # print(len(temp_x))
            # print(temp_x,temp_y)
            # get the longest lines for lane
            for i, j in zip(temp_x, temp_y):
                if len(i) > max_lenght:
                    max_lenght = len(i)
                    max_lenght_x = i
                    max_lenght_y = j
            out_x.append(max_lenght_x)
            out_y.append(max_lenght_y)
            # print(len(out_x))
        # print(out_x)

        return out_x, out_y

    ############################################################################
    ## generate cluster
    ############################################################################
    def generate_cluster(self, start_point, lane_x, lane_y, image = None):
        cluster_x = [start_point[0]]
        cluster_y = [start_point[1]]

        point = start_point
        while True:
            points = util.get_closest_upper_point(lane_x, lane_y, point, 3)
            
            max_num = -1
            max_point = None

            if len(points) == 0:
                break
            if len(points) < 3:
                for i in points: 
                    cluster_x.append(i[0])
                    cluster_y.append(i[1])                
                break
            for i in points: 
                num, shortest = util.get_num_along_point(lane_x, lane_y, point, i, image)
                if max_num < num:
                    max_num = num
                    max_point = i

            total_remain = len(np.array(lane_y)[np.array(lane_y) < point[1]])
            cluster_x.append(max_point[0])
            cluster_y.append(max_point[1])
            point = max_point
            
            if len(points) == 1 or max_num < total_remain/5:
                break

        return cluster_x, cluster_y

    ############################################################################
    ## remove same value on the prediction results
    ############################################################################
    def remove_same_point(self, x, y):
        out_x = []
        out_y = []
        for lane_x, lane_y in zip(x, y):
            temp_x = []
            temp_y = []
            for i in range(len(lane_x)):
                if len(temp_x) == 0 :
                    temp_x.append(lane_x[i])
                    temp_y.append(lane_y[i])
                else:
                    if temp_x[-1] == lane_x[i] and temp_y[-1] == lane_y[i]:
                        continue
                    else:
                        temp_x.append(lane_x[i])
                        temp_y.append(lane_y[i])     
            out_x.append(temp_x)  
            out_y.append(temp_y)  
        return out_x, out_y

    ############################################################################
    ## eliminate result that has fewer points than threshold
    ############################################################################
    def eliminate_fewer_points(self, x, y):
        # eliminate fewer points
        out_x = []
        out_y = []
        for i, j in zip(x, y):
            if len(i)>2:
                out_x.append(i)
                out_y.append(j)     
        return out_x, out_y   

    ############################################################################
    ## generate raw output
    ############################################################################
    def generate_result(self, confidance, offsets,instance, thresh):

        mask = confidance > thresh
        # print(confidance[mask])
        # print(mask.shape) (32, 64)
        # print(p.grid_location.shape) # (32, 64, 2)
        
        grid = self.p.grid_location[mask]
        offset = offsets[mask]
        feature = instance[mask]
        # print(grid.shape)
        # print(grid)
        # print(offset)
        # print(offset.shape)
        # print(feature.shape)
        # print(feature)
        
        # print(grid.shape[0])

        lane_feature = []
        x = []
        y = []
        for i in range(len(grid)):
            if (np.sum(feature[i]**2))>=0:
                point_x = int((offset[i][0]+grid[i][0])*self.p.resize_ratio)
                point_y = int((offset[i][1]+grid[i][1])*self.p.resize_ratio)
                if point_x > self.p.x_size or point_x < 0 or point_y > self.p.y_size or point_y < 0:
                    continue
                if len(lane_feature) == 0:
                    lane_feature.append(feature[i])
                    x.append([])
                    x[0].append(point_x)
                    y.append([])
                    y[0].append(point_y)
                    # print("1111111111111111111111111")
                    # print(x)
                    # print(y)
                    # print(lane_feature)
                else:
                    # print("22222222222222")
                    # print(lane_feature)
                    flag = 0
                    index = 0
                    for feature_idx, j in enumerate(lane_feature):
                        index += 1
                        if index >= 12:
                            index = 12
                        if np.linalg.norm((feature[i] - j)**2) <= self.p.threshold_instance:
                            # calculate the average feature value for the same instance
                            lane_feature[feature_idx] = (j*len(x[index-1]) + feature[i])/(len(x[index-1])+1)
                            # print(len(x[index-1]))
                            x[index-1].append(point_x)
                            y[index-1].append(point_y)
                            flag = 1
                            # print(x[index-1])
                            break
                    if flag == 0:
                        lane_feature.append(feature[i])
                        x.append([])
                        x[index].append(point_x) 
                        y.append([])
                        y[index].append(point_y)
        # print(x)
        # print(y)
        # for i, j in zip(x,y):
        #     print(i)
        #     print(j)
                    
        return x, y, grid.shape[0]


if __name__ == '__main__':
    # pc.set_scheduling_policy_deadline(os.getpid(),50000000,50000000,100000000)
    # print(os.getpid())
    rospy.init_node('pinet_node')
    ic = pinet_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()