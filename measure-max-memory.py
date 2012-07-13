#!/usr/bin/env python
import time
import psutil # pip install psutil

def find_max_mem(keyword):
    # find process
    for p in psutil.process_iter():
        if keyword in p.cmdline:
            break
    else: # not found
        return

    # find max memory
    maxmem = 0
    while p.is_running():
        time.sleep(0.1)
        mem = p.get_memory_info().rss*2**-30 # GiB
        if mem > maxmem:
            maxmem = mem
            print("%.3f" % mem)
    return maxmem

while True:
    try:
        mem = find_max_mem('longest_match.py')
    except psutil.error.NoSuchProcess:
        pass
    else:
        if mem is not None:
            print('*'*79)
    time.sleep(1)
