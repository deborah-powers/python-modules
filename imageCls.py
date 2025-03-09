#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import numpy
from PIL import Image, ImageOps, ImageDraw
from pillow_heif import register_heif_opener
import cv2
import colorsys
from mediaCls import MediaFile, MediaFolder
import mediaCls as media
from kmeans import KmeansTablesNb
import loggerFct as log

imgExtensions =[ 'jpg', 'bmp', 'gif', 'png', 'mp4', 'avi', 'heic', 'heif' ]

numpy.seterr (all='warn')
rgb_to_hsv = numpy.vectorize (colorsys.rgb_to_hsv)
hsv_to_rgb = numpy.vectorize (colorsys.hsv_to_rgb)
register_heif_opener()

class KmeansTablesCanal (KmeansTablesNb):
	def __init__ (self, table):
		KmeansTablesNb.__init__ (self, 1.0, table)

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

def blurr (table):
	rangeX = range (len (table[0]))
	rangeY = range (len (table))
	for y in rangeY:
		for x in rangeX: table[y][x] = blurrOne (table, y,x)
	return table

# ------------------------ instagram ------------------------

def drawBgReflet (imageOriginale, width, height, horizontal=True):
	# dessiner la nouvelle image de fond
	imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
	# la largeur est plus grande que la hauteur
	if horizontal:
		lenghtTmp = imageOriginale.size[0] - imageOriginale.size[1]
		lenghtTmp /=2
		lenghtBand = int (lenghtTmp)
		imageReflet = imageOriginale.crop ((0, 0, width, lenghtBand))
		imageReflet = ImageOps.flip (imageReflet)
		imageObj.paste (imageReflet, (0, 0))
		imageReflet = imageOriginale.crop ((0, imageOriginale.size[1] - lenghtBand, width, imageOriginale.size[1]))
		imageReflet = ImageOps.flip (imageReflet)
		imageObj.paste (imageReflet, (0, height - lenghtBand))
	# la hauteur est plus grande que la largeur
	else:
		lenghtTmp = imageOriginale.size[1] - imageOriginale.size[0]
		lenghtTmp /=2
		lenghtBand = int (lenghtTmp)
		imageReflet = imageOriginale.crop ((0, 0, lenghtBand, height))
		imageReflet = ImageOps.mirror (imageReflet)
		imageObj.paste (imageReflet, (0, 0))
		imageReflet = imageOriginale.crop ((imageOriginale.size[0] - lenghtBand, 0, imageOriginale.size[0], height))
		imageReflet = ImageOps.mirror (imageReflet)
		imageObj.paste (imageReflet, (width - lenghtBand, 0))
	drawing = ImageDraw.Draw (imageObj)
	return imageObj

def drawBgStripes (imageArray, width, height, horizontal=True):
	# dessiner la nouvelle image de fond
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

# ------------------------ o ------------------------

class ImageFile (MediaFile):
	def __init__ (self, image=None):
		MediaFile.__init__ (self)
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
		"""
		hue = 80
		saturation = 60
		brightness = 50
		"""
		hue = blurr (hue)
		saturation = 60
		brightness = 50
		hueKmeans = KmeansTablesCanal (hue)
		hueT = hue.T
		for group in hueKmeans.groups:
			for color in group[1:]:
				colorArea = (hueT == color)
			hue[hueT.T] = group[0]
		print (hue)
		self.fromHsv (hue, saturation, brightness)

	def heifToPng (self, nameSpace, addHour=False):
		# l'image fera 1000 pixel de haut
		dateCreation = media.getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
		self.open()
		self.resizeHeight1000()
		self.correctContrast()
		nameCreation = media.createDatedName (self.pathRoot, 'png', dateCreation)
		if nameCreation:
			self.image.save (nameCreation)
			self.toPath()
			os.remove (self.path)

	def renameDate (self, nameSpace, addHour=False):
		""" renommer un fichier en prenant en compte la date
		la fonction utilise les métadonnées de window
		"""
		aTraiter = self.renameDateEtape1 (nameSpace, addHour);
		if aTraiter:
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

	def swapColors (self, colOldStr, colNewStr):
		# colXStr = "30 67 23"
		colOld = colOldStr.split (" ")
		colOld[0] = int (colOld[0])
		colOld[1] = int (colOld[1])
		colOld[2] = int (colOld[2])
		colNew = colNewStr.split (" ")
		colNew[0] = int (colNew[0])
		colNew[1] = int (colNew[1])
		colNew[2] = int (colNew[2])
		self.array = numpy.array (self.image)
		red, green, blue = self.array.T
		colorArea = (red == colOld[0]) & (green == colOld[1]) & (blue == colOld[2])
		self.array[colorArea.T] = colNew
		self.image = Image.fromarray (self.array)

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
		log.logMsg (colSpan)
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

	# ------------------------ instagram ------------------------

	def insta (self, drawBgfonc, ratio=1, ratioB=1):
		if ratio < ratioB: ratio = ratio / ratioB
		else: ratio = ratioB / ratio
		if self.width > self.height:
			ratioB = self.height / self.width
			if ratioB == ratio: print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
			elif ratioB >= 0.9 * ratio: print ("votre image est presque au bon ratio, vous n'avez pas besoin de la transformer")
			elif ratioB <0.3: self.squareVideo()
			else: self.squarePicture (ratio, drawBgfonc)
		else:
			ratioB = self.width / self.height
			if ratioB == ratio: print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
			elif ratioB >= 0.9 * ratio: print ("votre image est presque au bon ratio, vous n'avez pas besoin de la transformer")
			elif ratioB <0.3: self.squareVideo()
			else: self.squarePicture (ratio, drawBgfonc)

	def squarePicture (self, ratio, drawBgfonc):
		self.title = self.title +' rect'
		self.array = numpy.array (self.image)
		# la largeur est plus grande que la hauteur
		if self.width > self.height:
			heightTmp = ratio * self.width
			heightNew = int (heightTmp)
			imageObj = None
			if drawBgfonc == drawBgReflet: imageObj = drawBgReflet (self.image, self.width, heightNew, True)
			else: imageObj = drawBgfonc (self.array, self.width, heightNew, True)
			wStripe = int ((heightNew - self.height) /2)
			imageObj.paste (self.image, (0, wStripe))
			self.height = heightNew
		# la hauteur est plus grande que la largeur
		else:
			widthTmp = ratio * self.height
			widthNew = int (widthTmp)
			if drawBgfonc == drawBgReflet: imageObj = drawBgReflet (self.image, widthNew, self.height, False)
			else: imageObj = drawBgfonc (self.array, widthNew, self.height, False)
			wStripe = int ((widthNew - self.width) /2)
			imageObj.paste (self.image, (wStripe, 0))
			self.width = widthNew
		self.image = imageObj

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

	# ------------------------ o ------------------------

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

	def fromMedia (self, mediaFile):
		self.path = mediaFile.path
		self.title = mediaFile.title
		self.extension = mediaFile.extension
		self.pathRoot = mediaFile.pathRoot
		self.open()

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
		isDrawable = MediaFile.draw (self)
		if isDrawable:
			if self.extension == 'heic' or self.extension == 'heif':
				print ('attention, vous avez faillit enregistrer une image heic')
			else: self.image.save (self.path)

class ImageFolder (MediaFolder):
	def ratio (self):
		ratio = self.list[0].width / self.list[0].height
		ratioMin = ratio
		ratioMax = ratio
		for image in self.list:
			ratio = image.width / image.height
			if ratio < ratioMin: ratioMin = ratio
			elif ratio > ratioMax: ratioMax = ratio
		log.logLst (ratioMin, ratioMax)

	def heicToPng (self, addHour=False):
		nameSpace = media.getNameSpace (self.path[:-1])
		self.get ('heic')
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.heifToPng (nameSpace, addHour)

	def heifToPng (self, addHour=False):
		nameSpace = media.getNameSpace (self.path[:-1])
		self.get ('heif')
		for image in self.list:
			if os.sep not in image.path:
				image.path = self.path + image.path
				image.heifToPng (nameSpace, addHour)

	def open (self):
		rangeList = range (len (self.list))
		for i in rangeList: self.list[i].open()

	def get (self, detail=""):
		if detail == 'new' or detail =="":
			MediaFolder.get (self, detail)
			rangeList = range (len (self.list))
			for i in rangeList:
				newImage = ImageFile (self.path + self.list[i].path)
				self.list[i] = newImage
			return
		elif detail == 'heic':
			for dirpath, SousListDossiers, subList in os.walk (self.path):
				if not subList: continue
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if subList[i][-5:] != '.heic': trash = subList.pop(i)
				if subList:
					for image in subList:
						fileTmp = ImageFile (os.path.join (dirpath, image))
						self.list.append (fileTmp)
		elif detail == 'heif':
			for dirpath, SousListDossiers, subList in os.walk (self.path):
				if not subList: continue
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if subList[i][-5:] != '.heif': trash = subList.pop(i)
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

""" sources
https://www.geeksforgeeks.org/python-pil-image-point-method/
https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
"""