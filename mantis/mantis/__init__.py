#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from mantis.object import MantisFile
help ="""
créer une fiche mantis perso.
python mantis.py cdm 29700 message (type / numint)
type vaut evo, ddt, ano
si un numéro de mantis interne est précisé à la place, le type est automatiquement fixé à ano.
"""

if len (argv) >3:
	module = argv[1]
	numext = argv[2]
	message = argv[3]
	numint ='0'
	type = '?'
	if len (argv) >4:
		type = argv[4]
		if type not in types:
			type = 'ano'
			numint = argv[4]
	fileMantis = Mantisfile (numext, message, module, numint, type)
	fileMantis.createFile()
# il manque des données
else: print (help)