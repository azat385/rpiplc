#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=новые комментарии да да

"""module docstring"""

# imports
import sys
import gspread
# constants
# exception classes
# interface functions
# classes
# internal functions & classes
def send_email(gmail_user, gmail_pwd, SUBJECT, TEXT):
            import smtplib

            #gmail_user = "user@gmail.com"
            #gmail_pwd = "secret"
            FROM = gmail_user
            TO = ['zadachki@googlegroups.com'] #must be a list
            #SUBJECT = "Testing sending using gmail"
            #TEXT = "Testing sending mail using gmail servers"

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            #try:
            #server = smtplib.SMTP(SERVER) 
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print 'successfully sent the mail'
            #except:
            #    print "failed to send mail"

def main():
	# user details
	gmail_user = 'interesnye.zadachki@gmail.com'
	gmail_pwd = 'zaq1xsw2_zadachki'

	# Login with your Google account
	gc = gspread.login(gmail_user, gmail_pwd)

	# Open a worksheet from spreadsheet with one shot
	wks = gc.open("interesnye_zadachki").sheet1

	# With coords cell(row,col)
	#val = wks.cell(1, 2).value
	
	# get data to send
	today_date = "12.09.2014"
	col1 = wks.col_values(1)
	data = wks.row_values(col1.index(today_date)+1)

	for i in data: 	print i
	
	send_email(gmail_user, gmail_pwd, 
		   SUBJECT=data[1].encode("utf-8"), 
                   TEXT=data[3].encode("utf-8"))

if __name__ == '__main__':
    status = main()
    sys.exit(status)
