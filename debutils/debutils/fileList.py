#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from debutils.file import File
from debutils.list import List, Table

help =""" un fichier contenant une liste """

class FileList (File, List):
	def __init__ (self, sepLin ='\n', file =None):
		File.__init__ (self, file)
		List.__init__ (self)
		self.sepLin = sepLin
	def fromFile (self):
		File.fromFile (self)
		List.fromText (self, self.sepLin, self.text)
	def toFile (self):
		self.text = self.toText (self.sepLin)
		File.toFile (self)
	def length (self):
		return len (self.list)

class FileTable (File, Table):
	def __init__ (self, sepLin='\n', sepCol='\t', file =None):
		File.__init__ (self, file)
		Table.__init__ (self)
		self.sepLin = sepLin
		self.sepCol = sepCol
	def fromFile (self):
		tmpList = FileList ()
		tmpList.copyFile (self)
		tmpList.fromFile ()
		rangeLin = tmpList.range ()
		for l in rangeLin:
			tmp = List ()
			tmp.fromText (self.sepCol, tmpList [l])
			self.addLine (tmp)
	def toFile (self):
		self.text = self.toText (self.sepLin, self.sepCol)
		File.toFile (self)
	def length (self):
		return len (self.list)
	def __str__ (self):
		return self.toText ('\n', '\t')