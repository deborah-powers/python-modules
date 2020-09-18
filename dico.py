#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import fileClass as fl
import textClass as tx
from listClass import ListPerso

fileTstName_va = "a/education/l'éducation des enfants.txt"
fileTstName = "b/articles\\articles\\je peux y arriver.txt"
suffix =[ 'amant', 'ament', 'elles', 'ement', 'ettes', 'euses', 'elle', 'ette', 'eurs', 'euse', 'mant', 'ment', 'eur', 'er', 'es', 'et', 'e', 's', 'x']
newPoints = "-'()/\\\""
fileRefName = 'b/dico.txt'

def sortRef (fileRefObj=None):
	if fileRefObj == None:
		fileRefObj = fl.FilePerso (fileRefName)
		fileRefObj.fromFile()
	tmpTab = fileRefObj.text.split ('\n')
	tmpRange = range (len (tmpTab))
	fileRefObj.text =""
	for l in tmpRange:
		tmpList = tmpTab[l].split (' ')
		tmpList.sort()
		fileRefObj.text = fileRefObj.text +' '.join (tmpList) +'\n'
	fileRefObj.toFile()

fileTstObj = fl.FilePerso (fileTstName)
fileTstObj.fromFile()
fileTstObj.clean()
for p in tx.pointsEnd: fileTstObj.replace (p,' ')
for p in newPoints: fileTstObj.replace (p,' ')
for p in suffix: fileTstObj.replace (p, ' ')
while '  ' in fileTstObj.text: fileTstObj.replace ('  ',' ')
fileTstObj.text = fileTstObj.text.lower()

wordList = ListPerso()
wordList.fromText (fileTstObj.text, ' ')
rangeWord = wordList.range()
rangeWord.reverse()
for w in rangeWord:
	if wordList.count (wordList[w]) >1: trash = wordList.pop (w)
wordList.sort()

fileRefObj = fl.FilePerso (fileRefName)
fileRefObj.fromFile()

for word in wordList:
	if word not in fileRefObj.text: fileRefObj.text = fileRefObj.text +' '+ word

sortRef (fileRefObj)



