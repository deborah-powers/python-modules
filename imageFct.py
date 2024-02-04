#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
from PIL import Image, ImageDraw, ImageOps
import fileLocal

def prepFile (imageFile):
	posExtension = imageFile.rfind ('.')
	imageFile = imageFile[:posExtension]
	imageFile = fileLocal.shortcut (imageFile)
	return imageFile

class Img():
	def __init__(self, imageFile=None):
		self.file = None
		self.image = None	# Image.Image
		self.colors = None	# numpy.ndarray width * height * (r,v,b,a)
		self.width =0
		self.height =0
		if imageFile: self.read (imageFile)

	def read (self, imageFile):
		# imageTmp = PIL.BmpImagePlugin.BmpImageFile
		if imageFile: self.file = imageFile
		self.file = fileLocal.shortcut (self.file)
		imageTmp = Image.open (self.file)
		self.image = imageTmp.convert ('RGBA')
		posExtension = self.file.rfind ('.')
		self.file = self.file[:posExtension]
		self.width = self.image.size[0]
		self.height = self.image.size[1]

	def write (self, imageFile):
		if imageFile: self.file = imageFile
		self.file = prepFile (self.file)
		self.file = self.file + '.bmp'
		self.image.format = 'BMP'
		self.image.save (self.file)

	def toArray (self):
		self.colors = numpy.array (self.image)

	def fromArray (self, colors=None):
		if colors: self.colors = colors
		self.image = Image.fromarray (self.colors)
		self.image.format = 'BMP'

	def crop (self, x,y, width, height):
		fragment = self.image.crop ((x,y, x+ width, y+ height))
		self.image = Image.new ('RGB', (width, height))
		self.image.paste (fragment)
		self.width = width
		self.height = height

	def copy (self):
		imageNew = Img()
		imageNew.image = self.image.copy()
		imageNew.width = self.width
		imageNew.height = self.height
		imageNew.file = self.file
		if self.colors: imageNew.colors.extends (self.colors)
		return imageNew

	def replace (self, colorDeb, colorFin):
		""" colorDeb = (r,v,b) ou (r,v,b,a)
			self.toArray() déjà fait
			self.fromArray() sera fait plus tard
		"""
		red, green, blue, alpha = self.colors.T	# Temporarily unpack the bands for readability
		colorArea = (red == colorDeb[0]) & (green == colorDeb[1]) & (blue == colorDeb[2])
		self.colors[..., :-1][colorArea.T] = colorFin

	def invert (self):
		red, green, blue, alpha = self.image.split()
		imgRgb = Image.merge ('RGB', (red, green, blue))
		imgInverted = ImageOps.invert (imgRgb)
		red, green, blue = imgInverted.split()
		self.image = Image.merge ('RGBA', (red, green, blue, alpha))
		if len (self.colors) >0: self.toArray()

imageOriginale = 'b/photo.bmp'
imageFinale = 'b/photo bis.bmp'

def testClass():
	image = Img (imageOriginale)
	image.toArray()
	image.replace ((0,0,0), (255, 0, 100))
	image.replace ((64, 64, 64), (100, 0, 255))
	image.fromArray()
#	image.crop (200, 200, 600, 600)
	image.invert()
	image.write (imageFinale)


testClass()

color256 =[ (0, 0, 0), (0, 0, 64), (0, 0, 128), (0, 0, 192), (0, 0, 255), (0, 32, 64), (0, 32, 128), (0, 32, 192), (0, 64, 0), (0, 64, 64), (0, 64, 128), (0, 64, 192), (0, 96, 0), (0, 96, 64), (0, 96, 128), (0, 96, 192), (0, 128, 0), (0, 128, 64), (0, 128, 128), (0, 128, 192), (0, 160, 0), (0, 160, 64), (0, 160, 128), (0, 160, 192), (0, 192, 0), (0, 192, 64), (0, 192, 128), (0, 192, 192), (0, 224, 0), (0, 224, 64), (0, 224, 128), (0, 255, 0), (0, 255, 255), (32, 0, 64), (32, 0, 128), (32, 0, 192), (32, 32, 64), (32, 32, 128), (32, 32, 192), (32, 64, 0), (32, 64, 64), (32, 64, 128), (32, 64, 192), (32, 96, 0), (32, 96, 64), (32, 96, 128), (32, 96, 192), (32, 128, 0), (32, 128, 64), (32, 128, 128), (32, 128, 192), (32, 160, 0), (32, 160, 64), (32, 160, 128), (32, 160, 192), (32, 192, 0), (32, 192, 64), (32, 192, 128), (32, 192, 192), (32, 224, 0), (32, 224, 64), (32, 224, 128), (64, 0, 64), (64, 0, 128), (64, 0, 192), (64, 32, 0), (64, 32, 64), (64, 32, 128), (64, 32, 192), (64, 64, 0), (64, 64, 64), (64, 64, 128), (64, 64, 192), (64, 96, 0), (64, 96, 64), (64, 96, 128), (64, 96, 192), (64, 128, 0), (64, 128, 64), (64, 128, 128), (64, 128, 192), (64, 160, 0), (64, 160, 64), (64, 160, 128), (64, 160, 192), (64, 192, 0), (64, 192, 64), (64, 192, 128), (64, 192, 192), (64, 224, 0), (64, 224, 64), (64, 224, 128), (96, 0, 64), (96, 0, 128), (96, 0, 192), (96, 32, 0), (96, 32, 64), (96, 32, 128), (96, 32, 192), (96, 64, 0), (96, 64, 64), (96, 64, 128), (96, 64, 192), (96, 96, 0), (96, 96, 64), (96, 96, 128), (96, 96, 192), (96, 128, 0), (96, 128, 64), (96, 128, 128), (96, 128, 192), (96, 160, 0), (96, 160, 64), (96, 160, 128), (96, 160, 192), (96, 192, 0), (96, 192, 64), (96, 192, 128), (96, 192, 192), (96, 224, 0), (96, 224, 64), (96, 224, 128), (128, 0, 0), (128, 0, 64), (128, 0, 128), (128, 0, 192), (128, 32, 0), (128, 32, 64), (128, 32, 128), (128, 32, 192), (128, 64, 0), (128, 64, 64), (128, 64, 128), (128, 64, 192), (128, 96, 0), (128, 96, 64), (128, 96, 128), (128, 96, 192), (128, 128, 0), (128, 128, 64), (128, 128, 128), (128, 128, 192), (128, 160, 0), (128, 160, 64), (128, 160, 128), (128, 160, 192), (128, 192, 0), (128, 192, 64), (128, 192, 128), (128, 192, 192), (128, 224, 0), (128, 224, 64), (128, 224, 128), (160, 0, 64), (160, 0, 128), (160, 0, 192), (160, 32, 0), (160, 32, 64), (160, 32, 128), (160, 32, 192), (160, 64, 0), (160, 64, 64), (160, 64, 128), (160, 64, 192), (160, 96, 0), (160, 96, 64), (160, 96, 128), (160, 96, 192), (160, 128, 0), (160, 128, 64), (160, 128, 128), (160, 128, 192), (160, 160, 0), (160, 160, 64), (160, 160, 128), (160, 160, 164), (160, 160, 192), (160, 192, 0), (160, 192, 64), (160, 192, 128), (160, 192, 192), (160, 224, 0), (160, 224, 64), (160, 224, 128), (166, 202, 240), (192, 0, 64), (192, 0, 128), (192, 0, 192), (192, 32, 0), (192, 32, 64), (192, 32, 128), (192, 32, 192), (192, 64, 0), (192, 64, 64), (192, 64, 128), (192, 64, 192), (192, 96, 0), (192, 96, 64), (192, 96, 128), (192, 96, 192), (192, 128, 0), (192, 128, 64), (192, 128, 128), (192, 128, 192), (192, 160, 0), (192, 160, 64), (192, 160, 128), (192, 160, 192), (192, 192, 0), (192, 192, 64), (192, 192, 128), (192, 192, 192), (192, 220, 192), (192, 224, 0), (192, 224, 64), (192, 224, 128), (224, 0, 64), (224, 0, 128), (224, 0, 192), (224, 32, 0), (224, 32, 64), (224, 32, 128), (224, 32, 192), (224, 64, 0), (224, 64, 64), (224, 64, 128), (224, 64, 192), (224, 96, 0), (224, 96, 64), (224, 96, 128), (224, 96, 192), (224, 128, 0), (224, 128, 64), (224, 128, 128), (224, 128, 192), (224, 160, 0), (224, 160, 64), (224, 160, 128), (224, 160, 192), (224, 192, 0), (224, 192, 64), (224, 192, 128), (224, 224, 0), (224, 224, 64), (224, 224, 128), (255, 0, 0), (255, 0, 255), (255, 251, 240), (255, 255, 0), (255, 255, 255) ]