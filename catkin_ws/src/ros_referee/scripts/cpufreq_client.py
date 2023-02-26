import socket
import os
import psutil
import yaml

SCHED_OTHER = 0
SCHED_FIFO = 1
SCHED_RR = 2
SCHED_BATCH = 3
SCHED_IDLE = 4
PROC_MANAGER_SOCK = "/tmp/cpufreq_manager"
PORT = 65500

cpug = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}

def send_to_proc_manager(order):
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	try:
		sock.connect(PROC_MANAGER_SOCK)
		# print("yes!")
	except socket.error:
		print('Failed connect to {}'.format(PROC_MANAGER_SOCK))
		return -1
	# print(order)
	# print(yaml.dump(order))
	sock.send(yaml.dump(order).encode())
	ret = sock.recv(1024)
	sock.close()
	# print(ret)
	return ret

def enable_all_cpu():
	order = {
		"name": "enable_all_cpu"
	}
	return send_to_proc_manager(order)

def reset():
	order = {
		"name": "reset"
	}
	return send_to_proc_manager(order)

def disable_hyperthread():
	order = {
		"name": "disable_hyperthread"
	}
	return send_to_proc_manager(order)

def disable_cpu(rg=cpug):
	order = {
		"name": "disable_cpu",
		"rg": rg
	}
	return send_to_proc_manager(order)

def enable_cpu(rg=cpug):
	order = {
		"name": "enable_cpu",
		"rg": rg
	}
	return send_to_proc_manager(order)

def set_frequencies(freq, rg=cpug):
	order = {
		"name": "set_frequencies",
		"freq": freq,
		"rg": rg
	}
	return send_to_proc_manager(order)

def set_min_frequencies(freq, rg=cpug):
	order = {
		"name": "set_min_frequencies",
		"minfreq": freq,
		"rg": rg
	}
	return send_to_proc_manager(order)

def set_max_frequencies(freq, rg=cpug):
	order = {
		"name": "set_max_frequencies",
		"maxfreq": freq,
		"rg": rg
	}
	return send_to_proc_manager(order)

def set_governors(gover, rg=cpug):
	order = {
		"name": "set_governors",
		"gover": gover,
		"rg": rg
	}
	return send_to_proc_manager(order)

def get_online_cpus():
	order = {
		"name": "get_online_cpus"
	}
	return send_to_proc_manager(order)

def get_governors():
	order = {
		"name": "get_governors"
	}
	return send_to_proc_manager(order)

def get_frequencies():
	order = {
		"name": "get_frequencies"
	}
	return send_to_proc_manager(order)

def get_available_governors():
	order = {
		"name": "get_available_governors"
	}
	return send_to_proc_manager(order)

def get_available_frequencies():
	order = {
		"name": "get_available_frequencies"
	}
	return send_to_proc_manager(order)

def get_driver():
	order = {
		"name": "get_driver"
	}
	return send_to_proc_manager(order)

if __name__ == "__main__":
    # proc = psutil.Process(os.getpid())
    # proc = psutil.Process(17302)
    # print(get_cpu_count())
    # print(get_proc_cpu_affinity(proc))
	# update_proc_cpu(24991)
	pid = 29004
	runtime = 20000000 # runtime in nanoseconds
	deadline = 50000000 # deadline in nanoseconds
	period = 50000000  # time period in nanoseconds
	# set_scheduling_policy_deadline(pid, runtime, deadline, period)
	# shutdown_proc_manager()
	get_frequencies()