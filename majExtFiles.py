#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileJs import FileJs

# comparer les fichiers copiés entre les extensions et site-dp

textFctFiles =[
	's/library-js\\textFct.js',
	'w/all-md-perso\\textFct.js',
]
htmlFctFiles =[
	's/library-js\\htmlFct.js',
	'w/all-md-perso\\htmlFct.js',
]

def compareFiles (fileNameList):
	fileRange = range (len (fileNameList))
	fileList =[]
	# ouvrir les fichiers
	for f in fileRange:
		fileList.append (FileJs (fileNameList[f]))
		fileList[-1].read()
		fileList[-1].toPath()
	# faire les comparaisons deux à deux
	for f in fileRange[1:]:
		fileList[f].title = fileList[f].title +" "+ str(f)
		fileList[0].comparer (fileList[f])

compareFiles (htmlFctFiles)
