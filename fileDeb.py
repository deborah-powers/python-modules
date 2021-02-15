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
if len (argv) <2: print (help)
elif argv [1] =='tmp':
	fileTxt = Article ()
	fileTxt.tmp ()
elif len (argv) ==4 and argv [1] [:3] == 'cpr':
	fpA = File (argv [2])
	fpB = File (argv [3])
	if argv [1] == 'cprs': fpA.compare (fpB, 'lsort')
	else: fpA.compare (fpB)
elif len (argv) ==3:
	filePerso = File (argv [2])
	filePerso.fromFile ()
	if argv [1] =='maj': filePerso.clean ()
	elif argv [1] =='mef': filePerso.shape ()
	elif argv [1] =='lis': filePerso.toLiseuse ()
	elif argv [1] =='md': filePerso.toMd ()
	filePerso.toFile ()
elif argv [1] == 'testFile':
	filePerso = File ()
	filePerso.test ()
elif argv [1] == 'testArtic':
	filePerso = Article ()
	filePerso.test ()
# le nom du fichier n'a pas ete donne
else: print (help)