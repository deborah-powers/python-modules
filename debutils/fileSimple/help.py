#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileSimple import File

wordImport = (('import ', 7), ('from ', 5))
wordFunction = (('class ', 6), ('def ', 4), ('\t""" ', 5), ('\treturn', 7), ('\tdef ', 5), ('\t\t""" ', 6), ('\t\treturn', 8))
filePython = File ()
filePython.path = 'b/python'
filePython.extension = 'py'
fileHelp = File ()
fileHelp.path = 'b/'
fileHelp.extension = 'txt'

def printHelp (pythonFile):
#	obtenir le code python
	if '/' in pythonFile:
		end = pythonFile.rfind ('/') +1
		filePython.path += pythonFile [:end]
		pythonFile = pythonFile [end:]
	filePython.title = pythonFile
	filePython.fileFromData ()
	filePython.fromFile ()
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
	fileHelp.title = 'aide '+ filePython.title
	fileHelp.replace ('\n\n\n', '\n\n')
	fileHelp.toFile ()
	print ('lire "'+ fileHelp.title +'" sur le bureau')
"""
ancienne méthode
from sys import argv
if __\name__ == '__main__': pass
elif len (argv) >1: printHelp (argv [1])
else: print ("entrez le nom du script à analyser")
"""
help = """
préciser le chemin du dossier python dans ce fichier.
par défaut, il vaut... /bureau/python
utilisation:
	printHelp (pythonFile)
	printHelp ('debutils/debutils/text.py')
"""
print (help)