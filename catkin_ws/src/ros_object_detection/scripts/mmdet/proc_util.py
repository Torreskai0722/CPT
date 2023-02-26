import os
from ros_referee.msg import ProcessStatus
import time
import json
import psutil

# from PIL import Image
import matplotlib.pyplot as plt

from jetson_benchmarks import utilities, benchmark_argparser
import sys
import glob
import numpy as np

def get_proc_status(pid):
    msg = ProcessStatus()
    ppid = os.getppid()
    proc = psutil.Process(pid)
    
    msg.pid = proc.pid
    msg.ppid = ppid
    msg.app = proc.name()
    msg.cpids = get_proc_children(proc)
    msg.scheduling_policy = sched_dict[os.sched_getscheduler(pid)]
    msg.priority = proc.nice()
    
    return msg

def get_proc_children(proc, r=True):
    a = proc.threads()
    id = []
    for i in a:
        id.append(i.id)
    # cmd = 'pstree -p 20026'
    # print(os.system(cmd))
    try:
		# return proc.children(recursive=r)
        # print(id)
        return id
    except AttributeError:
        # return proc.children(recursive=r)
        return []

#define SCHED_NORMAL		0
#define SCHED_FIFO		1
#define SCHED_RR		2
#define SCHED_BATCH		3
#define SCHED_IDLE		5
#define SCHED_DEADLINE		6
sched_dict = {0: "SCHED_OTHER", 
              1: "SCHED_FIFO", 
              2: "SCHED_RR", 
              3: "SCHED_BATCH", 
              5: "SCHED_IDLE", 
              6: "SCHED_DEADLINE"}

def benchmark_pre(args):
    # System Check
    system_check = utilities(jetson_devkit=args.jetson_devkit, gpu_freq=args.gpu_freq, dla_freq=args.dla_freq)
    system_check.close_all_apps()
    if system_check.check_trt():
        sys.exit()
    system_check.set_power_mode(args.power_mode, args.jetson_devkit)
    system_check.clear_ram_space()
    if args.jetson_clocks:
        system_check.set_jetson_clocks()
    else:
        system_check.run_set_clocks_withDVFS()
        system_check.set_jetson_fan(255)
        
def benchmark_post(args):
    system_check = utilities(jetson_devkit=args.jetson_devkit, gpu_freq=args.gpu_freq, dla_freq=args.dla_freq)
    system_check.clear_ram_space()
    system_check.set_jetson_fan(0)
