#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

def get_data(host = '127.0.0.1',port = '11211'):
	from memcached_stats import MemcachedStats
	m = MemcachedStats(host, port)
	import pylibmc
	import time
	shared = pylibmc.Client([host], binary=True)
	shared.behaviors = {"tcp_nodelay": True, "ketama": True}
        str_data = '<head>\n<meta http-equiv="refresh" content="20">\n</head>\n'
	str_data = str_data + '<b>Data of internal memchache server:</b></br>\n'
	str_data = str_data + str(time.strftime("%x %X %Z", time.localtime())) + '</br>\n'
	dict_data = shared.get_multi( m.keys())
	for k,v in sorted(dict_data.items()):
		str_data = str_data + str(k) + " : " + str(v) + " </br>\n"
	str_data = str_data + "-"*30 + " </br>\n"
	return str_data;

PORT_NUMBER = 8377

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(get_data())
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
