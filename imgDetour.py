#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageOps
import colorsys
from imgModif import openImage, getColors, imGtoHsv, hsVtoImg
import loggerFct as log

help ="""
détourer une image
attention, le détourage fonctionne mal pour les zones dont la couleur est proche.
le script fait le plus gros du travail, mais il faut le corriger manuellement
"""

 def unifyClosesColors (imageArray, colorList):
	# les couleurs, en nb, sont codées par un unique nombre
	colorList = getColors (imageOriginal)
	imageArray = numpy.array (imageOriginal)
	rangeColors = range (1, len (colorList))
	for c in rangeColors:
		score = int (colorList[c]) - int (colorList[c-1])
		if score >= -2 and score <=2:
			colorArea = imageArray == colorList[c-1]
			imageArray[colorArea] = colorList[c]

def eraseLonelyPixel (imageArray):
	# imageArray is a height x width numpy array, transformé par convert ('P', palette=Image.ADAPTIVE, colors=10)
	# coins hg, hd, bg, bd
	if imageArray[0][0] != imageArray[0][1] and imageArray[0][0] != imageArray[1][0]: imageArray[0][0] = imageArray[0][1]
	if imageArray[0][-1] != imageArray[0][-2] and imageArray[0][-1] != imageArray[1][-1]: imageArray[0][-1] = imageArray[0][-2]
	if imageArray[-1][0] != imageArray[-1][1] and imageArray[-1][0] != imageArray[-2][0]: imageArray[-1][0] = imageArray[-1][0]
	if imageArray[-1][-1] != imageArray[-1][1] and imageArray[-1][-1] != imageArray[-2][-1]: imageArray[-1][-1] = imageArray[-1][-2]
	# lignes h et b
	rangeWidth = range (1, len (imageArray[0]) -1)
	for b in rangeWidth:
		if imageArray[0][b] not in [ imageArray[1][b], imageArray[0][b+1], imageArray[0][b-1] ]:
			if imageArray[1][b] in [ imageArray[0][b+1], imageArray[0][b-1] ]: imageArray[0][b] = imageArray[1][b]
			else: imageArray[0][b] = imageArray[0][b+1]
		if imageArray[-1][b] not in [ imageArray[-2][b], imageArray[-1][b+1], imageArray[-1][b-1] ]:
			if imageArray[-2][b] in [ imageArray[-1][b+1], imageArray[-1][b-1] ]: imageArray[-1][b] = imageArray[-2][b]
			else: imageArray[-1][b] = imageArray[-1][b+1]
	# lignes g et d
	rangeHeight = range (1, len (imageArray) -1)
	for b in rangeHeight:
		if imageArray[b][0] not in [ imageArray[b][1], imageArray[b-1][0], imageArray[b+1][0] ]:
			if imageArray[b][1] in [ imageArray[b-1][0], imageArray[b+1][0] ]: imageArray[b][0] = imageArray[b][1]
			else: imageArray[b][0] = imageArray[b-1][0]
		if imageArray[b][-1] not in [ imageArray[b][-2], imageArray[b-1][-1], imageArray[b+1][-1] ]:
			if imageArray[b][-2] in [ imageArray[b-1][-1], imageArray[b+1][-1] ]: imageArray[b][-1] = imageArray[b][-2]
			else: imageArray[b][-1] = imageArray[b-1][-1]
	# milieu
	for h in rangeHeight:
		for w in rangeWidth:
			if [ imageArray[h][w-1], imageArray[h][w+1], imageArray[h-1][w], imageArray[h+1][w] ].count (imageArray[h][w]) <2:
				if imageArray[h][w-1] in [ imageArray[h][w+1], imageArray[h-1][w], imageArray[h+1][w] ]: imageArray[h][w] = imageArray[h][w-1]
				elif imageArray[h][w+1] in [ imageArray[h-1][w], imageArray[h+1][w] ]: imageArray[h][w] = imageArray[h][w+1]
				else: imageArray[h][w] = imageArray[h-1][w]
			"""
			if imageArray[h][w] not in [ imageArray[h][w-1], imageArray[h][w+1], imageArray[h-1][w], imageArray[h+1][w] ]:
				if imageArray[h][w-1] in [ imageArray[h][w+1], imageArray[h-1][w], imageArray[h+1][w] ]: imageArray[h][w] = imageArray[h][w-1]
				elif imageArray[h][w+1] in [ imageArray[h-1][w], imageArray[h+1][w] ]: imageArray[h][w] = imageArray[h][w+1]
				else: imageArray[h][w] = imageArray[h-1][w]
			"""
	return imageArray

def eraseBordColor (imageArray):
	lenHeight = len (imageArray)
	lenWidth = len (imageArray[0])
	# bords verticaux
	heightArray = imageArray.copy()
	rangeHeight = range (lenHeight)
	for h in rangeHeight:
		w=0
		while w< lenWidth and imageArray[h][w] == imageArray[h][0]:
			heightArray[h][w] =0
			w+=1
		w= lenWidth -1
		while w>=0 and imageArray[h][w] == imageArray[h][-1]:
			heightArray[h][w] =0
			w-=1
	# bords horizontaux
	rangeWidth = range (lenWidth)
	widthArray = imageArray.copy()
	for w in rangeWidth:
		h=0
		while h< lenHeight and (imageArray[h][w] == imageArray[0][w] or imageArray[h][w] ==0):
			widthArray[h][w] =0
			h+=1
		h= lenHeight -1
		while h>=0 and (imageArray[h][w] == imageArray[-1][w] or imageArray[h][w] ==0):
			widthArray[h][w] =0
			h-=1
	colorArea = heightArray ==0
	imageArray[colorArea] =0
	colorArea = widthArray ==0
	imageArray[colorArea] =0
	return imageArray

def eraseCenterColor (imageArray):
	lenHeight = len (imageArray)
	lenWidth = len (imageArray[0])
	halfHeight = int (lenHeight /2)
	halfWidth = int (lenWidth /2)
	# lignes horizontales
	rangeHeight = range (lenHeight)
	heightArray = imageArray.copy()
	for h in rangeHeight:
		if imageArray[h][halfWidth] !=0:
			w= halfWidth
			while w< lenWidth and imageArray[h][w] == imageArray[h][halfWidth]:
				heightArray[h][w] =255
				w+=1
			w= halfWidth
			while w>=0 and imageArray[h][w] == imageArray[h][halfWidth]:
				heightArray[h][w] =255
				w-=1
	# lignes verticales
	rangeWidth = range (lenWidth)
	widthArray = imageArray.copy()
	for w in rangeWidth:
		if imageArray[halfHeight][w] !=0:
			h= halfHeight
			while h< lenHeight and imageArray[h][w] == imageArray[halfHeight][w]:
				widthArray[h][w] =255
				h+=1
			h= halfWidth
			while h>=0 and imageArray[h][w] == imageArray[halfHeight][w]:
				widthArray[h][w] =255
				h-=1
	colorArea = heightArray ==255
	imageArray[colorArea] =255
	colorArea = widthArray ==255
	imageArray[colorArea] =255
	# effacer les boucles blanches
	for h in rangeHeight:
		if 255 in imageArray[h]:
			widthArray = numpy.asarray(imageArray[h]==255).nonzero()[0]
			rangeWidth = range (widthArray[0] +1, widthArray[-1])
			for w in rangeWidth:
				if imageArray[h][w] !=255: imageArray[h][w] =255
	colorArea = imageArray !=0
	imageArray[colorArea] =255
	return imageArray

def findBorder (imageOriginal):
	# détecter la bordure d'une image en la simplifiant
	# accentuer les couleurs
	imageLd = ImageOps.autocontrast (imageOriginal)
	hue, saturation, value = imGtoHsv (imageLd)
	rangeHeight = range (len (saturation))
	rangeWidth = range (len (saturation[0]))
	for h in rangeHeight:
		for w in rangeWidth: saturation[h][w] = 1.0
	imageArray = hsVtoImg (hue, saturation, value)
	imageLd = Image.fromarray (imageArray)
	# passage au noir et blanc
	imageLd = imageLd.convert ('P', palette=Image.ADAPTIVE, colors=3)
	imageLd = ImageOps.grayscale (imageLd)
	colors = getColors (imageLd)
	imageArray = numpy.array (imageLd)
	unifyClosesColors (imageArray, colors)
	# éliminer les pixels noirs et blancs
	colorArea = imageArray <10
	imageArray[colorArea] =10
	colorArea = imageArray >245
	imageArray[colorArea] =245
	# unification de l'image
	imageArray = eraseLonelyPixel (imageArray)
	imageArray = eraseBordColor (imageArray)
	imageArray = eraseCenterColor (imageArray)
	return imageArray

def eraseBorder (imageName):
	newName, imageOriginal = openImage (imageName)
	detourArray = findBorder (imageOriginal)
	imageArray = numpy.array (imageOriginal)

	# image détourée
	internArray = imageArray.copy()
	colorArea = detourArray ==0
	internArray[colorArea] = (0, 120, 100)
	imageNouvelle = Image.fromarray (internArray)
	imageNouvelle.save (newName + '-detour.bmp')

	# image masquée par le détourange
	colorArea = detourArray !=0
	imageArray[colorArea] = (125, 0, 25)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName + '-bord.bmp')

if __name__ == '__main__':
	print (help)
	if len (argv) >1: eraseBorder (argv[1])