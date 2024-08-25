#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
from imgModif import openImage, simplifyImageOriginal
import loggerFct as log

def computeScoreNb (pixelA, pixelO):
	score = int (pixelA) - int (pixelO)
	if score <0: score *=-1
	return score

scoreDifference =3

def findBorder (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-bord.bmp'
	imageArray = simplifyImageOriginal (imageOriginal)
	# si les deux pixels sont de couleur proches, le premier est coloré comme le second
	rangeHeight = range (imageOriginal.size[1])
	rangeWidth = range (imageOriginal.size[0])
	for h in rangeHeight:
		print (min (imageArray[h]), max (imageArray[h]))

	"""
	rangeHeight = range (1, imageOriginal.size[1])
	rangeWidth = range (1, imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			score = 1000000
			if imageArray[h-1][w-1] == imageArray[h-1][w] and imageArray[h-1][w-1] == imageArray[h][w-1]:
				score = computeScoreNb (imageArray[h][w-1], imageArray[h][w])
				if score < scoreDifference: imageArray[h][w] = imageArray[h][w-1]
	for h in rangeHeight:
		for w in rangeWidth:
			score = 1000000
			if imageArray[h-1][w-1] == imageArray[h-1][w] and imageArray[h-1][w-1] == imageArray[h][w-1] and imageArray[h-1][w-1] != imageArray[h][w]:
				score = computeScoreNb (imageArray[h-1][w-1], imageArray[h][w])
				if score < scoreDifference: imageArray[h][w] = imageArray[h-1][w-1]
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h-1][w] == imageArray[h][w-1] and imageArray[h-1][w] == imageArray[h-1][w-1]:
				score = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
				if score < scoreDifference: imageArray[h][w] = imageArray[h-1][w]
	rangeHeight = range (1, imageOriginal.size[1])
	rangeWidth = range (imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			score = 1000000
			if imageArray[h][w] != imageArray[h-1][w]:
				score = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
				if score < scoreDifference: imageArray[h][w] = imageArray[h-1][w]
	rangeHeight = range (1, imageOriginal.size[1])
	rangeWidth = range (1, imageOriginal.size[0])
	for h in rangeHeight:
		for w in rangeWidth:
			scoreH = 1000000
			scoreW = 1000000
			scoreM = 1000000
			if imageArray[h][w] == imageArray[h-1][w]: scoreH =0
			else: scoreH = computeScoreNb (imageArray[h][w], imageArray[h-1][w])
			if imageArray[h][w] == imageArray[h][w-1]: scoreW =0
			else: scoreW = computeScoreNb (imageArray[h][w], imageArray[h][w-1])
			if imageArray[h][w] == imageArray[h-1][w-1]: scoreM =0
			else: scoreM = computeScoreNb (imageArray[h][w], imageArray[h-1][w-1])
			if scoreH < scoreDifference and scoreW < scoreDifference and scoreM < scoreDifference:
				imageArray[h-1][w] = imageArray[h][w]
				imageArray[h][w-1] = imageArray[h][w]
				imageArray[h-1][w-1] = imageArray[h][w]
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
toHsv (imageName, revertLum)