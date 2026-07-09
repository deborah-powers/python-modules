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
imageRefName = 'C:\\Users\\deborah.powers\\Desktop\\ref.bmp'

nbArg = len (argv)
if nbArg <3: print (help)
elif argv[2] == 'help':
	from funcHelp import printHelp
	printHelp (argv[1])
elif argv[2] in 'es':
	image = ImageFile (argv[1])
	image.open()
	image.title = image.title +" bis"
	if argv[2] == 'e' and nbArg >3:
		imageRef = ImageFile (argv[3])
		imageRef.open()
		image.eraseColors (imageRef)
	elif argv[2] == 's': image.simplifyColors()
	image.draw()
else: print (help)
