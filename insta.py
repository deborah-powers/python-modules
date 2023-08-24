#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
from PIL import Image, ImageDraw
import cv2
import fileLcl
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

if len (argv) <2: print ("entrez le nom de l'image")
else:
	# récupérer le fichier
	nomImg = argv[1]
	nomImg = fileLcl.shortcut (nomImg)
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

