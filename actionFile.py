#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from classFile import File

help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python3 fileClass.py fichier tag (fichierB)
les valeurs de tag
	clean (reset upper):	nettoyer le texte. modifier ou pas la casse.
	mef (reset upper):	mettre en forme un texte utilisant ma mise en forme spécifique.
"""
nbArg = len (argv)
if nbArg <3: print (help)
elif nbArg >2:
	filePerso = File (argv[1])
	filePerso.read()
	if 'clean' in argv: filePerso.text = filePerso.text.clean()
	elif 'mef' in argv: filePerso.text = filePerso.text.shape()
	# rajouter un argument afin d'empêcher l'écriture des majuscules
	if 'reset' in argv and 'upper' in argv: filePerso.text = filePerso.text.upperCase ('upper reset')
	elif 'reset' in argv: filePerso.text = filePerso.text.upperCase ('reset')
	elif 'upper' in argv: filePerso.text = filePerso.text.upperCase ('upper')
	filePerso.write()
# le nom du fichier n'a pas ete donne
else: print (help)