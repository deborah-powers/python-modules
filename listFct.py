#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from random import choice

def rangeListVb (liste, start=0, end=0, step=1):
	# end peut valoir -1
	lenList = len (liste)
	if lenList ==0: return []
	while end <=0: end += lenList
	if end > lenList: end = lenList
	rangeLst = None
	if start > end: rangeLst = reversed (range (end, start, step))
	newList =[]
	while start <end:
		newList.append (start)
		start += step
	return newList

def rangeList (liste, start=0, end=0, step=1):
	# end peut valoir -1
	lenList = len (liste)
	if lenList ==0: return []
	while end <=0: end += lenList
	if end > lenList: end = lenList
	newList =[]
	while start <end:
		newList.append (start)
		start += step
	return newList

def deleteDoublons (liste):
	rangeLst = rangeList (liste)
	rangeLst.reverse()
	for l in rangeLst:
		if liste.count (liste[l]) >1: trash = liste.pop (l)
	return liste

def iterate (liste, function):
	rangeLst = rangeList (liste)
	newList =[]
	for i in rangeLst: newList.append (function (liste[i]))
	return newList

def sortFunc (liste, funcSort):
	if len (liste) <2: return liste
	listStart =[]
	listEnd =[]
	item = choice (liste)
	for l in liste:
		if funcSort (item, l): listEnd.append (l)
		else: listStart.append (l)
	if len (listStart) >1: sortFunc (listStart, funcSort)
	if len (listEnd) >1: sortFunc (listEnd, funcSort)
	newList =[]
	if listStart: newList.extend (listStart)
	if listEnd: newList.extend (listEnd)
	return newList

def comparer (listA, listB):
	if len (listA) != len (listB): print ('les données sont de taille différente')
	listCommon =[]
	listA.sort()
	listB.sort()
	rangeA = rangeList (listA)
	bd =0
	for a in rangeA:
		if listA[a] in listB[bd:]:
			bf = listB.index (listA[a], bd)
			while bd < bf:
				listCommon.append ((listB[bd], 'b'))
				bd +=1
			# listCommon.append ((listA[a], 'c'))
			bd +=1
		else: listCommon.append ((listA[a], 'a'))
	rangeB = rangeList (listB, bd)
	for b in rangeB: listCommon.append ((listB[b], 'b'))
	return listCommon

def copy (liste):
	newList =[]
	newList.extend (liste)
	return newList

def fromText (text, word):
	newList = text.split (word)
	return newList

def toText (liste, word):
	newList =""
	for item in liste: newList = newList + word + item
	newList = newList.replace (word, "", 1)
	return newList

def toTextList (liste):
	newList =[]
	for item in liste: newList.append (str (item))
	return newList

def col (liste, colId):
	# pour les tableaux
	newList =[]
	for line in liste:
		if len (line) > colId: newList.append (line[colId])
		else: newList.append (None)
	return newList

def testIterate (text):
	return 'e '+ text

def test():
	liste =[ 'a', 'b', 'c', 'd', 'e']
	text = toText (liste, ' ')
	liste = fromText (text, ' ')
	print ('toText\t', text)
	print ('fromText\t', liste)
	liste =[ 1,3,4]
	liste = toTextList (liste)
	print ('toTextList\t', liste)
	liste = iterate (liste, testIterate)
	print ('iterate\t', liste)

class ListText():
	def init (self, sep='\n'):
		self.list =[]
		self.sep = sep
		self.range =[]
		self.lenght =0
		self.rangeInit()

	def rangeInit (self):
		self.range =[]
		self.lenght = len (self.list)
		if self.lenght >0:
			r=0
			while r< self.lenght: self.range.append (r)

	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		if self.lenght ==0: return []
		while end <=0: end += self.lenght
		if end > self.lenght: end = self.lenght
		newList =[]
		while start <end:
			newList.append (start)
			start += step
		return newList

	def append (item):
		self.list.append (item)
		self.lenght +=1
		self.range.append (self.range[-1] +1)

	def pop (pos):
		trash = self.list.pop (pos)
		self.lenght -=1
		self.range.pop()

	def iterate (self, function):
		newList = ListText()
		for i in self.range: newList.append (function (liste[i]))
		return newList

	def __str__ (self):
		r=1
		infos = self.list[0]
		while len (infos) < 200 or r< self.lenght:
			infos = infos + self.sep + self.list[r]
			r+=1
		infos = 'liste de %d lignes, séparées par: %s\n' % (self.lenght, self.sep) + infos
		return infos

	def toText (self):
		return self.sep.join (self.list)

	def fromText (self, text):
		if not text: return
		while self.sep + self.sep in text: text = text.replace (self.sep + self.sep, self.sep)
		self.list = text.split (self.sep)
		self.rangeInit()

