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

def eraseLonelyPixelVa (imageArray):
	# coin haut gauche
	if not numpy.array_equal (imageArray[0][0], imageArray[0][1]) and not numpy.array_equal (imageArray[0][0], imageArray[1][0]):
		imageArray[0][0] = imageArray[0][1]
	# coin bas droit
	if not numpy.array_equal (imageArray[-1][-2], imageArray[-1][-1]) and not numpy.array_equal (imageArray[-2][-1], imageArray[-1][-1]):
		imageArray[-1][-1] = imageArray[-1][-2]
	# coin bas gauche
	if not numpy.array_equal (imageArray[-1][1], imageArray[-1][0]) and not numpy.array_equal (imageArray[-2][0], imageArray[-1][0]):
		imageArray[-1][0] = imageArray[-1][1]
	# coin haut droit
	if not numpy.array_equal (imageArray[0][-2], imageArray[0][-1]) and not numpy.array_equal (imageArray[1][-1], imageArray[0][-1]):
		imageArray[0][-1] = imageArray[0][-2]
	# bords haut et bas
	rangeWidth = range (1, len (imageArray[0]) -1)
	for w in rangeWidth:
		# bord haut
		if not numpy.array_equal (imageArray[0][w-1], imageArray[0][w]) and not numpy.array_equal (imageArray[0][w+1], imageArray[0][w]) and not numpy.array_equal (imageArray[1][w], imageArray[0][w]):
			imageArray[0][w] = imageArray[0][w+1]
		# bord bas
		if not numpy.array_equal (imageArray[-1][w-1], imageArray[-1][w]) and not numpy.array_equal (imageArray[-1][w+1], imageArray[-1][w]) and not numpy.array_equal (imageArray[-2][w], imageArray[-1][w]):
			imageArray[-1][w] = imageArray[-1][w+1]
	# bords gauche et droit
	rangeHeight = range (1, len (imageArray) -1)
	for h in rangeHeight:
		# bord gauche
		if not numpy.array_equal (imageArray[h-1][0], imageArray[h][0]) and not numpy.array_equal (imageArray[h+1][0], imageArray[h][0]) and not numpy.array_equal (imageArray[h][1], imageArray[h][0]):
			imageArray[h][0] = imageArray[h][1]
		# bord droit
		if not numpy.array_equal (imageArray[h-1][-1], imageArray[h][-1]) and not numpy.array_equal (imageArray[h+1][-1], imageArray[h][-1]) and not numpy.array_equal (imageArray[h][-2], imageArray[h][-1]):
			imageArray[h][-1] = imageArray[h][-2]
	# milieu
	for h in rangeHeight:
		for w in rangeWidth:
			if not numpy.array_equal (imageArray[h][w-1], imageArray[h][w]) and not numpy.array_equal (imageArray[h][w+1], imageArray[h][w]) and not numpy.array_equal (imageArray[h-1][w], imageArray[h][w]) and not numpy.array_equal (imageArray[h+1][w], imageArray[h][w]):
				imageArray[h][w] = imageArray[h][w+1]
	return imageArray

def findBorder (imageName):
	scoreDifference = 27	# 27 75 300 675
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)
	"""
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
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

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