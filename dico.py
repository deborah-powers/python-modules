#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import fileClass as fl
import textClass as tx
from listClass import ListPerso, TablePerso

suffix =( 'ations', 'itions', 'trices', 'ables', 'aires', 'amant', 'ament', 'ances', 'aient', 'ation', 'asmes', 'elles', 'ement', 'ences', 'esses', 'ettes', 'euses', 'ibles', 'ières', 'iques', 'ismes', 'ition', 'tions', 'trice', 'able', 'ages', 'aire', 'ance', 'asme', 'bles', 'eaux', 'elle', 'ence', 'esse', 'ères', 'ette', 'eurs', 'euse', 'ible', 'ière', 'iers', 'ions', 'ique', 'isme', 'ités', 'mant', 'ment', 'ques', 'sses', 'tion', 'age', 'ais', 'ait', 'ant', 'aux', 'ble', 'eau', 'ent', 'ère', 'eur', 'ées', 'ier', 'ion', 'ité', 'nes', 'ont', 'ons', 'que', 'sse', 'ai', 'al', 'au', 'er', 'es', 'et', 'ez', 'ée', 'ne', 'a', 'e', 'é', 's', 't', 'x')
prefix =( 'imm', 'inn', 'pré', 'dé', 'im', 'in', 're', 'ré', 'sur' )
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
				lenLine = wordTable[l].length()
				while d< lenLine:
					if d!=c and wordTable[l][c] in wordTable[l][d]:
						print (wordTable[l][c], wordTable[l][d])
						trash = wordTable[l].pop (c)
						d+= lenLine
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
	for p in prefix: fileTstObj.replace (' '+p, ' ')
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
else:
	fileTstName = 'a/education/' + fileTstName + '.txt'
	extractWord (fileTstName)