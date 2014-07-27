#!/usr/bin/env python
# -*- coding: utf-8 -*-
print u"Content-type: text/html; charset=utf-8\n\n"

#mycomment=новые комментарии да да

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from time import sleep

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

host='25.7.11.1'
port=502
sleep_time=0.2;#in sec

try:
	print'Открываем соединение...'
	client = ModbusClient(host, port); print'Подключились к хосту',host
	client.connect(); print'Установили соединение'
	start_address = 0x00; regs=2;
	for i in range(2):
		print "."*20,"we are going to read now"
		rq = client.read_holding_registers(start_address,regs,unit=1)
		print
		
		print "MY OUTPUT:",i, rq.registers
		rq.registers[1]=rq.registers[1]+1;
		sleep(sleep_time)
		print "."*20,"we are going to write now"
		client.write_register(1,rq.registers[1],unit=1)
		print
		sleep(sleep_time)
		
except:
    print'ошибка!'

else:
    print'Всё хорошо.'

finally:
    client.close()
    print 'Закрыли соединение'

