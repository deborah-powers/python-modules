#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileClass import FilePerso
from listClass import ListPerso, TablePerso

help =""" un fichier contenant une liste """

class ListFile (FilePerso, ListPerso):
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


class TableFile (FilePerso, TablePerso):
	def __init__(self, sepLin='\n', sepCol='\t', file =None):
		ListFile.__init__(self, sepLin, file)
		TablePerso.__init__(self)
		self.sepCol = sepCol

	def fromFile (self):
		tmpList = ListFile()
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

	def __str__ (self):
		return self.toText ('\n', '\t')


class TableFileVa (FilePerso, TablePerso):
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



