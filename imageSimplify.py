#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from kmeans import Kmeans, KmeansTablesNb
from imageCls import ImageFile
import loggerFct as log

class KmeansBw (Kmeans):
	def __init__ (self, colors):
		Kmeans.__init__ (self, 15, colors)

	def computeScore (self, groupId, itemId):
		score = self.groups [groupId][0] - self.values [itemId]
		if score <0: score *=-1
		return score

	def computeMean (self, groupId):
		groupLen = len (self.groups [groupId])
		groupRange = range (1, groupLen)
		score =0
		for g in groupRange: score += self.groups [groupId][g]
		groupLen -=1
		score /= groupLen
		return score

def findColorIslands (self):
	colors = self.getColors()
	lenH = len (self.array)
	lenW = len (self.array[0])
	rangeHeight = range (lenH)
	rangeWidth = range (lenW)
	startIsland = set()
	for color in colors:
		colorArea = (self.array == color)
		# lignes verticales
		for h in rangeHeight:
			nb=0
			for w in rangeWidth:
				if colorArea[h][w]: nb+=1
				elif nb>=3: nb=0
				elif nb>0:
					nbk = nb
					rangeK = range (w-nb, w+1)
					if h>0:
						for k in rangeK:
							if colorArea[h-1][k]: nbk+=1
					if h< lenH-1:
						for k in rangeK:
							if colorArea[h+1][k]: nbk+=1
					if nbk <3: startIsland.add ((h,w))
					nb=0
		# lignes horizontales
		for w in rangeWidth:
			nb=0
			for h in rangeHeight:
				if colorArea[h][w]: nb+=1
				elif nb>=3: nb=0
				elif nb>0:
					nbk = nb
					rangeK = range (h-nb, h+1)
					if w>0:
						for k in rangeK:
							if colorArea[k][w-1]: nbk+=1
					if w< lenW -1:
						for k in rangeK:
							if colorArea[k][w+1]: nbk+=1
					if nbk <3: startIsland.add ((h,w))
					nb=0
	print (startIsland)




def eraseLonelyPixelsNb (imageArray):
	# seuls les quatre pixels touchant directement le pixel central sont pris en compte
	# l'image est en noir et blanc
	# les coins de l'image
	if imageArray[0][0] != imageArray[0][1] and imageArray[0][0] != imageArray[1][0]: imageArray[0][0] = imageArray[1][0]
	if imageArray[-1][0] != imageArray[-1][1] and imageArray[-1][0] != imageArray[-2][0]: imageArray[-1][0] = imageArray[-2][0]
	if imageArray[0][-1] != imageArray[0][-2] and imageArray[0][-1] != imageArray[1][-1]: imageArray[0][-1] = imageArray[1][-1]
	if imageArray[-1][-1] != imageArray[-1][-2] and imageArray[-1][-1] != imageArray[-2][-1]: imageArray[-1][-1] = imageArray[-2][-1]
	# les bords de l'image
	rangeWidth = range (len (imageArray[0]))
	rangeHeight = range (len (imageArray))
	for w in rangeWidth:
		if imageArray[0][w] != imageArray[1][w]: imageArray[0][w] = imageArray[1][w]
		if imageArray[-1][w] != imageArray[-2][w]: imageArray[-1][w] = imageArray[-2][w]
	for h in rangeHeight:
		if imageArray[h][0] != imageArray[h][1]: imageArray[h][0] = imageArray[h][1]
		if imageArray[h][-1] != imageArray[h][-2]: imageArray[h][-1] = imageArray[h][-2]
	# le centre de l'image
	rangeWidth = range (1, len (imageArray[0]) -1)
	rangeHeight = range (1, len (imageArray) -1)
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h][w] == imageArray[h][w+1] or imageArray[h][w] == imageArray[h][w-1]: continue
			elif imageArray[h][w] == imageArray[h+1][w] or imageArray[h][w] == imageArray[h-1][w]: continue
			elif imageArray[h+1][w] == imageArray[h-1][w]: imageArray[h][w] = imageArray[h-1][w]
			elif imageArray[h][w+1] == imageArray[h][w-1]: imageArray[h][w] = imageArray[h][w-1]
			elif imageArray[h][w+1] == imageArray[h+1][w] or imageArray[h][w-1] == imageArray[h+1][w]: imageArray[h][w] = imageArray[h+1][w]
			elif imageArray[h][w+1] == imageArray[h-1][w] or imageArray[h][w-1] == imageArray[h-1][w]: imageArray[h][w] = imageArray[h-1][w]
	return imageArray

def eraseDoublonPixelsNb (imageArray):
	# effacer les couples de pixels au milieu d'un fond uni. lancé après eraseLonelyPixelsNb, il n'y a plus de pixels isolés
	# l'image est en noir et blanc
	# les coins de l'image
	if imageArray[0][0] == imageArray[0][1] and imageArray[0][0] != imageArray[0][2]:
		if imageArray[0][0] != imageArray[1][0] and imageArray[0][0] != imageArray[1][1]:
			imageArray[0][0] = imageArray[0][2]
			imageArray[0][1] = imageArray[0][2]
	if imageArray[0][0] == imageArray[1][0] and imageArray[0][0] != imageArray[2][0]:
		if imageArray[0][0] != imageArray[0][1] and imageArray[0][0] != imageArray[1][1]:
			imageArray[0][0] = imageArray[2][0]
			imageArray[1][0] = imageArray[2][0]
	if imageArray[-1][0] == imageArray[-1][1] and imageArray[-1][0] != imageArray[-1][2]:
		if imageArray[-1][0] != imageArray[-2][0] and imageArray[-1][0] != imageArray[-2][1]:
			imageArray[-1][0] = imageArray[-1][2]
			imageArray[-1][1] = imageArray[-1][2]
	if imageArray[-1][0] == imageArray[-2][0] and imageArray[-1][0] != imageArray[-3][0]:
		if imageArray[-1][0] != imageArray[-1][1] and imageArray[-1][0] != imageArray[-2][1]:
			imageArray[-1][0] = imageArray[-3][0]
			imageArray[-2][0] = imageArray[-3][0]
	if imageArray[0][-1] == imageArray[0][-2] and imageArray[0][-1] != imageArray[0][-3]:
		if imageArray[0][-1] != imageArray[1][-1] and imageArray[0][-1] != imageArray[1][-2]:
			imageArray[0][-1] = imageArray[0][-3]
			imageArray[0][-2] = imageArray[0][-3]
	if imageArray[0][-1] == imageArray[1][-1] and imageArray[0][-1] != imageArray[2][-1]:
		if imageArray[0][-1] != imageArray[0][-2] and imageArray[0][-1] != imageArray[1][-2]:
			imageArray[0][-1] = imageArray[2][-1]
			imageArray[1][-1] = imageArray[2][-1]
	if imageArray[-1][-1] == imageArray[-1][-2] and imageArray[-1][-1] != imageArray[-1][-3]:
		if imageArray[-1][-1] != imageArray[-2][-1] and imageArray[-1][-1] != imageArray[-2][-2]:
			imageArray[-1][-1] = imageArray[-1][-3]
			imageArray[-1][-2] = imageArray[-1][-3]
	if imageArray[-1][-1] == imageArray[-2][-1] and imageArray[-1][-1] != imageArray[-3][-1]:
		if imageArray[-1][-1] != imageArray[-1][-2] and imageArray[-1][-1] != imageArray[-2][-2]:
			imageArray[-1][-1] = imageArray[-3][-1]
			imageArray[-2][-1] = imageArray[-3][-1]
	# les bords de l'image
	# le centre de l'image
	rangeWidth = range (1, len (imageArray[0]) -2)
	rangeHeight = range (1, len (imageArray) -1)
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h][w] == imageArray[h][w+1] and imageArray[h][w] != imageArray[h][w-1] and imageArray[h][w] != imageArray[h][w+2]:
				if imageArray[h][w] != imageArray[h-1][w] and imageArray[h][w] != imageArray[h+1][w]:
					if imageArray[h][w] != imageArray[h-1][w+1] and imageArray[h][w] != imageArray[h+1][w+1]:
						imageArray[h][w] = imageArray[h][w-1]
						imageArray[h][w+1] = imageArray[h][w+2]
	rangeWidth = range (1, len (imageArray[0]) -1)
	rangeHeight = range (1, len (imageArray) -2)
	for h in rangeHeight:
		for w in rangeWidth:
			if imageArray[h][w] == imageArray[h+1][w] and imageArray[h][w] != imageArray[h-1][w] and imageArray[h][w] != imageArray[h+2][w]:
				if imageArray[h][w] != imageArray[h][w-1] and imageArray[h][w] != imageArray[h][w+1]:
					if imageArray[h][w] != imageArray[h+1][w-1] and imageArray[h][w] != imageArray[h+1][w+1]:
						imageArray[h][w] = imageArray[h-1][w]
						imageArray[h+1][w] = imageArray[h+2][w]
	return imageArray

def simplifyColors (self):
	self.tobw()
	self.toArray()
	colors = self.getColors()
	colorKmeans = KmeansBw (colors)
	colorKmeans.BuildGroup()
	groupRange = range (len (colorKmeans.groups))
	for g in groupRange: colorKmeans.groups[g][0] = int (colorKmeans.groups[g][0])
	for group in colorKmeans.groups:
		for color in group:
			grey = self.array.T
			colorArea = (grey == color)
			self.array[colorArea.T] = group[0]
	self.array = eraseLonelyPixelsNb (self.array)
	self.findColorIslands()
#	self.array = eraseDoublonPixelsNb (self.array)
	self.fromArray()

setattr (ImageFile, 'simplifyColors', simplifyColors)
setattr (ImageFile, 'findColorIslands', findColorIslands)
