#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
from PIL import Image, ImageDraw
import cv2
import fileLocal
from imgModif import openImage
import loggerFct as log
"""
créer un gif animé carré afin de mettre une grande image sur instagram

python -m pip install --upgrade pip
python -m pip install --upgrade numpy
python -m pip install --upgrade Pillow

https://pillow.readthedocs.io/en/latest/handbook/tutorial.html
The format attribute identifies the source of an image. If the image was not read from a file, it is set to None.
The size attribute is a 2-tuple containing width and height (in pixels).
The mode attribute defines the number and names of the bands in the image, and also the pixel type and depth.
Common modes are “L” (luminance) for greyscale images, “RGB” for true color images, and “CMYK” for pre-press images.

mode L: nuance de gris
mode RGB: couleurs

https://pypi.org/project/opencv-python/#installation-and-usage

pip install opencv-contrib-python

https://stackoverflow.com/questions/64506236/pil-image-list-into-a-video-slide-with-cv2-videowriter
https://stackoverflow.com/questions/64764601/creating-an-mp4-file-from-images-using-video-write-in-opencv
https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
"""
def creerGif (images):
	imageRef = images.pop(0)
	imageRef.save (nomGif, save_all=True, append_images=images, duration=1, loop=0)

def squareVideo (nomCarre, width, height, imageOriginal):
	nomCarre = nomCarre +'-anim.mp4'
	images =[]
	imagesReverse =[]
	# la largeur est plus grande que la hauteur
	if width > height:
		difference = width - height
		diffrange = range (0, difference, 5)
		for x in diffrange:
			fragment = imageOriginal.crop ((x,0, x+height, height))
			imageTmp = Image.new ('RGB', (height, height))
			imageTmp.paste (fragment)
			images.append (imageTmp)
			imagesReverse.append (imageTmp)
	# la hauteur est plus grande que la largeur
	else:
		difference = height - width
		diffrange = range (0, difference, 5)
		imagesReverse =[]
		for y in diffrange:
			fragment = imageOriginal.crop ((0,y, width, y+width))
			imageTmp = Image.new ('RGB', (width, width))
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
	if width < height: video = cv2.VideoWriter (nomCarre, fourcc, 30, (width, width))
	else: video = cv2.VideoWriter (nomCarre, fourcc, 30, (height, height))
	for img in images: video.write (cv2.cvtColor (numpy.array (img), cv2.COLOR_RGB2BGR))
	video.release()

def squarePictureComputeColors (color, pixel):
	color[0] += pixel[0]
	color[1] += pixel[1]
	color[2] += pixel[2]
	return color

def drawBgStripes (imageArray, width, height, horizontal=True):
	# dessiner la nouvelle image
	imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
	drawing = ImageDraw.Draw (imageObj)
	# la largeur est plus grande que la hauteur
	if horizontal:
		rangeBord = range (width)
		lengthalf = int (height /2)
		for p in rangeBord:
			drawing.rectangle (((p, 0), (p+1, lengthalf)), fill=( imageArray[0][p][0], imageArray[0][p][1], imageArray[0][p][2] ))
			drawing.rectangle (((p, lengthalf), (p+1, height)), fill=( imageArray[-1][p][0], imageArray[-1][p][1], imageArray[-1][p][2] ))
	# la hauteur est plus grande que la largeur
	else:
		rangeBord = range (height)
		lengthalf = int (width /2)
		for p in rangeBord:
			drawing.rectangle (((0, p), (lengthalf, p+1)), fill=( imageArray[p][0][0], imageArray[p][0][1], imageArray[p][0][2] ))
			drawing.rectangle (((lengthalf, p), (width, p+1)), fill=( imageArray[p][-1][0], imageArray[p][-1][1], imageArray[p][-1][2] ))
	drawing = ImageDraw.Draw (imageObj)
	return imageObj

def drawBgMix (imageArray, width, height, horizontal=True):
	# calculer la couleur moyenne de chaque coté
	colorA =[ 0,0,0 ]
	colorB =[ 0,0,0 ]
	if horizontal:
		rangeBord = range (width)
		for i in rangeBord:
			colorA[0] += imageArray[0][i][0]
			colorA[1] += imageArray[0][i][1]
			colorA[2] += imageArray[0][i][2]
			colorB[0] += imageArray[-1][i][0]
			colorB[1] += imageArray[-1][i][1]
			colorB[2] += imageArray[-1][i][2]
		colorA[0] = int (colorA[0] / width)
		colorA[1] = int (colorA[1] / width)
		colorA[2] = int (colorA[2] / width)
		colorB[0] = int (colorB[0] / width)
		colorB[1] = int (colorB[1] / width)
		colorB[2] = int (colorB[2] / width)
	else:
		rangeBord = range (height)
		for i in rangeBord:
			colorA[0] += imageArray[i][0][0]
			colorA[1] += imageArray[i][0][1]
			colorA[2] += imageArray[i][0][2]
			colorB[0] += imageArray[i][-1][0]
			colorB[1] += imageArray[i][-1][1]
			colorB[2] += imageArray[i][-1][2]
		colorA[0] = int (colorA[0] / height)
		colorA[1] = int (colorA[1] / height)
		colorA[2] = int (colorA[2] / height)
		colorB[0] = int (colorB[0] / height)
		colorB[1] = int (colorB[1] / height)
		colorB[2] = int (colorB[2] / height)
	# dessiner la nouvelle image
	imageObj = Image.new (mode='RGB', size=(width, height), color=(colorB[0], colorB[1], colorB[2]))
	drawing = ImageDraw.Draw (imageObj)
	# la largeur est plus grande que la hauteur
	if horizontal:
		lengthalf = int (height /2)
		drawing.rectangle (((0,0), (width, lengthalf)), fill=( colorA[0], colorA[1], colorA[2] ))
	# la hauteur est plus grande que la largeur
	else:
		lengthalf = int (width /2)
		drawing.rectangle (((0,0), (lengthalf, height)), fill=( colorA[0], colorA[1], colorA[2] ))
	drawing = ImageDraw.Draw (imageObj)
	return imageObj

def squarePicture (nomCarre, width, height, imageOriginal, drawBgfonc, ratio):
	nomCarre = nomCarre +'-rectan.jpg'
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x 4 numpy array
	# red, green, blue = imageArray.T	# Temporarily unpack the bands for readability
	# la largeur est plus grande que la hauteur
	if width > height:
		heightTmp = ratio * width
		heightNew = int (heightTmp)
		imageObj = drawBgfonc (imageArray, width, heightNew, True)
		wStripe = int ((heightNew - height) /2)
		imageObj.paste (imageOriginal, (0, wStripe))
	# la hauteur est plus grande que la largeur
	else:
		widthTmp = ratio * height
		widthNew = int (widthTmp)
		imageObj = drawBgfonc (imageArray, widthNew, height, False)
		wStripe = int ((widthNew - width) /2)
		imageObj.paste (imageOriginal, (wStripe, 0))
	imageObj.save (nomCarre)

if len (argv) <2: print ("entrez le nom de l'image")
else:
	# récupérer l'image originale
	nomCarre, imageOriginal = openImage (argv[1])
	width = imageOriginal.size[0]
	height = imageOriginal.size[1]
	ratio =1
	ratioB =1
	if len (argv) >2: ratio = int (argv[2])
	if len (argv) >3: ratioB = int (argv[3])
	if ratio < ratioB: ratio = ratio / ratioB
	else: ratio = ratioB / ratio
	if width > height:
		ratioB = height / width
		if ratioB == ratio: print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
		elif ratioB >= 0.9 * ratio: print ("votre image est presque au bon ratio, vous n'avez pas besoin de la transformer")
		elif ratioB <0.3: squareVideo (nomCarre, width, height, imageOriginal)
		else: squarePicture (nomCarre, width, height, imageOriginal, drawBgStripes, ratio)
	else:
		ratioB = width / height
		if ratioB == ratio: print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
		elif ratioB >= 0.9 * ratio: print ("votre image est presque au bon ratio, vous n'avez pas besoin de la transformer")
		elif ratioB <0.3: squareVideo (nomCarre, width, height, imageOriginal)
		else: squarePicture (nomCarre, width, height, imageOriginal, drawBgStripes, ratio)