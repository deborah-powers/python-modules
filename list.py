#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

def rangeNb (nb, start=0, step=1):
	rangeListTmp = range (start, nb, step)
	rangeList = List()
	for r in rangeListTmp: rangeList.append (r)
	return rangeList

class List():
	def __init__ (self):
		self.list = []

	def delDouble (self):
		""" transformer la liste [ a b b a c d e a f g ] en [ a b c d e f g ] """
		tmpRange = self.range()
		tmpRange.reverse()
		trash =0
		for w in tmpRange:
			if self.list.count (self.list[w]) >1: trash = self.list.pop (w)

	def iterate (self, function):
		rangeList = self.range()
		newList = List()
		for i in rangeList: newList.append (function (self.list[i]))
		return newList

	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = self.length()
		if end <=0: end += lenList
		elif end > lenList: end = lenList
		newList =[]
		while start <end:
			newList.append (start)
			start += step
		return newList

	def count (self, item):
		nb=0
		if item in self.list: nb= self.list.count (item)
		return nb

	def sortFunc (self, funcSort):
		if self.length() <2: return
		listStart = List()
		listEnd = List()
		item = choice (self.list)
		for l in self:
			if funcSort (item, l): listEnd.add (l)
			else: listStart.add (l)
		if listStart.length() >1: listStart.sortFunc (funcSort)
		if listEnd.length() >1: listEnd.sortFunc (funcSort)
		self.list = []
		if listStart: self.addList (listStart)
		if listEnd: self.addList (listEnd)

	def sort (self, funcSort=None):
		if sortFunc:
			from random import choice
			self.sortFunc (funcSort)
		else: self.list.sort()

	def length (self):
		return len (self.list)

	def index (self, item):
		nb=-1
		if item in self.list: nb= self.list.index (item)
		return nb

	def __str__ (self):
		return self.toText ('\n')

	def addList (self, newList):
		if type (newList) == list: self.list.extend (newList)
		else: self.list.extend (newList.list)

	def add (self, value, pos=-1):
		if pos ==-1: self.list.append (value)
		elif pos > self.length(): pass
		elif pos <0:
			pos += self.length()
			self.list.insert (pos, value)
		else: self.list.insert (pos, value)

	def pop (self, item, isIndex=True):
		if isIndex: trash = self.list.pop (item)
		else:
			id= self.index (item)
			trash = self.list.pop (id)

	def copy (self):
		newList = List()
		for line in self: newList.add (line)
		return newList

	def fromText (self, word, text):
		newList = text.split (word)
		self.addList (newList)

	def toText (self, word):
		newList =""
		for item in self.list: newList = newList + word + item
		# for item in self.list: newList = newList + word + str (item)
		newList = newList.replace (word, "", 1)
		return newList

	def reverse (self):
		self.list.reverse()

	def sort (self):
		self.list.sort()

	def __lt__ (self, newList):
		return self.__str__() < newList.__str__()

	def __setitem__ (self, pos, item):
		lenList = self.length()
		if pos <0: pos += lenList
		if pos < lenList: self.list[pos] = item
		else: self.add (item)

	def __getitem__ (self, pos):
		lenList = self.length()
		if type (pos) == int:
			if pos <0: pos += lenList
			if pos > lenList or pos <0: return None
			else: return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
			newList = List()
			for l in rangeList: newList.add (self [l])
			return newList
		else: return None

	def test (self):
		self.add ('a')
		self.add ('b')
		self.addList (['c', 'd'])
		newList = List()
		newList.add ('e')
		newList.add ('f')
		self.addList (newList)
		print (self)
		print (self[2])
		print (self[1:4])

class Table (List):

	def emptyTable (self, nlin, ncol, filling=None):
		rlin= range (nlin)
		rcol= range (ncol)
		for l in rlin:
#			creer une ligne
			self.addList (List())
			for c in rcol:
#				creer une case
				self [-1].add (filling)

	def __str__ (self):
		return self.toText ('\n', '\t')

	def addTable (self, itemTable):
		# regrouper deux tables
		if type (itemTable) == Table: self.list.extend (itemTable)
		elif type (itemTable) == List: self.list.append (itemTable)
		elif type (itemTable) == list:
			newList = List()
			newList.addList (itemTable)
			self.addList (newList, pLin)

	def addLine (self, itemList, pLin =-1):
		# rajouter une ligne au tableau
		if type (itemList) == List: List.add (self, itemList, pLin)
		elif type (itemList) == list:
			newList = List()
			newList.addList (itemList)
			List.add (self, newList, pLin)

	def addItems (self, itemList, pCol=-1):
		# rajouter un élément à chaque ligne de la table
		if type (itemList)!= list: return
		elif len (itemList)!= self.length(): return
		rangitem = self.range()
		for i in rangitem: self.list [i].add (itemList [i], pCol)

	def add (self, item, pLin, pCol):
		# rajouter un élément dans le tableau
		self.list [pLin].add (item, pCol)

	def getCol (self, pCol):
		cases = List()
		for line in self.list:
			if line.length() > pCol: cases.add (line [pCol])
			else: cases.add (None)
		return cases

	def toText (self, wordLin, wordCol):
		newList = List()
		for line in self.list: newList.add (line.toText (wordCol))
		return newList.toText (wordLin)

	def fromText (self, wordLin, wordCol, text):
		newList = text.split (wordLin)
		for line in newList:
			self.addList (line.split (wordCol))

	def test (self):
		self.emptyTable (3, 4, 0)
		self.addList ([1, 2, 3, 4])
		newList = List()
		newList.addList ([5, 6, 7, 8])
		self.addList (newList)
		self.addItems ([9, 10, 11, 12, 13])
		self.addItems ([14, 15, 16, 17, 18], 2)
		print (self)
		print (self[2][2])
