#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageDraw, ImageOps, ImageChops
import cv2
from imgModif import openImage, eraseLonelyPixel
import loggerFct as log

def pixelClose (pixelA, pixelO):
	score = int (pixelA) - int (pixelO)
	if score >= -25 and score <= 25: return True
	else: return False

def findBorder (imageName):
	# simplifier une image en vue de détecter sa bordure
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-simple.bmp'
	imageLd = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=10)
	imageLd = ImageOps.grayscale (imageLd)
	imageArray = numpy.array (imageLd)
	imageArray = eraseLonelyPixel (imageArray)
	# effacer la couleur des coins
	lenHeight = len (imageArray)
	rangeHeight = range (1, lenHeight -1)
	lenWidth = len (imageArray[0])
	rangeWidth = range (lenWidth)
	for h in rangeHeight:
		w=1
		while w< lenWidth and imageArray[h][w] == imageArray[h][0]:
			imageArray[h][w] =0
			w+=1
		w= lenWidth -2
		while w>=0 and imageArray[h][w] == imageArray[h][-1]:
			imageArray[h][w] =0
			w-=1
	for w in rangeWidth:
		h=1
		while h< lenHeight and (imageArray[h][w] == imageArray[0][w] or imageArray[h][w] ==0):
			imageArray[h][w] =0
			h+=1
		imageArray[0][w] =0
		h= lenHeight -2
		while h>=0 and (imageArray[h][w] == imageArray[-1][w] or imageArray[h][w] ==0):
			imageArray[h][w] =0
			h-=1
		imageArray[-1][w] =0
	rangeHeight = range (lenHeight)
	for h in rangeHeight:
		imageArray[h][0] =0
		imageArray[h][-1] =0
	# effacer l'intérieur
	colorArea = imageArray !=0
	imageArray[colorArea] =255
	# remplir les boucles blanches incluses dans du noir
	rangeHeight = range (lenHeight)
	rangeWidth = range (lenWidth)
	halfHeight = int (lenHeight /2)
	halfWidth = int (lenWidth /2)
	for h in rangeHeight:
		w= halfWidth
		while w>=0 and imageArray[h][w] ==255: w-=1
		while w>=0:
			if imageArray[h][w] ==255: imageArray[h][w] =0
			w-=1
		w= halfWidth
		while w< lenWidth and imageArray[h][w] ==255: w+=1
		while w< lenWidth:
			if imageArray[h][w] ==255: imageArray[h][w] =0
			w+=1
	for w in rangeWidth:
		h= halfHeight
		while h>=0 and imageArray[h][w] ==255: h-=1
		while h>=0:
			if imageArray[h][w] ==255: imageArray[h][w] =0
			h-=1
		h= halfHeight
		while h< lenHeight and imageArray[h][w] ==255: h+=1
		while h< lenHeight:
			if imageArray[h][w] ==255: imageArray[h][w] =0
			h+=1
	"""
	"""
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

imageName = 'b/test.bmp'
findBorder (imageName)