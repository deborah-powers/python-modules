#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
from imageCls import *
import loggerFct as log

help ="""modifier des images
utilisation
	le script est appelable dans un fichier
	python3 %s fichier tag (référence)
les valeurs de tag
	nb: passer l'image en nuance de gris
	ct: augmenter le contraste
	rv: inverser les couleurs
	dl ref: éffacer les couleurs contenues dans l'image de référence
	sc colOld colNew: remplacer une couleur par une autre
	colOld = "30 78 23"
""" % __file__

if len (argv) <3: print (help)
else:
	image = ImageFile (argv[1])
	image.open()
	if argv[2] == 'nb': image.tobw()
	elif argv[2] == 'ct': image.correctContrast()
	elif argv[2] == 'rv': image.reverseImage()
	elif argv[2] == 'tt': image.test()
	elif argv[2] == 'dl' and len (argv) >3:
		imageRef = ImageFile (argv[3])
		imageRef.open()
		image.eraseColors (imageRef)
	elif argv[2] == 'sc' and len (argv) >4:
		image.swapColors (argv[3], argv[4])
	image.title = image.title +" "+ argv[2]
	image.draw()
"""
	image.image.show()
	image.image.close()
"""
