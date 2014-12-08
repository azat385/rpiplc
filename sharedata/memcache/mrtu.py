#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mymod
shared = mymod.shared()
# shared["good_rx"] read expmple
import resource
import time
import serial
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

slaveId = 5
portName = '/dev/ttyUSB0'
baudrate = 115200
regsSp = 8 #кол-вщ регистров
timeoutSp=0.01

d_out_prev=(0)*8
sharedInitial = {"rtu_sleep_ms": 50.0,
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
master = modbus_rtu.RtuMaster(serial.Serial(port=portName, baudrate=baudrate, 
					    bytesize=8, parity='O', stopbits=1, xonxoff=0))
master.set_timeout(timeoutSp)
while (1):
    d_out=shared["d_out"]
    try:
	#read from Slave
	readData = master.execute(slaveId, cst.READ_DISCRETE_INPUTS, 0, regsSp)
	#write to Slave
        if d_out_prev<>d_out:
             master.execute(slaveId, cst.WRITE_MULTIPLE_COILS, 0, output_value=d_out)
             d_out_prev=d_out
    except (KeyboardInterrupt, SystemExit):
	#do not forget to use
	master.close()
        break;
    except:
        errCnt+=1
    else:	
        okCnt+=1
    finally:
    	#write data to memcache
        try:
	    shared.set_multi({'d_in': readData, 'good_rx': okCnt, 'bad_rx': errCnt});
	except NameError:
	    shared.set_multi({'good_rx': okCnt, 'bad_rx': errCnt});
    	#mymod time module
	cur_cycle_time.call()
    	if cur_cycle_time.ready:
	    shared["rtu_cycle_time"] = cur_cycle_time.cycle_time_ms[0]
	    shared["rtu_cycle_time_arr"] = cur_cycle_time.cycle_time_ms
	    sleep_delay = shared["rtu_sleep_ms"]
    #end main while loop
    time.sleep(sleep_delay/1000.0)
    if (okCnt+errCnt)%1000 == 0:
	master.close()
	print "Master closed! The master size is", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
	master = modbus_rtu.RtuMaster(serial.Serial(port=portName, baudrate=baudrate,
                                            bytesize=8, parity='O', stopbits=1, xonxoff=0))
	master.set_timeout(timeoutSp)
