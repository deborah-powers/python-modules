#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileClass import FilePerso
from tableClass import ListPerso, TablePerso

help ="""
un fichier contenant une liste
"""

class ListFile (FilePerso, ListPerso):
	def __init__(self, separator ='\n', file =None):
		FilePerso.__init__(self, file)
		ListPerso.__init__(self)
		self.sepLin = sepLin

	def fromFile (self):
		FilePerso.fromFile (self)
		self.fromText (self.sepLin, self.text)

	def toFile (self):
		self.text = self.toText (self.sepLin)
		FilePerso.toFile (self)


class TableFile (ListFile, TablePerso):
	def __init__(self, sepLin='\n', sepCol='\t', file =None):
		ListFile.__init__(self, file)
		TablePerso.__init__(self)
		self.sepCol = sepCol

	def fromFile (self):
		ListFile.fromFile (self)
		rangeLin = self.range()
		for l in rangeLin: self[l] = self[l].fromText (self.sepCol, self[l])

	def toFile (self):
		rangeLin = self.range()
		for l in rangeLin: self[l] = self[l].toText (self.sepCol)
		ListFile.toFile (self)

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



