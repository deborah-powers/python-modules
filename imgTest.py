#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
from imgModif import openImage, simplifyImageOriginal, computeScore
import loggerFct as log

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

def eraseLonelyPixel (imageArray):
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

def findBorder (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	imageOriginal = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=15)
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width numpy array
	# éliminer les points isolés
	eraseLonelyPixel (imageArray)

	"""
	imageArray = simplifyImageOriginal (imageOriginal)
	# si les deux pixels sont de couleur proches, le premier est coloré comme le second
	rangeHeight = range (1, imageOriginal.size[1])
	rangeWidth = range (1, imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			if numpy.array_equal (imageArray[h][w], imageArray[h-1][w]) and numpy.array_equal (imageArray[h][w], imageArray[h][w-1]):
				imageArray[h-1][w] = (255,255,255)
				imageArray[h][w-1] = (255,255,255)
			scoreH = 1000000
			scoreW = 1000000
			if numpy.array_equal (imageArray[h][w], imageArray[h-1][w]): imageArray[h-1][w] = (255,255,255)
			else: scoreH = computeScore (imageArray[h][w], imageArray[h-1][w])
			if numpy.array_equal (imageArray[h][w], imageArray[h][w-1]): imageArray[h][w-1] = (255,255,255)
			else: scoreW = computeScore (imageArray[h][w], imageArray[h-1][w])
			if scoreH <= scoreDifference and scoreW <= scoreDifference:
				imageArray[h-1][w] = (255,255,255)
				imageArray[h][w-1] = (255,255,255)
			if not numpy.array_equal (imageArray[h][w], imageArray[h-1][w]):
				score = computeScore (imageArray[h][w], imageArray[h-1][w])
				log.logMsg (score)
				if score <= scoreDifference: imageArray[h-1][w] = (255,255,255)
			if not numpy.array_equal (imageArray[h][w], imageArray[h][w-1]):
				score = computeScore (imageArray[h][w], imageArray[h][w-1])
				if score <= scoreDifference: imageArray[h][w-1] = (255,255,255)

			if not numpy.array_equal (imageArray[h][w], imageArray[h-1][w]):
				score = computeScore (imageArray[h][w], imageArray[h-1][w])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h-1][w]
			if not numpy.array_equal (imageArray[h][w], imageArray[h][w-1]):
				score = computeScore (imageArray[h][w], imageArray[h][w-1])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h][w-1]
	"""
	# retransformer imageArray en tableau de pixel
	newArray = numpy.ndarray (shape=(imageOriginal.size[1], imageOriginal.size[0], 3), dtype=int, order='F')
	rangeHeight = range (imageOriginal.size[1])
	rangeWidth = range (imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			value = 255 - 17* imageArray[h][w]
			newArray[h][w] =( value, value, value)
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (newArray.astype (numpy.uint8))
	imageNouvelle.save (newName)

imageName = 'b/test.bmp'
findBorder (imageName)