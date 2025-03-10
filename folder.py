#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from folderCls import Folder, FolderArticle
from imageCls import ImageFolder
import loggerFct as log

help ="""
ce script peut être appelé dans un autre script
python %s folderName action oldArg (newArg)
les valeurs de action:
	n	renommer les fichiers en remplacant un motif par un autre
	nd	renommer les fichiers modifiant la date
	nh	renommer les fichiers modifiant la date avec l'heure
	heic	traiter les images heic
	heif	traiter les images heif
	insta	modifier le format des images d'un dossier
	c	remplacer un motif par un autre dans le contenu du fichier
	m	déplacer les fichiers
	l	lister les fichiers
	d	vérifier s'il y a des doublons
	v	identifier les fichiers modifiés entre un dossier et sa sauvegarde
	s	lister les sujets
	i f	créer un index
	i a	créer un index pour les articles
""" % __file__

if len (argv) <3: print (help)
elif argv[2] in ('heic', 'heif', 'nd', 'nh', 'insta'):
	flist = ImageFolder (argv[1])
	if argv[2] == 'nd': flist.renameDate()
	elif argv[2] == 'nh': flist.renameDate (True)
	elif argv[2] == 'heic': flist.heicToPng()
	elif argv[2] == 'heif': flist.heifToPng()
	elif argv[2] == 'insta':
		flist.get ()
		flist.insta ('reflet')
else:
	flist = Folder (argv[1])
	action = argv[2]
	if action in 'd l':
		if len (argv) >3: flist.get (argv[3])
		else: flist.get()
		if action == 'd': flist.doublons()
		elif action == 'l': print (flist)
	elif len (argv) <4: print (help)
	elif action == 'v': flist.compareGit (argv[3])
	elif action == 's':
		flist = FolderArticle (argv[1])
		flist.listSubjects()
	elif action == 'i':
		if argv[3] == 'a': flist = FolderArticle (argv[1])
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
			flist.filter ('.py')
			flist.read()
			flist.replace (wordOld, wordNew)
		elif action =='m':
			if (wordNew): flist.get (wordNew)
			else: flist.get()
			flist.move (wordOld)
		else: print (help)
