#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
from PIL import Image, ImageDraw
import fileLcl

"""
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
"""
imageRef24 = 'b/python/couleurs-24.bmp'
imageRef256 = 'b/python/couleurs-256.bmp'
imageOriginale = 'b/couleurs-247.bmp'
imageFinale = 'b/couleurs-247 bis.bmp'

couleursConnues =[ (0, 0, 0), (0, 0, 64), (0, 0, 128), (0, 0, 192), (0, 0, 255), (0, 32, 64), (0, 32, 128), (0, 32, 192), (0, 64, 0), (0, 64, 64), (0, 64, 128), (0, 64, 192), (0, 96, 0), (0, 96, 64), (0, 96, 128), (0, 96, 192), (0, 128, 0), (0, 128, 64), (0, 128, 128), (0, 128, 192), (0, 160, 0), (0, 160, 64), (0, 160, 128), (0, 160, 192), (0, 192, 0), (0, 192, 64), (0, 192, 128), (0, 192, 192), (0, 224, 0), (0, 224, 64), (0, 224, 128), (0, 255, 0), (0, 255, 255), (32, 0, 64), (32, 0, 128), (32, 0, 192), (32, 32, 64), (32, 32, 128), (32, 32, 192), (32, 64, 0), (32, 64, 64), (32, 64, 128), (32, 64, 192), (32, 96, 0), (32, 96, 64), (32, 96, 128), (32, 96, 192), (32, 128, 0), (32, 128, 64), (32, 128, 128), (32, 128, 192), (32, 160, 0), (32, 160, 64), (32, 160, 128), (32, 160, 192), (32, 192, 0), (32, 192, 64), (32, 192, 128), (32, 192, 192), (32, 224, 0), (32, 224, 64), (32, 224, 128), (64, 0, 64), (64, 0, 128), (64, 0, 192), (64, 32, 0), (64, 32, 64), (64, 32, 128), (64, 32, 192), (64, 64, 0), (64, 64, 64), (64, 64, 128), (64, 64, 192), (64, 96, 0), (64, 96, 64), (64, 96, 128), (64, 96, 192), (64, 128, 0), (64, 128, 64), (64, 128, 128), (64, 128, 192), (64, 160, 0), (64, 160, 64), (64, 160, 128), (64, 160, 192), (64, 192, 0), (64, 192, 64), (64, 192, 128), (64, 192, 192), (64, 224, 0), (64, 224, 64), (64, 224, 128), (96, 0, 64), (96, 0, 128), (96, 0, 192), (96, 32, 0), (96, 32, 64), (96, 32, 128), (96, 32, 192), (96, 64, 0), (96, 64, 64), (96, 64, 128), (96, 64, 192), (96, 96, 0), (96, 96, 64), (96, 96, 128), (96, 96, 192), (96, 128, 0), (96, 128, 64), (96, 128, 128), (96, 128, 192), (96, 160, 0), (96, 160, 64), (96, 160, 128), (96, 160, 192), (96, 192, 0), (96, 192, 64), (96, 192, 128), (96, 192, 192), (96, 224, 0), (96, 224, 64), (96, 224, 128), (128, 0, 0), (128, 0, 64), (128, 0, 128), (128, 0, 192), (128, 32, 0), (128, 32, 64), (128, 32, 128), (128, 32, 192), (128, 64, 0), (128, 64, 64), (128, 64, 128), (128, 64, 192), (128, 96, 0), (128, 96, 64), (128, 96, 128), (128, 96, 192), (128, 128, 0), (128, 128, 64), (128, 128, 128), (128, 128, 192), (128, 160, 0), (128, 160, 64), (128, 160, 128), (128, 160, 192), (128, 192, 0), (128, 192, 64), (128, 192, 128), (128, 192, 192), (128, 224, 0), (128, 224, 64), (128, 224, 128), (160, 0, 64), (160, 0, 128), (160, 0, 192), (160, 32, 0), (160, 32, 64), (160, 32, 128), (160, 32, 192), (160, 64, 0), (160, 64, 64), (160, 64, 128), (160, 64, 192), (160, 96, 0), (160, 96, 64), (160, 96, 128), (160, 96, 192), (160, 128, 0), (160, 128, 64), (160, 128, 128), (160, 128, 192), (160, 160, 0), (160, 160, 64), (160, 160, 128), (160, 160, 164), (160, 160, 192), (160, 192, 0), (160, 192, 64), (160, 192, 128), (160, 192, 192), (160, 224, 0), (160, 224, 64), (160, 224, 128), (166, 202, 240), (192, 0, 64), (192, 0, 128), (192, 0, 192), (192, 32, 0), (192, 32, 64), (192, 32, 128), (192, 32, 192), (192, 64, 0), (192, 64, 64), (192, 64, 128), (192, 64, 192), (192, 96, 0), (192, 96, 64), (192, 96, 128), (192, 96, 192), (192, 128, 0), (192, 128, 64), (192, 128, 128), (192, 128, 192), (192, 160, 0), (192, 160, 64), (192, 160, 128), (192, 160, 192), (192, 192, 0), (192, 192, 64), (192, 192, 128), (192, 192, 192), (192, 220, 192), (192, 224, 0), (192, 224, 64), (192, 224, 128), (224, 0, 64), (224, 0, 128), (224, 0, 192), (224, 32, 0), (224, 32, 64), (224, 32, 128), (224, 32, 192), (224, 64, 0), (224, 64, 64), (224, 64, 128), (224, 64, 192), (224, 96, 0), (224, 96, 64), (224, 96, 128), (224, 96, 192), (224, 128, 0), (224, 128, 64), (224, 128, 128), (224, 128, 192), (224, 160, 0), (224, 160, 64), (224, 160, 128), (224, 160, 192), (224, 192, 0), (224, 192, 64), (224, 192, 128), (224, 224, 0), (224, 224, 64), (224, 224, 128), (255, 0, 0), (255, 0, 255), (255, 251, 240), (255, 255, 0), (255, 255, 255) ]

imageOriginale = fileLcl.shortcut (imageOriginale)
imageFinale = fileLcl.shortcut (imageFinale)

def trier (couleurs):
	couleurs.sort()
	print (len (couleurs))
	print (couleurs)

def dessinerCarres_va (couleurs):
	imageObj = Image.new ('RGBA', (1+40* len (couleurs), 41))
	drawing = ImageDraw.Draw (imageObj)
	p=1
	for couleur in couleurs:
		drawing.rectangle (((p,1), (p+38, 39)), fill=couleur)
		p+=40
	imageObj.save (imageFinale)

def dessinerCarres256 (couleurs):
	imageObj = Image.new ('RGBA', (160, 160))
	drawing = ImageDraw.Draw (imageObj)
	x=0
	y=0
	for couleur in couleurs:
		drawing.rectangle (((x,y), (x+9, y+9)), fill=couleur)
		x+=10
		if x>=160:
			x=0
			y+=10
	imageObj.save (imageFinale)

def creerCouleurs():
	# dessiner l'image
	imageObj = Image.new ('RGBA', (3240, 180))
	drawing = ImageDraw.Draw (imageObj)
	x=0
	y=0
	# créer les couleurs
	print ('récupérer les couleurs')
	r=7
	v=7
	b=7
	while r<256:
		v=0
		while v<256:
			b=0
			while b<256:
				print (r,v,b)
				drawing.rectangle (((x,y), (x+10, y+10)), fill=( r,v,b ))
				x+=10
				if x>=3240:
					x=0
					y+=10
				b=b+15
			v=v+15
		r=r+15
	print ("enregistrer l'image")
	imageObj.save ('C:\\Users\\dpowers-consultant01\\Desktop\\couleurs-247.bmp')
	print ('fin du batch des couleurs')

def traiterImage():
	# éffacer les couleurs déjà connues
	imageObj = Image.open (imageOriginale)
	imageObj = imageObj.convert ('RGBA')
	# imageObj.format = 'BMP'
	data = numpy.array (imageObj)		# "data" is a height x width x 4 numpy array
	red, green, blue, alpha = data.T	# Temporarily unpack the bands for readability
	for r,v,b in couleursConnues:
		colorArea = (red == r) & (green == v) & (blue == b)
		data[..., :-1][colorArea.T] = (255, 255, 255)
	imageBis = Image.fromarray (data)
	# isoler les couleurs inconnues
	couleursNb = imageBis.getcolors (imageBis.size[0] * imageBis.size[1])
	couleurs =[]
	for nb, couleur in couleursNb:
		if (couleur[0], couleur[1], couleur[2]) not in couleurs and (couleur[0], couleur[1], couleur[2]) != (255, 255, 255):
			couleurs.append ((couleur[0], couleur[1], couleur[2]))
	if couleurs:
		trier (couleurs)
		dessinerCarres256 (couleurs)
	else: print ('aucune couleurs')

traiterImage()

def effacerCouleurs():
	imageObj = Image.open (imageOriginale)
	imageObj = imageObj.convert ('RGBA')
	imageObj.format = 'BMP'
	data = numpy.array (imageObj)		# "data" is a height x width x 4 numpy array
	red, green, blue, alpha = data.T	# Temporarily unpack the bands for readability
	for r,v,b in couleursConnues:
		colorArea = (red == r) & (green == v) & (blue == b)
		data[..., :-1][colorArea.T] = (257, 257, 257)
	imageBis = Image.fromarray (data)
	imageBis.save (imageFinale)

def extraireCouleurs():
	imageObj = Image.open (imageOriginale)
	imageObj = imageObj.convert ('RGBA')
	imageObj.format = 'BMP'
	couleursNb = imageObj.getcolors()
	couleurs =[]
	for nb, couleur in couleursNb:
		if (couleur[0], couleur[1], couleur[2]) not in couleurs: couleurs.append ((couleur[0], couleur[1], couleur[2]))
		else: print ('oui')
	couleurs.sort()
	print (couleurs)

def testDessiner():
	imageObj = Image.new ('RGBA', (400, 100))
	box = (50, 50, 60, 40)
	drawing = ImageDraw.Draw (imageObj)
	drawing.rectangle (((50, 50), (60, 80)), fill='red')
	drawing.text ((40, 70), 'un message', fill='orange')
	imageObj.save (imageFinale)

def testB():
	# remplacer une couleur
	imageObj = Image.open (imageOriginale)
	imageObj = imageObj.convert ('RGBA')
	imageObj.format = 'BMP'
	data = numpy.array (imageObj)		# "data" is a height x width x 4 numpy array
	red, green, blue, alpha = data.T	# Temporarily unpack the bands for readability
	colorArea = (red == 0) & (blue == 0) & (green == 0)
	data[..., :-1][colorArea.T] = (0, 257, 0)
	imageBis = Image.fromarray (data)
	imageBis.save (imageFinale)

def testA():
	# passer l'image en nuance de gris
	imageObj = Image.open (imageOriginale)
	print (imageObj.format, imageObj.size, imageObj.mode)
	imageObj = imageObj.convert ('L')
	imageObj.format = 'BMP'
	print (imageObj.format, imageObj.size, imageObj.mode)
	imageObj.save (imageFinale)
