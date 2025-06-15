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

# ------------------------ o ------------------------

class ImageFile (MediaFile):
	def __init__ (self, image=None):
		MediaFile.__init__ (self)
		self.image = None
		self.array =[]
		self.width =0
		self.height =0
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
		nameCreation = self.renameDateEtape1 (nameSpace, addHour);
		if nameCreation:
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

	def insta (self, drawBgfonc, ratio=1.0):
		""" ratio = largeur / hauteur """
		ratioImg = self.width / self.height
		posW =0
		posH =0
		widthNew = self.width
		heightNew = self.height
		if ratioImg < ratio:
			# rajouter bandes latérales
			widthNew = int (self.width * ratio / ratioImg)
			posW = int ((widthNew - self.width) /2.0)
		elif ratioImg > ratio:
			# rajouter bandes haut et bas
			heightNew = int (self.height * ratioImg / ratio)
			posH = int ((heightNew - self.height) /2.0)
		else:
			print ("votre image est déjà au bon ratio, vous n'avez pas besoin de la transformer")
			return False
	#	self.title = self.title +' insta'
		imageObj = None
		if drawBgfonc == 'stripes': imageObj = self.drawBgStripes (widthNew, heightNew)
		elif drawBgfonc == 'average': imageObj = self.drawBgAverage (widthNew, heightNew)
		elif drawBgfonc == 'reflet': imageObj = self.drawBgReflet (widthNew, heightNew)
		else: imageObj = self.drawBgAverage (widthNew, heightNew)
		imageObj.paste (self.image, (posW, posH))
		drawing = ImageDraw.Draw (imageObj)
		self.setImage (imageObj)
		return True

	def drawBgStripes (self, width, height):
		imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
		drawing = ImageDraw.Draw (imageObj)
		if self.width == width:
			# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
			height = int (height /2.0)
			bord = self.image.crop ((0,0, self.width, 1))
			bord = bord.resize ((bord.size[0], height), Image.Resampling.LANCZOS)
			imageObj.paste (bord, (0,0))
			bord = self.image.crop ((0, self.height -1, self.width, self.height))
			bord = bord.resize ((bord.size[0], height), Image.Resampling.LANCZOS)
			imageObj.paste (bord, (0,height))
		else:
			# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
			width = int (width /2.0)
			bord = self.image.crop ((0,0,1, self.height))
			bord = bord.resize ((width, bord.size[1]), Image.Resampling.LANCZOS)
			imageObj.paste (bord, (0,0))
			bord = self.image.crop ((self.width -1,0, self.width, self.height))
			bord = bord.resize ((width, bord.size[1]), Image.Resampling.LANCZOS)
			imageObj.paste (bord, (width,0))
		return imageObj

	def drawBgReflet (self, width, height):
		imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
		drawing = ImageDraw.Draw (imageObj)
		if self.width == width:
			# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
			bandSize = int ((height - self.height) /2.0)
			height = int (height /2.0)
			bord = self.image.crop ((0,0, self.width, bandSize))
			bord = ImageOps.flip (bord)
			imageObj.paste (bord, (0,0))
			bord = self.image.crop ((0, self.height - bandSize, self.width, self.height))
			bord = ImageOps.flip (bord)
			imageObj.paste (bord, (0, imageObj.size[1] - bandSize))
		else:
			# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
			bandSize = int ((width - self.width) /2.0)
			width = int (width /2.0)
			bord = self.image.crop ((0,0, bandSize, self.height))
			bord = ImageOps.mirror (bord)
			imageObj.paste (bord, (0,0))
			bord = self.image.crop ((self.width - bandSize, 0, self.width, self.height))
			bord = ImageOps.mirror (bord)
			imageObj.paste (bord, (imageObj.size[0] - bandSize, 0))
		return imageObj

	def drawBgAverage (self, width, height):
		imageObj = Image.new (mode='RGB', size=(width, height), color=(0,0,0))
		drawing = ImageDraw.Draw (imageObj)
		self.array = numpy.array (self.image)
		colorA =[ 0,0,0 ]
		colorB =[ 0,0,0 ]
		if self.width == width:
			# la largeur est plus grande que la hauteur. rajouter des bandes en haut et en bas
			height = int (height /2.0)
			rangeBord = range (width)
			for i in rangeBord:
				colorA[0] += self.array[0][i][0]
				colorA[1] += self.array[0][i][1]
				colorA[2] += self.array[0][i][2]
				colorB[0] += self.array[-1][i][0]
				colorB[1] += self.array[-1][i][1]
				colorB[2] += self.array[-1][i][2]
			colorA[0] = int (colorA[0] / width)
			colorA[1] = int (colorA[1] / width)
			colorA[2] = int (colorA[2] / width)
			colorB[0] = int (colorB[0] / width)
			colorB[1] = int (colorB[1] / width)
			colorB[2] = int (colorB[2] / width)
			bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorA))
			imageObj.paste (bord, (0,0))
			bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorB))
			imageObj.paste (bord, (0,height))
		else:
			# la largeur est plus petite que la hauteur. rajouter des bandes de chaque coté
			width = int (width /2.0)
			rangeBord = range (height)
			for i in rangeBord:
				colorA[0] += self.array[i][0][0]
				colorA[1] += self.array[i][0][1]
				colorA[2] += self.array[i][0][2]
				colorB[0] += self.array[i][-1][0]
				colorB[1] += self.array[i][-1][1]
				colorB[2] += self.array[i][-1][2]
			colorA[0] = int (colorA[0] / height)
			colorA[1] = int (colorA[1] / height)
			colorA[2] = int (colorA[2] / height)
			colorB[0] = int (colorB[0] / height)
			colorB[1] = int (colorB[1] / height)
			colorB[2] = int (colorB[2] / height)
			bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorA))
			imageObj.paste (bord, (0,0))
			bord = Image.new (mode='RGB', size=(width, height), color=tuple (colorB))
			imageObj.paste (bord, (width,0))
		return imageObj

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

	def setImage (self, imageNew):
		self.image = imageNew.convert ('RGB')
		self.width = self.image.size[0]
		self.height = self.image.size[1]

	def open (self):
		self.toPath()
		if not os.path.exists (self.path): return
		self.setImage (Image.open (self.path))

	def draw (self):
		isDrawable = MediaFile.draw (self)
		if isDrawable:
			if self.extension == 'heic' or self.extension == 'heif':
				print ('attention, vous avez faillit enregistrer une image heic')
			else: self.image.save (self.path)

class ImageFolder (MediaFolder):
	def test (self):
		self.path = 'b/cgi'
		self.get ('deborah')
		self.insta()

	def insta (self, drawBgfonc='average'):
		self.open()
		ratio = self.list[0].width / self.list[0].height
		ratioMin = ratio
		ratioMax = ratio
		for image in self.list:
			ratio = image.width / image.height
			if ratio < ratioMin: ratioMin = ratio
			elif ratio > ratioMax: ratioMax = ratio
		imageRange = range (len (self.list))
		if ratioMax <1.0:
			for i in imageRange:
				regrowMade = self.list[i].insta (drawBgfonc, ratioMax)
				if regrowMade:
					self.list[i].title = self.list[i].title +' insta'
					self.list[i].draw()
		elif ratioMin >1.0:
			for i in imageRange:
				regrowMade = self.list[i].insta (drawBgfonc, ratioMin)
				if regrowMade:
					self.list[i].title = self.list[i].title +' insta'
					self.list[i].draw()
		else:
			for i in imageRange:
				regrowMade = self.list[i].insta (drawBgfonc, 1.0)
				if regrowMade:
					self.list[i].title = self.list[i].title +' insta'
					self.list[i].draw()

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
		imageRange = range (len (self.list))
		for i in imageRange: self.list[i].open()

	def get (self, detail=""):
		if detail == 'heic':
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
		else:
			MediaFolder.get (self, detail)
			imageRange = range (len (self.list))
			for i in imageRange:
				imageNew = ImageFile (self.list[i])
				self.list[i] = imageNew
		self.list.sort()

""" sources
https://www.geeksforgeeks.org/python-pil-image-point-method/
https://pillow.readthedocs.io/en/stable/reference/ImageOps.html
"""