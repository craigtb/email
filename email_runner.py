#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime
import mysql.connector
import time

EMAIL_ACCOUNT = "craigemailprgm@gmail.com"
EMAIL_FOLDER = "Testing"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "UNSEEN")
    if rv != 'OK':
        print "No messages found!"
        return
    cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1', database='test')
    cursor = cnx.cursor(dictionary=True);
    query = ("SELECT * FROM test.post ORDER BY CRT_TS DESC")
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        #print 'Message %s: %s' % (num, subject)
        #print 'Raw Date:', msg['Date']
	#print 'Message: ', msg
	stuff = str(msg)
	cell_provider_arr = msg['From'].split('@')
	print(cell_provider_arr[1])
	message = ""
	arr2 = []
	if cell_provider_arr[1] == 'vzwpix.com':
		print "its from verizon"
		arr = stuff.split('Content-Location: text_0.txt\n\n', 1)
		arr2 = arr[1].split('\n--__', 1)
		message = arr2[0]
	elif cell_provider_arr[1] == 'mms.att.net':
		print "its from att"
		arr = stuff.split('<td>', 1)
		arr_att = arr[1].split('</td>')
		message = arr_att[0].strip()
        
	msgfrom = "Unknown"
	print 'Message? :',message
	if  msg['From'] == '4048054545@vzwpix.com' :
		msgfrom = 'Craig'
	elif msg['From'] == '3343982141@vzwpix.com' :
		msgfrom = 'Neely'
	elif msg['From'] == '4043233229@mms.att.net' :
		msgfrom = 'Frank'
	else :
		msgfrom = 'Unknown'
	query = "INSERT INTO test.post (name, message) values ('%s', '%s')" % (msgfrom, message)
	print 'query: ', query
	cursor.execute(query)
	cnx.commit()

while True:

	M = imaplib.IMAP4_SSL('imap.gmail.com')

	try:
	    rv, data = M.login(EMAIL_ACCOUNT, 'craig1234')
	except imaplib.IMAP4.error:
	    print "LOGIN FAILED!!! "
	    sys.exit(1)

	print rv, data

	rv, mailboxes = M.list()
	if rv == 'OK':
	    print "Mailboxes:"
	    print mailboxes

	rv, data = M.select(EMAIL_FOLDER)
	if rv == 'OK':
	    print "Processing mailbox...\n"
	    process_mailbox(M)
	    M.close()
	else:
	    print "ERROR: Unable to open mailbox ", rv

	M.logout()
	time.sleep(60)
