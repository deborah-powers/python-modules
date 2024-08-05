#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
from imgModif import openImage, simplifyImageOriginal
import loggerFct as log

"""
def eraseColor (imageLine, x):
	xd=x-1
	xf=x+1
	pixelRef = (imageLine[x][0], imageLine[x][1], imageLine[x][2])
	while xd >=0 and imageLine[x], imageLine[xd]):
		imageLine[xd] =(255,255,255)
		xd-=1
	lenLine = len (imageLine)
	while xf < lenLine and imageLine[x], imageLine[xf]):
		imageLine[xf] =(255,255,255)
		xf+=1
	# xd est le premier pixel blanc, xf est le premier pixel coloré
	return (xd+1, xf)
"""
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

def computeScoreNb (pixelA, pixelO):
	score = int (pixelA) - int (pixelO)
	if score <0: score *=-1
	return score

scoreDifference =2

def findBorder (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)

	# si les deux pixels sont de couleur proches, le premier est coloré comme le second
	rangeHeight = range (1, imageOriginal.size[1])
	rangeWidth = range (1, imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			scoreH = 1000000
			scoreW = 1000000
			if imageArray[h][w] == imageArray[h-1][w] and imageArray[h][w] == imageArray[h][w-1]:
				imageArray[h-1][w] =1
				imageArray[h][w-1] =1
			elif imageArray[h][w] == imageArray[h-1][w]:
				imageArray[h-1][w] =1
				scoreW = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
			elif imageArray[h][w] == imageArray[h][w-1]:
				imageArray[h][w-1] =1
				scoreH = computeScoreNb (imageArray[h][w], imageArray[h-1][w])


			else: scoreH = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
			if imageArray[h][w] == imageArray[h][w-1]: imageArray[h][w-1] =1
			else: scoreW = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
			if scoreH <= scoreDifference and scoreW <= scoreDifference:
				imageArray[h-1][w] =1
				imageArray[h][w-1] =1
			if imageArray[h][w] != imageArray[h-1][w]:
				score = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
				if score <= scoreDifference: imageArray[h-1][w] =1
			if imageArray[h][w] != imageArray[h][w-1]:
				score = computeScoreNb (imageArray[h][w], imageArray[h][w-1])
				if score <= scoreDifference: imageArray[h][w-1] =1
			if imageArray[h][w] != imageArray[h-1][w]:
				score = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h-1][w]
			if imageArray[h][w] != imageArray[h][w-1]:
				score = computeScoreNb (imageArray[h][w], imageArray[h][w-1])
				if score <= scoreDifference: imageArray[h][w] = imageArray[h][w-1]
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