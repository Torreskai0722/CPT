#!/usr/bin/env python3.6
import cpufreq_client as cpufreq
from statistics import mean, stdev, variance
from collections import Counter
import time
import math

gover = ["conservative", "ondemand", "userspace", "powersave", "performance", "schedutil"]
freq = [3301000, 3300000, 3100000, 3000000, 2800000, 2700000, 2500000, 2400000, 2200000, 2100000, 1900000, 1800000, 1600000, 1500000, 1300000, 1200000]
NUM = 100

cpufreq.reset()
print(cpufreq.get_available_frequencies())
# [3301000, 3300000, 3100000, 3000000, 2800000, 2700000, 2500000, 2400000, 2200000, 2100000, 1900000, 1800000, 1600000, 1500000, 1300000, 1200000]
print(cpufreq.get_available_governors())
print(cpufreq.get_driver())

print(type(freq[0]))

cpufreq.set_governors(gover[2])
data = []
# change frequencies time overhead
for i in range(len(freq)):
    for j in range(len(freq)):
        if i != j:
            line = []
            for k in range(NUM):
                cpufreq.set_frequencies(freq[i])
                t0 = time.time()
                cpufreq.set_frequencies(freq[j])
                t1 = time.time()
                line.append(1000*(t1-t0))
                # print("Frequency %s to Frequency %s, latency: %s" % (freq[i], freq[j], str(t1-t0)))
                time.sleep(0.2)
            a = mean(line)
            b = max(line)
            c = min(line)
            d = stdev(line) / a
            x = [freq[i],freq[j], a, b, c, b-c, d]
            data.append(x)
            print(x)
            # print("\n")
    # print(cpufreq.get_frequencies())

# change governors time overhead
# for i in range(len(gover)):
#     for j in range(len(gover)):
#         if i != j:
#             for k in range(NUM):
#                 cpufreq.set_governors(gover[i])
#                 t0 = time.time()
#                 cpufreq.set_governors(gover[j])
#                 t1 = time.time()
#                 print("%s to %s, latency: %s" % (gover[i], gover[j], str(t1-t0)))
#                 time.sleep(0.2)
#             print("\n")
    #print(cpufreq.get_governors())

#cpufreq.reset()
#cpu.reset()
# cpu.disable_hyperthread()

# freqs= cpu.get_frequencies()
# print(freqs)

# govs= cpu.get_governors()
# print(govs)

# online_cpus= cpu.get_online_cpus()
# print(online_cpus)

#available_govs = cpufreq.available_governors()
#print(available_govs)

# cpu.set_governors("powersave")
# govs= cpu.get_governors()
# print(govs)

# cpu.set_governors("performance")
# govs= cpu.get_governors()
# print(govs)

# cpu.set_governors("userspace")
# govs= cpu.get_governors()
# print(govs)

# available_freqs= cpu.available_frequencies
# print(available_freqs)
# for f in available_freqs[1:]:
    # cpu.set_frequencies(f)
    # mfreq= []
    # for _ in range(10):
        # freqs= cpu.get_frequencies()
        # mfreq.append(Counter(freqs))
        # time.sleep(0.1)
    # print(sum(mfreq,Counter()))
    
# cpu.disable_cpu(2)
# print(cpu.get_online_cpus())
# cpu.enable_cpu(2)
# print(cpu.get_online_cpus())
cpufreq.reset()