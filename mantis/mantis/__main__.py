#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from mantis import MantisFile
import debutils.logger as logger

help ="""ce script fait deux actions
a- convertir une fiche au format html
	python mantisAction.py html 345
b- créer une fiche mantis perso
	python mantisAction.py cdm 29700 message (type / numint)
	python mantisAction.py ref.html (type)
type vaut evo, ddt, ano
si un numéro de mantis interne est précisé à la place, le type est automatiquement fixé à ano.
"""

nbArg = len (argv)
"""
# convertir une fiche au format html
elif argv[1] == 'html':
	from debutils.html import FileHtml
	fileName = 'm/mantis %s.txt' % argv[2]
	fhtml = FileHtml()
	fhtml.fromFileName (fileName)
"""
if nbArg <3: print (help)
# créer une fiche mantis perso
# à partir d'un fichier html
elif argv[1][-5:] == '.html':
	fileMantis = MantisFile()
	fileMantis.type = 'ano'
	if nbArg >2: fileMantis.type = argv[2]
	fileMantis.fromHtml (argv[1])
# à partir de rien
elif nbArg >3:
	module = argv[1]
	numext = argv[2]
	message = argv[3]
	numint ='0'
	type = '?'
	if nbArg >4:
		if argv[4][0] in '0123456789': numint = argv[4]
		else: type = argv[4]
	fileMantis = MantisFile (numext, message, module, numint, type)
	fileMantis.createFile()
# il manque des données
else: print (help)

