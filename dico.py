#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# http://www.pallier.org/extra/liste.de.mots.francais.frgut.txt
from sys import argv
from debutils.text import wordsEnd
from fileSimple import File
from fileSimple.fileList import FileList
import debutils.logger as logger

newPoints = "-'() /_\"\n\t<> [](){}|%#$@=+*°&0123456789"
ref = File ('b/liste-mots.txt')

class FileSrc (FileList):
	def log (self):
		d= self.index ('mcehywkh')
		print (self.text[d-20:d+20])

	def clean (self):
		self.text = self.text.lower()
		FileList.clean (self)
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

	def full (self):
		self.fromFile()
		self.clean()
		self.groom()
		self.unknowWords()

if len (argv) <2: print ('il manque le fichier')
elif argv[1] == 'tri':
	refSort = FileList (' ', 'b/liste-mots.txt')
	refSort.fromFile()
	refSort.sort()
	print ('c')
	refSort.text =""
	for item in refSort.list: refSort.text = refSort.text +' '+ item
	File.toFile (refSort)
	print ('d')
elif argv[1] == 'test':
	ref.fromFile()
	src = FileSrc (' ', 'C:\\Users\\deborah.powers\\Desktop\\journal.txt')
	src.full()
else:
	ref.fromFile()
	src = FileSrc (' ', 'C:\\Users\\deborah.powers\\Desktop\\articles\\' + argv[1] +'.txt')
	src.full()
