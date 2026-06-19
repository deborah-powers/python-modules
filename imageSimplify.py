#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
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

def findColorIsland (self, coords, island, neighbourgs):
	if coords in island: return island, neighbourgs
	island.add (coords)
	neighbourgList =[]
	if coords[0] >0:
		if self.array[coords[0]][coords[1]] == self.array[coords[0] -1][coords[1]]: neighbourgList.append ((coords[0] -1, coords[1]))
		elif self.array[coords[0] -1][coords[1]] in neighbourgs.keys(): neighbourgs [self.array[coords[0] -1][coords[1]]] +=1
		else: neighbourgs [self.array[coords[0] -1][coords[1]]] =1
	if coords[0] < len (self.array) -1:
		if self.array[coords[0]][coords[1]] == self.array[coords[0] +1][coords[1]]: neighbourgList.append ((coords[0] +1, coords[1]))
		elif self.array[coords[0] +1][coords[1]] in neighbourgs.keys(): neighbourgs [self.array[coords[0] +1][coords[1]]] +=1
		else: neighbourgs [self.array[coords[0] +1][coords[1]]] =1
	if coords[1] >0:
		if self.array[coords[0]][coords[1]] == self.array[coords[0]][coords[1] -1]: neighbourgList.append ((coords[0], coords[1] -1))
		elif self.array[coords[0]][coords[1] -1] in neighbourgs.keys(): neighbourgs [self.array[coords[0]][coords[1] -1]] +=1
		else: neighbourgs [self.array[coords[0]][coords[1] -1]] =1
	if coords[1] < len (self.array[0]) -1:
		if self.array[coords[0]][coords[1]] == self.array[coords[0]][coords[1] +1]: neighbourgList.append ((coords[0], coords[1] +1))
		elif self.array[coords[0]][coords[1] +1] in neighbourgs.keys(): neighbourgs [self.array[coords[0]][coords[1] +1]] +=1
		else: neighbourgs [self.array[coords[0]][coords[1] +1]] =1
	if len (neighbourgList) >2:	# si plus de trois éléments dans l'îlot, il est considéré comme un continent
		for neigh in neighbourgList: island.add (neigh)
	else:
		for neigh in neighbourgList: island, neighbourgs = self.findColorIsland (neigh, island, neighbourgs)
	return island, neighbourgs

def eraseColorIsland (self, island, neighbourgs):
	colors = neighbourgs.keys()
	color = list (colors)[0]
	for col in colors:
		if neighbourgs [col] > neighbourgs [color]: color = col
	for h,w in island: self.array[h][w] = color

def eraseColorIslands (self):
	rangeHeight = range (len (self.array))
	rangeWidth = range (len (self.array[0]))
	seenPoints = set()
	for h in rangeHeight:
		for w in rangeWidth:
			island, neighbourgs = self.findColorIsland ((h,w), set(), dict())
			seenPoints.update (island)
			if len (island) <4: self.eraseColorIsland (island, neighbourgs)

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
	self.eraseColorIslands()
	self.fromArray()

setattr (ImageFile, 'simplifyColors', simplifyColors)
setattr (ImageFile, 'eraseColorIslands', eraseColorIslands)
setattr (ImageFile, 'findColorIsland', findColorIsland)
setattr (ImageFile, 'eraseColorIsland', eraseColorIsland)

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


