#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# http://www.pallier.org/extra/liste.de.mots.francais.frgut.txt
from sys import argv
from debutils.text import wordsEnd
from fileSimple import File
from fileSimple.fileList import FileList
# import debutils.logger as logger

newPoints = "-'() /_\"\n\t<> [](){}|%#$@=+*°&0123456789"
ref = File ('b/liste-mots.txt')
ref.fromFile()

class FileSrc (FileList):
	def clean (self):
		FileList.clean (self)
		self.text = self.text.lower()
		for p in newPoints: self.replace (p, ' ')
		for p in wordsEnd: self.replace (p, ' ')
		self.text =' '+ self.text +' '
		self.fromText()

	def groom (self):
		self.sort()
		self.delDouble()
		tmpRange = self.range()
		tmpRange.reverse()
		trash =0
		for w in tmpRange:
			if ref.contain (self.list[w]): trash = self.list.pop (w)

	def unknowWords (self):
		print ('liste des mots inconnus')
		for word in self.list: print (word)

if len (argv) <2: print ('il manque le fichier')
else:
	# src = FileSrc ('a/romans/quand la terre hurla.txt')
	src = FileSrc (' ', 'C:\\Users\\deborah.powers\\Desktop\\articles\\' + argv[1] +'.txt')
	src.fromFile()
	src.clean()
	src.groom()
	src.unknowWords()



