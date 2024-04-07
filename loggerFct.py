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

def tolog (message):
	if type (message) == int and message ==0: return 'O'
	elif type (message) == bool:
		if message: return 'oui'
		else: return 'non'
	elif not message: return ""
	elif type (message) == dict:
		messageKeys = list (message.keys())
		res = "dictionnaire à "+ tolog (len (messageKeys)) + " entrées\n"
		nbkeys = len (messageKeys)
		if nbkeys >10: nbkeys =10
		rkeys = range (nbkeys)
		for k in rkeys: res = res + tolog (messageKeys[k]) +"\t"+ tolog (message[messageKeys[k]]) +"\n"
		return res
	elif type (message) == list:
		res = "liste à "+ tolog (len (message)) + " éléments\n"
		for line in message[:10]: res = res + tolog (line) +"\n"
		return res
	elif type (message) == str: return message[:100]
	else: return str (message)

def logone (message):
	trace = traceLine()
	# trace = traceDate() +' '+ trace
	res = tolog (message)
	trace = trace +'\t'+ res
	print (trace)

def log (*messages):
	trace = traceLine()
	# trace = traceDate() +' '+ trace
	for message in messages:
		res = tolog (message)
		if '\n' in res: trace = trace +'\n'+ res
		else: trace = trace +'\t'+ res
	print (trace)

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
