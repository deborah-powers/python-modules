#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
from imgModif import openImage, eraseLonelyPixel
import loggerFct as log

def pixelClose (pixelA, pixelO):
	score = int (pixelA) - int (pixelO)
	if score >= -10 and score <= 10: return True
	else: return False

def getColors (imageOriginal):
	colorsOriginal = imageOriginal.getcolors (imageOriginal.size[0] * imageOriginal.size[1])
	colors =[]
	for nb, color in colorsOriginal:
		if color not in colors: colors.append (color)
	colors.sort()
	return colors

def findBorder (imageName):
	# simplifier une image en vue de détecter sa bordure
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-simple.bmp'
	imageLd = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=3)
	imageLd = ImageOps.grayscale (imageLd)
	colors = getColors (imageLd)
	imageArray = numpy.array (imageLd)
	# unir les couleurs proches
	rangeColors = (2,1)
	for c in rangeColors:
		score = int (colors[c]) - int (colors[c-1])
		if score >= -10 and score <= 10:
			colorArea = imageArray == colors[c]
			imageArray[colorArea] = colors[c-1]
	imageArray = eraseLonelyPixel (imageArray)
	# effacer la couleur des bords
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
	# effacer la couleur du centre
	halfHeight = int (lenHeight /2)
	halfWidth = int (lenWidth /2)
	# lignes horizontales
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
	widthArray = imageArray.copy()
	for w in rangeWidth:
		if imageArray[halfHeight][w] !=0:
			h= halfHeight
			while h< lenHeight and imageArray[h][w] == imageArray[halfHeight][w]:
				heightArray[h][w] =255
				h+=1
			h= halfWidth
			while h>=0 and imageArray[h][w] == imageArray[halfHeight][w]:
				heightArray[h][w] =255
				h-=1
	colorArea = heightArray ==255
	imageArray[colorArea] =255
	colorArea = widthArray ==255
	imageArray[colorArea] =255
	colorArea = numpy.logical_and (imageArray !=255, imageArray !=0)
	imageArray[colorArea] =130
	# effacer les boucles blanches
	print (numpy.where (imageArray==255))
	# https://stackoverflow.com/questions/66930670/attributeerror-numpy-ndarray-object-has-no-attribute-index

	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def findBorder_fin (newName, imageArray):
	# remplir les boucles blanches incluses dans du noir
	halfHeight = int (lenHeight /2)
	halfWidth = int (lenWidth /2)
	for h in rangeHeight:
		w= halfWidth
		while w>=0 and imageArray[h][w] !=0: w-=1
		while w>=0:
			if imageArray[h][w] !=0: imageArray[h][w] =255
			w-=1
		w= halfWidth
		while w< lenWidth and imageArray[h][w] !=0: w+=1
		while w< lenWidth:
			if imageArray[h][w] !=0: imageArray[h][w] =255
			w+=1
	for w in rangeWidth:
		h= halfHeight
		while h>=0 and imageArray[h][w] !=0: h-=1
		while h>=0:
			if imageArray[h][w] !=0: imageArray[h][w] =255
			h-=1
		h= halfHeight
		while h< lenHeight and imageArray[h][w] !=0: h+=1
		while h< lenHeight:
			if imageArray[h][w] !=0: imageArray[h][w] =255
			h+=1
	colorArea = imageArray !=0
	imageArray[colorArea] =255
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

imageName = 'b/test.bmp'
findBorder (imageName)