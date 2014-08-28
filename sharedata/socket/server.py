#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print 'connected:', addr
i=1
while True:
    data = conn.recv(1024)
    if  data: 
	print "data recived:", data
	conn.send(data.upper())
	print "data send:", data.upper()    
    else:
	conn.send(str(i))
    	i+=1
    	time.sleep(5)
conn.close()
