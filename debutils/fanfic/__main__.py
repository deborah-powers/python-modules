#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fanfic import Fanfic

help = """
récupérer les pages de certains sites que j'aime beaucoup
utilisation: python fanfic url
l'url peut correspondre à une page ou un fichier local
"""

if len (argv) >=2:
	url = argv[1]
	subject = None
	page = Fanfic()
	if len (argv) >=3: subject = argv[2]
	page.ficWeb (url, subject)
# le nom du fichier n'a pas ete donne
else: print (help)