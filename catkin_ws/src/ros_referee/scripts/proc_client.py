import socket
import os
import psutil
import yaml

SCHED_OTHER = 0
SCHED_FIFO = 1
SCHED_RR = 2
SCHED_BATCH = 3
SCHED_IDLE = 4
PROC_MANAGER_SOCK="/tmp/proc_manager"
  
def update_proc_cpu(pid, policy = SCHED_FIFO, priority = 1):
	proc = psutil.Process(pid)

	d = { 'OTHER':SCHED_OTHER, 'FIFO':SCHED_FIFO, 'RR':SCHED_RR, "BATCH":SCHED_BATCH, "IDLE":SCHED_IDLE }
	# policy = SCHED_OTHER
	# priority = 10

	procs = [ proc.pid ] + get_proc_children(proc, r=True)
	print(procs)
	for proc in procs:
		# print('pid={}'.format(proc.pid))
		# nice = get_proc_nice(proc)
		# if set_process_nice(proc, nice) is False:
		# 	print('Err set_process_nice()')
		# cpus = get_proc_cpu_affinity(proc)
		# print('cpus={}'.format(cpus))
		# if set_process_cpu_affinity(proc, cpus) is False:
		# 	print('Err set_process_cpu_affinity()')

		policy_str = next( (k for (k,v) in d.items() if v == policy), '?')
		print(policy_str)
		print('sched policy={} prio={}'.format(policy_str, priority))
		if set_scheduling_policy(proc, policy, priority) is False:
			print('Err scheduling_policy()')

def send_to_proc_manager(order):
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	try:
		sock.connect(PROC_MANAGER_SOCK)
		print("yes!")
	except socket.error:
		print('Failed connect to {}'.format(PROC_MANAGER_SOCK))
		return -1
	print(order)
	print(yaml.dump(order))
	sock.send(yaml.dump(order).encode())
	ret = sock.recv(1024)
	sock.close()
	return int(ret) == 0

def set_process_nice(proc, value):
	order = {
		"name": "nice",
		"pid": proc.pid,
		"nice": value
	}
	return send_to_proc_manager(order)

def set_process_cpu_affinity(proc, cpus):
	order = {
		"name": "cpu_affinity",
		"pid": proc.pid,
		"cpus": cpus,
	}
	return send_to_proc_manager(order)

def shutdown_proc_manager():
	order = {
		"name": "shutdown",
	}
	return send_to_proc_manager(order)

def set_scheduling_policy(pid, policy, priority):
	order = {
		"name": "scheduling_policy",
		"pid": pid,
		"policy": policy,
		"priority": priority,
	}
	return send_to_proc_manager(order)

def set_scheduling_policy_deadline(pid, runtime, deadline, period):
	order = {
		"name": "scheduling_policy_deadline",
		"pid": pid,
		"runtime": runtime,
		"deadline": deadline,
		"period": period
	}
	return send_to_proc_manager(order)

# psutil 3.x to 1.x backward compatibility
def get_cpu_count():
	try:
		return psutil.NUM_CPUS
	except AttributeError:
		return psutil.cpu_count()

def get_proc_children(proc, r=True):
	a = proc.threads()
	id = []
	for i in a:
		id.append(i.id)
	# cmd = 'pstree -p 20026'
	# print(os.system(cmd))
	try:
		# return proc.children(recursive=r)
		print(id)
		return id
	except AttributeError:
		# return proc.children(recursive=r)
		return []

def get_proc_nice(proc):
	try:
		return proc.get_nice()
	except AttributeError:
		return proc.nice()

def get_proc_cpu_affinity(proc):
	try:
		return proc.get_cpu_affinity()
	except AttributeError:
		return proc.cpu_affinity()

if __name__ == "__main__":
    # proc = psutil.Process(os.getpid())
    # proc = psutil.Process(17302)
    # print(get_cpu_count())
    # print(get_proc_cpu_affinity(proc))
	# update_proc_cpu(24991)
	pid = 17744
	runtime = 20000000 # runtime in nanoseconds
	deadline = 50000000 # deadline in nanoseconds
	period = 50000000  # time period in nanoseconds
	set_scheduling_policy_deadline(pid, runtime, deadline, period)
	# shutdown_proc_manager()