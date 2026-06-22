#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from imageCls import ImageFile
import imageSimplify

help ="""
modifier une image
utilisation
	le script est appelable dans un fichier
	python image.py fichier tag (fichierB)
les valeurs de tag
	e imageRef: éffacer certaines couleurs de l'image principale. imageRef contient ces couleurs
	s: simplifier les couleurs
"""

nbArg = len (argv)
if nbArg <3: print (help)
elif argv[2] == 'help':
	from funcHelp import printHelp
	printHelp (argv[1])
elif argv[2] == 'e' and nbArg >3:
	image = ImageFile (argv[1])
	image.open()
	imageRef = ImageFile (argv[3])
	imageRef.open()
	image.title = image.title +" bis"
	image.toPath()
	image.eraseColors (imageRef)
	image.draw()
elif argv[2] == 's':
	image = ImageFile (argv[1])
	image.open()
	image.title = image.title +" bis"
	image.toPath()
	image.simplifyColors()
	image.draw()
else: print (help)
