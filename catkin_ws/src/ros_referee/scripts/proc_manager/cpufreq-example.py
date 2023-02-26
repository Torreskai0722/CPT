#!/usr/bin/env python3.6
import cpufreq_client as cpufreq
from collections import Counter
import time

gover = ["conservative", "ondemand", "powersave", "performance", "schedutil"]

cpufreq.reset()
#cpu.reset()
# cpu.disable_hyperthread()

# freqs= cpu.get_frequencies()
# print(freqs)

# govs= cpu.get_governors()
# print(govs)

# online_cpus= cpu.get_online_cpus()
# print(online_cpus)

available_govs = cpufreq.available_governors()
print(available_govs)

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