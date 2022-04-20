#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from sys import argv
from classText import Text
from classFile import File
from classList import List

def cleanLog (self):
	self.read()
	self.text = self.text.clean()
	self.text = self.text.replace ('. ','.')
	self.text = self.text.replace ('\nat ', '\n\tat ')
	self.reverseLines()
	listLine = List()
	listLine = listLine.fromText ('\n', self.text)
	rangeLine = listLine.range (end=-1)
	rangeLine.reverse()
	for l in rangeLine:
		if not listLine[l]: trash = listLine.pop (l)
		elif ' fr.asp.synergie.core.ael.' in listLine[l]: trash = listLine.pop (l)
		elif ' - Choosing bean (' in listLine[l]: trash = listLine.pop (l)
		elif 'TaskProcessNewExecutionCoordinator.onNewNotification' in listLine[l]: trash = listLine.pop (l)
		elif "' was evaluated and did not match a property. The literal value '" in listLine[l]: trash = listLine.pop (l)
		elif "could not locate the message resource with key " in listLine[l]: trash = listLine.pop (l)
		elif "(CommonsLogger.java: 56)" in listLine[l]: trash = listLine.pop (l)
		elif '\t' == listLine[l][0] and '(<generated>)' in listLine[l]: trash = listLine.pop (l)
		elif '\t' == listLine[l][0] and 'fr.asp.synergie.' not in listLine[l]: trash = listLine.pop (l)
		elif 'core.web.' in listLine[l]: trash = listLine.pop (l)
		elif "INFO" in listLine[l] and ("INFO" in listLine[l+1] or "WARN" in listLine[l+1] or "ERROR" in listLine[l+1]): trash = listLine.pop (l)
	self.text = Text ('\n'.join (listLine))
	self.text = self.text.replace ('com.opensymphony.xwork2.util.logging.commons.')
	self.text = self.text.replace ('fr.asp.synergie.app.')
	self.text = self.text.replace ('fr.asp.synergie.')
	self.cleanDate()
	self.title = self.title +' bis'
	self.write()

def cleanDate (self):
	listLine = List()
	listLine = listLine.fromText ('\n2022-', self.text)
	rangeLine = listLine.range()
	trash = rangeLine.pop (0)
	rangeLine.reverse()
	for l in rangeLine:
		tmpDate = listLine[l][:21].replace (': ',':')
		tmpDate = tmpDate.replace (', ',',')
		listLine[l] = tmpDate + listLine[l][21:]
	self.text = Text ('\n2022-'.join (listLine))

def reverseLines (self):
	d= self.text.find ('\n2022')
	dateMin = self.text[d:d+27]
	f= self.text.rfind ('\n2022')
	dateMax = self.text[f:f+27]
	if dateMin > dateMax:
		listLine = List()
		listLine = listLine.fromText ('\n', self.text)
		listLine.reverse()
		self.text = Text ('\n'.join (listLine))


setattr (File, 'reverseLines', reverseLines)
setattr (File, 'cleanLog', cleanLog)
setattr (File, 'cleanDate', cleanDate)

log = File ('b/log.txt')
log.cleanLog()
