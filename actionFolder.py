#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from classFolder import Folder, FolderArticle

help ="""
ce script peut être appelé dans un autre script
python %s folderName action oldArg (newArg)
les valeurs de action:
	n	renommer les fichiers en remplacant un motif par un autre
	nd	renommer les fichiers modifiant la date
	c	remplacer un motif par un autre dans le contenu du fichier
	m	déplacer les fichiers
	l	lister les fichiers
	d	vérifier s'il y a des doublons
	v	identifier les fichiers modifiés entre un dossier et sa sauvegarde
	s	lister les sujets
	i	créer un index
	a	créer un index pour les articles
""" % __file__

if len (argv) <3: print (help)
else:
	flist = Folder (argv[1])
	action = argv[2]
	if action in 'd l':
		if len (argv) >3: flist.get (argv[3])
		else: flist.get()
		if action == 'd': flist.doublons()
		elif action == 'l': print (flist)
	elif action == 'nd': flist.renameDate()
	elif len (argv) <4: print (help)
	elif action == 'v': flist.compareGit (argv[3])
	elif action == 's':
		flist = FolderArticle (argv[1])
		flist.listSubjects()
	elif action == 'i':
		flist = Folder (argv[1])
		flist.createIndex()
	elif action == 'a':
		flist = FolderArticle (argv[1])
		flist.createIndex()
	else:
		wordOld = argv[3]
		wordNew =""
		if len (argv) >4: wordNew = argv[4]
		if action =='n':
			flist.get (wordOld)
			flist.rename (wordOld, wordNew)
		elif action =='c':
			if (len (argv) >5): flist.get (argv[5])
			else: flist.get()
			flist.replace (wordOld, wordNew)
		elif action =='m':
			if (wordNew): flist.get (wordNew)
			else: flist.get()
			flist.move (wordOld)
		else: print (help)