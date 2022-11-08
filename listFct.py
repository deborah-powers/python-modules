#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from random import choice

def range (liste, start=0, end=0, step=1):
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

def iterate (liste, function):
	rangeList = range (liste)
	newList =[]
	for i in rangeList: newList.append (function (liste[i]))
	return newList

def sortFunc (liste, funcSort):
	if len (liste) <2: return liste
	listStart =[]
	listEnd =[]
	item = choice (liste)
	for l in liste:
		if funcSort (item, l): listEnd.append (l)
		else: listStart.append (l)
	if len (listStart) >1: listStart.sortFunc (funcSort)
	if len (listEnd) >1: listEnd.sortFunc (funcSort)
	newList =[]
	if listStart: newList.extend (listStart)
	if listEnd: newList.extend (listEnd)
	return newList

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

