#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9090))
sock.send('client trys to connect')

while True:
  # try:
	data = sock.recv(1024)
	if not data: break
	print data
  # finally:
sock.close()
