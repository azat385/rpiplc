#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=работа с GPIO

import RPi.GPIO as GPIO  
print GPIO.VERSION  
print GPIO.RPI_REVISION

import time
from time import sleep     # this lets us have a time delay (see line 12)

def my_callback(intCh):
	import time
	if intCh==25:
	    if GPIO.input(24):k=0
	    else: k=1
	if intCh==23: k=0
	GPIO.output(24, k)
	print "Channel is off",intCh,"LED:",k,"time:",time.time()
	print "read directly:",GPIO.input(24)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   	# set GPIO25 as input (button)
GPIO.setup(24, GPIO.OUT)   				# set GPIO24 as an output (LED)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# not connected

StartTime=time.time()
j=0
raw_input("Press Enter when ready\n>")  
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=300)
try:
    print "Waiting for rising edge on port 22"  
    GPIO.wait_for_edge(22, GPIO.RISING)  
    print "Rising edge detected on port 22. Here endeth the third lesson."
except KeyboardInterrupt:  
    GPIO.cleanup()
finally:
    GPIO.cleanup()
GPIO.cleanup()          
