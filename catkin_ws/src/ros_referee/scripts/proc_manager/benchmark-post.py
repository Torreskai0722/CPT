import os
import time
import json

# import sys
# py_dll_path = os.path.join(sys.exec_prefix, 'Library', 'bin')
# os.environ['PATH'] += py_dll_path

from jetson_benchmarks import utilities, benchmark_argparser
import sys

import glob

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


if __name__ == '__main__':
    arg_parser = benchmark_argparser()
    args = arg_parser.make_args()
    
    benchmark_post(args)