#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=новые комментарии да да

"""module docstring"""

# imports
from threading import Timer
import time
import sys
# constants
NOT_RUNNING = -1
RUNNING = 0
FINISH = 1
DELAY_VALUE_DEFAULT = 5
# exception classes
# interface functions
get_edge = lambda x,y: 1 if x and (not y) else 0 
get_on = lambda x,y: get_edge(x,y)
get_off = lambda x,y: get_edge(y,x)
# classes
class TON(object):
	#name_str = "TON"
	def __init__(self,input, delay_value = DELAY_VALUE_DEFAULT):
		self.status = NOT_RUNNING
		self.input = input
                self.input_prev = 0 #input #!!!important comment
		self.delay_value = delay_value
		self.count = 0
		self.do = 0
		self.di = input
		self.name_str = self.__class__.__name__
	def start(self):
		self.started_time = time.time()
		self.status = RUNNING
		print self.name_str,"started",
	def stop(self):
		self.status = NOT_RUNNING
		self.count = 0	
		print self.name_str," stopped",
	def check(self):
		if self.status == RUNNING:
			if time.time()-self.started_time > self.delay_value:
				self.status = FINISH
				self.count = self.delay_value			
				print self.name_str,"finished",
			else:
				self.count = time.time()-self.started_time
		return self.status
	def out(self,input,delay_value = DELAY_VALUE_DEFAULT):
		self.delay_value = delay_value
		self.input=input
		#get_edge = lambda x,y: 1 if x and (not y) else 0
		on = get_edge(self.input, self.input_prev)
		off = get_edge(self.input_prev, self.input)
		if on:
			self.start()
		if off:
			self.stop()
		self.check()
		self.input_prev = self.input
		#here is changing part
		self.di = input
                self.do = 1 if self.status==FINISH else 0
                self.do = self.do and self.di
		return self.di, self.do, self.count, self.name_str
	def out_str(self):
		return bcolors.OKGREEN + "DI:" + bcolors.ENDC + str(self.di)+ \
			bcolors.OKGREEN + " DO:" + bcolors.ENDC + str(self.do)
	pass
class TOFF(TON):
	def __init__(self, input, delay_value = DELAY_VALUE_DEFAULT):
		TON.__init__(self, not input)	#call parent method with inverted input
		self.di = input 		#override some parametrs
	def out(self,input,delay_value = DELAY_VALUE_DEFAULT):
		TON.out(self, not input)
		self.di = input
		self.do = 1 if self.status==RUNNING else 0
		self.do = self.do or self.di
		return self.di, self.do, self.count, self.name_str
	pass
class TONOFF(TON):
	def __init__(self,input,delay_value_on = DELAY_VALUE_DEFAULT,delay_value_off = DELAY_VALUE_DEFAULT):
		self._t1 = TON(input,delay_value_on)
		self._t1.out(input,delay_value_on)
		self._t2 = TOFF(self._t1.do,delay_value_off)
		TON.__init__(self,input)	#just for init
		return None
	def out(self,input,delay_value_on = DELAY_VALUE_DEFAULT, delay_value_off = DELAY_VALUE_DEFAULT):
		self._t1.out(input,delay_value_on)
		self._t2.out(self._t1.do,delay_value_off)
		#self.do = self._t2.do
		if self._t1.status == RUNNING and self._t2.status != RUNNING:
			self.do = self._t1.do
		else:
			self.do = self._t2.do
		self.di = input
		return self.di, self.do, self._t1.count, self._t2.count, self.name_str
	pass
class TONF(object):
        def __init__(self,input,delay_value_on = DELAY_VALUE_DEFAULT,delay_value_off = DELAY_VALUE_DEFAULT):
		return None
	pass
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
	self.BOLD = ''
"""
from mytimer import TON
t1=TON()
t2=TOFF()
"""

# internal functions & classes

def main():
	#-----------for debug
	import pylibmc
	shared = pylibmc.Client(["127.0.0.1"], binary=True)
    	shared.behaviors = {"tcp_nodelay": True, "ketama": True}
	shared["input_bool"] = 1
	shared["delay_var"] = 5
	#-----------
	print bcolors.WARNING + "Warning: No active frommets remain. Continue?"+ bcolors.ENDC
	print "main is started"
	print "press ^C to escape"
	l1 = shared["input_bool"]
	v1 = shared["delay_var"]
	t1 = TON(l1)
	t2 = TOFF(l1)
	t3 = TOFF(t1.do)
	t4 = TONOFF(l1)
	#t3 = childTOFF(l1)
	while True:
	    #try:
		l1 = shared["input_bool"]
		v1 = shared["delay_var"]
		#print "t1: in",int(t1.input),"out",t1.out(l1,v1),"t2: in",int(t2.input),"out",t2.out(t1.out(l1,v1)[0],v1),\
		#	"the sum:", t1.out(l1,v1)[0] or t2.out(t1.out(l1,v1)[0],v1)[0]
		#print "t3:in", int(t3.input), "out",t3.out(l1,v1),"DI",t3.di, "DO",t3.do
		for var,i in zip(("t1","t2","t3","t4"),(t1, t2, t3, t4)):
			#i.out(l1,v1)
			t1.out(l1,v1)
			t2.out(l1,v1)
			t3.out(t1.do,v1)
			t4.out(l1,4,8)
			print var,i.out_str(),
		print
		time.sleep(1)
	    #except:
		#print " main is stopping"
		#break
if __name__ == '__main__':
    #status = main()
    #sys.exit(status)
    main()
