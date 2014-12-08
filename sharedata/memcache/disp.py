#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
import mymod
shared = mymod.shared()

import time
import RPi.GPIO as GPIO

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont

global rotate_deg
rotate_deg = 180
global contrastValue
contrastValue = 30

def my_callback(intCh):
	global rotate_deg
	global contrastValue
	if GPIO.input(25)==GPIO.input(22):	
		GPIO.output(22, not GPIO.input(25))
		#print GPIO.input(25),GPIO.input(22)
		rotate_deg = 0 if GPIO.input(22) else 180
		if contrastValue >= 70:
		    contrastValue = 30
		else:
		   contrastValue += 5
		disp.begin(contrast=contrastValue) 
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
GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback, bouncetime=3)
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

try:
    #----------------------------------------------static write-----------------------------------------------
    while True:
	rotate_deg = 0 if GPIO.input(22) else 180
	mystr_arr1=['мега ПЛК cV:'+str(contrastValue),
			time.strftime("%H:%M:%S", time.localtime()),
			'CPU:'+ str(shared["cpu"])+'|'+str(shared["ram"])+'%',
			'OKrx:'+ str(shared["good_rx"]),
			'BADrx:'+ str(shared["bad_rx"]),
			'cycle:'+ str(shared["rtu_cycle_time"])+'ms']
	y=0
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	for i in mystr_arr1:
	    #draw.text((0,y), i.decode('utf-8').lower(), font=font_bold)
	    draw.text((0,y), i.decode('utf-8'), font=font)
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

