#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=новые комментарии да да

"""module docstring"""

# imports
import time
# constants
DEFAULT_SLEEP_DELAY = 50.0
MINIMUM_SLEEP_DELAY = 5.0
# exception classes
# interface functions
def get_arg(_default_sleep_delay = DEFAULT_SLEEP_DELAY, argv = None, _debug = False):
    """
    TODO!!!!!!!!
    enter here text about usage
    """
    import sys
    _proper_set = 0
    if not argv:
        argv = sys.argv
    if len(argv) >= 2 :
        try:
            float(argv[1])
            _sleep_delay=float(argv[1]) 
	    if float(argv[1])>=MINIMUM_SLEEP_DELAY:
	    	_sleep_delay = float(argv[1])
	    	_proper_set = 1
		if _debug: print "The delay is loaded from cmd line!!!"
	    else:
		if _debug: print "The default is loaded!!! Enter delay more than",MINIMUM_SLEEP_DELAY
		_sleep_delay = _default_sleep_delay
        except:
           if _debug: print "The default is loaded!!! Enter proper number!!!"
           _sleep_delay = _default_sleep_delay
    else:
        _sleep_delay = _default_sleep_delay
    if _debug: print "Sleep time delay is",_sleep_delay,"[ms]"
    return _sleep_delay,_proper_set

def shared(host = "127.0.0.1"):
	import pylibmc
	s = pylibmc.Client([host], binary=True)
	s.behaviors = {"tcp_nodelay": True, "ketama": True}
	return s
# classes
class cycle_time():
	def __init__(self):
		self.length = 10
		self.cycle_time_ms = []
		self.cycle_s_arr = [0]
		self.tstamp = [0]
		self.i = 0
		self.ready = 0
		self.cycle_average = 0
		self.cycle_max = 0
		self.cycle_min = 0
	def call(self):
		self.tstamp.append(time.time())
		if len(self.tstamp)>self.length: self.tstamp.pop(0)
		if self.i==self.length:
			self.i = 0
			self.cycle_s_arr = [j-i for i, j in zip(self.tstamp[:-1], self.tstamp[1:])]
	                self.cycle_average = round((sum(self.cycle_s_arr)/float(len(self.cycle_s_arr)))*1000,2)
			self.ready = 1
			self.cycle_max = round(max(self.cycle_s_arr)*1000,2)
			self.cycle_min = round(min(self.cycle_s_arr)*1000,2)
			self.cycle_time_ms = [self.cycle_average, self.cycle_max, self.cycle_min]
		else:
			self.ready = 0	
            	self.i+=1
		#return cycle_time_ms
	#return cycle_time_ms
# internal functions & classes

def main():
    
	return None
if __name__ == '__main__':
    #status = main()
    #sys.exit(status)
    main()
