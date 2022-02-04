#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple.fileList import FileList
from fileSimple import File
from listFiles import ListFile

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
	self.clean()
	nbList = '0123456789'
	for nb in nbList: self.replace (', '+nb, ','+nb)
	artefacts =( '<label>Voir</label>', '</label>', '</xmlResult>]) sur la Queue queue://ord-com-out ...', 'fr.asp.synergie.app.', 'fr.asp.synergie.')
	for word in artefacts: self.replace (word)
	self.clean()
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
	#	elif '\t' == self[l][0] and 'fr.asp.synergie.' not in self[l]: trash = self.pop (l)

def cleanLog (self):
	else: self.fromFile()
	self.cleanLines()
	self.toText()
	self.cleanModule()
	self.reverseLines()
	# self.title = self.title + ' bis'
	self.fileFromData()
	File.toFile (self)

setattr (File, 'cleanModule', cleanModule)
setattr (FileList, 'cleanLines', cleanLines)
setattr (FileList, 'cleanLog', cleanLog)

flist = ListFile ('b/logs')
flist.get()

if len (argv) >1:
	flist = FileList ('\n', argv[1])
	flist.cleanLog()
