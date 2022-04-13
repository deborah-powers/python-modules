#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from random import choice

class List (list):

	def iterate (self, function):
		rangeList = self.range()
		newList = List()
		for i in rangeList: newList.append (function (self[i]))
		return newList

	def sortFunc (self, funcSort):
		if len (self) <2: return self
		listStart = List()
		listEnd = List()
		item = choice (self)
		for l in self:
			if funcSort (item, l): listEnd.append (l)
			else: listStart.append (l)
		if len (listStart) >1: listStart.sortFunc (funcSort)
		if len (listEnd) >1: listEnd.sortFunc (funcSort)
		newList = List()
		if listStart: newList.extend (listStart)
		if listEnd: newList.extend (listEnd)
		return newList

	def copy (self):
		newList = List()
		newList.extend (self)
		return newList

	def fromText (self, word, text):
		newList = List()
		newList.extend (self)
		newList.extend (text.split (word))
		return newList

	def toText (self, word):
		newList =""
		for item in self: newList = newList + word + item
		newList = newList.replace (word, "", 1)
		return newList

	def toTextList (self):
		newList = List()
		for item in self: newList.append (str (item))
		return newList

	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = len (self)
		while end <=0: end += lenList
		if end > lenList: end = lenList
		newList =[]
		while start <end:
			newList.append (start)
			start += step
		return newList

	def col (self, colId):
		# pour les tableaux
		newList = List()
		for line in self:
			if len (line) > colId: newList.append (line[colId])
			else: newList.append (None)
		return newList

