#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from sys import argv
from fileList import FileList
from fileSimple import File

def getDate (self, dateMin=None, dateMax=None):
	if dateMin:
		d= self.index (dateMin)
		self.text = self.text[d:]
	if dateMax:
		d= self.rindex (dateMax)
		self.text = self.text[:d]
	self.clean()
	nbList = '0123456789'
	for nb in nbList: self.replace (', '+nb, ','+nb)

def cleanModule (self):
	artefacts =( 'com', 'org')
	for word in artefacts: self.replace (' '+ word +'.',' ')
	# self.clean()
	nbList = '0123456789'
	for nb in nbList: self.replace (', '+nb, ','+nb)
	artefacts =( '<label>Voir</label>', '</label>', '</xmlResult>]) sur la Queue queue://ord-com-out ...', 'fr.asp.synergie.app.', 'fr.asp.synergie.')
	for word in artefacts: self.replace (word)
	artefacts =( 'ac', 'cdm', 'aec', 'sif', 'can', 'edi', 'ord', 'cdm-batch', 'sif-batch', 'cdm-ech', 'sif-ech')
	for word in artefacts: self.replace ('['+ word +']', word)
	artefacts =( 'DEBUG', 'INFO', 'WARN', 'ERROR')
	for word in artefacts: self.replace ('['+ word +']', word)
	# self.clean()
	for nb in nbList: self.replace (', '+nb, ','+nb)

def cleanLines (self):
	rangeLine = self.range()
	rangeLine.reverse()
	for l in rangeLine:
		if not self[l]: trash = self.pop (l)
		elif ' fr.asp.synergie.core.ael.' in self[l]: trash = self.pop (l)
		elif ' - Choosing bean (' in self[l]: trash = self.pop (l)
		elif 'TaskProcessNewExecutionCoordinator.onNewNotification' in self[l]: trash = self.pop (l)
		elif "' was evaluated and did not match a property. The literal value '" in self[l]: trash = self.pop (l)
		elif "could not locate the message resource with key " in self[l]: trash = self.pop (l)
		elif '\t' == self[l][0] and '(<generated>)' in self[l]: trash = self.pop (l)
		elif '\t' == self[l][0] and 'fr.asp.synergie.' not in self[l]: trash = self.pop (l)
		elif "INFO" in self[l]: trash = self.pop (l)

def reverseLines (self):
	d= self.index ('\n2022')
	dateMin = self.text[d:d+24]
	f= self.rindex ('\n2022')
	dateMax = self.text[f:f+24]
	print (d,f)
	if dateMin > dateMax:
		self.fromText()
		self.reverse()
		self.toText()

def cleanLog (self, dateMin=None, dateMax=None):
	if dateMin:
		fileDate = File (self.file)
		fileDate.fromFile()
		fileDate.getDate (dateMin, dateMax)
		self.text = fileDate.text
		self.fromText()
	else: self.fromFile()
	self.cleanLines()
	print (self.text[900:])
	self.toText()
	print (self.text[900:])
	self.cleanModule()
	self.reverseLines()
	self.title = self.title + ' bis'
	self.fileFromData()
	File.toFile (self)

setattr (File, 'getDate', getDate)
setattr (File, 'cleanModule', cleanModule)
setattr (FileList, 'cleanLines', cleanLines)
setattr (FileList, 'reverseLines', reverseLines)
setattr (FileList, 'cleanLog', cleanLog)

def test():
	filePattern = 'b/mantis 1560\\mantis 1560 log 03-08 %s.txt'
	moduleNames =( 'aec', 'sbt', 'edi')
	for module in moduleNames:
		flist = FileList ('\n', filePattern % module)
		flist.cleanLog()

if len (argv) >1:
	dateMin = None
	dateMax = None
	flist = FileList ('\n', argv[1])
	if len (argv) >2: dateMin = argv[2]
	if len (argv) >3: dateMax = argv[3]
	flist.cleanLog (dateMin, dateMax)
else: test()
