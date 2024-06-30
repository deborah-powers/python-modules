#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw
import cv2
import fileLocal
import warnings

help ="""modifier des images
utilisation
	le script est appelable dans un fichier
	python3 %s fichier tag
les valeurs de tag
	col: inverser les couleurs
	lum: inverser la luminosité
	all: inverser la luminosité et les couleurs
""" % __file__

def ouvrirImage (nomOriginal):
	nomOriginal = fileLocal.shortcut (argv[1])
	imageOriginal = Image.open (nomOriginal)
	d= nomOriginal.rfind ('.')
	nomNouveau = nomOriginal[:d]
	return nomNouveau, imageOriginal

def dessinerImage (nomNouveau, imageNouvelle):
	drawing = ImageDraw.Draw (imageNouvelle)
	imageNouvelle.save (nomNouveau)

def tabColor (nomOriginal, extension, funcPixel):
	nomNouveau, imageOriginal = ouvrirImage (nomOriginal)
	nomNouveau = nomNouveau +'-'+ extension +'.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x 4 numpy array
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
		#	print (imageOriginal.size, w,h)
			imageArray[h][w] = funcPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	dessinerImage (nomNouveau, imageNouvelle)

def reverseColor (pixel):
	pixel[0] = 255- pixel[0]
	pixel[1] = 255- pixel[1]
	pixel[2] = 255- pixel[2]
	return pixel

def reverseLum (pixel):
	lumTot = int (pixel[0]) + int (pixel[1]) + int (pixel[2])
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	pixel[0] += lumTot
	pixel[1] += lumTot
	pixel[2] += lumTot
	return pixel

def reverseAll (pixel):
	lumTot = int (pixel[0]) + int (pixel[1]) + int (pixel[2])
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	pixel[0] += lumTot
	pixel[1] += lumTot
	pixel[2] += lumTot
	pixel[0] = 255- pixel[0]
	pixel[1] = 255- pixel[1]
	pixel[2] = 255- pixel[2]
	return pixel

if len (argv) <3: print ("entrez le nom de l'image et l'action à faire", help)
elif argv[2] == 'col': tabColor (argv[1], 'reverse-color', reverseColor)
elif argv[2] == 'lum': tabColor (argv[1], 'reverse-lum', reverseLum)
elif argv[2] == 'all': tabColor (argv[1], 'reverse-all', reverseAll)