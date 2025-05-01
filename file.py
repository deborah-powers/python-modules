#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import textFct
from fileCls import File, Article
from htmlCls import Html
import loggerFct as log

help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python3 fileClass.py fichier tag (fichierB)
les valeurs de tag
	clean (ru - r - u):	nettoyer le texte. modifier ou pas la casse.
	mef (ru):	mettre en forme un texte utilisant ma mise en forme spécifique.
	help:		afficher l'aide d'un fichier python.
	convert:	transformer un fichier html en texte et vice-versa.
	md:			transformer un fichier txt en markdown
	comp:		comparer deux fichiers
	art:		transformer un texte simple en article
	inde:		transformer un fichier html local en fichier adapté pour ma liseuse
	pdf:		mettre en forme le texte copié - collé d'un fichier pdf
"""
nbArg = len (argv)
if nbArg <3: print (help)
elif argv[2] == 'help':
	from funcHelp import printHelp
	printHelp (argv[1])
elif argv[2] == 'pdf':
	page = File (argv[1])
	page.read()
	page.text = textFct.cleanPdf (page.text)
	page.write()
elif argv[2] == 'art':
	page = File (argv[1])
	page.read()
	article = Article (argv[1])
	article.text = page.text
	article.write()
elif argv[2] == 'md':
	page = File (argv[1])
	page.read()
	page.toMarkdown()
	page.write()
elif argv[2] == 'inde':
	pageHtml = Html()
	if argv[1][-5:] == '.html':
		pageHtml = Html (argv[1])
		pageHtml.read()
	elif argv[1][-4:] == '.txt':
		page = Article (argv[1])
		page.read()
		pageHtml.fromText (page)
	pageHtml.toEreader()
elif argv[2] == 'conv':
	page = None
	if argv[1][-4:] == '.txt':
		page = Article (argv[1])
		page.read()
		pageHtml = Html()
		pageHtml.fromText (page)
		pageHtml.write()
	if argv[1][-4:] == 'html':
		page = Html (argv[1])
		page.read()
		page = page.toText()
		if page: page.write()
elif nbArg >2 and argv[2] == 'comp':
	fileA = File (argv[1])
	fileA.read()
	fileB = File (argv[3])
	fileB.read()
	fileA.comparer (fileB)
elif nbArg >2:
	# TODO: à refaire
	filePerso = File (argv[1])
	filePerso.read()
	if 'clean' in argv:
		if filePerso.path[-5:] == '.html' or filePerso.path[-6:] == '.xhtml' or filePerso.path[-4:] == '.xml': filePerso.text = textFct.cleanHtml (filePerso.text)
		# formats dérivés du xml
		elif filePerso.path[-4:] == '.ops' or filePerso.path[-4:] == '.opf' or filePerso.path[-4:] == '.ncx': filePerso.text = textFct.cleanHtml (filePerso.text)
		elif filePerso.path[-4:] == '.css': filePerso.text = textFct.cleanCss (filePerso.text)
		else: filePerso.text = textFct.cleanText (filePerso.text)
	elif 'mef' in argv: filePerso.text = textFct.shape (filePerso.text)
	if nbArg >3:
		# rajouter un argument afin d'empêcher l'écriture des majuscules
		if 'r' in argv[3] and 'u' in argv[3]: filePerso.text = textFct.upperCase (filePerso.text, 'reset upper')
		elif 'r' in argv[3]: filePerso.text = textFct.upperCase (filePerso.text, 'reset')
		elif 'u' in argv[3]: filePerso.text = textFct.upperCase (filePerso.text, 'upper')
	filePerso.write()
# le nom du fichier n'a pas ete donne
else: print (help)