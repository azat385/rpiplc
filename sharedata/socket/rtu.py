#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=тест modbus-tk

import time
import traceback
import serial
import modbus_tk.defines as tkCst
import modbus_tk.modbus_rtu as tkRtu

#import memcache
import pylibmc

slavesArr = [5]
iterSp = 10**4 #кол-во повторов
regsSp = 8 #кол-вщ регистров
portName = '/dev/ttyUSB0'
baudrate = 115200

timeoutSp=0.01 + regsSp*0
#print "timeout: %s [s]" % timeoutSp

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

StartT = startTs = time.time()
cycle_s_arr=[0,0]*5
cycle_s_arr_i=0
#for i in range(iterSp):
#shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared = pylibmc.Client(["127.0.0.1"], binary=True)
shared.behaviors = {"tcp_nodelay": True, "ketama": True}
d_out_prev=(0,0)*4
try: 
	shared["rtu_sleep_ms"]
except: 
	shared["rtu_sleep_ms"]=10.0
while (1):
  try:
   for slaveId in slavesArr:
    try:
	rr=tkmc.execute(slaveId, tkCst.READ_DISCRETE_INPUTS, 0,regsSp)
	#rq=input_assign(rr)#inverted array
	#wr=logic(rq)
	d_out=shared["d_out"]

	if d_out_prev<>d_out:
	     tkmc.execute(slaveId, tkCst.WRITE_MULTIPLE_COILS, 0, output_value=d_out)
	     d_out_prev=d_out

	#cycle_time = round((time.time()-startTs)/(i-errCnt+1)*1000,2) #cycle time in ms!!!!!!!!!
	#print "good rx:",i-errCnt,"bad rx:",errCnt, "d_in:",arr_to_str(rr),"[ms]:",cycle_time," \r",
	
	#"d_in1:",arr_to_str(rq),"d_out:",arr_to_str(wr),"cycle/s:",round(cycle_freq,2),
    	#shared.set('d_in', arr_to_str(rr));#shared.set('d_in1',arr_to_str(rq));shared.set('d_out',arr_to_str(wr));
	shared.set_multi({'d_in': rr, 'good_rx': i-errCnt, 'bad_rx': errCnt});

        cycle_s_arr[cycle_s_arr_i]=(time.time()-StartT)
        cycle_s_arr_i+=1
        if cycle_s_arr_i >= len(cycle_s_arr):
            cycle_s_arr_i=0
            shared["rtu_cycle_time"] = round((sum(cycle_s_arr)/float(len(cycle_s_arr)))*1000,2)
	StartT = time.time()
	sleep_s=shared["rtu_sleep_ms"]/1000.0
	time.sleep(sleep_s)
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
