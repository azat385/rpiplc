#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from webs import myclass
m1=myclass()
import time
import RPi.GPIO as GPIO

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont

global rotate_deg
rotate_deg = 0

def my_callback(intCh):
	global rotate_deg
	if GPIO.input(25)==GPIO.input(22):	
		GPIO.output(22, not GPIO.input(25))
		#print GPIO.input(25),GPIO.input(22)
		rotate_deg = 180 if GPIO.input(22) else 0
	return GPIO.input(22)

#from get_str_arr_from_web import get_arr

def get_arr_func():
    arr_str=[]
	
    return arr_str;
# GPIO stuff
GPIO.setmode(GPIO.BCM)     				# set up BCM GPIO numbering
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)     	# set GPIO25 as input (button)
GPIO.setup(22, GPIO.OUT)                                # set GPIO22 as an output (LED)
GPIO.remove_event_detect(25)
GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback, bouncetime=0)
# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=30)

# Clear display.
disp.clear()
disp.display()

image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

# Draw some shapes.
#draw.ellipse((2,2,22,22), outline=0, fill=255)
#draw.rectangle((24,2,44,22), outline=0, fill=255)
#draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
#draw.line((68,22,81,2), fill=0)
#draw.line((68,2,81,22), fill=0)

# Load default font.
font_default = ImageFont.load_default()
font=ImageFont.truetype("DejaVuSans.ttf", 9)
font_bold=ImageFont.truetype("DejaVuSans-Bold.ttf", 9)
inc_vert=8
#font=ImageFont.truetype("712_serif.ttf", 10)

# Write some text.
#draw.text((8,30), 'I LOVE YOU', font=font)

# Display image.
disp.image(image)
disp.display()

print 'Press Ctrl-C to quit.'
#mystr_arr=[unicode('Мин сине','utf-8'), unicode('яратам','utf-8'), unicode('Җаным','utf-8'), unicode('Лилиям','utf-8')]
mystr_arr1=['Мин','сине', 'яратам', 'Лилиям', 'Җаным','Матурым', 'Акыллым','Бердәнберем','Кояшым','Кадерлем','Күз нурым','Алтыным','Бәгырем']
#mystr_arr1=['Min sine', 'iratam', 'Janim','Liliya', 'Tegeen!!!','Bariber!!!!!!']
#print mystr_arr1
#print u'җдәөһ'.upper()
mystr_arr2=[]

#for i in mystr_arr1:	mystr_arr2.append(i.decode('utf-8').upper())
for i,j in zip(mystr_arr1,xrange(len(mystr_arr1))):    mystr_arr2.append((str(j)+i).decode('utf-8').upper())
#print mystr_arr2
#mystr_arr1=[unicode(i, 'utf-8') for i in mystr_arr1]
#mystr_arr1=[unicode(str(i).decode('utf-8').upper(), 'utf-8') for i in mystr_arr1]
#print mystr_arr1
#mystr='I LOVE YOU'
#mystr=unicode('cyrtxt: татарча', 'utf-8')
try:
    #----------------------------------------------dynamic write-----------------------------------------------
    while True:
	y=0
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	for mystr,arr_number in zip(mystr_arr2,xrange(len(mystr_arr2))):
	    if arr_number<=5:
	        for i in range(1,len(mystr)+1):
	            draw.text((0,y), mystr[:i], font=font_bold)
	            disp.image(image.rotate(rotate_deg)) 
                    #disp.image(image.rotate(45))
 	            disp.display()
	            time.sleep(0.1)
	        y+=inc_vert
	    else:
	    	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
		y=0
		for i in mystr_arr2[arr_number-5:arr_number]:
		    draw.text((0,y),i, font=font_bold)
		    y+=inc_vert
		disp.image(image)
        	disp.display()    
	        for i in range(1,len(mystr)+1):
                    draw.text((0,y), mystr[:i], font=font_bold)
                    disp.image(image.rotate(rotate_deg))
                    disp.display()
                    time.sleep(0.1)
	#---scroll up-----
	for arr_number in xrange(len(mystr_arr2)-1,0,-1):
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
                y=inc_vert*5#
		check_up=lambda x: x-6 if (x>=6) else 0
                for i in (mystr_arr2[check_up(arr_number):arr_number])[::-1]:
                    draw.text((0,y),i, font=font_bold)
                    y-=inc_vert
                disp.image(image.rotate(rotate_deg))
                disp.display()
 		time.sleep(0.5)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	disp.image(image.rotate(rotate_deg))
	disp.display()
	time.sleep(1)
	#---draw hart----
	# Alternatively load a different format image, resize it, and convert to 1 bit color.
	image_img = Image.open('hart.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	# Display image.
	disp.image(image_img.rotate(rotate_deg))
	disp.display()
	time.sleep(1)
	# Clear display.
	disp.clear()
	disp.display()
        # whole cycle completed, sleep for keep clear display
	time.sleep(1)
	#try to get new data from web
	#mystr_arr2=mystr_arr2 if len(mystr_arr2)>=len(m1.data_get()) else get_arr()
	mystr_arr2 =[i.decode("utf-8") for i in  m1.get_data()]
	rotate_deg = 180 if GPIO.input(22) else 0
    #----------------------------------------------static write-----------------------------------------------
    while False:
	rotate_deg = 180 if GPIO.input(22) else 0
	mystr_arr1=['Мин сине', 'яратам', 'Җаным','Лилиям', time.strftime("%H:%M:%S", time.localtime()),'БАРЫБЕР!!!!!!']
	y=0
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	for i in mystr_arr1:
	    draw.text((0,y), i.decode('utf-8').upper(), font=font_bold)
	    y+=inc_vert
	disp.image(image.rotate(rotate_deg))
	disp.display()
	time.sleep(0.5)
finally:
	# Clear display.
	disp.clear()
	disp.display()
	GPIO.remove_event_detect(25)
	GPIO.cleanup()
GPIO.remove_event_detect(25)
GPIO.cleanup()

