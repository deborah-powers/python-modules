#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.html import FileHtml
from debutils.htmlArticle import ArticleHtml
help ="""lancer le script
	python htmlClean.py url"""
if len (argv) >=2:
	url = argv [1]
	subject =None
	page = ArticleHtml ()
	if len (argv) >=3: subject = argv [2]
	if url [:4] == 'http': page.fromWeb (url, subject)
	elif url [-5:] == '.html':
		if subject == 'totext':
			page.file = url
			page.toFileText ()
		else: page.fromLocal (url, subject)
	elif url [-4:] == '.txt':
		if subject != 'article': page = FileHtml ()
		page.fromFileName (url)
# le nom du fichier n'a pas ete donne
else: print (help)