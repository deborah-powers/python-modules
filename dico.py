#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

def dictGetKeyByValue (dictionnary, value):
	return list (dictionnary.keys()) [list (dictionnary.values()).index (value) ]

class Dico():
	def __init__ (self):
		self.dico = {}
		self.keys = []

	def getKeys (self):
		for item in self.dico.keys: self.keys.append (item)

	def __str__ (self):
		return self.toText ('\n', '\t')

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
			tmpList = List()
			tmpList.addList (newList)
			self.dico [key] = tmpList
			if key not in self.keys: self.keys.append (key)
		else: return

	def test (self):
		self ['a'] = 'coucou'
		tmpList = List()
		tmpList.addList ([ 'a', 'b', 'c', 'd' ])
		self ['b'] = tmpList
		print (self)
		print (self ['c'])