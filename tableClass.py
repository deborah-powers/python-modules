#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
help ="""
ce script peut etre appele dans d'autres scripts
"""
def dictGetKeyByValue (dictionnary, value):
	return list(dictionnary.keys())[list(dictionnary.values()).index(value)]

def rangeNb (nb, start=0, step=1):
	rangeListTmp = range (start, nb, step)
	rangeList = ListPerso()
	for r in rangeListTmp: rangeList.append (r)
	return rangeList

class ListPerso():
	def __init__(self):
		self.list =[]

	def delDuplicates (self):
		""" transformer la liste [ a b b a c d e a f g ] en [ a b c d e f g ] """
		rangeList = self.range()
		rangeList.reverse()
		for i in rangeList:
			nb= self.count (self.list[i])
			if nb>1: self.list.pop(i)

	def iterate (self, function):
		rangeList = self.range()
		newList = ListPerso()
		for i in rangeList: newList.append (function (self.list[i]))
		return newList

	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = self.length()
		if end <=0: end += lenList
		elif end > lenList: end = lenList
		newList = ListPerso()
		while start <end:
			newList.add (start)
			start += step
		return newList

	def __str__(self):
		return self.toText ('\n')

	def addList (self, newList):
		if type (newList) == list: self.list.extend (newList)
		elif type (newList) == ListPerso: self.list.extend (newList.list)

	def add (self, value, pos=-1):
		if pos ==-1: self.list.append (value)
		elif pos > self.length(): pass
		elif pos <0:
			pos += self.length()
			self.list.insert (pos, value)
		else: self.list.insert (pos, value)

	def fromText (self, word, text):
		newList = text.split (word)
		self.addList (newList)

	def toText (self, word):
		newList =[]
		for item in self.list: newList.append (str (item))
		return word.join (newList)

	def reverse (self):
		self.list.reverse()
	def sort (self):
		self.list.sort()

	def __setitem__ (self, pos, value):
		if pos <0: pos += self.length()
		if pos >= self.length(): self.add (value)
		elif pos >=0: self.add (value, pos)

	def __getitem__ (self, pos):
		if pos <0: pos += self.length()
		if pos > self.length() or pos <0: return None
		else: return self.list[pos]

	def length (self):
		return len (self.list)

	def test (self):
		self.add ('a')
		self.add ('b')
		self.addList (['c','d'])
		newList = ListPerso()
		newList.add ('e')
		newList.add ('f')
		self.addList (newList)
		print (self)
		print (self[2])

class TablePerso (ListPerso):
	def emptyTable (self, nlin, ncol, filling=None):
		rlin= range (nlin)
		rcol= range (ncol)
		for l in rlin:
#			creer une ligne
			self.addList (ListPerso())
			for c in rcol:
#				creer une case
				self[-1].add (filling)

	def __str__ (self):
		return self.toText ('\n', '\t')

	def addTable (self, itemTable):
		if type (itemTable) == TablePerso: self.list.extend (itemTable)
		elif type (itemTable) == ListPerso: self.list.append (itemTable)
		elif type (itemTable) == list:
			newList = listPerso()
			newList.addList (itemTable)
			self.addList (newList, pLin)

	def addList (self, itemList, pLin =-1):
		if type (itemList) == ListPerso: ListPerso.add (self, itemList, pLin)
		elif type (itemList) == list:
			newList = ListPerso()
			newList.addList (itemList)
			ListPerso.add (self, newList, pLin)

	def addItems (self, itemList, pCol=-1):
		if type (itemList) != list: return
		elif len (itemList) != self.length(): return
		rangitem = self.range()
		for i in rangitem: self.list[i].add (itemList[i], pCol)

	def add (self, item, pLin, pCol):
		self.list[pLin].add (item, pCol)

	def toText (self, wordLin, wordCol):
		newList = ListPerso()
		for line in self: newList.add (line.toText (wordCol))
		return newList.toText (wordLin)

	def fromText (self, wordLin, wordCol, text):
		newList = text.split (wordLin)
		for line in newList:
			self.addList (line.fromText (wordCol))

	def test (self):
		self.emptyTable (3,4,0)
		self.addList ([1,2,3,4])
		newList = ListPerso()
		newList.addList ([5,6,7,8])
		self.addList (newList)
		self.addItems ([9,10,11,12,13])
		self.addItems ([14,15,16,17,18], 2)
		print (self)
		print (self[2][2])

class DicoPerso():
	def __init__(self):
		self.dico ={}
		self.keys =[]

	def getKeys (self):
		for item in self.dico.keys: self.keys.append (item)

	def __str__ (self):
		return self.toText ('\n', '\t')

	def fromText (self, wordLin, wordCol, text):
		newList = text.split (wordLin)
		rangeList = range (len (newList))
		for l in rangeList:
			tmpValue = newList[l].split (wordCol)
			self[tmpValue[0]] = tmpValue[1]

	def toText (self, wordLin, wordCol):
		newList =[]
		for key in self.keys: newList.append (key + wordCol + str (self.dico[key]))
		return wordLin.join (newList)

	def delete (self, key):
		self.dico.pop (key)
		pos = self.keys.index (key)
		self.keys.pop (pos)

	def __setitem__ (self, key, value):
		self.dico[key] = value
		if key not in self.keys: self.keys.append (key)

	def __getitem__ (self, key):
		if key in self.keys: return self.dico[key]
		else: return None

	def test (self):
		self['a'] = 'coucou'
		self['b'] = 'tvb?'
		print (self)
		print (self['c'])

class DicoTabPerso (DicoPerso):

	def toText (self, wordLin, wordCol):
		newList =[]
		tmpText =""
		for key in self.keys:
			tmpText =""
			for item in self.dico[key]: tmpText = tmpText + wordCol + item
			newList.append (key + tmpText)
		return wordLin.join (newList)

	def __setitem__ (self, key, newList):
		if type (newList) == ListPerso:
			self.dico[key] = newList
			if key not in self.keys: self.keys.append (key)
		elif type (newList) == list:
			tmpList = ListPerso()
			tmpList.addList (newList)
			self.dico[key] = tmpList
			if key not in self.keys: self.keys.append (key)
		else: return

	def test (self):
		self['a'] = 'coucou'
		tmpList = ListPerso()
		tmpList.addList ([ 'a','b','c','d' ])
		self['b'] = tmpList
		print (self)
		print (self['c'])


