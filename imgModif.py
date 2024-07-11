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
""" % __file__

def openImage (imageName):
	imageName = fileLocal.shortcut (imageName)
	imageOriginal = Image.open (imageName)
	imageOriginal = imageOriginal.convert ('RGB')
	d= imageName.rfind ('.')
	newName = imageName[:d]
	return newName, imageOriginal

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

def computeScore (pixelA, pixelO):
	return (int (pixelA[0]) - int (pixelO[0])) **2 + (int (pixelA[1]) - int (pixelO[1])) **2 + (int (pixelA[2]) - int (pixelO[2])) **2

def computeScoreKmeans (pixelA, pixelO):
	return (pixelA[0] - pixelO[0]) **2 + (pixelA[1] - pixelO[1]) **2 + (pixelA[2] - pixelO[2]) **2

def kmeansColor (colorList):
	scoreDifference =675
	colorGroup =[[[ colorList[0][0], colorList[0][1], colorList[0][2] ], colorList[0] ]]	# la case 0 contient la moyenne
	rangeColors = range (1, len (colorList))
	for c in rangeColors:
		# calculer les scores de la color étudiée avec la moyenne de chaque groupe
		groupId =0
		groupScore = 1000000
		rangeGroup = range (len (colorGroup))
		for g in rangeGroup:
			score = computeScoreKmeans (colorGroup[g][0], colorList[c])
			if score < groupScore:
				groupScore = score
				groupId = g
		# trouver le groupe dont elle est le plus proche
		if groupScore <= scoreDifference:
			# calculer la nouvelle moyenne
			lenGroup = len (colorGroup [groupId]) -1
			colorGroup [groupId][0][0] = (colorGroup [groupId][0][0] * lenGroup + colorList[c][0]) / (lenGroup +1)
			colorGroup [groupId][0][1] = (colorGroup [groupId][0][1] * lenGroup + colorList[c][1]) / (lenGroup +1)
			colorGroup [groupId][0][2] = (colorGroup [groupId][0][2] * lenGroup + colorList[c][2]) / (lenGroup +1)
			colorGroup [groupId].append (colorList[c])
		# créer un nouveau groupe
		else: colorGroup.append ([[ colorList[c][0], colorList[c][1], colorList[c][2] ], colorList[c] ])
	rangeGroup = range (len (colorGroup))
	for g in rangeGroup: colorGroup[g][0] =[ int (colorGroup[g][0][0]), int (colorGroup[g][0][1]), int (colorGroup[g][0][2]) ]
	return colorGroup

def eraseLonelyPixel (imageArray):
	# coin haut gauche
	if numpy.array_not_equal (imageArray[0][0], imageArray[0][1]) and numpy.array_not_equal (imageArray[0][0], imageArray[1][0]):
		imageArray[0][0] = imageArray[0][1]
	# coin bas droit
	if numpy.array_not_equal (imageArray[-1][-2], imageArray[-1][-1]) and numpy.array_not_equal (imageArray[-2][-1], imageArray[-1][-1]):
		imageArray[-1][-1] = imageArray[-1][-2]
	# coin bas gauche
	if numpy.array_not_equal (imageArray[-1][1], imageArray[-1][0]) and numpy.array_not_equal (imageArray[-2][0], imageArray[-1][0]):
		imageArray[-1][0] = imageArray[-1][1]
	# coin haut droit
	if numpy.array_not_equal (imageArray[0][-2], imageArray[0][-1]) and numpy.array_not_equal (imageArray[1][-1], imageArray[0][-1]):
		imageArray[0][-1] = imageArray[0][-2]
	# bords haut et bas
	rangeWidth = range (1, len (imageArray[0]) -1)
	for w in rangeWidth:
		# bord haut
		if numpy.array_not_equal (imageArray[0][w-1], imageArray[0][w]) and numpy.array_not_equal (imageArray[0][w+1], imageArray[0][w]) and numpy.array_not_equal (imageArray[1][w], imageArray[0][w]):
			imageArray[0][w] = imageArray[0][w+1]
		# bord bas
		if numpy.array_not_equal (imageArray[-1][w-1], imageArray[-1][w]) and numpy.array_not_equal (imageArray[-1][w+1], imageArray[-1][w]) and numpy.array_not_equal (imageArray[-2][w], imageArray[-1][w]):
			imageArray[-1][w] = imageArray[-1][w+1]
	# bords gauche et droit
	rangeHeight = range (1, len (imageArray) -1)
	for h in rangeHeight:
		# bord gauche
		if numpy.array_not_equal (imageArray[h-1][0], imageArray[h][0]) and numpy.array_not_equal (imageArray[h+1][0], imageArray[h][0]) and numpy.array_not_equal (imageArray[h][1], imageArray[h][0]):
			imageArray[h][0] = imageArray[h][1]
		# bord droit
		if numpy.array_not_equal (imageArray[h-1][-1], imageArray[h][-1]) and numpy.array_not_equal (imageArray[h+1][-1], imageArray[h][-1]) and numpy.array_not_equal (imageArray[h][-2], imageArray[h][-1]):
			imageArray[h][-1] = imageArray[h][-2]
	# milieu
	for h in rangeHeight:
		for w in rangeWidth:
		if numpy.array_not_equal (imageArray[h][w-1], imageArray[h][w]) and numpy.array_not_equal (imageArray[h][w+1], imageArray[h][w]) and numpy.array_not_equal (imageArray[h-1][w], imageArray[h][w]) and numpy.array_not_equal (imageArray[h+1][w], imageArray[h][w]):
			imageArray[h][w] = imageArray[h][w+1]
	return imageArray

def simplifyImageOriginal (imageOriginal):
	colorList = extractColors (imageOriginal)
	colorGroup = kmeansColor (colorList)
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b,a) numpy array
	red, green, blue = imageArray.T		# Temporarily unpack the bands for readability
	for group in colorGroup:
		for r,g,b in group:
			colorArea = (red == r) & (green == g) & (blue == b)
			imageArray[colorArea.T] =(group[0][0], group[0][1], group[0][2])
#	imageArray = eraseLonelyPixel (imageArray)
	return imageArray

def simplifyImage (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-simple.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)
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

if __name__ != 'main': pass
elif len (argv) <3: print ("entrez le nom de l'image et l'action à faire", help)
elif argv[2] == 'nb': tobw (argv[1])
elif argv[2] == 'col': reverseColor (argv[1])
elif argv[2] == 'simple': simplifyImage (argv[1])
elif argv[2] == 'all': replaceColors (argv[1], 'reverse', reverseAllColors)
elif argv[2] == 'lum': replaceColors (argv[1], 'reverse', reverseLumColors)
elif argv[2] == 'del' and len (argv) >3: eraseColors (argv[1], argv[3])
# elif argv[2] == 'lum': replacePixels (argv[1], 'reverse', reverseLumPixel)
