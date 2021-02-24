#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.file import File, Article
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
if len (argv) <3: print (help)
elif argv[2] =='tmp':
	fileTxt = Article()
	fileTxt.tmp()
elif len (argv) ==4 and argv[2][:3] == 'cpr':
	fpA = File (argv[1])
	fpB = File (argv[3])
	if argv[2] == 'cprs': fpA.compare (fpB, 'lsort')
	else: fpA.compare (fpB)
elif len (argv) ==3:
	filePerso = File (argv[1])
	filePerso.fromFile()
	if argv[2] =='maj': filePerso.clean()
	elif argv[2] =='mef': filePerso.shape()
	elif argv[2] =='lis': filePerso.toLiseuse()
	elif argv[2] =='md': filePerso.toMd()
	filePerso.toFile()
elif argv[2] == 'testFile':
	filePerso = File()
	filePerso.test()
elif argv[2] == 'testArtic':
	filePerso = Article()
	filePerso.test()
# le nom du fichier n'a pas ete donne
else: print (help)