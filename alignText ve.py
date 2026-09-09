#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

def getPosScoreTrioMin (scoreTrio):
	score = scoreTrio[0]
	pos =0
	if scoreTrio[1] < score:
		score = scoreTrio[1]
		pos =1
	if scoreTrio[2] < score:
		score = scoreTrio[2]
		pos =2
	return score, pos

class AlignText():
	def __init__ (self, textA, textI):
		self.textA = textA
		self.textI = textI
		self.scoreGapOpen =2
		self.scoreGapFill =2
		self.aliMatrix =[]
		self.scoreMatrix ={}

	""" ------------------------ créer la matrice des scores ------------------------ """

	def setScorePair (self, score, la, lo):
		self.scoreMatrix [la + lo] = score
		self.scoreMatrix [lo + la] = score

	def setScoreGroup (self, score, letterGroup):
		lenGroup = len (letterGroup)
		rangeGroup = range (lenGroup -1)
		for a in rangeGroup:
			rangeTmp = range (a+1, lenGroup)
			for b in rangeTmp: self.setScorePair (score, letterGroup[a], letterGroup[b])

	def createScoreMatrix (self):
		# renvoi un dictionnaire { appariment2char: score }, { 'ab': 5 }
		# varie chez les classes filles
		allLetters = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz \t\n\r0123456789"\'`/\\=+*-~_.?!:;,¨^°%$@&#<>{}()[]'
		alphabet = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz'
		voyels = 'aàeéèêëiîïoôöuùy';
		consomns = 'bcçdfghjklmnpqrstvwxz'
		numbers = '0123456789'
		spaces = ' \t\n\r';
		quotes = '"\'`';
		brackets = '{}()[]';
		tirets = '_-~';
		points = '.?!:;,'
		mathOperator ='+-*/^<>='
		others = '^°%$@&#'
		self.scoreMatrix = {}
		self.setScoreGroup (5, allLetters)
		self.setScoreGroup (4, alphabet)
		self.setScoreGroup (3, voyels)
		self.setScoreGroup (3, consomns)
		self.setScoreGroup (3, numbers)
		self.setScoreGroup (3, points)
		self.setScoreGroup (3, tirets)
		self.setScoreGroup (2, spaces)
		self.setScoreGroup (2, quotes)
		# cas particuliers
		self.setScorePair (2, '/', '\\')
		self.setScorePair (2, '(', '[')
		self.setScorePair (2, ')', ']')
		self.setScorePair (1, 'a', 'à')
		self.setScorePair (1, 'u', 'ù')
		self.setScorePair (1, 'u', 'y')
		self.setScorePair (1, 'c', 'ç')
		self.setScorePair (1, 'i', 'î')
		self.setScorePair (1, 'i', 'ï')
		self.setScorePair (1, 'î', 'ï')
		self.setScorePair (1, 'i', 'y')
		self.setScorePair (1, 'o', 'ô')
		self.setScorePair (1, 'o', 'ö')
		self.setScorePair (1, 'ô', 'ö')
		self.setScorePair (1, 'e', 'é')
		self.setScorePair (1, 'e', 'è')
		self.setScorePair (1, 'e', 'ê')
		self.setScorePair (1, 'e', 'ë')
		self.setScorePair (1, 'e', '€')
		self.setScorePair (1, 'é', 'è')
		self.setScorePair (1, 'é', 'ê')
		self.setScorePair (1, 'é', 'ë')
		self.setScorePair (1, 'è', 'ê')
		self.setScorePair (1, 'è', 'ë')
		self.setScorePair (1, 'ê', 'ë')
		for l in allLetters: self.scoreMatrix[l+l] =0

	"""
	0 identiques
	1 variantes de lettres
	2 lettres souvent confondues
	3 lettres de la même catégories
	4 lettres de l'alphabet
	5 le reste
	"""
	""" ------------------------ créer la matrice d'alignement ------------------------ """

	def initAliMatrix (self):
		# les textes commencent déjà par un caractère symbolisant le gap
		lenI = len (self.textI)
		self.aliMatrix =[]
		for char in self.textA:
			self.aliMatrix.append ([])	# initier la matrice vide
			for chir in self.textI: self.aliMatrix[-1].append ((self.scoreGapOpen, 3))
		rangeO = range (1, len (self.textA))
		for a in rangeO: self.aliMatrix[a][0] =( self.aliMatrix[a-1][0][0] + self.scoreGapOpen, 3)
		rangeO = range (1, lenI)
		for i in rangeO: self.aliMatrix[0][i] =( self.aliMatrix[0][i-1][0] + self.scoreGapOpen, 3)

	def computeCaseScore (self, a,i):
		scoreTrio =[]
		scoreTrio.append (self.aliMatrix[a-1][i][0] + self.scoreGapFill)	# gap en i aligné en face de la lettre de a
		scoreTrio.append (self.aliMatrix[a-1][i-1][0] + self.scoreMatrix [self.textA[a] + self.textI[i]])
		scoreTrio.append (self.aliMatrix[a][i-1][0] + self.scoreGapFill)	# gap en a aligné en face de la lettre de i
	#	scoreTrio.append (self.aliMatrix[0][i][0])	# gap en a aligné en face de la lettre de i
		return getPosScoreTrioMin (scoreTrio)

	def createAliMatrix (self):
		self.textA = '#'+ self.textA	## symbolise le gap
		self.textI = '#'+ self.textI
		self.initAliMatrix()
		lenA = len (self.textA)
		lenI = len (self.textI)
		rangeA = range (1, lenA)
		rangeI = range (1, lenI)
		for a in rangeA:
			for i in rangeI: self.aliMatrix[a][i] = self.computeCaseScore (a,i)

	def upwalkAliMatrix (self):
		a= len (self.textA) -1
		i= len (self.textI) -1
		textAnv =""
		textInv =""
		while a>0 and i>0:
			if self.aliMatrix[a][i][1] ==1:	# alignement
				textAnv = self.textA[a] + textAnv
				textInv = self.textI[i] + textInv
				a-=1
				i-=1
			elif self.aliMatrix[a][i][1] ==0:	# gap dans i
				textAnv = self.textA[a] + textAnv
				textInv = '_'+ textInv
				a-=1
			elif self.aliMatrix[a][i][1] ==2:	# gap dans a
				textAnv = '_'+ textAnv
				textInv = self.textI[i] + textInv
				i-=1
		while a>0:	# gap dans i
			textAnv = self.textA[a] + textAnv
			textInv = '_'+ textInv
			a-=1
		while i>0:	# gap dans a
			textAnv = '_'+ textAnv
			textInv = self.textI[i] + textInv
			i-=1
	#	textAnv = textAnv[::-1]
		return textAnv, textInv

	def align (self):
		print ('séquences originales\n' + self.textA +'\n'+ self.textI)
		self.createScoreMatrix()
		self.createAliMatrix()
		textAnv, textInv = self.upwalkAliMatrix()
		print ('séquences finales\n' + textAnv +'\n'+ textInv)

alignText = AlignText ('zrzog,el', 'nanczk,vl;')
alignText.align()

class AlignFileName (AlignText):
	def createScoreMatrix (self):
		# renvoi un dictionnaire { appariment2char: score }, { 'ab': 5 }
		allLetters = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz 0123456789-_.'
		alphabet = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz'
		voyels = 'aàeéèêëiîïoôöuùy';
		consomns = 'bcçdfghjklmnpqrstvwxz'
		numbers = '0123456789'
		self.scoreMatrix = {}
		self.setScoreGroup (5, allLetters)
		self.setScoreGroup (4, alphabet)
		self.setScoreGroup (3, voyels)
		self.setScoreGroup (3, consomns)
		self.setScoreGroup (3, numbers)
		# cas particuliers
		self.setScorePair (3, '.', '-')
		self.setScorePair (3, '.', '_')
		self.setScorePair (3, '-', '_')
		self.setScorePair (1, " ", '_')
		self.setScorePair (1, 'a', 'à')
		self.setScorePair (1, 'u', 'ù')
		self.setScorePair (1, 'u', 'y')
		self.setScorePair (1, 'c', 'ç')
		self.setScorePair (1, 'i', 'î')
		self.setScorePair (1, 'i', 'ï')
		self.setScorePair (1, 'î', 'ï')
		self.setScorePair (1, 'i', 'y')
		self.setScorePair (1, 'o', 'ô')
		self.setScorePair (1, 'o', 'ö')
		self.setScorePair (1, 'ô', 'ö')
		self.setScorePair (1, 'e', 'é')
		self.setScorePair (1, 'e', 'è')
		self.setScorePair (1, 'e', 'ê')
		self.setScorePair (1, 'e', 'ë')
		self.setScorePair (1, 'e', '€')
		self.setScorePair (1, 'é', 'è')
		self.setScorePair (1, 'é', 'ê')
		self.setScorePair (1, 'é', 'ë')
		self.setScorePair (1, 'è', 'ê')
		self.setScorePair (1, 'è', 'ë')
		self.setScorePair (1, 'ê', 'ë')
		for l in allLetters: self.scoreMatrix[l+l] =0