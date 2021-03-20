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
	page = FileHtml (url)
	if len (argv) >=3: page = ArticleHtml (url)
	if url [-5:] == '.html':
		page.fromFile()
		page.toFileText()
	elif url [-4:] == '.txt': page.fromFileText()
# le nom du fichier n'a pas ete donne
else: print (help)