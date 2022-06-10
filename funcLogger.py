#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from inspect import stack

addDate = False

def traceDate():
	# date est un objet datetime.datetime
	now = datetime.today()
	strDate = '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)
	while len (strDate) <15: strDate = strDate +' '
	return strDate

def traceLine():
	stackList = stack()
	stackLen = len (stackList)
	i=0
	while i< stackLen and __file__ in stackList[i].filename: i+=1
	strNum = str (stackList[i].lineno)
	while len (strNum) <3: strNum = strNum +' '
	strFile = stackList[i].filename
	strFile = strFile.replace ('/home/deborah/python/', "")
	strFile = strFile.replace ('/home/deborah/Bureau/', "")
	strFile = strFile.replace ('/home/deborah/', "")
	strFile = strFile.replace ('C:\\Users\\deborah.powers\\python\\debutils\\', "")
	strFile = strFile.replace ('C:\\Users\\deborah.powers\\python\\', "")
	strFile = strFile.replace ('C:\\Users\\deborah.powers\\', "")
	strFile = strFile.replace ('AppData\\Local\\Programs\\Python\\Python38\\lib\\site-packages\\', "")
	strFile = strFile.replace ('\\__init__.py', "")
	strFile = strFile.replace ('mantis-0.1-py3.8.egg\\mantis', 'mantis')
	return '%s\t%s %s' % (strFile, strNum, stackList[i].function)

def log (message=None):
	trace = traceLine()
	if addDate: trace = traceDate() +' '+ trace
	if not message: print (trace)
	elif message and type (message) == dict:
		print (trace)
		messageKeys = message.keys()
		for key in messageKeys: print ('\t', key, '\t', message[key])
	elif message and type (message) == list:
		print (trace)
		for line in message: print ('\t', line)
	elif type (message) == int and message ==0: print (trace +'\tO')
	else: print (trace +'\t', message)

def message (message=None, obj=None):
	msgAffichable =""
	if message:
		msgAffichable = message
		if obj: msgAffichable = msgAffichable +'\t'+ str (obj)
	elif obj: msgAffichable = str (obj)
	log (msgAffichable)

def exists (obj):
	if (obj): log (obj)
	else: log ('objet null')

def coucou():
	log ('coucou')

alphabet = 'abcdefghijklmnopqrstuvwxyz'
letterPos =0

def letter():
	log (alphabet [letterPos])
	letterPos = letterPos +1
	if letterPos >25: letterPos =0