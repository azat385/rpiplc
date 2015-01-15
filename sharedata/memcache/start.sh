#!/bin/bash
#starting delay to wait all the staff is started
sleep 30
myDelay=2
myPath="/home/pi/myscripts/rpiplc/sharedata/memcache/"
cd $myPath
#start write to memcache data about cpu usage and etc
echo "starting cpu.py"
python cpu.py &
#start read/write data M-7050D via USB0X/tty serail port adapter
sleep $myDelay
echo "starting rtuSerial.py"
python rtuSerial.py &
#start logic cycles
sleep $myDelay
echo "starting logic.py"
python logic.py &
#start webserver to see information from the memcache server localhost:PORT_NUMBER = 8385
sleep $myDelay
echo "start webserver.py"
python /home/pi/myscripts/rpiplc/webserver.py &
# start server to display data on nokia 3110 screen
sleep $myDelay
echo "starting disp.py"
python disp.py &
#python
#start archiving server
#python archive.py &
# start web sql access on port 8377
#python websqlread.py &
#start watchdog
echo "All process are running"
#
#to do an array start
#declare -a myArr=("cpu.py" "rtu.py" "logic.py")
#for item in ${myArr[*]}
#do
#    python  $item
#    echo " \n"{1..10}
#done
