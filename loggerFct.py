#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from inspect import stack
from fileLocal import pathRoot, pathDesktop

def traceLine():
	stackList = stack()
	stackLen = len (stackList)
	i=0
	while i< stackLen and __file__ in stackList[i].filename: i+=1
	strNum = str (stackList[i].lineno)
	while len (strNum) <3: strNum = strNum +' '
	strFile = stackList[i].filename
	strFile = strFile.replace ('AppData\\Local\\Programs\\Python\\Python38\\lib\\site-packages\\', "")
	strFile = strFile.replace ('\\__init__.py', "")
	strFile = strFile.replace (pathDesktop + 'python\\', "")
	strFile = strFile.replace (pathDesktop, "")
	strFile = strFile.replace (pathRoot, "")
	return '%s\t%s %s' % (strFile, strNum, stackList[i].function)

def computeTrace():
	# date est un objet datetime.datetime
	now = datetime.today()
	strDate = '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)
	strDate = strDate[:12]
	while len (strDate) <13: strDate = strDate +' '
	return strDate

def traceDate():
	return computeTrace() + traceLine()

def objToStr (message):
	if type (message) == int and message ==0: return 'O'
	elif type (message) == bool:
		if message: return 'oui'
		else: return 'non'
	elif not message: return ""
	elif type (message) == dict:
		messageKeys = list (message.keys())
		res = "dictionnaire à "+ objToStr (len (messageKeys)) + " entrées\n"
		nbkeys = len (messageKeys)
		if nbkeys >10: nbkeys =10
		rkeys = range (nbkeys)
		for k in rkeys: res = res + objToStr (messageKeys[k]) +"\t"+ objToStr (message[messageKeys[k]]) +"\n"
		return res
	elif type (message) == list:
		res = "liste à "+ objToStr (len (message)) + " éléments\n"
		for line in message[:10]: res = res + objToStr (line) +"\n"
		return res
	elif type (message) == str: return message[:100]
	else: return str (message)

def logInfo (showDate=False):
	trace = traceLine()
	if showDate: trace = computeTrace() + trace
	print (trace)

def message (message, showDate=False):
	trace = traceLine()
	if showDate: trace = computeTrace() + trace
	res = objToStr (message)
	trace = trace +'\t'+ res
	print (trace)

def coucou (showDate=False):
	logMsg ('coucou', showDate)

def log (*messages, showDate=False):
	trace = traceLine()
	if showDate: trace = computeTrace() + trace
	for message in messages:
		res = objToStr (message)
		if '\n' in res: trace = trace +'\n'+ res
		else: trace = trace +'\t'+ res
	print (trace)

def exists (obj):
	if (obj): log (obj)
	else: log ('objet null')

alphabet = 'abcdefghijklmnopqrstuvwxyz'
letterPos =0

def letter():
	log (alphabet [letterPos])
	letterPos = letterPos +1
	if letterPos >25: letterPos =0
