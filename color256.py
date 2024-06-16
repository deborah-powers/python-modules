#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
from PIL import Image, ImageDraw
import fileLocal
from color256dep import couleursConnues, couleursJetees

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
imageOriginale = 'b/photo.bmp'
imageFinale = 'b/photo bis.bmp'


imageOriginale = fileLocal.shortcut (imageOriginale)
imageFinale = fileLocal.shortcut (imageFinale)

def drawColors_va (colorList):
	# enregistrer l'image
	lenX = 160
	lenY = 160
	imageFin = Image.new ('RGBA', (lenX, lenY))
	imageFin.format = 'BMP'
	drawing = ImageDraw.Draw (imageFin)
	x=0
	y=0
	colorList.sort()
	for couleur in colorList:
		drawing.rectangle (((x,y), (x+9, y+9)), fill=couleur)
		x+=10
		if x>= lenX:
			x=0
			y+=10
	imageFin.save (imageFinale)

def drawColors (fileName, colorList):
	# enregistrer l'image
	lenX = 160
	lenY = 160
	imageFin = Image.new ('RGBA', (lenX, lenY))
	imageFin.format = 'BMP'
	print ('fin', imageFin)
	drawing = ImageDraw.Draw (imageFin)
	print ('draw', drawing)
	x=0
	y=0
	colorList.sort()
	for couleur in colorList:
		drawing.rectangle (((x,y), (x+9, y+9)), fill=couleur)
		x+=10
		if x>= lenX:
			x=0
			y+=10
	imageFin.save (fileName)

def newColors():
	couleurs =[]
	colRangeFull = range (0,256,3)
	colRange = range (5,256,15)
	for r in colRange:
		for v in colRange:
			for b in colRangeFull:
				if (r,v,b) not in couleursConnues and (r,v,b) not in couleursJetees and (r,v,b) not in couleurs:
					print ('nouvelle', (r,v,b))
					couleurs.append (( r,v,b ))
	couleurs.sort()
	print (couleurs)
	drawColors (couleurs)

def traiterImage():
	imageObj = Image.open (imageOriginale)
	imageObj = imageObj.convert ('RGBA')
	# éffacer les couleurs déjà connues
	data = numpy.array (imageObj)		# "data" is a height x width x 4 numpy array
	print ('datas', data.__class__)
	red, green, blue, alpha = data.T	# Temporarily unpack the bands for readability
	print ('éffacer les couleurs déjà connues')
	for r,v,b in couleursConnues:
		colorArea = (red == r) & (green == v) & (blue == b)
		data[..., :-1][colorArea.T] = (255, 255, 255)
	imageBis = Image.fromarray (data)
	print ('bis\n', imageBis)
	drawColors (imageFinale, couleursConnues)

def rangerImage (nom):
	nom = 'C:\\Users\\LENOVO\\Desktop\\' + nom + '.bmp'
	imageObj = Image.open (nom)
	imageObj = imageObj.convert ('RGBA')
	data = numpy.array (imageObj)		# "data" is a height x width x 4 numpy array
	red, green, blue, alpha = data.T	# Temporarily unpack the bands for readability
	imageBis = Image.fromarray (data)
	# isoler les couleurs inconnues
	print ('isoler les couleurs inconnues')
	couleursNb = imageBis.getcolors (imageBis.size[0] * imageBis.size[1])
	couleurs =[]
	for nb, couleur in couleursNb:
		if (couleur[0], couleur[1], couleur[2]) != (0,0,0): couleurs.append ((couleur[0], couleur[1], couleur[2]))
	couleurs.sort()
	drawColors (nom, couleurs)

traiterImage()

"""
rangerImage (argv[1])
newColors()
traiterImage()
drawColors (couleursConnues)
"""