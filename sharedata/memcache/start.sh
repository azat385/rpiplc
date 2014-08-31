#!/bin/bash
#start write to memcache data about cpu usage and etc
python cpu.py &
#start read/write data M-7050D via USB0X/tty serail port adapter
python rtu.py &
#start logic cycles
python logic.py &
#start webserver to see information from the memcache server localhost:PORT_NUMBER = 8385
python /home/pi/myscripts/rpiplc/webserver.py &
#start server to display data on nokia 3110 screen
python
#start archiving server
python
#start watchdog

