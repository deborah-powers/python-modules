#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageOps
import colorsys
from pillow_heif import register_heif_opener
import fileLocal
import loggerFct as log

register_heif_opener()

help ="""modifier des images
utilisation
	le script est appelable dans un fichier
	python3 %s fichier tag (référence)
les valeurs de tag
	rev: inverser les couleurs
	lum: inverser la luminosité
	col: inverser la luminosité et les couleurs
	del: éffacer les couleurs contenues dans l'image de référence
	nb: passer l'image en nuance de gris

https://www.geeksforgeeks.org/python-pil-image-point-method/
https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
""" % __file__

def openImage (imageName):
	imageName = fileLocal.shortcut (imageName)
	imageOriginal = Image.open (imageName)
	imageOriginal = imageOriginal.convert ('RGB')
	d= imageName.rfind ('.')
	newName = imageName[:d]
	return newName, imageOriginal

def heicToPng (imageName, nameSpace):
	""" calculer le nouveau nom à partir de la date de création
	nameSpace est l'espace de nom créé par windows
	"""
	d=1+ imageName.rfind (os.sep)
	fileData = nameSpace.ParseName (imageName[d:])
	# repérer la date de création. Date taken ou Date created
	dateCreation = nameSpace.GetDetailsOf (fileData, 12).replace (" ","")
	if dateCreation:
		dateCreation = dateCreation.replace ('‎', "")
		dateCreation = dateCreation.replace ('‏', '/')
	else: dateCreation = nameSpace.GetDetailsOf (fileData, 4).replace (" ",'/')
	# mettre en forme la date de création
	dateCreation = dateCreation.replace (':', '-')
	dateList = dateCreation.split ('/')
	dateCreation = dateList[2] +'-'+ dateList[1] +'-'+ dateList[0] +'-'+ dateList[3]
	# vérifier si le nom existe déjà
	alpabet = 'abcdefghijklmnopqrstuvwxyz'
	newName =""
	l=0
	while l<26:
		newName = imageName[:d] + dateCreation +" "+ alpabet[l] + '.png'
		if not os.path.exists (newName): l=27
		l+=1
	# convertir l'image heic en png. elle fera 1000 pixels de haut
	if l==27:
		heightHeic =1000
		imageNameBis, imageOriginal = openImage (imageName)
		percentHeic = float (heightHeic / float (imageOriginal.size[1]))
		widthHeic = int (imageOriginal.size[0] * percentHeic)
		imageNew = imageOriginal.resize ((widthHeic, heightHeic), Image.Resampling.LANCZOS)
		imageNew.save (newName)
		os.remove (imageName)
	else: print ("je n'ai pas réussi à renommer l'image:", imageName)

""" ________________________________________________ modifier les couleurs ________________________________________________ """

rgb_to_hsv = numpy.vectorize (colorsys.rgb_to_hsv)
hsv_to_rgb = numpy.vectorize (colorsys.hsv_to_rgb)

def imGtoHsv (imageOriginal):
	"""
	hue is a height x width x (0.0 ... 1) numpy array
	saturation is a height x width x (0.0 ... 1) numpy array
	value is a height x width x (0.0 ... 256) numpy array
	"""
	imageArray = numpy.array (imageOriginal).astype ('float')
	red, green, blue = imageArray.T
	hue, saturation, value = rgb_to_hsv (red, green, blue)
	return hue, saturation, value

def hsVtoImg (hue, saturation, value):
	red, green, blue = hsv_to_rgb (hue, saturation, value)
	red = red.T
	green = green.T
	blue = blue.T
	imageArray = numpy.dstack ((red, green, blue))
	imageArray = imageArray.astype ('uint8')
	return imageArray

def getColors (imageOriginal):
	colorsOriginal = imageOriginal.getcolors (imageOriginal.size[0] * imageOriginal.size[1])
	colorsSet = set (colorsOriginal)
	colors =[]
	for nb, color in colorsSet: colors.append (color)
	colors.sort()
	return colors

def eraseColors (imageName, referName):
	# éffacer certaines couleurs d'une image à partir d'une image de référence qui les contient
	# récupérer l'image de référence
	referName = fileLocal.shortcut (referName)
	referImg = Image.open (referName)
	referImg = referImg.convert ('RGB')
	# récupérer les couleurs à partir de l'image de référence
	colors = getColors (imageOriginal)
	# récupérer l'image à modifier
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-del.bmp'
	imageArray = numpy.array (imageOriginal)
	red, green, blue = imageArray.T
	"""
	imageArray is a height x width x (r,g,b) numpy array
	red is a height x width x (0.0 ... 100) numpy array
	"""
	# éffacer les couleurs
	for r,g,b in colors:
		colorArea = (red == r) & (green == g) & (blue == b)
		imageArray[colorArea.T] = (255, 255, 255)
	# dessiner la nouvelle image
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def reverseColors (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-reverse.bmp'
	imageNouvelle = ImageOps.invert (imageOriginal)
	imageNouvelle.save (newName)

def reverseLumins (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-reverse.bmp'
	hue, saturation, value = imGtoHsv (imageOriginal)
	value = 255.0 - value
	imageArray = hsVtoImg (hue, saturation, value)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

def reverseImage (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-reverse.bmp'
	hue, saturation, value = imGtoHsv (imageOriginal)
	value = 255.0 - value
	imageArray = hsVtoImg (hue, saturation, value)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle = ImageOps.invert (imageNouvelle)
	imageNouvelle.save (newName)

def tobw (imageName):
	newName, imageOriginal = openImage (imageName)
	newName = newName +'-nb.bmp'
	imageNouvelle = ImageOps.grayscale (imageOriginal)
	imageNouvelle.save (newName)

""" ________________________________________________ simplifier l'image ________________________________________________ """

def simplifyImage (imageName):
	# simplifier une image en vue de détecter sa bordure
	newName, imageOriginal = openImage (imageName)
	newName = newName + '-simple.bmp'
	imageLd = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=3)
	imageLd = ImageOps.grayscale (imageLd)
	imageArray = numpy.array (imageLd)
	imageArray = eraseLonelyPixel (imageArray)
	imageNouvelle = Image.fromarray (imageArray)
	imageNouvelle.save (newName)

if __name__ != '__main__': pass
elif len (argv) <3: print (help)
elif argv[2] == 'nb': tobw (argv[1])
elif argv[2] == 'col': reverseColors (argv[1])
elif argv[2] == 'lum': reverseLumins (argv[1])
elif argv[2] == 'rev': reverseImage (argv[1])
elif argv[2] == 'del' and len (argv) >3: eraseColors (argv[1], argv[3])

