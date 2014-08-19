#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=тест modbus-tk

import time
import traceback
import serial
import modbus_tk.defines as tkCst
import modbus_tk.modbus_rtu as tkRtu

import memcache
import pylibmc

slavesArr = [5]
iterSp = 10**4 #кол-во повторов
regsSp = 8 #кол-вщ регистров
portName = '/dev/ttyUSB0'
baudrate = 115200

timeoutSp=0.01 + regsSp*0
print "timeout: %s [s]" % timeoutSp

tb = None
errCnt = 0


import os 
# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

def logic(input):
    output=[0,0,0]
    output[0]=input[0];
    output[1]=input[1];
    output[2]=not(input[2]);
    #for i in output: output[i]=int(output[i]);
    return output;

def arr_to_str(arr_in):
    mystr=""
    for i in arr_in:
	mystr=mystr+str(int(i));
    return mystr;

def input_assign(raw_in):
    myinput=[]
    for i in raw_in:
	myinput.append(not(i));
    return myinput;


tkmc = tkRtu.RtuMaster(serial.Serial(port=portName, baudrate=baudrate,parity='O'))
tkmc.set_timeout(timeoutSp)

errCnt = 0
i = 0
cpu_usage =330.0
wr_prev=[]

startTs = time.time()
#for i in range(iterSp):
#shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared = pylibmc.Client(["127.0.0.1"], binary=True)
shared.behaviors = {"tcp_nodelay": True, "ketama": True}

while (1):
  try:
   for slaveId in slavesArr:
    try:
	for _ in range(1):
		rr=tkmc.execute(slaveId, tkCst.READ_DISCRETE_INPUTS, 0,regsSp)
	
	rq=input_assign(rr)
	wr=logic(rq)
	if wr<>wr_prev:
	     tkmc.execute(slaveId, tkCst.WRITE_MULTIPLE_COILS, 0, output_value=wr)
	     wr_prev=wr
	
	cycle_freq = (i-errCnt+1)/(time.time()-startTs)
	print "good rx:",i-errCnt,"bad rx:",errCnt,\
		"CPU:",cpu_usage,\
		"d_in:",arr_to_str(rr),\
		"d_in1:",arr_to_str(rq),\
		"d_out:",arr_to_str(wr),\
		"cycle/s:",round(cycle_freq,2),\
		"[ms]:",round(1000/cycle_freq,2),\
		" \r",
    	#shared.set('d_in', arr_to_str(rr));#shared.set('d_in1',arr_to_str(rq));shared.set('d_out',arr_to_str(wr));
	#shared.set_multi({'d_in': arr_to_str(rr), 'd_in1': arr_to_str(rq), 'd_out':arr_to_str(wr),
	#		  'good_rx': i-errCnt, 'bad_rx': errCnt, 'cycle_time':round(1000/cycle_freq,2) });
    except KeyboardInterrupt:
	raise
    except:
        errCnt += 1
        tb = traceback.format_exc()
	print "error=",errCnt,"current request=",i,tb
  except (KeyboardInterrupt, SystemExit):
    break;
  i+=1
stopTs = time.time()
timeDiff = stopTs  - startTs
iterSp=i-errCnt+1
print "modbus-tk:\ttime to read %s x %s (x %s regs): %.3f [s] / %.3f [s/req] / %.3f [req/s]" % (len(slavesArr),iterSp, regsSp, timeDiff, timeDiff/iterSp, iterSp/timeDiff)
if errCnt >0:
    print "   !modbus-tk:\terrCnt: %s; last tb: %s" % (errCnt, tb)
tkmc.close()
