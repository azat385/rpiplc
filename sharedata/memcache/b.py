#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcd8544.lcd as lcd
import time, os, sys, psutil

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

ON, OFF = [1, 0]

def cyrstr(j):
     i=0
     q=[]
     while i<len(j):
         #print i,j[i],ord(j[i]),hex(ord(j[i]))
         if ord(j[i])>127:
             q.append(j[i:i+2])
             i=i+2
         else:
             q.append(j[i])
             i+=1
     return q;

try:
  lcd.init()
  lcd.cls()
  lcd.set_contrast(155)
  lcd.backlight(ON)
  LastTime=0
  invert_arr=[0,0,0,0,0,0]
  i_int=-1
  while 1:
     if time.time()-LastTime > 3 :
    	 mycpu=" CPU: "+(str(psutil.cpu_percent(0))).rjust(5,' ')+"%  "
	 LastTime=time.time()
	 i_int+=1
	 if i_int>5: i_int=0
	 for i in range(0,len(invert_arr)):
		if i==i_int: invert_arr[i]=1
		else: invert_arr[i]=0
     lcd.gotorc(0,0)
     lcd.text(" 0.RPI PLC    ",invert=invert_arr[0])
     lcd.gotorc(1,0)
     lcd.text(mycpu, invert=invert_arr[1])
     #print mycpu,"\r",
     lcd.gotorc(2,0)
     lcd.text(" "+time.strftime("%d %b %Y", time.localtime())+"   ", invert=invert_arr[2])
     lcd.gotorc(3,0)
     lcd.text(" Time:        ",invert=invert_arr[3])
     lcd.gotorc(4,0)
     lcd.text(" "+time.strftime("%H:%M:%S", time.localtime())+"     ",invert=invert_arr[4])
     lcd.gotorc(5,0)
     lcd.text(cyrstr(" Меню  Alarms "),invert=invert_arr[5])
          
     time.sleep(0.25)
except KeyboardInterrupt:
  pass
finally:
  lcd.cls()
  lcd.backlight(OFF)

