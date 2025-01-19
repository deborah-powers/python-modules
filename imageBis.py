#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from imageCls import *

if argv[2] == 'cd': image.correctContrastDark()
elif argv[2] == 'cl': image.correctContrastLight()

class ImageFileBis (ImageFile):
	def eraseColorsDark (self, mode='dark'):
		# éffacer les couleurs sombres d'une image
		self.array = numpy.array (self.image)
		red, green, blue = self.array.T
		# éffacer les couleurs
		if mode == 'dark':
			colorArea = (red >128) & (green >128) & (blue >128)
			self.array[colorArea.T] = (255, 255, 255)
		else:
			colorArea = (red <127) & (green <127) & (blue <127)
			self.array[colorArea.T] = (0, 0, 0)
		# dessiner la nouvelle image
		self.image = Image.fromarray (self.array)

	def cernedByDark (self, y, x):
		limit = 127
		if self.array[y][x][0] > limit and self.array[y][x][1] > limit and self.array[y][x][2] > limit: cerned = False
		cerned = True
		if y< len (self.array) -1:
			if self.array[y+1][x][0] > limit and self.array[y+1][x][1] > limit and self.array[y+1][x][2] > limit: cerned = False
			elif x< len (self.array[0]) -1 and self.array[y+1][x+1][0] > limit and self.array[y+1][x+1][1] > limit and self.array[y+1][x+1][2] > limit:
				cerned = False
		if x< len (self.array[0]) -1 and self.array[y][x+1][0] > limit and self.array[y][x+1][1] > limit and self.array[y][x+1][2] > limit: cerned = False
		return cerned

	def cernedByLight (self, y, x):
		limit = 128
		if self.array[y][x][0] < limit and self.array[y][x][1] < limit and self.array[y][x][2] < limit: cerned = False
		cerned = True
		if y< len (self.array) -1:
			if self.array[y+1][x][0] < limit and self.array[y+1][x][1] < limit and self.array[y+1][x][2] < limit: cerned = False
			elif x< len (self.array[0]) -1 and self.array[y+1][x+1][0] < limit and self.array[y+1][x+1][1] < limit and self.array[y+1][x+1][2] < limit:
				cerned = False
		if x< len (self.array[0]) -1 and self.array[y][x+1][0] < limit and self.array[y][x+1][1] < limit and self.array[y][x+1][2] < limit: cerned = False
		return cerned

	def correctContrastBrightness (self):
		hue, saturation, brightness = self.toHsv()
		# brightness
		brightLim = 128.0
		brightMin = min (brightness[0])
		brightMax =0.0
		for bright in brightness:
			brightTmp = min (bright)
			if brightTmp < brightMin: brightMin = brightTmp
			brightTmp = max (bright)
			if brightTmp > brightMax and brightTmp < brightLim: brightMax = brightTmp
		brightSpan = brightMax - brightMin
		# saturation
		satLim = 0.5
		satMin = min (saturation[0])
		satMax =0.0
		for sat in saturation:
			satTmp = min (sat)
			if satTmp < satMin: satMin = satTmp
			satTmp = max (sat)
			if satTmp > satMax: satMax = satTmp
		satSpan = satMax - satMin
		# modification des pixels
		rangeY = range (len (brightness))
		rangeX = range (len (brightness[0]))
		brightA = 255.0 / brightSpan
		brightB = brightMin * brightA
		saturA = 1.0 / satSpan
		saturB = satMin * saturA
		for y in rangeY:
			for x in rangeX:
				if brightness[y][x] < brightLim: brightness[y][x] = brightA * brightness[y][x] - brightB
				saturation[y][x] = saturA * saturation[y][x] - saturB
		self.fromHsv (hue, saturation, brightness)

	def correctContrastDark (self):
		# récupérer les couleurs
		limit = 86
		colors = self.getColors()
		colMin =[ colors[0][0], colors[0][1], colors[0][2] ]
		colMax =[ 0, 0, 0 ]
		for color in colors:
			if color[0] < colMin[0]: colMin[0] = color[0]
			elif color[0] > colMax[0] and color[0] < limit: colMax[0] = color[0]
			if color[1] < colMin[1]: colMin[1] = color[1]
			elif color[1] > colMax[1] and color[1] < limit: colMax[1] = color[1]
			if color[2] < colMin[2]: colMin[2] = color[2]
			elif color[2] > colMax[2] and color[2] < limit: colMax[2] = color[2]
		# modifier les pixels
		colSpan =[ colMax[0] - colMin[0], colMax[1] - colMin[1], colMax[2] - colMin[2] ]
		self.array = numpy.array (self.image).astype ('float')
		rangeY = range (len (self.array))
		rangeX = range (len (self.array[0]))
		if colSpan[0] <200:
			factorA = 255.0 / colSpan[0]
			factorB = colMin[0] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][0] < limit: self.array[y][x][0] = factorA * self.array[y][x][0] - factorB
		if colSpan[1] <200:
			factorA = 255.0 / colSpan[1]
			factorB = colMin[1] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][1] < limit: self.array[y][x][1] = factorA * self.array[y][x][1] - factorB
		if colSpan[2] <200:
			factorA = 255.0 / colSpan[2]
			factorB = colMin[2] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][2] < limit: self.array[y][x][2] = factorA * self.array[y][x][2] - factorB
		self.array = self.array.astype ('uint8')
		self.image = Image.fromarray (self.array)

	def correctContrastLight (self):
		# récupérer les couleurs
		limit = 169
		colors = self.getColors()
		colMin =[ 255, 255, 255 ]
		colMax =[ colors[0][0], colors[0][1], colors[0][2] ]
		for color in colors:
			if color[0] < colMin[0] and color[0] > limit: colMin[0] = color[0]
			elif color[0] > colMax[0]: colMax[0] = color[0]
			if color[1] < colMin[1] and color[1] > limit: colMin[1] = color[1]
			elif color[1] > colMax[1]: colMax[1] = color[1]
			if color[2] < colMin[2] and color[2] > limit: colMin[2] = color[2]
			elif color[2] > colMax[2]: colMax[2] = color[2]
		# modifier les pixels
		colSpan =[ colMax[0] - colMin[0], colMax[1] - colMin[1], colMax[2] - colMin[2] ]
		self.array = numpy.array (self.image).astype ('float')
		rangeY = range (len (self.array))
		rangeX = range (len (self.array[0]))
		if colSpan[0] <200:
			factorA = 255.0 / colSpan[0]
			factorB = colMin[0] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][0] > limit: self.array[y][x][0] = factorA * self.array[y][x][0] - factorB
		if colSpan[1] <200:
			factorA = 255.0 / colSpan[1]
			factorB = colMin[1] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][1] > limit: self.array[y][x][1] = factorA * self.array[y][x][1] - factorB
		if colSpan[2] <200:
			factorA = 255.0 / colSpan[2]
			factorB = colMin[2] * factorA
			for y in rangeY:
				for x in rangeX:
					if self.array[y][x][2] > limit: self.array[y][x][2] = factorA * self.array[y][x][2] - factorB
		self.array = self.array.astype ('uint8')
		self.image = Image.fromarray (self.array)

	def correctContrast_vb (self):
		hue, saturation, brightness = self.toHsv()
		hue = 0.6
		# chercher les limites
		satLim =[ saturation[0][0], saturation[0][0], 100.0 ]	# min, max, span
		briLim =[ brightness[0][0], brightness[0][0], 100.0 ]
		for y in self.rangeWidth:
			for x in self.rangeHeight:
				if saturation[y][x] < satLim[0]: satLim[0] = saturation[y][x]
				elif saturation[y][x] > satLim[1]: satLim[1] = saturation[y][x]
				if brightness[y][x] < briLim[0]: briLim[0] = brightness[y][x]
				elif brightness[y][x] > briLim[1]: briLim[1] = brightness[y][x]
		satLim[2] = satLim[1] - satLim[0]
		briLim[2] = briLim[1] - briLim[0]
		log.logLst (satLim[2], briLim[2])
		# corriger la saturation
		if satLim[2] <95.0 and satLim[2] >0.0:
			factorA = 100.0 / satLim[2]
			factorB = satLim[0] * factorA
			for y in self.rangeWidth:
				for x in self.rangeHeight: saturation[y][x] = factorA * saturation[y][x] - factorB
		# corriger la luminosité
		if briLim[2] <95.0 and briLim[2] >0.0:
			factorA = 100.0 / briLim[2]
			factorB = briLim[0] * factorA
			for y in self.rangeWidth:
				for x in self.rangeHeight: brightness[y][x] = factorA * brightness[y][x] - factorB
		self.fromHsv (hue, saturation, brightness)

	def blurr (self):
		self.array = numpy.array (self.image).astype ('float')
		self.rangeWidth = range (self.width)
		self.rangeHeight = range (self.height)
		for y in self.rangeHeight:
			for x in self.rangeWidth:
				self.blurrOne (y,x)
		self.array = self.array.astype ('uint8')
		self.image = Image.fromarray (self.array)

	def blurrTwo (self, y,x):
		# calculer la valeur moyenne
		nbCases =1
		if x>0:
			self.array[y][x][0] += self.array[y][x-1][0]
			self.array[y][x][1] += self.array[y][x-1][1]
			self.array[y][x][2] += self.array[y][x-1][2]
			nbCases +=1
		if x< self.width -1:
			self.array[y][x][0] += self.array[y][x+1][0]
			self.array[y][x][1] += self.array[y][x+1][1]
			self.array[y][x][2] += self.array[y][x+1][2]
			nbCases +=1
		if y>0:
			if x>0:
				self.array[y][x][0] += self.array[y-1][x-1][0]
				self.array[y][x][1] += self.array[y-1][x-1][1]
				self.array[y][x][2] += self.array[y-1][x-1][2]
				nbCases +=1
			if x< self.width -1:
				self.array[y][x][0] += self.array[y-1][x+1][0]
				self.array[y][x][1] += self.array[y-1][x+1][1]
				self.array[y][x][2] += self.array[y-1][x+1][2]
				nbCases +=1
		if y< self.height -1:
			if x>0:
				self.array[y][x][0] += self.array[y+1][x-1][0]
				self.array[y][x][1] += self.array[y+1][x-1][1]
				self.array[y][x][2] += self.array[y+1][x-1][2]
				nbCases +=1
			if x< self.width -1:
				self.array[y][x][0] += self.array[y+1][x+1][0]
				self.array[y][x][1] += self.array[y+1][x+1][1]
				self.array[y][x][2] += self.array[y+1][x+1][2]
				nbCases +=1
		self.array[y][x][0] /= nbCases
		self.array[y][x][1] /= nbCases
		self.array[y][x][2] /= nbCases

	def blurrOne (self, y,x):
		# calculer la valeur moyenne
		nbCases =[ 1,1,1 ]
		newCase =[ self.array[y][x][0], self.array[y][x][1], self.array[y][x][2] ]
		if x>0:
			if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
				newCase[0] += self.array[y][x-1][0]
				nbCases[0] +=1
			if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
				newCase[1] += self.array[y][x-1][1]
				nbCases[1] +=1
			if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
				newCase[2] += self.array[y][x-1][2]
				nbCases[2] +=1
		if x< self.width -1:
			if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
				newCase[0] += self.array[y][x+1][0]
				nbCases[0] +=1
			if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
				newCase[1] += self.array[y][x+1][1]
				nbCases[1] +=1
			if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
				newCase[2] += self.array[y][x+1][2]
				nbCases[2] +=1
		if y>0:
			if x>0:
				if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
					newCase[0] += self.array[y-1][x-1][0]
					nbCases[0] +=1
				if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
					newCase[1] += self.array[y-1][x-1][1]
					nbCases[1] +=1
				if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
					newCase[2] += self.array[y-1][x-1][2]
					nbCases[2] +=1
			if x< self.width -1:
				if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
					newCase[0] += self.array[y-1][x+1][0]
					nbCases[0] +=1
				if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
					newCase[1] += self.array[y-1][x+1][1]
					nbCases[1] +=1
				if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
					newCase[2] += self.array[y-1][x+1][2]
					nbCases[2] +=1
		if y< self.height -1:
			if x>0:
				if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
					newCase[0] += self.array[y+1][x-1][0]
					nbCases[0] +=1
				if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
					newCase[1] += self.array[y+1][x-1][1]
					nbCases[1] +=1
				if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
					newCase[2] += self.array[y+1][x-1][2]
					nbCases[2] +=1
			if x< self.width -1:
				if (self.array[y][x][0] - self.array[y][x-1][0])**2 <400:
					newCase[0] += self.array[y+1][x+1][0]
					nbCases[0] +=1
				if (self.array[y][x][1] - self.array[y][x-1][1])**2 <400:
					newCase[1] += self.array[y+1][x+1][1]
					nbCases[1] +=1
				if (self.array[y][x][2] - self.array[y][x-1][2])**2 <400:
					newCase[2] += self.array[y+1][x+1][2]
					nbCases[2] +=1
		self.array[y][x][0] = newCase[0] / nbCases[0]
		self.array[y][x][1] = newCase[1] / nbCases[1]
		self.array[y][x][2] = newCase[2] / nbCases[2]

def nbClose (nbA, nbO, nbLim):
	nbI = nbA - nbO
	if nbI <0: nbI = -1* nbI
	if nbI < nbLim: return True
	else: return False

def blurrOne (table, y,x, nbLim):
	# calculer la valeur moyenne
	nbCases =1
	newCase = table[y][x]
	lenX = len (table[0]) -1
	lenY = len (table) -1
	if x>0:
		if nbClose (table[y][x], table[y][x-1], nbLim):
			newCase += table[y][x-1]
			nbCases +=1
	if x< lenX:
		if nbClose (table[y][x], table[y][x-1], nbLim):
			newCase += table[y][x+1]
			nbCases +=1
	if y>0:
		if x>0:
			if nbClose (table[y][x], table[y][x-1], nbLim):
				newCase += table[y-1][x-1]
				nbCases +=1
		if x< lenX:
			if nbClose (table[y][x], table[y][x-1], nbLim):
				newCase += table[y-1][x+1]
				nbCases +=1
	if y< lenY:
		if x>0:
			if nbClose (table[y][x], table[y][x-1], nbLim):
				newCase += table[y+1][x-1]
				nbCases +=1
		if x< lenX:
			if nbClose (table[y][x], table[y][x-1], nbLim):
				newCase += table[y+1][x+1]
				nbCases +=1
	return newCase / nbCases

def blurrVa (table, nbLim):
	rangeX = range (len (table[0]))
	rangeY = range (len (table))
	for y in rangeY:
		for x in rangeX: table[y][x] = blurrOne (table, y,x, nbLim)
	return table

def blurrVb (table, nbLim):
	step = nbLim / 10.0
	rangeStep = ( 0, step, 2.0 * step, 3.0 * step, 4.0 * step, 5.0 * step, 6.0 * step, 7.0 * step, 8.0 * step, 9.0 * step, nbLim )
	rangeX = range (len (table[0]))
	rangeY = range (len (table))
	for y in rangeY:
		for x in rangeX:
			s=0
			while table[y][x] > rangeStep[s]: s+=1
			table[y][x] = rangeStep[s]
	return table
