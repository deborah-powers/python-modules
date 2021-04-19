#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple import File, Article
help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python3 fileClass.py fichier tag (fichierB)
les valeurs de tag
	maj: rajouter les majuscules dans un texte
	mef: mettre en forme un texte utilisant ma mise en forme spécifique
	cpr: comparer deux fichiers ligne à ligne
	md: transformer mon fichier en md
"""
nbArg = len (argv)
if nbArg <3: print (help)
elif argv[2] == 'testFile':
	filePerso = File()
	filePerso.test()
elif argv[2] == 'testArtic':
	filePerso = Article()
	filePerso.test()
elif argv[2] =='tmp':
	fileTxt = Article()
	fileTxt.tmp()
elif nbArg ==4 and argv[2][:3] == 'cpr':
	fpA = File (argv[1])
	fpB = File (argv[3])
	if argv[2] == 'cprs': fpA.compare (fpB, 'lsort')
	else: fpA.compare (fpB)
elif nbArg >2:
	filePerso = File (argv[1])
	filePerso.fromFile()
	if argv[2] =='maj': filePerso.clean()
	elif argv[2] =='mef': filePerso.shape()
	# rajouter un argument afin d'empêcher l'écriture des majuscules
	if nbArg <4: filePerso.upperCase()
	filePerso.toFile()
# le nom du fichier n'a pas ete donne
else: print (help)