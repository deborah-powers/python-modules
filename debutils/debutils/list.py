#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
def dictGetKeyByValue (dictionnary, value):
	return list (dictionnary.keys ()) [list (dictionnary.values ()).index (value) ]
def rangeNb (nb, start=0, step=1):
	rangeListTmp = range (start, nb, step)
	rangeList = List ()
	for r in rangeListTmp: rangeList.append (r)
	return rangeList
class List ():
	def __init__ (self):
		self.list = []
	def delDouble (self):
		""" transformer la liste [ a b b a c d e a f g ] en [ a b c d e f g ] """
		tmpRange = self.range ()
		tmpRange.reverse ()
		trash =0
		for w in tmpRange:
			if self.list.count (self.list [w]) >1: trash = self.list.pop (w)
	def iterate (self, function):
		rangeList = self.range ()
		newList = List ()
		for i in rangeList: newList.append (function (self.list [i]))
		return newList
	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = self.len ()
		if end <=0: end += lenList
		elif end > lenList: end = lenList
		newList = []
		while start <end:
			newList.append (start)
			start += step
		return newList
	def count (self, item):
		nb=0
		if item in self.list: nb= self.list.count (item)
		return nb
	def sortFunc (self, funcSort):
		if self.length () <2: return
		listStart = List ()
		listEnd = List ()
		item = choice (self.list)
		for l in self:
			if funcSort (item, l): listEnd.add (l)
			else: listStart.add (l)
		if listStart.length () >1: listStart.sortFunc (funcSort)
		if listEnd.length () >1: listEnd.sortFunc (funcSort)
		self.list = []
		if listStart: self.addList (listStart)
		if listEnd: self.addList (listEnd)
	def sort (self, funcSort=None):
		if sortFunc:
			from random import choice
			self.sortFunc (funcSort)
		else: self.list.sort ()
	def length (self):
		return len (self.list)
	def index (self, item):
		nb=-1
		if item in self.list: nb= self.list.index (item)
		return nb
	def __str__ (self):
		return self.toText ('n')
	def addList (self, newList):
		if type (newList) == list: self.list.extend (newList)
		elif type (newList) == List: self.list.extend (newList.list)
	def add (self, value, pos=-1):
		if pos ==-1: self.list.append (value)
		elif pos > self.len (): pass
		elif pos <0:
			pos += self.len ()
			self.list.insert (pos, value)
		else: self.list.insert (pos, value)
	def pop (self, item, isIndex=True):
		if isIndex: trash = self.list.pop (item)
		else:
			id= self.index (item)
			trash = self.list.pop (id)
	def copy (self):
		newList = List ()
		for line in self: newList.add (line)
		return newList
	def fromText (self, word, text):
		newList = text.split (word)
		self.addList (newList)
	def toText (self, word):
		newList =""
		for item in self.list: newList = newList + word + str (item)
		newList = newList.replace (word,"", 1)
		return newList
	def reverse (self):
		self.list.reverse ()
	def sort (self):
		self.list.sort ()
	def __lt__ (self, newList):
		return self.__str__ () < newList.__str__ ()
	def __setitem__ (self, pos, value):
		if pos <0: pos += self.len ()
		if pos >0 and pos < self.len (): self.list [pos] = value
		elif pos >= self.len (): self.add (value)
	def __getitem__ (self, pos):
		if type (pos) == int:
			if pos <0: pos += self.len ()
			if pos > self.len () or pos <0: return None
			else: return self.list [pos]
		else: return None
	def __getitem__vb (self, pos):
		if type (pos) == int:
			if pos <0: pos += self.len ()
			if pos > self.len () or pos <0: return None
			else: return self.list [pos]
		elif type (pos) == slice:
			posIndex = pos.indices (self.len ())
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
			newList = List ()
			for l in rangeList: newList.add (self [l])
			return newList
		else: return None
	def len (self):
		return len (self.list)
	def test (self):
		self.add ('a')
		self.add ('b')
		self.addList (['c', 'd'])
		newList = List ()
		newList.add ('e')
		newList.add ('f')
		self.addList (newList)
		print (self)
		print (self [2])
class Table (List):
	def emptyTable (self, nlin, ncol, filling=None):
		rlin= range (nlin)
		rcol= range (ncol)
		for l in rlin:
#			creer une ligne
			self.addList (List ())
			for c in rcol:
#				creer une case
				self [-1].add (filling)
	def __str__ (self):
		return self.toText ('n', 't')
	def addTable (self, itemTable):
		# regrouper deux tables
		if type (itemTable) == Table: self.list.extend (itemTable)
		elif type (itemTable) == List: self.list.append (itemTable)
		elif type (itemTable) == list:
			newList = List ()
			newList.addList (itemTable)
			self.addList (newList, pLin)
	def addLine (self, itemList, pLin =-1):
		# rajouter une ligne au tableau
		if type (itemList) == List: List.add (self, itemList, pLin)
		elif type (itemList) == list:
			newList = List ()
			newList.addList (itemList)
			List.add (self, newList, pLin)
	def addItems (self, itemList, pCol=-1):
		# rajouter un élément à chaque ligne de la table
		if type (itemList)!= list: return
		elif len (itemList)!= self.len (): return
		rangitem = self.range ()
		for i in rangitem: self.list [i].add (itemList [i], pCol)
	def add (self, item, pLin, pCol):
		# rajouter un élément dans le tableau
		self.list [pLin].add (item, pCol)
	def getCol (self, pCol):
		cases = List ()
		for line in self.list:
			if line.len () > pCol: cases.add (line [pCol])
			else: cases.add (None)
		return cases
	def toText (self, wordLin, wordCol):
		newList = List ()
		for line in self.list: newList.add (line.toText (wordCol))
		return newList.toText (wordLin)
	def fromText (self, wordLin, wordCol, text):
		newList = text.split (wordLin)
		for line in newList:
			self.addList (line.split (wordCol))
	def test (self):
		self.emptyTable (3, 4, 0)
		self.addList ([1, 2, 3, 4])
		newList = List ()
		newList.addList ([5, 6, 7, 8])
		self.addList (newList)
		self.addItems ([9, 10, 11, 12, 13])
		self.addItems ([14, 15, 16, 17, 18], 2)
		print (self)
		print (self [2] [2])
class Dico ():
	def __init__ (self):
		self.dico = {}
		self.keys = []
	def getKeys (self):
		for item in self.dico.keys: self.keys.append (item)
	def __str__ (self):
		return self.toText ('n', 't')
	def fromText (self, wordLin, wordCol, text):
		newList = text.split (wordLin)
		rangeList = range (len (newList))
		for l in rangeList:
			tmpValue = newList [l].split (wordCol)
			self [tmpValue [0] ] = tmpValue [1]
	def toText (self, wordLin, wordCol):
		newList = []
		for key in self.keys: newList.append (key + wordCol + str (self.dico [key]))
		return wordLin.join (newList)
	def delete (self, key):
		self.dico.pop (key)
		pos = self.keys.index (key)
		self.keys.pop (pos)
	def __setitem__ (self, key, value):
		self.dico [key] = value
		if key not in self.keys: self.keys.append (key)
	def __getitem__ (self, key):
		if key in self.keys: return self.dico [key]
		else: return None
	def test (self):
		self ['a'] = 'coucou'
		self ['b'] = 'tvb ?'
		print (self)
		print (self ['c'])
class DicoTabPerso (Dico):
	def toText (self, wordLin, wordCol):
		newList = []
		tmpText =""
		for key in self.keys:
			tmpText =""
			for item in self.dico [key]: tmpText = tmpText + wordCol + item
			newList.append (key + tmpText)
		return wordLin.join (newList)
	def __setitem__ (self, key, newList):
		if type (newList) == List:
			self.dico [key] = newList
			if key not in self.keys: self.keys.append (key)
		elif type (newList) == list:
			tmpList = List ()
			tmpList.addList (newList)
			self.dico [key] = tmpList
			if key not in self.keys: self.keys.append (key)
		else: return
	def test (self):
		self ['a'] = 'coucou'
		tmpList = List ()
		tmpList.addList ([ 'a', 'b', 'c', 'd' ])
		self ['b'] = tmpList
		print (self)
		print (self ['c'])