#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=новые комментарии да да

"""module docstring"""

# imports
import sys
import mymod
import time
# constants
# exception classes
# interface functions
# classes
# internal functions & classes

def main():
    	sleep_delay,sleep_delay_forced = mymod.get_arg()	# get value of sleep delay,  get a status
	shared = mymod.shared()					# connect to memcache server
	try:
		shared["archive_sleep_ms"]
	except:
		shared["archive_sleep_ms"] = sleep_delay	# if a such name doesnt exist create and load defailt value
	if sleep_delay_forced: 
		shared["archive_sleep_ms"] = sleep_delay	# force load of a new  value 
	sleep_delay = shared["archive_sleep_ms"]
	count = 0
	cur_cycle_time = mymod.cycle_time()
	cur_cycle_time.length = 50
	# main to run once
	import sqlite3
	import datetime
	db = sqlite3.connect('rpiplc00.db', detect_types=sqlite3.PARSE_DECLTYPES)
	c = db.cursor()
	try:
		c.execute("""create table dio 
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT, 
			val INTEGER, 
			tstamp TIMESTAMP,
			sqltstamp DATETIME DEFAULT CURRENT_TIMESTAMP
			)""")
	except:
		print "table already exists"
	# get data
	di_prev = shared["d_in"]
	do_prev = shared["d_out"]
	while True:
		# begin main cycle is here
		di = shared["d_in"]
        	do = shared["d_out"]
		dio = {"di":(di,di_prev),"do":(do,do_prev)}
   	        mystr=[]
		for key,value in dio.items()[::-1]:
		    if value[0]!=value[1]:
			    for i,cur,prev in zip(xrange(len(value[0])),value[0],value[1]):
				if cur!=prev: 
					mystr.append((key+str(i),"on" if cur else "off"))
		if len(mystr)>0:
		    print  mystr
		    for j in mystr:
			c.execute('insert into dio (name, val, tstamp) values (?, ?, ?)', (j[0], j[1], datetime.datetime.now()))
		    db.commit()
		di_prev = di
		do_prev = do
		# end main cycle
		cur_cycle_time.call()
		if cur_cycle_time.ready:
			shared["archive_cycle_time"] = cur_cycle_time.cycle_time_ms
			sleep_delay = shared["archive_sleep_ms"]
		time.sleep(sleep_delay/1000.0)
		shared["archive_count"] = count
		count+=1
if __name__ == '__main__':
	status = main()
    	sys.exit(status)
	#main()
