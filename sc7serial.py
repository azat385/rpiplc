#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=тест serial port

import serial
import time

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
bytearr=[0x05,0x02,0x00,0x00,0x00,0x08,0x78,0x48]
j=1
getBin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:]
StartT=time.time()
while True:
	ser.write(bytearr)
	response = ser.read(size=6)
	freq=j/(time.time()-StartT)
	print j,"request:  "," ".join(str(hex(i)) for i in bytearr),\
	" -->  response: "," ".join(hex(ord(i)) for i in response),\
	"data: ",getBin(ord(response[2]),8),getBin(ord(response[3]),8),\
	"req/s:",round(freq,2),\
	" [ms] ",round(1000/freq,2),\
	"\r",
	j+=1
	break
"""
numOfLines = 0
while True:
        response = ser.read()
        response = ser.read(size=6)
	print response
	#print("read data: " + str(hex(ord(response))))
        numOfLines = numOfLines + 1
        if (numOfLines >= 6):
            break
"""
ser.close() 
#print s
