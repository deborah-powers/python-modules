#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.listFile import ListFile
help ="""
ce script peut être appelé dans un autre script
python %s fileName action oldArg (newArg)
les valeurs de action:
	n	renommer les fichiers en remplacant un motif par un autre
	c	remplacer un motif par un autre dans le contenu du fichier
	m	déplacer les fichiers
	l	lister les fichiers
	d	vérifier s'il y a des doublons
""" % __file__
if len (argv) <3: print (help)
else:
	flist = ListFile (argv [1])
	action = argv [2]
	if action in 'd l':
		if len (argv) >3: flist.get (argv [3])
		else: flist.get ()
		if action == 'd': flist.doublons ()
		else: print (flist)
	elif len (argv) <4: print (help)
	else:
		wordOld = argv [3]
		wordNew =""
		if len (argv) >4: wordNew = argv [4]
		if action =='n':
			flist.get (wordOld)
			flist.rename (wordOld, wordNew)
		elif action =='c':
			if (len (argv) >5): flist.get (argv [5])
			else: flist.get ()
			flist.replace (wordOld, wordNew)
		elif action =='m':
			if (wordNew): flist.get (wordNew)
			else: flist.get ()
			flist.move (wordOld)
		else: print (help)