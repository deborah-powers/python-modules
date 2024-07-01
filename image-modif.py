#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
import fileLocal
import warnings

help ="""modifier des images
utilisation
	le script est appelable dans un fichier
	python3 %s fichier tag
les valeurs de tag
	col: inverser les colors
	lum: inverser la luminosité
	all: inverser la luminosité et les colors
""" % __file__

def ouvrirImage (imageName):
	imageName = fileLocal.shortcut (argv[1])
	imageOriginal = Image.open (imageName)
	d= imageName.rfind ('.')
	nomNouveau = imageName[:d]
	return nomNouveau, imageOriginal

def tabColor (imageName, extension, funcPixel):
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	nomNouveau = nomNouveau +'-'+ extension +'.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x 4 numpy array
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight: imageArray[h][w] = funcPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (nomNouveau)

def reverseLumPixel (pixel):
	lumTot = int (pixel[0]) + int (pixel[1]) + int (pixel[2])
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	pixel[0] += lumTot
	pixel[1] += lumTot
	pixel[2] += lumTot
	return pixel

def extrairecolors (imageOriginal):
	print (imageOriginal.getcolors())

def extrairecolorsVa (imageName):
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	imageArray = numpy.array (imageOriginal)
	colors =[]
	for w in rangeWidth:
		for h in rangeHeight:
			if imageArray[h][w] not in colors: colors.append (imageArray[h][w])
	return colors

def decolorer (imageName, nomReference):
	# éffacer certaines couleurs d'une image à partir d'une image de référence qui les contient
	colors = extrairecolors (nomReference)
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b) numpy array
	red, green, blue = imageArray.T		# Temporarily unpack the bands for readability
	for r,g,b in colors:
		colorArea = (red == r) & (green == g) & (blue == b)
		imageArray[..., :-1][colorArea.T] = (255, 255, 255)
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (nomNouveau)

def reverseAll (imageName):
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	nomNouveau = nomNouveau +'-reverse.bmp'
	imageOriginal = ImageOps.invert (imageOriginal)
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	imageArray = numpy.array (imageOriginal)
	for w in rangeWidth:
		for h in rangeHeight: imageArray[h][w] = reverseLumPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (nomNouveau)

def reverseLum (imageName):
	pass

def tobw (imageName):
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	nomNouveau = nomNouveau +'-nb.bmp'
	imageNouvelle = ImageOps.grayscale (imageOriginal)
	imageNouvelle.save (nomNouveau)

def reverseColor (imageName):
	nomNouveau, imageOriginal = ouvrirImage (imageName)
	nomNouveau = nomNouveau +'-reverse.bmp'
	imageNouvelle = ImageOps.invert (imageOriginal)
	imageNouvelle.save (nomNouveau)


imageName = 'b/cgi\\photo-deborah.jpg'
nomNouveau, imageOriginal = ouvrirImage (imageName)
print (imageOriginal.getcolors())

"""
if len (argv) <3: print ("entrez le nom de l'image et l'action à faire", help)
# elif argv[2] == 'col': tabColor (argv[1], 'reverse-color', reverseColorPixel)
elif argv[2] == 'col': reverseColor (argv[1])
elif argv[2] == 'all': reverseAll (argv[1])
elif argv[2] == 'lum': tabColor (argv[1], 'reverse', reverseLumPixel)
"""