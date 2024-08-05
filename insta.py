#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
from PIL import Image, ImageDraw
import cv2
import fileLocal
from imgModif import openImage
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

def squarePictureDraw (colorA, colorB, length, horizontal=True):
	# couleurs moyenne
	colorA[0] = int (colorA[0] / length)
	colorA[1] = int (colorA[1] / length)
	colorA[2] = int (colorA[2] / length)
	colorB[0] = int (colorB[0] / length)
	colorB[1] = int (colorB[1] / length)
	colorB[2] = int (colorB[2] / length)
	lengthalf = int (length /2)
	# dessiner la nouvelle image
	imageObj = Image.new (mode='RGB', size=(length, length), color=(colorB[0], colorB[1], colorB[2]))
	drawing = ImageDraw.Draw (imageObj)
	# la largeur est plus grande que la hauteur
	if horizontal: drawing.rectangle (((0,0), (length, lengthalf)), fill=( colorA[0], colorA[1], colorA[2] ))
	# la hauteur est plus grande que la largeur
	else: drawing.rectangle (((0,0), (lengthalf, length)), fill=( colorA[0], colorA[1], colorA[2] ))
	drawing = ImageDraw.Draw (imageObj)
	return imageObj

def squarePicture (nomCarre, width, height, imageOriginal):
	nomCarre = nomCarre +'-carre.jpg'
	# calculer la couleur des bords
	colorA =[ 0,0,0 ]
	colorB =[ 0,0,0 ]
	imageArray = numpy.array (imageOriginal)	# imageArray is a height x width x 4 numpy array
	# red, green, blue = imageArray.T	# Temporarily unpack the bands for readability
	# la largeur est plus grande que la hauteur
	if width > height:
		# calculer les couleurs des bords
		rangeBord = range (width)
		for i in rangeBord:
			colorA = squarePictureComputeColors (colorA, imageArray[0][i])
			colorB = squarePictureComputeColors (colorB, imageArray[-1][i])
		# dessiner la nouvelle image
		imageObj = squarePictureDraw (colorA, colorB, width, True)
		wStripe = int ((width - height) /2)
		imageObj.paste (imageOriginal, (0, wStripe))
	# la hauteur est plus grande que la largeur
	else:
		# calculer les couleurs des bords
		rangeBord = range (height)
		for i in rangeBord:
			colorA = squarePictureComputeColors (colorA, imageArray[i][0])
			colorB = squarePictureComputeColors (colorB, imageArray[i][-1])
		# dessiner la nouvelle image
		imageObj = squarePictureDraw (colorA, colorB, height, False)
		wStripe = int ((height - width) /2)
		imageObj.paste (imageOriginal, (wStripe, 0))
	imageObj.save (nomCarre)

if len (argv) <2: print ("entrez le nom de l'image")
else:
	# récupérer l'image originale
	nomCarre, imageOriginal = openImage (argv[1])
	width = imageOriginal.size[0]
	height = imageOriginal.size[1]
	# vérification sur ses dimensions
	if width == height: print ("votre image est déjà un carré, vous n'avez pas besoin de la transformer")
	elif width > height:
		if height / width >=0.9: print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
		elif height / width <0.5: squareVideo (nomCarre, width, height, imageOriginal)
		else: squarePicture (nomCarre, width, height, imageOriginal)
	elif width / height >=0.9: print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
	elif width / height <0.5: squareVideo (nomCarre, width, height, imageOriginal)
	else: squarePicture (nomCarre, width, height, imageOriginal)