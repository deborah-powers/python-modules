#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileJs import FileJs

# comparer les fichiers copiés entre les extensions et site-dp

textFctFiles =[
	's/library-js\\textFct.js',
	'w/all-md-perso-va\\textFct 2025.js',
	'w/all-md-perso-va\\textFct 2023.js'
]
htmlFctFiles =[
	's/library-js\\htmlFct.js',
	'w/all-md-perso-va\\htmlFct 2025.js',
	'w/all-md-perso-va\\htmlFct 2023.js'
]

def compareFiles (fileNameList):
	fileRange = range (len (fileNameList))
	fileList =[]
	# ouvrir les fichiers
	for f in fileRange:
		fileList.append (FileJs (fileNameList[f]))
		fileList[-1].read()
		fileList[-1].title = fileList[-1].title +" "+ str(f)
		fileList[-1].toPath()
	# faire les comparaisons deux à deux
	for f in fileRange[:-1]:
		for g in fileRange[f+1:]: fileList[f].comparer (fileList[g])

compareFiles (textFctFiles)
