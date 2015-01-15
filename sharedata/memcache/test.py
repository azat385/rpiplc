#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mymod
shared = mymod.shared()
# shared["good_rx"] read expmple
import time
shared["test_sleep_ms"]=1.0
sleep_delay = shared["test_sleep_ms"]
#set up cycle time issues	
cur_cycle_time = mymod.cycle_time()
cur_cycle_time.length = 50
k = 0
while (1):
    for i in xrange(0):
	q = 123.456**7.89
    # mymod time module
    cur_cycle_time.call()
    if cur_cycle_time.ready:
        shared["test_time"] = cur_cycle_time.cycle_time_ms[0]
        shared["test_time_arr"] = cur_cycle_time.cycle_time_ms
        sleep_delay = shared["test_sleep_ms"]
	shared["test_count"] = k
    k+=1
    print k,"\r",
    # end main while loop
    time.sleep(sleep_delay/1000.0)
