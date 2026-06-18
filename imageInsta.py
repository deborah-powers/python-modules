#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
from PIL import Image, ImageOps, ImageDraw
import cv2
from imageCls import ImageFile

def insta (self, drawBgfonc, ratio=1.0):
	""" ratio = largeur / hauteur """
	ratioImg = self.width / self.height
	posW =0
	posH =0
	widthNew = self.width
	heightNew = self.height
	if ratioImg < ratio:
		# rajouter bandes latérales
		widthNew = int (self.width * ratio / ratioImg)
		posW = int ((widthNew - self.width) /2.0)
	elif ratioImg > ratio:
		# rajouter bandes haut et bas
		heightNew = int (self.height * ratioImg / ratio)
		posH = int ((heightNew - self.height) /2.0)
	else:
		print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
		return False
#	self.title = self.title +' insta'
	imageObj = None
	if drawBgfonc == 'stripes': imageObj = self.drawBgStripes (widthNew, heightNew)
	elif drawBgfonc == 'average': imageObj = self.drawBgAverage (widthNew, heightNew)
	elif drawBgfonc == 'reflet': imageObj = self.drawBgReflet (widthNew, heightNew)
	else: imageObj = self.drawBgAverage (widthNew, heightNew)
	imageObj.paste (self.image, (posW, posH))
	drawing = ImageDraw.Draw (imageObj)
	self.setImage (imageObj)
	return True

def drawBgStripes (self, width, height):
	imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
	drawing = ImageDraw.Draw (imageObj)
	if self.width == width:
		# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
		height = int (height /2.0)
		bord = self.image.crop ((0,0, self.width, 1))
		bord = bord.resize ((bord.size[0], height), Image.Resampling.LANCZOS)
		imageObj.paste (bord, (0,0))
		bord = self.image.crop ((0, self.height -1, self.width, self.height))
		bord = bord.resize ((bord.size[0], height), Image.Resampling.LANCZOS)
		imageObj.paste (bord, (0,height))
	else:
		# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
		width = int (width /2.0)
		bord = self.image.crop ((0,0,1, self.height))
		bord = bord.resize ((width, bord.size[1]), Image.Resampling.LANCZOS)
		imageObj.paste (bord, (0,0))
		bord = self.image.crop ((self.width -1,0, self.width, self.height))
		bord = bord.resize ((width, bord.size[1]), Image.Resampling.LANCZOS)
		imageObj.paste (bord, (width,0))
	return imageObj

def drawBgReflet (self, width, height):
	imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
	drawing = ImageDraw.Draw (imageObj)
	if self.width == width:
		# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
		bandSize = int ((height - self.height) /2.0)
		height = int (height /2.0)
		bord = self.image.crop ((0,0, self.width, bandSize))
		bord = ImageOps.flip (bord)
		imageObj.paste (bord, (0,0))
		bord = self.image.crop ((0, self.height - bandSize, self.width, self.height))
		bord = ImageOps.flip (bord)
		imageObj.paste (bord, (0, imageObj.size[1] - bandSize))
	else:
		# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
		bandSize = int ((width - self.width) /2.0)
		width = int (width /2.0)
		bord = self.image.crop ((0,0, bandSize, self.height))
		bord = ImageOps.mirror (bord)
		imageObj.paste (bord, (0,0))
		bord = self.image.crop ((self.width - bandSize, 0, self.width, self.height))
		bord = ImageOps.mirror (bord)
		imageObj.paste (bord, (imageObj.size[0] - bandSize, 0))
	return imageObj

def drawBgAverage (self, width, height):
	imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
	drawing = ImageDraw.Draw (imageObj)
	self.array = numpy.array (self.image)
	colorA =[ 0,0,0 ]
	colorB =[ 0,0,0 ]
	if self.width == width:
		# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
		height = int (height /2.0)
		rangeBord = range (width)
		for i in rangeBord:
			colorA[0] += self.array[0][i][0]
			colorA[1] += self.array[0][i][1]
			colorA[2] += self.array[0][i][2]
			colorB[0] += self.array[-1][i][0]
			colorB[1] += self.array[-1][i][1]
			colorB[2] += self.array[-1][i][2]
		colorA[0] = int (colorA[0] / width)
		colorA[1] = int (colorA[1] / width)
		colorA[2] = int (colorA[2] / width)
		colorB[0] = int (colorB[0] / width)
		colorB[1] = int (colorB[1] / width)
		colorB[2] = int (colorB[2] / width)
		bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorA))
		imageObj.paste (bord, (0,0))
		bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorB))
		imageObj.paste (bord, (0,height))
	else:
		# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
		width = int (width /2.0)
		rangeBord = range (height)
		for i in rangeBord:
			colorA[0] += self.array[i][0][0]
			colorA[1] += self.array[i][0][1]
			colorA[2] += self.array[i][0][2]
			colorB[0] += self.array[i][-1][0]
			colorB[1] += self.array[i][-1][1]
			colorB[2] += self.array[i][-1][2]
		colorA[0] = int (colorA[0] / height)
		colorA[1] = int (colorA[1] / height)
		colorA[2] = int (colorA[2] / height)
		colorB[0] = int (colorB[0] / height)
		colorB[1] = int (colorB[1] / height)
		colorB[2] = int (colorB[2] / height)
		bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorA))
		imageObj.paste (bord, (0,0))
		bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorB))
		imageObj.paste (bord, (width,0))
	return imageObj

def squareVideo (self):
	videoTitle = self.path + self.title +' anim.mp4'
	images =[]
	imagesReverse =[]
	# la largeur est plus grande que la hauteur
	if self.width > self.height:
		difference = self.width - self.height
		diffrange = range (0, difference, 5)
		for x in diffrange:
			fragment = self.image.crop ((x,0, x+ self.height, self.height))
			imageTmp = Image.new ('RGB', (self.height, self.height))
			imageTmp.paste (fragment)
			images.append (imageTmp)
			imagesReverse.append (imageTmp)
	# la hauteur est plus grande que la largeur
	else:
		difference = self.height - self.width
		diffrange = range (0, difference, 5)
		imagesReverse =[]
		for y in diffrange:
			fragment = self.image.crop ((0,y, self.width, y+ self.width))
			imageTmp = Image.new ('RGB', (self.width, self.width))
			imageTmp.paste (fragment)
			images.append (imageTmp)
			imagesReverse.append (imageTmp)
	# préparer les images
	imagesReverse.reverse()
	imagesReverse.pop (0)
	images.extend (imagesReverse)
	# enregistrer la video
	fourcc = cv2.VideoWriter_fourcc (*'avc1')
	video = None
	if self.width < self.height: video = cv2.VideoWriter (videoTitle, fourcc, 30, (self.width, self.width))
	else: video = cv2.VideoWriter (videoTitle, fourcc, 30, (self.height, self.height))
	for img in images: video.write (cv2.cvtColor (numpy.array (img), cv2.COLOR_RGB2BGR))
	video.release()

setattr (ImageFile, 'drawBgAverage', drawBgAverage)
setattr (ImageFile, 'drawBgStripes', drawBgStripes)
setattr (ImageFile, 'drawBgReflet', drawBgReflet)
setattr (ImageFile, 'squareVideo', squareVideo)
setattr (ImageFile, 'insta', insta)
