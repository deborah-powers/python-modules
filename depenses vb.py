#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import textFct
from fileCls import FileTable
import loggerFct as log

def getInfosCourses (self):
		newTab = FileTable()
		newTab.path = 'b/\t.tsv'
		newTab.title = self.title +' bis'
		newTab.toPath()
		newList =[]
		for line in self.list:
			if line[2] in ('courses', 'restau', 'tgtg'):
			#	log.logMsg (line)
				newList.append ([ line[0], float (line[4]) ])
		year = newList[0][0][:4]
		amount =0.0
		for line in newList:
			if year == line[0][:4]: amount += line[1]
			else:
				newTab.append ([year, str (amount)])
				year = line[0][:4]
				amount = line[1]
		newTab.append ([year, str (amount)])
		return newTab

def getInfosTout (self):
		newTab = FileTable()
		newTab.path = 'b/\t.tsv'
		newTab.title = self.title +' bis'
		newTab.toPath()
		year = self.list[0][0][:7]
		amount =0.0
		for line in self.list[1:]:
			if year == line[0][:7]: amount += float (line[4])
			else:
				amount = round (amount, 2)
				newTab.append ([year, str (amount)])
				year = line[0][:7]
				amount = float (line[4])
		amount = round (amount, 2)
		newTab.append ([year, str (amount)])
		return newTab

setattr (FileTable, 'getInfos', getInfosTout)

fileName = 'b/perso\\depenses.tsv'
fileTab = FileTable (fileName)
fileTab.read()
newTab = fileTab.getInfos()
newTab.write()