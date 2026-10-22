#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileList import FileTable
from list import List
from event import DatePerso

depFileName = '/home/lenovo/Bureau/divers/perso/depenses.tsv'
class DepenseList (FileTable):
	def __init__ (self):
		FileTable.__init__ (self, file=depFileName)
		self.titles = List ()
	def fromFile (self):
		FileTable.fromFile (self)
		self.titles.addList (self [0])
		self.pop (0)
		rangeLin = self.range ()
		for l in rangeLin: self [l] [4] = float (self [l] [4])
	def recent (self, period):
		dateRef = DatePerso ()
		dateRef.today ()
		if period == 'year': dateRef.year -=1
		else: dateRef.remMonth ()
		dateRefStr = str (dateRef)
		newDep = DepenseList ()
		newDep.titles = self.titles.copy ()
		for dep in self:
			if dep [0] >= dateRefStr: newDep.addLine (dep)
		return newDep
	def theme (self, ref):
		newDep = DepenseList ()
		newDep.titles = self.titles.copy ()
		for dep in self:
			if dep [2] == ref: newDep.addLine (dep)
		return newDep
	def themeList (self):
		dictTheme = {}
		for line in self:
			if line [2] in dictTheme.keys (): dictTheme [line [2] ] += line [4]
			else: dictTheme [line [2] ] = line [4]
		return dictTheme
	def total (self):
		nb=0.0
		for line in self: nb+= line [4]
		return nb
depList = DepenseList ()
depList.fromFile ()
newDep = DepenseList ()
if len (argv) >1:
	info = argv [1]
	if info == 'month':
		newDep = depList.recent ('month')
		tot = newDep.total ()
		print ('vous avez dépensé', tot, 'e ce moi-ci')
	else:
		newDep = depList.recent ('year')
		if info == 'year':
			totDict = newDep.themeList ()
			print ("vos dépenses de l'année:")
			for dep in totDict.keys (): print (dep, ':t', totDict [dep])
			tot = newDep.total ()
			print ('le total est de', tot, 'e')
		else:
			newDep = newDep.theme (info)
			tot = newDep.total ()
			print ('vous avez dépensé', tot, 'e en', info, 'cette année')