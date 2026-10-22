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

class AlignList():
	def __init__ (self, listA, listI):
		self.listA = listA
		self.listI = listI
		self.scoreGapOpen =2
		self.scoreGapFill =2
		self.aliMatrix =[]

	def initAliMatrix (self):
		# les listes commencent déjà par un caractère symbolisant le gap
		lenI = len (self.listI)
		self.aliMatrix =[]
		for char in self.listA:
			self.aliMatrix.append ([])	# initier la matrice vide
			for chir in self.listI: self.aliMatrix[-1].append ((self.scoreGapOpen, 3))
		rangeO = range (1, len (self.listA))
		for a in rangeO: self.aliMatrix[a][0] =( self.aliMatrix[a-1][0][0] + self.scoreGapOpen, 3)
		rangeO = range (1, lenI)
		for i in rangeO: self.aliMatrix[0][i] =( self.aliMatrix[0][i-1][0] + self.scoreGapOpen, 3)

	def computeCaseScore (self, a,i):
		scoreTrio =[]
		scoreTrio.append (self.aliMatrix[a-1][i][0] + self.scoreGapFill)	# gap en i aligné en face de la lettre de a
		scoreSim =0
		if self.listA[a] != self.listI[i]: scoreSim = self.scoreGapFill
		scoreTrio.append (self.aliMatrix[a-1][i-1][0] + scoreSim)
		scoreTrio.append (self.aliMatrix[a][i-1][0] + self.scoreGapFill)	# gap en a aligné en face de la lettre de i
	#	scoreTrio.append (self.aliMatrix[0][i][0])	# gap en a aligné en face de la lettre de i
		return getPosScoreTrioMin (scoreTrio)

	def createAliMatrix (self):
		self.listA.insert (0, "_")	# le gap
		self.listI.insert (0, "_")
		self.initAliMatrix()
		lenA = len (self.listA)
		lenI = len (self.listI)
		rangeA = range (1, lenA)
		rangeI = range (1, lenI)
		for a in rangeA:
			for i in rangeI: self.aliMatrix[a][i] = self.computeCaseScore (a,i)

	def upwalkAliMatrix (self):
		a= len (self.listA) -1
		i= len (self.listI) -1
		listAnv =[]
		listInv =[]
		while a>0 and i>0:
			if self.aliMatrix[a][i][1] ==1:	# alignement
				listAnv.insert (0, self.listA[a])
				listInv.insert (0, self.listI[i])
				a-=1
				i-=1
			elif self.aliMatrix[a][i][1] ==0:	# gap dans i
				listAnv.insert (0, self.listA[a])
				listInv.insert (0, "_")
				a-=1
			elif self.aliMatrix[a][i][1] ==2:	# gap dans a
				listAnv.insert (0, "_")
				listInv.insert (0, self.listI[i])
				i-=1
		while a>0:	# gap dans i
			listAnv.insert (0, self.listA[a])
			listInv.insert (0, "_")
			a-=1
		while i>0:	# gap dans a
			listAnv.insert (0, "_")
			listInv.insert (0, self.listI[i])
			i-=1
	#	listAnv = listAnv[::-1]
		return listAnv, listInv

	def align (self):
		print ('séquences originales\n' + str (self.listA) +'\n'+ str (self.listI))
		self.createAliMatrix()
		listAnv, listInv = self.upwalkAliMatrix()
		print ('séquences finales\n' + str (listAnv) +'\n'+ str (listInv))

alignList = AlignList ([ 'a', '7', 'e', '8', 'g', '9' ], [ '7', 'a', 'e', '8', 'g' ])
alignList.align()