#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
from sys import argv
from debutils.fileList import FileList
from debutils.file import File

def cleanLog (self):
	self.fromFile()
	# préparer le texte
	self.toText()
	self.clean()
	artefacts =( 'com', 'org')
	for word in artefacts: self.replace (' '+ word +'.',' ')
	artefacts =( '<label>Voir</label>', '</label>', '</xmlResult>]) sur la Queue queue://ord-com-out ...')
	for word in artefacts: self.replace (word)
	artefacts =( 'ac', 'cdm', 'aec', 'sif', 'can', 'cdm-batch', 'sif-batch', 'cdm-ech', 'sif-ech')
	for word in artefacts: self.replace ('['+ word +'] ')
	artefacts =( 'DEBUG', 'INFO', 'WARN', 'ERROR')
	for word in artefacts: self.replace ('['+ word +']', word)
	self.clean()
	# supprimer les lignes inutiles
	self.fromText()
	rangeLine = self.range()
	rangeLine.reverse()
	for l in rangeLine:
		if ' fr.asp.synergie.core.ael.' in self[l]: trash = self.pop (l)
		elif "' was evaluated and did not match a property. The literal value '" in self[l]: trash = self.pop (l)
		elif "could not locate the message resource with key " in self[l]: trash = self.pop (l)
		elif '\t' == self[l][0] and '(<generated>)' in self[l]: trash = self.pop (l)
		elif '\t' == self[l][0] and 'fr.asp.synergie.' not in self[l]: trash = self.pop (l)
	self.toText()
	self.replace ('fr.asp.synergie.app.')
	self.replace ('fr.asp.synergie.')
	# au cas où le fichier est inversé
	if self.contain ('\tat '):
		d= File.index (self, '[ERROR]')
		f= File.index (self, '\tat ')
		if d<f:
			self.fromText()
			self.reverse()
			self.toText()
	# écrire le fichier
	self.title = self.title + ' bis'
	self.fileFromData()
	File.toFile (self)

setattr (FileList, 'cleanLog', cleanLog)

def test():
	filePattern = 'b/mantis 1560\\mantis 1560 log 03-08 %s.txt'
	moduleNames =( 'aec', 'sbt', 'edi')
	for module in moduleNames:
		flist = FileList ('\n', filePattern % module)
		flist.cleanLog()

if len (argv) >1:
	flist = FileList ('\n', argv[1])
	flist.cleanLog()
else: test()
