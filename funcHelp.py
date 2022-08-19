#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from classFile import File

wordImport = (('import ', 7), ('from ', 5))
wordFunction = (('class ', 6), ('def ', 4), ('\t""" ', 5), ('\treturn', 7), ('\tdef ', 5), ('\t\t""" ', 6), ('\t\treturn', 8))
filePython = File ('b/python/\t.py')
fileHelp = File ('b/\t.txt')

def printHelp (pythonFile):
	filePython.title = pythonFile
	filePython.shortcut()
	filePython.toPath()
	fileHelp.title = 'aide '+ pythonFile
	fileHelp.shortcut()
	fileHelp.toPath()
#	obtenir le code python
	filePython.read()
	while '\n\n' in filePython.text: filePython.text = filePython.text.replace ('\n\n', '\n')
	listHelp = []
	listHelpRaw = filePython.text.split ('\n')
	# récupérer l'aide
	if '\nhelp' in filePython.text:
		posS = filePython.text.find ('\nhelp') +10
		posE = filePython.text.find ('"', posS)
		helpMessage = filePython.text [:posE]
		posS = helpMessage.rfind ('"') +1
		helpMessage = helpMessage [posS:]
		helpMessage = helpMessage.strip ()
		listHelp.append ('____________ Message ____________\n')
		listHelp.append (helpMessage)
	# récupérer les imports
	listHelp.append ('\n____________ imports ____________\n')
	for line in listHelpRaw:
		for word, lenght in wordImport:
			if word == line [:lenght]:
				listHelp.append (line)
				break
	# récupérer les fonctions
	listHelp.append ('\n____________ Fonctions ____________\n')
	for line in listHelpRaw:
		for word, lenght in wordFunction:
			if word == line [:lenght]:
				listHelp.append (line)
				break
	fileHelp.text = '\n'.join (listHelp)
	fileHelp.text = fileHelp.text.replace ('\nclass', '\n\nclass')
	fileHelp.text = fileHelp.text.replace ('\n\n\n', '\n\n')
	fileHelp.write()
	print ('lire "'+ fileHelp.title +'" sur le bureau')

help = """
préciser le chemin du dossier python dans ce fichier.
par défaut, il vaut... /bureau/python
utilisation:
	printHelp (pythonFile)

j'ai /bureau/python/pythonFile.py sur mon ordi.
"""
if __name__ == 'main':
	if len (argv) >1: printHelp (argv [1])
	else: print (help)