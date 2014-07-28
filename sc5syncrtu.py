#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=тест скорости RTU sync

from pymodbus.client.sync import ModbusSerialClient as ModbusRtuClient

from time import sleep

#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

sleep_time=0.2;#in sec

try:
	print'Открываем соединение...'
	client = ModbusRtuClient(method="rtu",port="/dev/ttyUSB0",stopbits=1,bytesize=8,parity="O",baudrate=115200,timeout=0.01);
	print client
	client.connect(); print'Установили соединение'
	start_address = 0x00; regs=8;i=0;
	#for i in range(200):
	while (True):
		#print "."*20,"we are going to read now","."*20
		rq = client.read_discrete_inputs(start_address,regs,unit=0x05)
		print i,"M-7050D ",rq.bits
		if not(rq.bits[0]) : client.write_coil(0, True, unit=0x05) #print "send on";
		if rq.bits[0]: client.write_coil(0, False, unit=0x05) #print "sen off";
		#rq = client.read_discrete_inputs(start_address,16,unit=0x04)
		#print i,"modsim32",rq.bits
		i+=1
		#sleep(sleep_time)
		
except:
	print'ошибка!'

else:
	print'Всё хорошо.'

finally:
	client.close()
	print 'Закрыли соединение'

