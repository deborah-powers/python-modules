#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from inspect import stack

logon = True

def traceDate():
	# date est un objet datetime.datetime
	now = datetime.today()
	return '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)

def traceLine():
	stackList = stack()
	stackLen = len (stackList)
	i=0
	while i< stackLen and __file__ in stackList[i].filename: i+=1
	return '%s\t%d\t%s' %( stackList[i].filename, stackList[i].lineno, stackList[i].function)

def log (message=None):
	trace = traceDate() +' '+ traceLine()
	if logon and message: print (trace, message)
	elif logon: print (trace)

def coucou():
	log ('coucou')

alphabet = 'abcdefghijklmnopqrstuvwxyz'
letterPos =0
def letter():
	log (alphabet [letterPos])
	letterPos +=1
	if letterPos >25: letterPos =0

"""
class Logger():
	def __init__ (self, logon=True):
		self.logon = logon
		self.date =""
		self.line =""

	def traceDate (self):
		# date est un objet datetime.datetime
		now = datetime.today()
		self.date = '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)

	def traceLine (self):
		stackList = stack()
		stackLen = len (stackList)
		i=0
		while i< stackLen and __file__ in stackList[i].filename: i+=1
		self.line = '%s:%d: %s' %( stackList[i].filename, stackList[i].lineno, stackList[i].function)

	def __str__ (self):
		self.traceDate()
		self.traceLine()
		return self.date +' '+ self.line

	def log (self, message=None):
		if self.logon and message: print (self.__str__(), message)
		elif self.logon: print (self.__str__())

	def coucou (self):
		self.log ('coucou')
"""
