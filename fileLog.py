#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from debutils.fileList import FileList
from debutils.file import File

def cleanLog (self):
	self.fromFile()
	self.text = self.toText ('\n')
	self.clean()
	self.replace (' com.',' ')
	self.replace (' org.',' ')
	self.replace ('&lt;', '<')
	self.replace ('&gt;', '>')
	self.replace ('<label>Voir</label>')
	self.replace ('</label>')
	self.replace ('</xmlResult>]) sur la Queue queue://ord-com-out ...')
	self.replace ('</xmlResult>]) sur la Queue queue://ord-com-out...')
	self.clean()
	self.list =[]
	self.fromText ('\n', self.text)
	rangeLine = self.range()
	rangeLine.reverse()
	for l in rangeLine:
		if ' fr.asp.synergie.core.ael.' in self[l]: trash = self.pop (l)
		elif '	at ' in self[l] and '(<generated>)' in self[l]: trash = self.pop (l)
		elif '	at ' in self[l] and 'fr.asp.synergie.' not in self[l]: trash = self.pop (l)
	"""
	countLine =0
	lenList = len (self.list)
	l=0
	while l< lenList:
		if '	at ' not in self[l]: l+=1; countLine =0
		elif countLine <4: l+=1; countLine +=1
		else: lenList -=1; trash = self.pop (l)
	"""
	self.text = self.toText ('\n')
	self.replace (' fr.asp.synergie.',' ')
	self.title = self.title + ' bis'
	self.fileFromData()
	File.toFile (self)

setattr (FileList, 'cleanLog', cleanLog)

filePattern = 'b/mantis 1560\\mantis 1560 log 03-08 %s.txt'
moduleNames =( 'sbt', 'edi')
for module in moduleNames:
	flist = FileList ('\n', filePattern % module)
	flist.cleanLog()
