#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=тест serial port

import serial
import time
import mymod
shared = mymod.shared()
import crc16

DEBUG = 1

def getByte(arr):
    num = 0
    for i in xrange(8):
	num += arr[i]*2**i
    return num

d_out_prev=(0)*8
sharedInitial = {"rtu_sleep_ms": 5.0,
		"d_out": d_out_prev,
		"good_rx": 0,
		"bad_rx": 0
		}
for key, value in sharedInitial.iteritems():
    try:
	shared[key]
    except:
	shared[key] = value

errCnt = shared["bad_rx"]
okCnt = shared["good_rx"]
sleep_delay = shared["rtu_sleep_ms"]
#set up cycle time issues	
cur_cycle_time = mymod.cycle_time()
cur_cycle_time.length = 50
#set port
ser = serial.Serial(port='/dev/ttyUSB0', 
baudrate=115200, 
bytesize=8, 
parity='O', 
stopbits=1, 
timeout=0.03, 
xonxoff=0, 
rtscts=0)

#print ser
#print ser.name
#ser.write(chr(x05)+chr(x02)+chr(x00)+chr(x00)+chr(x00)+chr(x08)+chr(x78)+chr(x48))      # write a string
getDIstatusCRC02 = [0x05,0x02,0x00,0x00,0x00,0x08,0x78,0x48]
writeDO = [0x05,0x0F,0x00,0x00,0x00,0x08,0x01]
getDOstatusCRC = [0x05,0x01,0x00,0x00,0x00,0x08,0x3C,0x48]
getDIstatusCRC = [0x05,0x01,0x00,0x20,0x00,0x08,0x3D,0x82]

j=1
getBin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:]
getTuple=lambda x: tuple([int(bin(x>>i)[-1]) for i in xrange(8)])
StartT=time.time()
while True:
    d_out=shared["d_out"]
    try:
	#send READ request
	ser.write(getDIstatusCRC)
	#get READ response: 3 byte is data in str
	response = ord(ser.read(size=10)[3])
	#format to tuple
	readData = getTuple(response)
	#look up the d_out
	if d_out_prev<>d_out:
	    ser.write(crc16.addCRC(writeDO+[getByte(d_out)]))
	    ser.read(size=10)#we have to read response
	    d_out_prev=d_out
    except (KeyboardInterrupt, SystemExit):
	#do not forget to use
	ser.close()
        break;
    except:
	errCnt+=1
    else:	
	okCnt+=1
    finally:
	#write data to memcache
	shared.set_multi({'d_in': readData, 'good_rx': okCnt, 'bad_rx': errCnt});
	
	#mymod time module
	cur_cycle_time.call()
    	if cur_cycle_time.ready:
	    shared["rtu_cycle_time"] = cur_cycle_time.cycle_time_ms[0]
	    shared["rtu_cycle_time_arr"] = cur_cycle_time.cycle_time_ms
	    sleep_delay = shared["rtu_sleep_ms"]
	    if DEBUG: print "d_in:{0} d_out:{1} good:{2} bad:{3} time:{4}ms".format(readData,d_out,okCnt,errCnt,cur_cycle_time.cycle_time_ms[0])
    #end main while loop
    time.sleep(sleep_delay/1000.0)


"""
# to get a proper tuple
# d_in : (1, 1, 1, 1, 1, 1, 1, 0) 
#tuple([int(x)for x in tuple(str(bin(31))[2:].zfill(8))])[::-1]
#tuple([int(bin(127>>i)[-1]) for i in xrange(8)])
"""
ser.close() 
#print s
