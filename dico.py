#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import fileClass as fl
import textClass as tx
from listClass import ListPerso

fileTstName_va = "a/education/l'éducation des enfants.txt"
fileTstName_vb = "m/mantis 29724.txt"

suffix =[ 'ations', 'ables', 'aires', 'amant', 'ament', 'ation', 'elles', 'ement', 'ettes', 'euses', 'ibles', 'tions', 'able', 'aire', 'bles', 'elle', 'ette', 'eurs', 'euse', 'ible', 'ions', 'iers', 'mant', 'ment', 'tion', 'ant', 'aux', 'ble', 'ent', 'eur', 'ées', 'ier', 'ion', 'ont', 'ons', 'al', 'au', 'er', 'es', 'et', 'ée', 'e', 'é', 's', 'x']
newPoints = "-'()/_\\\"\n\t<>[](){}|%#$"
fileRefName = 'b/dico.txt'

def sortRef():
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

def extractWord (fileTstName):
	# récupérer le nouveau texte
	fileTstObj = fl.FilePerso (fileTstName)
	fileTstObj.fromFile()
	fileTstObj.clean()
	for p in tx.pointsEnd: fileTstObj.replace (p,' ')
	for p in newPoints: fileTstObj.replace (p,' ')
	for p in suffix: fileTstObj.replace (p, ' ')
	while '  ' in fileTstObj.text: fileTstObj.replace ('  ',' ')
	fileTstObj.text = fileTstObj.text.lower()
	# lister ses mots
	wordList = ListPerso()
	wordList.fromText (' ', fileTstObj.text)
	rangeWord = wordList.range()
	rangeWord.reverse()
	for w in rangeWord:
		if wordList.count (wordList[w]) >1: trash = wordList.pop (w)
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