#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import textFct
from fileCls import File, Article
import loggerFct

help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python3 fileClass.py fichier tag (fichierB)
les valeurs de tag
	clean (reset upper):	nettoyer le texte. modifier ou pas la casse.
	mef (reset upper):	mettre en forme un texte utilisant ma mise en forme spécifique.
	help:			afficher l'aide d'un fichier python.
	convert:		transformer un fichier html en texte et vice-versa.
	md:				transformer un fichier txt en markdown
	comp:			comparer deux fichiers
	art:			transformer un texte simple en article
"""

nbArg = len (argv)
if nbArg <3: print (help)
elif argv[2] == 'help':
	from funcHelp import printHelp
	printHelp (argv[1])
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
elif argv[2] == 'convert':
	page = Article (argv[1])
	page.read()
	if argv[1][-5:] == '.html': page = page.toText()
	elif argv[1][-6:] == '.xhtml': page = page.toText()
	elif argv[1][-4:] == '.txt': page = page.toHtml()
	loggerFct.log (page.text)
	page.write()
elif nbArg >2 and argv[2] == 'comp':
	fileA = File (argv[1])
	fileA.read()
	fileB = File (argv[3])
	fileB.read()
	fileA.comparer (fileB)
elif nbArg >2:
	filePerso = File (argv[1])
	filePerso.read()
	if 'clean' in argv:
		if filePerso.path[-5:] == '.html': filePerso.text = textFct.cleanHtml (filePerso.text)
		if filePerso.path[-4:] == '.css': filePerso.text = textFct.cleanCss (filePerso.text)
		else: filePerso.text = textFct.cleanText (filePerso.text)
	elif 'mef' in argv: filePerso.text = textFct.shape (filePerso.text)
	# rajouter un argument afin d'empêcher l'écriture des majuscules
	if 'reset' in argv and 'upper' in argv: filePerso.text = textFct.upperCase (filePerso.text, 'reset upper')
	elif 'reset' in argv: filePerso.text = textFct.upperCase (filePerso.text, 'reset')
	elif 'upper' in argv: filePerso.text = textFct.upperCase (filePerso.text, 'upper')
	filePerso.write()
# le nom du fichier n'a pas ete donne
else: print (help)