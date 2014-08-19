#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=memcache writes cpu values every defined X sec
import time
import pylibmc
import psutil

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return round(float(cpu_temp)/1000,1)

shared = pylibmc.Client(["127.0.0.1"], binary=True)
shared.behaviors = {"tcp_nodelay": True, "ketama": True}
try:
    while True:
	shared.set_multi({	'cpu': psutil.cpu_percent(0),
				'disk': psutil.disk_usage('/').percent,
				'ram': psutil.phymem_usage().percent,
				'cpu_temp': get_cpu_temp(),
				'date': time.strftime("%y/%m/%d", time.localtime()),
				'time': time.strftime("%H:%M", time.localtime())
			})
	time.sleep(5.0)
finally:
    #shared.flush_all()
    shared.disconnect_all()
    print "\nclosed"
