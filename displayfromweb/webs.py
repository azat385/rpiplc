#!/usr/bin/python
# -*- coding: utf-8 -*-
#mycomment=тест server

def get_str():
	import pylibmc
	shared = pylibmc.Client(["127.0.0.1"], binary=True)
	shared.behaviors = {"tcp_nodelay": True, "ketama": True}
	try:
		shared["disp_arr"]
	except:
		shared["disp_arr"]=["Liliia","Janim"]
	disp_arr=[i.upper().encode("utf-8") for i in shared["disp_arr"]]
	disp_str = " </br>".join(disp_arr)
	return disp_str;

class myclass():
	"""
	here is some notes how to use the class
	"""
	str = "thats a string"
	int = 385

	def __init__(self):
		"""initialize most data """
	        import pylibmc
        	self.shared = pylibmc.Client(["127.0.0.1"], binary=True)
        	self.shared.behaviors = {"tcp_nodelay": True, "ketama": True}
		self.name = "disp_arr"
		self.default_arr = ["Liliia","Janim"]
		#self.data = ["without","init"]
		self.data=["some","words"]
		self.error = "no error"

	def get_data(self):
	        try:
        	        self.shared[self.name]
        	except:
                	self.shared[self.name]=self.default_arr
		self.data = self.shared[self.name]
		self.data = [i.encode('utf-8') for i in self.data]
		return self.data
	
	def add_data_old(self,data_to_add):
		if isinstance(data_to_add, str):
			self.set_data(self.shared[self.name]+[data_to_add])
                elif isinstance(data_to_add, list):
                        self.set_data(self.shared[self.name]+data_to_add)
		elif isinstance(data_to_add, tuple):
			self.set_data(self.shared[self.name]+list(data_to_add))
		else:
			self.error = "some bad data added"
			print self.error
		return self.get_data()
	def set_data(self,data_to_enter):
		self.shared[self.name] = data_to_enter
		return self.get_data()
	def set_init(self):
		self.set_data(self.default_arr)
		return self.get_data()
	def add_data(self,*multiple):
		self.set_data(self.shared[self.name]+list(multiple))
		return self.get_data()
	pass
#for python debuging
"""
from webs import myclass
m1=myclass()
m1.data
m1.get_data()
m1.add_data("super new")
m1.set_data("12345")
"""
def web_add_form():
	mystr = """
		<form method="POST" action="/add_data_form">
		<label>Add here some words: </label>
		<input type="text" name="your_str" title=" type sweet words here" placeholder="the max lenght is 10 symbols"
		maxlength="12" size="15"/>
		<input type="submit" value="Press here to add"/>
		</form>
		</br>
                <form method="POST" action="/reset_data_form">
                <label>Click here to reset the data to initials: </label>
                <input type="submit" value="Press here to reset"/>
                </form>

		"""
	return mystr

def web_go_back_button():
	mystr="""
	<script>
	function goBack() {
    		window.history.back()
	}
	</script>

	<body>
	<button onclick="javascript:window.location.reload(history.go(-1));">Go Back</button>
	</body>
	"""
	return mystr

def web_timeout():
	mystr="""
	<script type="text/javascript">
	window.setTimeout('javascript:window.location.reload(history.back());', 5000); 
	</script>
	"""
	return mystr

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import ssl

PORT_NUMBER = 80
global m1
m1 =  myclass()
mystr = ["МИН","СИНЕ","ЯРАТАМ","ЛИЛИЯМ","ҖАНЫМ","МАТУРЫМ","КАДЕРЛЕМ","АЛТЫНЫМ"]
m1.default_arr = [i.decode('utf-8') for i in mystr] 
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html; charset=UTF-8')
		self.end_headers()
		# Send the html message
		#global m1 
		#m1 = myclass()
		self.wfile.write("</br>".join(m1.get_data()))
		self.wfile.write(web_add_form())
		return
#Handler for the POST requests
	def do_POST(self):
		self.send_response(200)
                self.send_header('Content-type','text/html; charset=UTF-8')
                self.end_headers()
		if self.path=="/add_data_form":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			try:
				print len(str(form["your_str"].value)) < 1
				str_to_add = str(form["your_str"].value)[:28]
				str_to_add = str_to_add.decode('utf-8').upper()
				print "Your added str is: %s" % str_to_add
				m1.add_data(str_to_add)
				self.wfile.write("Thanks! Your have succesufully added: <b>%s</b>" % str_to_add.encode('utf-8'))
			
			except:
				print "nothing to add!!!"
				self.wfile.write("Ooops nothing is added!")
			self.wfile.write(web_go_back_button())
			self.wfile.write(web_timeout())
			#time.sleep(5)
			#self.do_GET()
		if self.path=="/reset_data_form":
			m1.set_init()
			msg = "data reinitialized!!!"
			print msg
                        self.wfile.write(msg)
                        self.wfile.write(web_go_back_button())
                        self.wfile.write(web_timeout())
			return

def main():
    try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	
	print 'Started httpserver on port ' , PORT_NUMBER
	m1.set_init()
	#Wait forever for incoming htto requests
	server.serve_forever()

    except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()


if __name__ == '__main__':
    main()
