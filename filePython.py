#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import codecs
from debutils.file import File
from debutils.fileList import FileList

help ="""lancement: python filePy
	python mantisDeb
	python debutils/debutils/text

pas besoin de rajouter l'extension .py.
si votre fichier est dans le dossier python, vous pouvez indiquer le chemin à partir de ce dossier.
précisez pathRoot et pathPython."""

pathRoot = 'C:\\Users\\deborah.powers' + os.sep
pathPython = pathRoot + 'python' + os.sep

wordImport = (('import ', 7), ('from ', 5))
wordFunction = (('import ', 7), ('from ', 5), ('class ', 6), ('def ', 4), ('\t""" ', 5), ('\treturn', 7), ('\tdef ', 5), ('\t\t""" ', 6), ('\t\treturn', 8))

class FilePy (File):
	def __init__ (self, file =None):
		if file:
			if pathRoot not in file: file = pathPython + file
			if file[-3:] != '.py': file = file + '.py'
			if os.sep != '/': file = file.replace ('/', os.sep)
		File.__init__ (self, file)
		self.extension = 'py'

	def clean (self):
		self.text = self.text.strip()
		self.replace ('\r')
		self.replace ('(', ' (')
		while self.contain ('   '): self.replace ('   ','  ')
		self.replace ('  (', ' (')
		self.replace (' ()', '()')
		blankSpaces = '\n \t'
		for char in blankSpaces:
			while self.contain (char +'\n'): self.replace (char +'\n','\n')
		while self.contain ('\n '): self.replace ('\n ','\n')
		self.replace ('\ndef ', '\n\ndef ')
		self.replace ('\n\tdef ', '\n\n\tdef ')
		self.replace ('\nclass ', '\n\nclass ')

	def fromFile (self):
		if not os.path.exists (self.file): return
		self.dataFromFile()
		# ouvrir le file et recuperer le texte au format str
		textBrut = open (self.file, 'rb')
		tmpByte = textBrut.read()
		encodingList = ('utf-8', 'ascii', 'ISO-8859-1')
		for encoding in encodingList:
			try: self.text = codecs.decode (tmpByte, encoding=encoding)
			except UnicodeDecodeError: pass
			else: break
		textBrut.close()
		self.clean()

	def test (self):
		self.fromFile()
		self.title = self.title +'-bis'
		print ('création de %s') % self.title
		self.fileFromData()
		self.toFile()

	def help (self):
		self.fromFile()
		self.replace ('\n\n', '\n')
		flist = FileList ('\n', 'b/' + self.title + '-help.txt')
		flist.helpPy (self.text)

def helpPy (self, text):
	self.fromText ('\n', text)
	rangePy = self.range()
	rangePy.reverse()
	for p in rangePy:
		flag = False
		for (word, width) in wordFunction:
			if word == self[p][:width] and 'def __' not in self[p]:
				flag = True
				if word in '\t\treturn ':
					self[p] = self[p] +'\n'
		if flag == False: self.pop (p)
	self.toFile()

setattr (FileList, 'helpPy', helpPy)


if __name__ != '__main__': pass
elif len (argv) <2: print (help)
else:
	pyFile = FilePy (argv[1])
	pyFile.help()