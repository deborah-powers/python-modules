#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import funcList
import funcText
from classFile import File

def cleanLog (self):
	self.read()
	self.text = funcText.clean (self.text)
	self.replace ('. ','.')
	self.text ='\n'+ self.text
	self.replace ('\nat ', '\n\tat ')
	self.reverseLines()
	listLine = funcList.fromText (self.text, '\n')
	rangeLine = funcList.range (listLine, end=-1)
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
	#	elif "INFO" in listLine[l] and ("INFO" in listLine[l+1] or "WARN" in listLine[l+1] or "ERROR" in listLine[l+1]): trash = listLine.pop (l)
	self.text = '\n'.join (listLine)
	self.replace ('com.opensymphony.xwork2.util.logging.commons.')
	self.replace ('fr.asp.synergie.app.')
	self.replace ('fr.asp.synergie.')
	self.replace (': 8080/', ':8080/')
	self.replace ('[DEBUG] ', 'DEBUG ')
	self.replace ('[INFO] ', 'INFO ')
	self.replace ('[WARN] ', 'WARN ')
	self.replace ('[ERROR] ', 'ERROR ')
	self.replace ('[edi]')
	self.replace ('[ord]')
	self.replace ('[cdm-batch]')
	self.replace ('[cdm]')
	self.replace ('[cdm-lb-0]')
	self.replace ('[cdm-lb-1]')
	self.replace ('[cdm-backend]')
	self.replace ('[cdm-backend-lb-0]')
	self.replace ('[cdm-backend-lb-1]')
	self.replace ('[sif]')
	self.replace ('[sif-batch]')
	self.replace ('[sif-ech]')
	self.title = self.title +' bis'
	self.write()

def reverseLines (self):
	d= self.text.find ('\n2022')
	dateMin = self.text[d:d+27]
	f= self.text.rfind ('\n2022')
	dateMax = self.text[f:f+27]
	if dateMin > dateMax:
		listLine =[]
		listLine = funcList.fromText (self.text, '\n')
		listLine.reverse()
		self.text = '\n'.join (listLine)

setattr (File, 'reverseLines', reverseLines)
setattr (File, 'cleanLog', cleanLog)

log = File ('b/log.txt')
log.cleanLog()
