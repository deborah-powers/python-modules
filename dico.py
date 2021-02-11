#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileClass import FilePerso
from fileList import FileList, FileTable
from textClass import pointsEnd
from listClass import ListPerso
from listFile import ListFile

suffix =( 'ations', 'itions', 'trices', 'ables', 'aires', 'amant', 'ament', 'ances', 'aient', 'ation', 'asmes', 'elles', 'ement', 'ences', 'esses', 'ettes', 'euses', 'ibles', 'ières', 'iques', 'ismes', 'ition', 'tions', 'trice', 'able', 'ages', 'aire', 'ance', 'asme', 'bles', 'eaux', 'elle', 'ence', 'esse', 'ères', 'ette', 'eurs', 'euse', 'ible', 'ière', 'iers', 'ions', 'ique', 'isme', 'ités', 'mant', 'ment', 'ques', 'sses', 'tion', 'age', 'ais', 'ait', 'ant', 'aux', 'ble', 'eau', 'ent', 'ère', 'eur', 'ées', 'ier', 'ion', 'ité', 'nes', 'ont', 'ons', 'que', 'sse', 'ai', 'al', 'au', 'er', 'es', 'et', 'ez', 'ée', 'ne', 'a', 'e', 'é', 's', 't', 'x')
prefix =( 'imm', 'inn', 'pré', 'dé', 'im', 'in', 're', 'ré', 'sur' )
newPoints = "-'()/_\\\"\n\t<>[](){}|%#$@=+*°"
fileRefName = 'b/dico.txt'
lang = None

class FileRef (FileTable):
	def __init__ (self):
		FileTable.__init__ (self, '\n',' ', fileRefName)
		self.fromFile()
		if self.length() <3: self.add (ListPerso())

	def sort (self):
		tmpRange = self.range()
		for l in tmpRange: self[l].sort()

class ListSrc (ListFile):
	def get (self):
		ListFile.get (self)
		rangeFile = self.range()
		rangeFile.reverse()
		for f in rangeFile:
			if self[f].extension not in 'txt html': trash = self.pop (f)

class FileSrc (FileList):
	def __init__ (self, fileName=None):
		FileList.__init__ (self, ' ')
		if fileName:
			self.file = fileName
			self.fromFile()

	def listWords (self):
		for p in pointsEnd: self.replace (p,' ')
		for p in newPoints: self.replace (p,' ')
		self.clean()
		self.addList (self.text.split (' '))
		self.delDouble()
		self.list.sort()

	def fromFile (self):
		FilePerso.fromFile (self)
		self.listWords()

	def toFile (self, message=None):
		self.list.sort()
		self.text = ' '.join (self.list)
		if not message: message = 'dico'
		self.title = self.title +' '+ message
		self.path = 'b/'
		self.fileFromData()
		FilePerso.toFile (self)

	def checkWordLen (self, lang):
		if not self.list: self.fromFile()
		tmpRange = self.range()
		tmpRange.reverse()
		wordLen =10
		if lang == 'fr': wordLen =17
		for w in tmpRange:
			if len (self.list[w]) < wordLen: trash = self.list.pop (w)
		self.toFile ('mots longs')

	def dictPrep (self):
		if not self.text: self.fromFile()
		self.text = self.sep.join (self.list)
		for p in suffix: self.replace (p+' ', ' ')
		for p in prefix: self.replace (' '+p, ' ')
		numbers = '0123456789'
		for n in numbers: self.replace (n)
		while '  ' in self.text: self.replace ('  ',' ')
		self.text = self.text.lower()
		self.list = self.text.split (self.sep)
		self.delDouble()

	def dictList (self):
		self.dictPrep()
		dictRef = FileRef()
		tmpRange = self.range()
		tmpRange.reverse()
		for w in tmpRange:
			if self[w] not in dictRef[0] and self[w] not in dictRef[1] and self[w] not in dictRef[2]:
				dictRef[2].add (self[w])
		dictRef[2].sort()
		dictRef.toFile()

fileTstName = argv[1]
if fileTstName == 'tri':
	dictRef = FileRef()
	dictRef.sort()
	dictRef.toFile()
else:
	fileTstName = 'a/romans/' + fileTstName + '.txt'
	dictSrc = FileSrc (fileTstName)
	if len (argv) >2 and argv[2] in 'fr an':
		lang = argv[2]
		dictSrc.checkWordLen (lang)
	else: dictSrc.dictList()
