#!/usr/bin/env python
# -*- coding: utf-8 -*-
#print u"Content-type: text/html; charset=utf-8\n\n"
#mycomment=новые комментарии да да

"""module docstring"""

# imports
import sys
import gspread
import mypwd
import vk
# constants
DEBUG = 0
# exception classes
# interface functions
# classes
# internal functions & classes
def getDateTimeInTimeZone(changeHour):
	import datetime
	time_utc = datetime.datetime.utcnow()
	time_tz = time_utc + +datetime.timedelta(hours=changeHour)
	return  time_tz.strftime("%d.%m.%Y"), time_tz.hour

def main():
	# user details
	gmail_user = mypwd.gmailZadachki.user
	gmail_pwd = mypwd.gmailZadachki.pwd

	# Login with your Google account
	gc = gspread.login(gmail_user, gmail_pwd)

	# Open a worksheet from spreadsheet with one shot
	wkbook = gc.open("interesnye_zadachki")
	wks = wkbook.get_worksheet(0) #DATA
	wkd = wkbook.get_worksheet(1) #Settings

	# With coords cell(row,col)
	#val = wks.cell(1, 2).value
	kzn_tz = int(wkd.cell(1,2).value)
	hours_to_trigger = [int(wkd.cell(2,2).value), int(wkd.cell(3,2).value)]
	if DEBUG: 
		print "Kazan tz is",kzn_tz
		print "time to trigger", hours_to_trigger
	# get data to send
	kzn_date,kzn_hour = getDateTimeInTimeZone(kzn_tz)
	# "18.09.2014" 9
	if kzn_hour in hours_to_trigger:
	    col1 = wks.col_values(1)
	    if kzn_date in col1:
		data = wks.row_values(col1.index(kzn_date)+1)
		# [date, number, subject, question, answer]
		number = data[1]
		subject = data[2]
		if hours_to_trigger.index(kzn_hour)==0:
		    text = data[3]
		    title = "Вопрос"
		if hours_to_trigger.index(kzn_hour)==1:
		    text = data[4]
		    title = "Ответ"
		title_new = "%s№%s"%(title, number)
		whole_text = "%s\n%s\n%s"%(subject, title_new.decode('utf-8'), text)
		if DEBUG:
			print whole_text
		# connect to vk profile and post msg on wall
		vkapi = vk.API(access_token=mypwd.vk.token)
		test_group = -77148101
		real_group = -76944895
		msg = vkapi.wall.post(owner_id=real_group,from_group=1,message=whole_text)
		if DEBUG:
			print mag
	    else:
		data = None
		print "no such a date in DATA column 1"
	else:
	    print "its not time"
	# NOTE!!! while sending message through GMAIL
	# do not forget to encode/decode!!!
	# ===========================================
	# send_email(gmail_user, gmail_pwd, 
	#	   SUBJECT=data[1].encode("utf-8"), 
        #           TEXT=data[3].encode("utf-8"))
	# ===========================================

if __name__ == '__main__':
    status = main()
    sys.exit(status)
