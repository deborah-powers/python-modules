#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
from PIL import Image, ImageDraw
import cv2
import fileLocal
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
images =[]
imagesReverse =[]

def frameX (x):
	fragment = imageOriginal.crop ((x,0, x+height, height))
	imageTmp = Image.new ('RGB', (height, height))
	imageTmp.paste (fragment)
	return imageTmp

def frameY (y):
	fragment = imageOriginal.crop ((0,y, width, y+width))
	imageTmp = Image.new ('RGB', (width, width))
	imageTmp.paste (fragment)
	return imageTmp

def frameListX():
	# width > height
	if height / width >= 0.8:
		print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
		return []
	difference = width - height
	diffrange = range (0, difference, 5)
	images =[]
	imagesReverse =[]
	for x in diffrange:
		imageTmp = frameX (x)
		images.append (imageTmp)
		imagesReverse.append (imageTmp)
	imagesReverse.reverse()
	imagesReverse.pop (0)
	images.extend (imagesReverse)
	return images

def frameListY():
	# height > width
	if width / height >= 0.8:
		print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
		return []
	difference = height - width
	diffrange = range (0, difference, 5)
	images =[]
	imagesReverse =[]
	for y in diffrange:
		imageTmp = frameY (y)
		images.append (imageTmp)
		imagesReverse.append (imageTmp)
	imagesReverse.reverse()
	imagesReverse.pop (0)
	images.extend (imagesReverse)
	return images

def creerGif (images):
	imageRef = images.pop(0)
	imageRef.save (nomGif, save_all=True, append_images=images, duration=1, loop=0)

def creerMp4 (images, size):
	fourcc = cv2.VideoWriter_fourcc (*'avc1')
	video = cv2.VideoWriter (nomMp4, fourcc, 30, (size, size))
	for img in images: video.write (cv2.cvtColor (numpy.array (img), cv2.COLOR_RGB2BGR))
	video.release()

def squarePicture (nomImg):
	# trouver le nom
	nomImg = fileLocal.shortcut (nomImg)
	d= nomImg.rfind ('.')
	nomCarre = nomImg[:d] +'-carre.bmp'
	# récupérer l'image
	imageOriginal = Image.open (nomImg)
	width = imageOriginal.size[0]
	height = imageOriginal.size[1]
	# calculer la couleur des bords
	colorA =[ 0,0,0 ]
	colorB =[ 0,0,0 ]
	imageArray = numpy.array (imageOriginal)	# "data" is a height x width x 4 numpy array
	red, green, blue = imageArray.T	# Temporarily unpack the bands for readability
	if width == height: print ("votre image est déjà un carré, vous n'avez pas besoin de la transformer")
	# la largeur est plus grande que la hauteur
	elif width > height:
		if height / width >=0.8: print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
		else:
			# calculer les couleurs des bords
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
			# dessiner la nouvelle image
			imageObj = Image.new ('RGBA', (width, width))
			drawing = ImageDraw.Draw (imageObj)
			wStripe = int ((width - height) /2)
			imageObj.paste (imageOriginal, (0, wStripe))
			drawing.rectangle (((0,0), (width, wStripe)), fill=(colorA[0], colorA[1], colorA[2]))
			drawing.rectangle (((0, height + wStripe), (width, height + 2* wStripe)), fill=(colorB[0], colorB[1], colorB[2]))
	# la hauteur est plus grande que la largeur
	elif width / height >= 0.8: print ("votre image est presque carrée, vous n'avez pas besoin de la transformer")
	else:
		# calculer les couleurs des bords
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
		imageObj = Image.new ('RGBA', (height, height))
		drawing = ImageDraw.Draw (imageObj)
		wStripe = int ((height - width) /2)
		imageObj.paste (imageOriginal, (wStripe, 0))
		drawing.rectangle (((0,0), (wStripe, height)), fill=( 100,100,100 ))
		drawing.rectangle (((width + wStripe, 0), (width + 2* wStripe, height)), fill=( 100,100,100 ))
	imageObj.save (nomCarre)

if len (argv) <2: print ("entrez le nom de l'image")
elif len (argv) ==2: squarePicture (argv[1])
else:
	# créer un gif
	# récupérer le fichier
	nomImg = argv[1]
	nomImg = fileLocal.shortcut (nomImg)
	d= nomImg.rfind ('.')
	# nomGif = nomImg[:d] +'-anim.gif'
	nomMp4 = nomImg[:d] +'-anim.mp4'
	# données de l'image originale
	imageOriginal = Image.open (nomImg)
	width = imageOriginal.size[0]
	height = imageOriginal.size[1]
	# traitement de l'image
	if width == height: print ("votre image %s est déjà un carré, vous n'avez pas besoin de la transformer")
	elif width > height:
		images = frameListX()
		if images: creerMp4 (images, height)
	else:
		images = frameListY()
		if images: creerMp4 (images, width)

