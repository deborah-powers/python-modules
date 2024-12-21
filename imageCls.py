#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import win32com.client as wclient
import numpy
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
import colorsys
import fileLocal
from folderCls import Folder
import loggerFct as log

dateFormatDay = '%Y-%m-%d'
dateFormatHour = dateFormatDay + '-%H-%M'
imgExtensions =[ 'jpg', 'bmp', 'gif', 'png', 'mp4', 'heic' ]
metadataWindow =[
	'Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type',
	'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating',
	'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
	'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords'
]
alpabet = 'abcdefghijklmnopqrstuvwxyz'

numpy.seterr (all='warn')
rgb_to_hsv = numpy.vectorize (colorsys.rgb_to_hsv)
hsv_to_rgb = numpy.vectorize (colorsys.hsv_to_rgb)
register_heif_opener()


def getDateCreation (nameImg, nameSpace, addHour=False):
	fileData = nameSpace.ParseName (nameImg)
	# repérer la date de création. Date taken ou Date created
	dateCreation = nameSpace.GetDetailsOf (fileData, 12).replace (" ","")
	if dateCreation and '202' in dateCreation:
		dateCreation = dateCreation.replace ('‎', "")
		dateCreation = dateCreation.replace ('‏', '/')
	else: dateCreation = nameSpace.GetDetailsOf (fileData, 4).replace (" ",'/')
	# mettre en forme la date de création
	dateCreation = dateCreation.replace (':', '-')
	dateList = dateCreation.split ('/')
	dateCreation = dateList[2] +'-'+ dateList[1] +'-'+ dateList[0]
	if addHour: dateCreation = dateCreation +'-'+ dateList[3]
	return dateCreation

def createDatedName (pathImg, extImg, dateCreation):
	newName =""
	l=0
	while l<26:
		newName = pathImg + dateCreation +" "+ alpabet[l] +'.'+ extImg
		if not os.path.exists (newName): l=27
		l+=1
	if l<27:
		newName =""
		print ("je n'ai pas réussi à renommer l'image:", pathImg)
	return newName


class ImageFile():
	def __init__ (self, image=None):
		self.path =""
		self.title =""
		self.extension =""
		self.image = None
		self.array =[]
		if image:
			self.path = image
			self.fromPath()

	def heicToPng (self, nameSpace, addHour=False):
		# l'image fera 1000 pixel de haut
		dateCreation = getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
		self.open()
		self.resizeHeight1000()
		self.fromPath()
		nameCreation = createDatedName (self.path, 'png', dateCreation)
		if nameCreation:
			imageNew.save (nameCreation)
			self.toPath()
			os.remove (self.path)

	def renameDate (self, nameSpace, addHour=False):
		""" renommer un fichier en prenant en compte la date
		la fonction utilise les métadonnées de window
		"""
		aTraiter = True
		newName = self.title.lower()
		if newName[:4] not in 'img_ img- vid_' and newName[:6] != 'video_':
			l=0
			while l<26:
				if alpabet[l] in newName:
					aTraiter = False
					l=27
				l+=1
		if aTraiter:
			self.toPath()
			dateCreation = getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
			self.fromPath()
			nameCreation = createDatedName (self.path, self.extension, dateCreation)
			if nameCreation:
				self.open()
				self.resizeHeight1000()
				self.draw()
				os.rename (self.path, nameCreation)

	def resizeHeight1000 (self):
		heightNew =1000
		if self.image.size[1] > heightNew:
			percentScale = float (heightNew / float (self.image.size[1]))
			widthNew = int (self.image.size[0] * percentScale)
			self.image = self.image.resize ((widthNew, heightNew), Image.Resampling.LANCZOS)

	def eraseColors (self, referImg):
		# éffacer certaines couleurs d'une image à partir d'une image de référence qui les contient
		colors = referImg.getColors()
		self.title = self.title + '-del'
		self.array = numpy.array (self.image)
		red, green, blue = self.array.T
		"""
		self.array is a height x width x (r,g,b) numpy array
		red is a height x width x (0.0 ... 100) numpy array
		"""
		# éffacer les couleurs
		for r,g,b in colors:
			colorArea = (red == r) & (green == g) & (blue == b)
			self.array[colorArea.T] = (255, 255, 255)
		# dessiner la nouvelle image
		self.image = Image.fromarray (self.array)

	def reverseColors (self):
		self.title = self.title + '-rev'
		self.image = ImageOps.invert (self.image)

	def reverseLumins (self):
		self.title = self.title + '-rev'
		hue, saturation, value = self.toHsv()
		value = 255 - value
		self.fromHsv (hue, saturation, value)

	def reverseImage (self):
		self.title = self.title + '-rev'
		self.image = ImageOps.invert (self.image)
		hue, saturation, value = imGtoHsv (imageNouvelle)
		value = 255 - value
		self.fromHsv (hue, saturation, value)

	def tobw (self):
		self.title = self.title + '-nb'
		self.image = ImageOps.grayscale (self.image)

	def getColors (self):
		colorsOriginal = self.image.getcolors (self.image.size[0] * self.image.size[1])
		colorsSet = set (colorsOriginal)
		colors =[]
		for nb, color in colorsSet: colors.append (color)
		colors.sort()
		return colors

	def toHsv (self):
		"""
		hue is a height x width x (0.0 ... 1) numpy array
		saturation is a height x width x (0.0 ... 1) numpy array
		value is a height x width x (0.0 ... 256) numpy array
		"""
		self.array = numpy.array (self.image).astype ('float')
		red, green, blue = self.array.T
		hue, saturation, value = rgb_to_hsv (red, green, blue)
		return hue, saturation, value

	def fromHsv (self, hue, saturation, value):
		red, green, blue = hsv_to_rgb (hue, saturation, value)
		red = red.T
		green = green.T
		blue = blue.T
		self.array = numpy.dstack ((red, green, blue))
		self.array = self.array.astype ('uint8')

	def fromPath (self):
		if '.'+ self.extension not in self.path: return
		if os.sep not in self.path or '.' not in self.path:
			print ('fichier malformé:\n' + self.path)
			return
		elif self.path.rfind (os.sep) > self.path.rfind ('.'):
			# print ('fichier malformé:\n' + self.path)
			return
		posS = self.path.rfind (os.sep) +1
		posE = self.path.rfind ('.')
		self.title = self.path [posS:posE]
		self.extension = self.path[posE+1:]
		self.path = self.path [:posS]

	def toPath (self):
		if '.'+ self.extension not in self.path:
			self.path = self.path + self.title +'.'+ self.extension
			self.path = fileLocal.shortcut (self.path)

	def remove (self):
		self.toPath()
		if os.path.exists (self.path): os.remove (self.path)

	def open (self):
		self.toPath()
		if not os.path.exists (self.path): return
		self.image = Image.open (self.path)
		self.image = self.image.convert ('RGB')

	def draw (self):
		if self.extension == 'heic':
			print ('attention, vous avez faillit enregistrer une image heic')
			return
		chars = '/\\\t\n'; c=0
		while chars != 'error' and c<4:
			if chars[c] in self.title:
				print ('le fichier est mal formé:', self.title [:100])
				print (c, chars[c])
				chars = 'error'
			c+=1
		if chars != 'error':
			self.toPath()
			self.image.save (self.path)

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		self.toPath()
		newFile.toPath()
		return self.path < newFile.path

class ImageFolder (Folder):
	def __init__ (self, path='i/'):
		Folder.__init__(self, path)

	def heicToPng (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get (True)
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.heicToPng (nameSpace, addHour)

	def renameDate (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get()
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.renameDate (nameSpace, addHour)
				image.path = image.path.replace (self.path, "")

	def get (self, heic=False):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			range_tag = range (len (subList) -1, -1, -1)
			if heic:
				for i in range_tag:
					if subList[i][-5:] != '.heic': trash = subList.pop(i)
			else:
				for i in range_tag:
					if subList[i][-3:] not in imgExtensions or subList[i][-4] !='.': trash = subList.pop(i)
			if subList:
				for image in subList:
					fileTmp = ImageFile (os.path.join (dirpath, image))
					self.list.append (fileTmp)
		self.list.sort()
		self.fromPath()
