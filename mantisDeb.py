#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
help ="""ce script fait deux actions
a- convertir une fiche au format html
	python mantisAction.py html 345
b- créer une fiche mantis perso
	python mantisAction.py cdm 29700 message (type / numint)
type vaut evo, ddt, ano
si un numéro de mantis interne est précisé à la place, le type est automatiquement fixé à ano.
"""
nbArg = len (argv)
if nbArg <3: print (help)
# convertir une fiche au format html
elif argv [1] == 'html':
	from debutils.html import FileHtml
	fileName = 'm/mantis %s.txt' % argv [2]
	fhtml = FileHtml ()
	fhtml.fromFileName (fileName)
# créer une fiche mantis perso
elif nbArg >3:
	from mantis import MantisFile
	module = argv [1]
	numext = argv [2]
	message = argv [3]
	numint ='0'
	type = ' ?'
	if len (argv) >4:
		type = argv [4]
		if type not in types:
			type = 'ano'
			numint = argv [4]
	fileMantis = Mantisfile (numext, message, module, numint, type)
	fileMantis.createFile ()
# il manque des données
else: print (help)