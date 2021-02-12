#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from debutils.file import FilePerso
from debutils.list import ListPerso, TablePerso

help =""" un fichier contenant une liste """

class FileList (FilePerso, ListPerso):
	def __init__(self, sepLin ='\n', file =None):
		FilePerso.__init__(self, file)
		ListPerso.__init__(self)
		self.sepLin = sepLin


	def fromFile (self):
		FilePerso.fromFile (self)
		ListPerso.fromText (self, self.sepLin, self.text)

	def toFile (self):
		self.text = self.toText (self.sepLin)
		FilePerso.toFile (self)

	def length (self):
		return len (self.list)


class FileTable (FilePerso, TablePerso):
	def __init__(self, sepLin='\n', sepCol='\t', file =None):
		FilePerso.__init__(self, file)
		TablePerso.__init__(self)
		self.sepLin = sepLin
		self.sepCol = sepCol

	def fromFile (self):
		tmpList = FileList()
		tmpList.copyFile (self)
		tmpList.fromFile()
		rangeLin = tmpList.range()
		for l in rangeLin:
			tmp = ListPerso()
			tmp.fromText (self.sepCol, tmpList[l])
			self.addLine (tmp)

	def toFile (self):
		self.text = self.toText (self.sepLin, self.sepCol)
		FilePerso.toFile (self)

	def length (self):
		return len (self.list)

	def __str__ (self):
		return self.toText ('\n', '\t')


class FileTableVa (FilePerso, TablePerso):
	def __init__(self, sepLin='\n', sepCol='\t', file =None):
		FilePerso.__init__(self, file)
		TablePerso.__init__(self)
		self.sepLin = sepLin
		self.sepCol = sepCol

	def fromFile (self):
		FilePerso.fromFile (self)
		self.fromText (self.sepLin, self.sepCol, self.text)

	def toFile (self):
		self.text = self.toText (self.sep)
		FilePerso.toFile (self)



