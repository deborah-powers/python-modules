#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import fileClass as fl
import textClass as tx
from listClass import ListPerso, TablePerso

fileTstName_va = "a/education/l'éducation des enfants.txt"
fileTstName_vb = "m/mantis 29724.txt"

suffix =[ 'ations', 'ables', 'aires', 'amant', 'ament', 'ances', 'ation', 'elles', 'ement', 'ences', 'ettes', 'euses', 'ibles', 'iques', 'tions', 'able', 'aire', 'ance', 'bles', 'eaux', 'elle', 'ence', 'ette', 'eurs', 'euse', 'ible', 'iers', 'ions', 'ique', 'mant', 'ment', 'ques', 'tion', 'ais', 'ait', 'ant', 'aux', 'ble', 'eau', 'ent', 'eur', 'ées', 'ier', 'ion', 'nes', 'ont', 'ons', 'que', 'ai', 'al', 'au', 'er', 'es', 'et', 'ez', 'ée', 'ne', 'e', 'é', 's', 'x']
newPoints = "-'()/_\\\"\n\t<>[](){}|%#$@=+*°"
fileRefName = 'b/dico.txt'

def sortRef():
	fileRefObj = fl.FilePerso (fileRefName)
	fileRefObj.fromFile()
	wordTable = TablePerso()
	wordTable.fromText ('\n', ' ', fileRefObj.text)
	wordRange = wordTable.range()
	fileRefObj.text =""
	trash = None
	for l in wordRange:
		wordTable[l].sort()
		linRange = wordTable[l].range()
		linRange.reverse()
		for c in linRange:
			if wordTable[l].count (wordTable[l][c]) >1: trash = wordTable[l].pop (c)
			else:
				d=0
				while d<c:
					if wordTable[l][c] in wordTable[l][d]:
						trash = wordTable[l].pop (c)
						d+=c
					d+=1
	fileRefObj.text = wordTable.toText ('\n', ' ')
	fileRefObj.toFile()

def extractWord (fileTstName):
	# récupérer le nouveau texte
	fileTstObj = fl.FilePerso (fileTstName)
	fileTstObj.fromFile()
	fileTstObj.clean()
	numbers = '0123456789'
	for n in numbers: fileTstObj.replace (n)
	fileTstObj.text = fileTstObj.text +' '
	for p in tx.pointsEnd: fileTstObj.replace (p,' ')
	for p in newPoints: fileTstObj.replace (p,' ')
	for p in suffix: fileTstObj.replace (p+' ', ' ')
	while '  ' in fileTstObj.text: fileTstObj.replace ('  ',' ')
	fileTstObj.text = fileTstObj.text.lower()
	# lister ses mots
	wordList = ListPerso()
	wordList.fromText (' ', fileTstObj.text)
	rangeWord = wordList.range()
	rangeWord.reverse()
	for w in rangeWord:
		if len (wordList[w]) >15 or len (wordList[w]) <3: trash = wordList.pop (w)
		elif wordList.count (wordList[w]) >1: trash = wordList.pop (w)
	wordList.sort()
	# récupérer la liste de mots connus
	fileRefObj = fl.FilePerso (fileRefName)
	fileRefObj.fromFile()
	fileRefObj.text = fileRefObj.text +'\n'
	for word in wordList:
		if word not in fileRefObj.text: fileRefObj.text = fileRefObj.text +' '+ word
	fileRefObj.replace ('\n ', '\n')
	fileRefObj.toFile()

fileTstName = argv[1]
if fileTstName == 'tri': sortRef()
else: extractWord (fileTstName)