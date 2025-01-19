#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import win32com.client as wclient
import numpy
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
import colorsys
from urllib import request as urlRequest
import fileLocal
from folderCls import Folder
import loggerFct as log

dateFormatDay = '%Y-%m-%d'
dateFormatHour = dateFormatDay + '-%H-%M'
imgExtensions =[ 'jpg', 'bmp', 'gif', 'png', 'mp4', 'heic', 'heif' ]
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

def blurrOne (table, y,x):
	# calculer la valeur moyenne
	neighbours =[]
	if y>0: neighbours.append (table[y-1][x])
	if y< (len (table) -1): neighbours.append (table[y+1][x])
	if x>0: neighbours.append (table[y][x-1])
	if x< (len (table[0]) -1): neighbours.append (table[y][x+1])
	n=0
	lenbours = len (neighbours)
	while n< lenbours and neighbours.count (neighbours[n]) <2: n+=1
	if n== lenbours: return neighbours[1]
	else: return neighbours[n]

def blurr (table, nbLim):
	rangeX = range (len (table[0]))
	rangeY = range (len (table))
	for y in rangeY:
		for x in rangeX: table[y][x] = blurrOne (table, y,x)
	return table

def imageAtraiter (imgTitle):
	imgTitle = imgTitle.lower()
	if imgTitle[:4] in ('img_', 'img-', 'vid_') or imgTitle[:6] == 'video_': return True
	else:
		l=0
		while l<26:
			if alpabet[l] in imgTitle: l=27
			l+=1
		if l==28: return False
		else: return True

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

def imgFromWeb (imgUrl, imgFile):
	try: urlRequest.urlretrieve (imgUrl, imgFile)
	except Exception as e:
		print (e)
		return False
	else: return True

class ImageFile():
	def __init__ (self, image=None):
		self.path =""
		self.title =""
		self.extension =""
		self.pathRoot =""
		self.image = None
		self.array =[]
		self.width =0
		self.height =0
		self.rangeWidth =[]
		self.rangeHeight =[]
		if image:
			self.path = image
			self.fromPath()

	def test (self):
		hue, saturation, brightness = self.toHsv()
		saturation = blurr (saturation, 100.0)
		brightness = blurr (brightness, 100.0)
		self.fromHsv (hue, saturation, brightness)

	def heifToPng (self, nameSpace, addHour=False):
		# l'image fera 1000 pixel de haut
		dateCreation = getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
		self.open()
		self.resizeHeight1000()
		self.correctContrast()
		nameCreation = createDatedName (self.pathRoot, 'png', dateCreation)
		if nameCreation:
			self.image.save (nameCreation)
			self.toPath()
			os.remove (self.path)

	def renameDate (self, nameSpace, addHour=False):
		""" renommer un fichier en prenant en compte la date
		la fonction utilise les métadonnées de window
		"""
		if imageAtraiter (self.title):
			self.toPath()
			dateCreation = getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
			nameCreation = createDatedName (self.pathRoot, self.extension, dateCreation)
			if nameCreation:
				self.open()
				self.resizeHeight1000()
				self.correctContrast()
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
		self.image = ImageOps.invert (self.image)

	def reverseLumins (self):
		hue, saturation, brightness = self.toHsv()
		brightness = 100.0 - brightness
		self.fromHsv (hue, saturation, brightness)

	def reverseImage (self):
		self.reverseLumins()
		self.image = ImageOps.invert (self.image)

	def tobw (self):
		self.image = ImageOps.grayscale (self.image)

	def correctContrast (self):
		# calculer le contraste des couleurs. une valeur pas canal rvb
		colors = self.getColors()
		colMin =[ colors[0][0], colors[0][1], colors[0][2] ]
		colMax =[ colors[0][0], colors[0][1], colors[0][2] ]
		for color in colors:
			if color[0] < colMin[0]: colMin[0] = color[0]
			elif color[0] > colMax[0]: colMax[0] = color[0]
			if color[1] < colMin[1]: colMin[1] = color[1]
			elif color[1] > colMax[1]: colMax[1] = color[1]
			if color[2] < colMin[2]: colMin[2] = color[2]
			elif color[2] > colMax[2]: colMax[2] = color[2]
		colSpan =[ colMax[0] - colMin[0], colMax[1] - colMin[1], colMax[2] - colMin[2] ]
		self.array = numpy.array (self.image).astype ('float')
		rangeY = range (len (self.array))
		rangeX = range (len (self.array[0]))
		if colSpan[0] <200:
			factorA = 255.0 / colSpan[0]
			factorB = colMin[0] * factorA
			for y in rangeY:
				for x in rangeX: self.array[y][x][0] = factorA * self.array[y][x][0] - factorB
		if colSpan[1] <200:
			factorA = 255.0 / colSpan[1]
			factorB = colMin[1] * factorA
			for y in rangeY:
				for x in rangeX: self.array[y][x][1] = factorA * self.array[y][x][1] - factorB
		if colSpan[2] <200:
			factorA = 255.0 / colSpan[2]
			factorB = colMin[2] * factorA
			for y in rangeY:
				for x in rangeX: self.array[y][x][2] = factorA * self.array[y][x][2] - factorB
		self.array = self.array.astype ('uint8')
		self.image = Image.fromarray (self.array)

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
		brightness is a height x width x (0.0 ... 256) numpy array
		je les normalise à 100
		"""
		self.array = numpy.array (self.image).astype ('float')
		red, green, blue = self.array.T
		hue, saturation, brightness = rgb_to_hsv (red, green, blue)
		hue *= 100.0
		saturation *= 100.0
		brightness *= 100.0
		brightness /= 255.0
		return hue, saturation, brightness

	def fromHsv (self, hue, saturation, brightness):
		hue /= 100.0
		saturation /= 100.0
		brightness *= 2.55
		red, green, blue = hsv_to_rgb (hue, saturation, brightness)
		red = red.T
		green = green.T
		blue = blue.T
		self.array = numpy.dstack ((red, green, blue))
		self.array = self.array.astype ('uint8')
		self.image = Image.fromarray (self.array)

	def fromPath (self):
		if self.pathRoot: return
		self.path = fileLocal.shortcut (self.path)
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
		self.pathRoot = self.path [:posS]

	def toPath (self):
		self.path = self.pathRoot + self.title +'.'+ self.extension

	def remove (self):
		self.toPath()
		if os.path.exists (self.path): os.remove (self.path)

	def open (self):
		self.toPath()
		if not os.path.exists (self.path): return
		self.image = Image.open (self.path)
		self.image = self.image.convert ('RGB')
		self.width = self.image.size[0]
		self.height = self.image.size[1]
		self.rangeWidth = range (self.width)
		self.rangeHeight = range (self.height)

	def draw (self):
		self.toPath()
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

	def __str__ (self):
		self.toPath()
		return self.path

class ImageFolder (Folder):
	def __init__ (self, path='i/'):
		Folder.__init__(self, path)

	def heicToPng (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get ('heic')
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.heifToPng (nameSpace, addHour)

	def heifToPng (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get ('heif')
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.heifToPng (nameSpace, addHour)

	def renameDate (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get ('new')
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.renameDate (nameSpace, addHour)
				image.path = image.path.replace (self.path, "")

	def get (self, detail=""):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			range_tag = range (len (subList) -1, -1, -1)
			if detail == 'heic':
				for i in range_tag:
					if subList[i][-5:] != '.heic': trash = subList.pop(i)
			elif detail == 'heif':
				for i in range_tag:
					if subList[i][-5:] != '.heif': trash = subList.pop(i)
			else:
				for i in range_tag:
					if subList[i][-3:] not in imgExtensions or subList[i][-4] !='.': trash = subList.pop(i)
				if detail == 'new':
					range_tag = range (len (subList) -1, -1, -1)
					for i in range_tag:
						if not imageAtraiter (subList[i][:-4]): trash = subList.pop(i)
			if subList:
				for image in subList:
					fileTmp = ImageFile (os.path.join (dirpath, image))
					self.list.append (fileTmp)
		self.list.sort()
		self.fromPath()

	def get_a (self, heic=False):
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

	def __str__ (self):
		strText = 'liste à %d éléments dans le dossier %s' %( len (self.list), self.path)
		self.fromPath()
		for image in self.list[:6]: strText = strText + '\n\t' + str (image).replace (self.path, "")
		return strText

""" sources
https://www.geeksforgeeks.org/python-pil-image-point-method/
https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
"""