#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.html import FileHtml
from debutils.htmlArticle import ArticleHtml

help ="""ce script fait deux actions
a- convertir un fichier html en txt
	python htmlDeb.py file.html
b- convertir un fichier txt en html
	python htmlDeb.py file.txt
	python htmlDeb.py file.txt article"""

if len (argv) >=2:
	url = argv [1]
	page = ArticleHtml()
	if url [-5:] == '.html':
		page.file = url
		page.toArticle()
	elif url [-4:] == '.txt':
		subject = None
		if len (argv) >=3: subject = argv [2]
		if subject == 'article': page.fromArticleName (url)
		else:
			page = FileHtml()
			page.fromFilePersoName (url)
# le nom du fichier n'a pas ete donne
else: print (help)

"""
	if url [:4] == 'http': page.fromWeb (url, subject)
	elif url [-5:] == '.html':
		if subject == 'totext':
			page.file = url
			page.toArticle()
		else: page.fromLocal (url, subject)
	elif url [-4:] == '.txt':
		if subject == 'article': page.fromArticleName (url)
		else:
			page = FileHtml()
			page.fromFilePersoName (url)
"""