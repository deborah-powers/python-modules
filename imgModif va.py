#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import os
import time
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageOps
import fileLocal
import loggerFct as log

help ="""modifier des images
utilisation
	le script est appelable dans un fichier
	python3 %s fichier tag (référence)
les valeurs de tag
	col: inverser les couleurs
	lum: inverser la luminosité
	all: inverser la luminosité et les couleurs
	del: éffacer les couleurs contenues dans l'image de référence
	nb: passer l'image en nuance de gris
	simple: simplifier les couleurs

https://www.geeksforgeeks.org/python-pil-image-point-method/
https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
""" % __file__

def openImage (imageName):
	imageName = fileLocal.shortcut (imageName)
	imageOriginal = Image.open (imageName)
	imageOriginal = imageOriginal.convert ('RGB')
	d= imageName.rfind ('.')
	newName = imageName[:d]
	return newName, imageOriginal

def extractColors (imageOriginal):
	colorsOriginal = imageOriginal.getcolors (imageOriginal.size[0] * imageOriginal.size[1])
	colors =[]
	for nb, color in colorsOriginal:
		if (color[0], color[1], color[2]) not in colors: colors.append ((color[0], color[1], color[2]))
	colors.sort()
	return colors

def extractColorsFromReference (nomReference):
	nomReference = fileLocal.shortcut (nomReference)
	imageOriginal = Image.open (nomReference)
	imageOriginal = imageOriginal.convert ('RGB')
	return extractColors (imageOriginal)

def replaceColors (imageName, extension, funcPixel):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-'+ extension +'.bmp'
	colors = extractColors (imageOriginal)
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b) numpy array
	red, green, blue = imageArray.T				# Temporarily unpack the bands for readability
	for r,g,b in colors:
		colorArea = (red == r) & (green == g) & (blue == b)
		newColor = funcPixel (r,g,b)
		imageArray[colorArea.T] = newColor
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def eraseColors (imageName, nomReference):
	# éffacer certaines colors d'une image à partir d'une image de référence qui les contient
	colors = extractColorsFromReference (nomReference)
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-del.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b) numpy array
	red, green, blue = imageArray.T		# Temporarily unpack the bands for readability
	for r,g,b in colors:
		colorArea = (red == r) & (green == g) & (blue == b)
		imageArray[colorArea.T] = (255, 255, 255)
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def reverseLumColors (r,g,b):
	lumTot = r+g+b
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	r+= lumTot
	g+= lumTot
	b+= lumTot
	return (r,g,b)

def reverseAllColors (r,g,b):
	r,g,b = reverseLumColors (r,g,b)
	r= 255 -r
	g= 255 -g
	b= 255 -b
	return (r,g,b)

def tobw (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-nb.bmp'
	imageNouvelle = ImageOps.grayscale (imageOriginal)
	imageNouvelle.save (newName)

def reverseColor (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-reverse.bmp'
	imageNouvelle = ImageOps.invert (imageOriginal)
	imageNouvelle.save (newName)

def constrast (imageArray):
	lenHeight = len (imageArray)
	lenWidth = len (imageArray[0])
	rangeHeight = range (lenHeight)
	rangeWidth = range (lenWidth)
	pixelMoy =[0,0,0]
	# trouver les moyennes de l'image
	for h in rangeHeight:
		for w in rangeWidth:
			pixelMoy[0] += imageArray[h][w][0]
			pixelMoy[1] += imageArray[h][w][1]
			pixelMoy[2] += imageArray[h][w][2]
	lenHeight *= lenWidth
	pixelMoy[0] /= lenHeight
	pixelMoy[1] /= lenHeight
	pixelMoy[2] /= lenHeight
	"""
	pixelMoy[0] = int (pixelMoy[0])
	pixelMoy[1] = int (pixelMoy[1])
	pixelMoy[2] = int (pixelMoy[2])
	"""
	log.logMsg (pixelMoy)
	# constraster l'image à partir de la référence
	for h in rangeHeight:
		for w in rangeWidth:
			imageArray[h][w][0] = 2* imageArray[h][w][0] - pixelMoy[0]
			if imageArray[h][w][0] >=255: imageArray[h][w][0] =255
			elif imageArray[h][w][0] <=0: imageArray[h][w][0] =0
			else: imageArray[h][w][0] = int (imageArray[h][w][0])
			imageArray[h][w][1] = 2* imageArray[h][w][1] - pixelMoy[1]
			if imageArray[h][w][1] >=255: imageArray[h][w][1] =255
			elif imageArray[h][w][1] <=0: imageArray[h][w][1] =0
			else: imageArray[h][w][1] = int (imageArray[h][w][1])
			imageArray[h][w][2] = 2* imageArray[h][w][2] - pixelMoy[2]
			if imageArray[h][w][2] >=255: imageArray[h][w][2] =255
			elif imageArray[h][w][2] <=0: imageArray[h][w][2] =0
			else: imageArray[h][w][2] = int (imageArray[h][w][2])
	return imageArray

def constrastSimple (imageArray):
	rangeHeight = range (len (imageArray))
	rangeWidth = range (len (imageArray[0]))
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h][w][0] >=96 and imageArray[h][w][0] <=160: imageArray[h][w][0] = 2* imageArray[h][w][0] -128
			if imageArray[h][w][1] >=96 and imageArray[h][w][1] <=160: imageArray[h][w][1] = 2* imageArray[h][w][1] -128
			if imageArray[h][w][2] >=96 and imageArray[h][w][2] <=160: imageArray[h][w][2] = 2* imageArray[h][w][2] -128
	return imageArray

def replaceColor (imageArray, rvbOriginal, rvbNew):
	red, green, blue = imageArray.T				# Temporarily unpack the bands for readability
	colorArea = (red == rvbOriginal[0]) & (green == rvbOriginal[1]) & (blue == rvbOriginal[2])
	imageArray[colorArea.T] = rvbNew
	return imageArray

def computeScore (pixelA, pixelO):
	return (int (pixelA[0]) - int (pixelO[0])) **2 + (int (pixelA[1]) - int (pixelO[1])) **2 + (int (pixelA[2]) - int (pixelO[2])) **2

def eraseLonelyPixelNb (imageArray):
	# imageArray is a height x width numpy array, transformé par convert ('P', palette=Image.ADAPTIVE, colors=10)
	rangeHeight = range (len (imageArray))
	rangeWidth = range (1, len (imageArray[0]) -1)
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h][w-1] != imageArray[h][w] and imageArray[h][w+1] != imageArray[h][w]: imageArray[h][w] = imageArray[h][w-1]
	rangeHeight = range (1, len (imageArray) -1)
	rangeWidth = range (len (imageArray[0]))
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h-1][w] != imageArray[h][w] and imageArray[h+1][w] != imageArray[h][w]: imageArray[h][w] = imageArray[h-1][w]
	return imageArray

def eraseLonelyPixel (imageArray):
	# imageArray is a height x width x (r,v,b) numpy array
	rangeHeight = range (len (imageArray))
	rangeWidth = range (1, len (imageArray[0]) -1)
	for h in rangeHeight:
		for w in rangeWidth:
			if not numpy.array_equal (imageArray[h][w-1], imageArray[h][w]) and not numpy.array_equal (imageArray[h][w+1], imageArray[h][w]): imageArray[h][w] = imageArray[h][w-1]
	rangeHeight = range (1, len (imageArray) -1)
	rangeWidth = range (len (imageArray[0]))
	for h in rangeHeight:
		for w in rangeWidth:
			if not numpy.array_equal (imageArray[h-1][w], imageArray[h][w]) and not numpy.array_equal (imageArray[h+1][w], imageArray[h][w]): imageArray[h][w] = imageArray[h-1][w]
	return imageArray

def simplifyImageOriginal (imageOriginal):
	imageOriginal = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=10)
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b,a) numpy array
	imageArray = eraseLonelyPixelNb (imageArray)
	return imageArray

def simplifyImage (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-simple.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def constrastImage (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-contraste.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b,a) numpy array
	imageArray = constrast (imageArray)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def reverseLumPixel (pixel):
	lumTot = int (pixel[0]) + int (pixel[1]) + int (pixel[2])
	lumTot = lumTot /3
	lumTot = 255- 2* lumTot
	lumTot = int (lumTot)
	pixel[0] += lumTot
	pixel[1] += lumTot
	pixel[2] += lumTot
	return pixel

def replacePixels (imageName, extension, funcPixel):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-'+ extension +'.bmp'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b) numpy array
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight: imageArray[h][w] = funcPixel (imageArray[h][w])
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

if __name__ != '__main__': pass
elif len (argv) <3: print ("entrez le nom de l'image et l'action à faire", help)
elif argv[2] == 'nb': tobw (argv[1])
elif argv[2] == 'col': reverseColor (argv[1])
elif argv[2] == 'simple': simplifyImage (argv[1])
elif argv[2] == 'constrast': constrastImage (argv[1])
elif argv[2] == 'all': replaceColors (argv[1], 'reverse', reverseAllColors)
elif argv[2] == 'lum': replaceColors (argv[1], 'reverse', reverseLumColors)
elif argv[2] == 'del' and len (argv) >3: eraseColors (argv[1], argv[3])
# elif argv[2] == 'lum': replacePixels (argv[1], 'reverse', reverseLumPixel)
