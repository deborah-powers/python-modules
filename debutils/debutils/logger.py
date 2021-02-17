#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from inspect import stack
def traceDate ():
	# date est un objet datetime.datetime
	now = datetime.today ()
	return '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)
def traceLine ():
	stackList = stack ()
	stackLen = len (stackList)
	i=0
	while i< stackLen and __file__ in stackList [i].filename: i+=1
	return '%s\t%d\t%s' % (stackList [i].filename, stackList [i].lineno, stackList [i].function)
def log (message=None):
	trace = traceDate () +' '+ traceLine ()
	if message: print (trace, message)
	else: print (trace)
def message (message=None, obj=None):
	msgAffichable =""
	if message:
		msgAffichable = message
		if obj: msgAffichable = msgAffichable +'\t'+ str (obj)
	elif obj: msgAffichable = str (obj)
	log (msgAffichable)
def coucou ():
	log ('coucou')
alphabet = 'abcdefghijklmnopqrstuvwxyz'
letterPos =0
def letter ():
	log (alphabet [letterPos])
	letterPos +=1
	if letterPos >25: letterPos =0