#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
from imgModif import openImage, eraseLonelyPixel, simplifyImageOriginal, extractColors, computeScore, countColorArray

def eraseColor (imageLine, x):
	xd=x-1
	xf=x+1
	pixelRef = (imageLine[x][0], imageLine[x][1], imageLine[x][2])
	while xd >=0 and numpy.array_equal (imageLine[x], imageLine[xd]):
		imageLine[xd] =(255,255,255)
		xd-=1
	lenLine = len (imageLine)
	while xf < lenLine and numpy.array_equal (imageLine[x], imageLine[xf]):
		imageLine[xf] =(255,255,255)
		xf+=1
	# xd est le premier pixel blanc, xf est le premier pixel coloré
	return (xd+1, xf)

def eraseLonelyPixelVb (imageArray):
	print ("éffaçage des pixels isolés")
	refArray = numpy.copy (imageArray)
	rangeWidth = range (len (imageArray[0]))
	rangeHeight = range (len (imageArray))
	width = len (imageArray[0]) -1
	height = len (imageArray) -1
	for w in rangeWidth:
		for h in rangeHeight:
			# récupérer les voisins
			neighbors =[]
			if h>0:
				if w>0: neighbors.append (imageArray[h-1][w-1])
				if w< width: neighbors.append (imageArray[h-1][w+1])
				neighbors.append (imageArray[h-1][w])
			if h< height:
				if w>0: neighbors.append (imageArray[h+1][w-1])
				if w< width: neighbors.append (imageArray[h+1][w+1])
				neighbors.append (imageArray[h+1][w])
			if w>0: neighbors.append (imageArray[h][w-1])
			if w< width: neighbors.append (imageArray[h][w+1])
			# vérifier si les voisins sont de la même couleur que le pixel analysé
			nbSameColor = countColorArray (neighbors, imageArray[h][w])
			# peux de pixel de la même couleur, l'effacer
			if nbSameColor <2:
				nbNeighbors = int (len (neighbors) /2)
				arraySameColor =[]
				rangeNeighbors = range (len (neighbors) -1)
				for n in rangeNeighbors: arraySameColor.append (countColorArray (neighbors, neighbors[n]))
				nbSameColor = max (arraySameColor)
				if nbSameColor >= nbNeighbors: imageArray[h][w] = neighbors [arraySameColor.index (nbSameColor)]
	if numpy.array_equal (refArray, imageArray): return imageArray
	else: return eraseLonelyPixelVb (imageArray)

def findBorder (imageName):
	scoreDifference =27
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	"""
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x (r,g,b,a) numpy array
	imageArray = eraseLonelyPixelVb (imageArray)
	imageArray = simplifyImageOriginal (imageOriginal)
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (1, imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
			if numpy.array_equal (imageArray[h][w], imageArray[h-1][w]): imageArray[h-1][w] =(255,255,255)
	rangeWidth = range (1, imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
			if numpy.array_equal (imageArray[h][w], imageArray[h][w-1]): imageArray[h][w-1] =(255,255,255)
	imageOriginal = Image.fromarray (imageArray)

	for w in rangeWidth:
		for h in rangeHeight:
			if not numpy.array_equal (imageArray[h][w], imageArray[h-1][w]):
				score = computeScore (imageArray[h][w], imageArray[h-1][w])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h-1][w]
	rangeWidth = range (1, imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
			if not numpy.array_equal (imageArray[h][w], imageArray[h][w-1]):
				score = computeScore (imageArray[h][w], imageArray[h][w-1])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h][w-1]
	# décolorer le tour
	limitD =0
	limitF = len (imageArray[0])
	for h in rangeHeight:
		rangeWidth = range (limitD)
		limitD, limitF = eraseColor (imageArray[h], limit[0])
	# je considère que le pixel (0,0) fait partie du fond à détourer
	red, green, blue = imageArray.T		# Temporarily unpack the bands for readability
	colorArea = (red == imageArray[0][0][0]) & (green == imageArray[0][0][1]) & (blue == imageArray[0][0][2])
	imageArray[colorArea.T] = (255, 255, 255)
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)
	"""

def findBorderVa (imageName):
	scoreDifference =300
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)
	rangeWidth = range (imageOriginal.size[0])
	rangeHeight = range (1, imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
			if not numpy.array_equal (imageArray[h][w], imageArray[h-1][w]):
				score = (int (imageArray[h][w][0]) - int (imageArray[h-1][w][0])) **2 + (int (imageArray[h][w][1]) - int (imageArray[h-1][w][1])) **2 + (int (imageArray[h][w][2]) - int (imageArray[h-1][w][2])) **2
				if score <= scoreDifference: imageArray[h][w] = imageArray[h-1][w]
	rangeWidth = range (1, imageOriginal.size[0])
	rangeHeight = range (imageOriginal.size[1])
	for w in rangeWidth:
		for h in rangeHeight:
			if not numpy.array_equal (imageArray[h][w], imageArray[h][w-1]):
				score = (int (imageArray[h][w][0]) - int (imageArray[h][w-1][0])) **2 + (int (imageArray[h][w][1]) - int (imageArray[h][w-1][1])) **2 + (int (imageArray[h][w][2]) - int (imageArray[h][w-1][2])) **2
				if score <= scoreDifference: imageArray[h][w] = imageArray[h][w-1]
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

imageName = 'b/test.bmp'
findBorder (imageName)