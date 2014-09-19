#!/usr/bin/python
# -*- coding: utf-8 -*-
#mycomment=тест server
DEFAULT_SQL_STR = "SELECT * FROM dio WHERE name = 'do5' ORDER BY id DESC limit 10"

def get_data(sqlstr = DEFAULT_SQL_STR):
	import sqlite3
	import datetime
        db = sqlite3.connect('/home/pi/db/rpiplc00.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = db.cursor()
	sql_result = ' '
	try:
	    for row in c.execute(sqlstr):
		sql_result = sql_result + str(row) + "</br>\n"
	except:
	  	sql_result = "Error!!!"
	db.close()
	return "</br>\n" + sql_result;
def web_add_form(sqlstr = DEFAULT_SQL_STR):
	mystr1 = """
		<form method="POST" action="/get_data_form">
		</br>
		<label>Type your sql request here: </label>
		</br>
		<TEXTAREA name="your_long_sql" rows=10 cols=120>
"""
#Enter sql request here
	mystr2 = """
</TEXTAREA>
                </br>
		<input type="text" name="your_sql" title=" type SQL words here" placeholder="see the example above"
		maxlength="1200" size="150" value="here id defailt value"/>
		<input type="submit" value="Press here to get data"/>
		</form>
		</br>
                <form method="POST" action="/reset_data_form">
                <label>Click here to reset the data to initials: </label>
                <input type="submit" value="Press here to reset"/>
                </form>

		"""
	return mystr1 + sqlstr + mystr2

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
class mysql_request(object):
	def __init__(self):
		self.data = DEFAULT_SQL_STR
	
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import ssl

PORT_NUMBER = 8377
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html; charset=UTF-8')
		self.end_headers()
		# Send the html message
		self.wfile.write(get_data(s1.data))
		self.wfile.write("</br>\n"+ DEFAULT_SQL_STR + "</br>\n")
		self.wfile.write(web_add_form(s1.data))
		return
#Handler for the POST requests
	def do_POST(self):
		self.send_response(200)
                self.send_header('Content-type','text/html; charset=UTF-8')
                self.end_headers()

		if self.path=="/get_data_form":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			try:
				print len(str(form["your_sql"].value)) < 10
				#print "textarea:",str(form["your_long_sql"].value)	# msg to debug
				str_to_add = str(form["your_long_sql"].value)
				str_to_add = str_to_add.decode('utf-8')
				#print "Your SQL is: %s" % str_to_add 			# msg to debug
				#self.wfile.write(get_data(str_to_add))
				s1.data = str_to_add
				self.do_GET()
			except:
				print "nothing to add!!!"
				self.wfile.write("Ooops nothing is added!")
			#self.wfile.write(web_go_back_button())
			#self.wfile.write(web_timeout())
		if self.path=="/reset_data_form":
			m1.set_init()
			msg = "data reinitialized!!!"
			print msg
                        self.wfile.write(msg)
                        self.wfile.write(web_go_back_button())
                        self.wfile.write(web_timeout())
			return

def main():
    global s1
    s1 = mysql_request()
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


if __name__ == '__main__':
    main()
