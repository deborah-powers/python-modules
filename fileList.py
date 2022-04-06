#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileSimple import File
from list import List, Table
import logger

help =""" un fichier contenant une liste """

class FileList (File, List):
	def __init__ (self, sepLin ='\n', file =None):
		File.__init__ (self, file)
		List.__init__ (self)
		self.sepLin = sepLin

	def fromText (self):
		self.list =[]
		List.fromText (self, self.sepLin, self.text)

	def toText (self):
		self.text =""
		for item in self.list: self.text = self.text + self.sepLin + item
		self.text = self.text.replace (self.sepLin, "", 1)

	def fromFile (self):
		File.fromFile (self)
		self.fromText()

	def toFile (self):
		self.toText()
		File.toFile (self)

	def length (self):
		return len (self.list)

	def replace (self, oldWord, newWord='', toText=''):
		if 'deb' in toText: self.toText()
		self.text = self.text.replace (oldWord, newWord)
		if 'fin' in toText: self.fromText()

	# ________________________ utiliser les fonctions de Text ________________________

"""
	def clean (self):
		self.toText()
		File.clean (self)
		self.fromText()

	def replace (self, oldWord, newWord=''):
		self.toText()
		File.replace (self, oldWord, newWord)
		self.fromText()
"""
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
			self.appendLine (tmp)

	def toFile (self):
		self.text = self.toText (self.sepLin, self.sepCol)
		File.toFile (self)

	def length (self):
		return len (self.list)

	def __str__ (self):
		return self.toText ('\n', '\t')