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

def tabColor (nomOriginal, extension, funcPixel):
	nomNouveau, imageOriginal = ouvrirImage (nomOriginal)
	nomNouveau = nomNouveau +'-'+ extension +'.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x 4 numpy array
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight: imageArray[h][w] = funcPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (nomNouveau)

def reverseColorPixel (pixel):
	pixel[0] = 255- pixel[0]
	pixel[1] = 255- pixel[1]
	pixel[2] = 255- pixel[2]
	return pixel

def reverseLumPixel (pixel):
	lumTot = int (pixel[0]) + int (pixel[1]) + int (pixel[2])
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	pixel[0] += lumTot
	pixel[1] += lumTot
	pixel[2] += lumTot
	return pixel

def reverseAll (nomOriginal):
	nomNouveau, imageOriginal = ouvrirImage (nomOriginal)
	nomNouveau = nomNouveau +'-reverse-all.bmp'
	imageOriginal = ImageOps.invert (imageOriginal)
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	imageArray = numpy.array (imageOriginal)
	for w in rangeWidth:
		for h in rangeHeight: imageArray[h][w] = reverseLumPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (nomNouveau)

def reverseLum (nomOriginal):
	pass

def tobw (nomOriginal):
	nomNouveau, imageOriginal = ouvrirImage (nomOriginal)
	nomNouveau = nomNouveau +'-nb.bmp'
	imageNouvelle = ImageOps.grayscale (imageOriginal)
	imageNouvelle.save (nomNouveau)

def reverseColor (nomOriginal):
	nomNouveau, imageOriginal = ouvrirImage (nomOriginal)
	nomNouveau = nomNouveau +'-reverse-color.bmp'
	imageNouvelle = ImageOps.invert (imageOriginal)
	imageNouvelle.save (nomNouveau)

if len (argv) <3: print ("entrez le nom de l'image et l'action à faire", help)
# elif argv[2] == 'col': tabColor (argv[1], 'reverse-color', reverseColorPixel)
elif argv[2] == 'col': reverseColor (argv[1])
elif argv[2] == 'all': reverseAll (argv[1])
elif argv[2] == 'lum': tabColor (argv[1], 'reverse-lum', reverseLumPixel)
