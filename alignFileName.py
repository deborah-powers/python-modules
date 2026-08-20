#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import random

""" ------------------------ créer la matrice des scores ------------------------ """

def setScorePair (scoreMatrix, score, la, lo):
	scoreMatrix [la + lo] = score
	scoreMatrix [lo + la] = score

def setScoreGroup (scoreMatrix, score, letterGroup):
	lenGroup = len (letterGroup)
	rangeGroup = range (lenGroup -1)
	for a in rangeGroup:
		rangeTmp = range (a+1, lenGroup)
		for b in rangeTmp: setScorePair (letterGroup[a], letterGroup[b])
		#	if letterGroup[a] + letterGroup[b] in scoreMatrix.keys():

def createScoreMatrix():
	# renvoi un dictionnaire { appariment2char: score }, { 'ab': 5 }
	allLetters = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz 0123456789-_.'
	alphabet = 'aàbcçdeéèêëfghiîïjklmnoôöpqrstuùvwxyz'
	voyels = 'aàeéèêëiîïoôöuùy';
	consomns = 'bcçdfghjklmnpqrstvwxz'
	numbers = '0123456789'
	scoreMatrix = {}
	setScoreGroup (scoreMatrix, 5, allLetters)
	setScoreGroup (scoreMatrix, 4, alphabet)
	setScoreGroup (scoreMatrix, 3, voyels)
	setScoreGroup (scoreMatrix, 3, consomns)
	setScoreGroup (scoreMatrix, 3, numbers)
	# cas particuliers
	setScorePair (scoreMatrix, 3, '.', '-')
	setScorePair (scoreMatrix, 3, '.', '_')
	setScorePair (scoreMatrix, 3, '-', '_')
	setScorePair (scoreMatrix, 1, " ", '_')
	setScorePair (scoreMatrix, 1, 'a', 'à')
	setScorePair (scoreMatrix, 1, 'u', 'ù')
	setScorePair (scoreMatrix, 1, 'u', 'y')
	setScorePair (scoreMatrix, 1, 'c', 'ç')
	setScorePair (scoreMatrix, 1, 'i', 'î')
	setScorePair (scoreMatrix, 1, 'i', 'ï')
	setScorePair (scoreMatrix, 1, 'î', 'ï')
	setScorePair (scoreMatrix, 1, 'i', 'y')
	setScorePair (scoreMatrix, 1, 'o', 'ô')
	setScorePair (scoreMatrix, 1, 'o', 'ö')
	setScorePair (scoreMatrix, 1, 'ô', 'ö')
	setScorePair (scoreMatrix, 1, 'e', 'é')
	setScorePair (scoreMatrix, 1, 'e', 'è')
	setScorePair (scoreMatrix, 1, 'e', 'ê')
	setScorePair (scoreMatrix, 1, 'e', 'ë')
	setScorePair (scoreMatrix, 1, 'e', '€')
	setScorePair (scoreMatrix, 1, 'é', 'è')
	setScorePair (scoreMatrix, 1, 'é', 'ê')
	setScorePair (scoreMatrix, 1, 'é', 'ë')
	setScorePair (scoreMatrix, 1, 'è', 'ê')
	setScorePair (scoreMatrix, 1, 'è', 'ë')
	setScorePair (scoreMatrix, 1, 'ê', 'ë')
	for l in allLetters: scoreMatrix[l+l] =0
	return scoreMatrix

"""
0 identiques
1 variantes de lettres
2 lettres souvent confondues
3 lettres de la même catégories
4 lettres de l'alphabet
5 le reste
"""
""" ------------------------ créer la matrice d'alignement ------------------------ """

scoreGapOpen =2
scoreGapFill =2
scoreMatrix = createScoreMatrix()

def initAliMatrix (textA, textI):
	# les textes commencent déjà par un caractère symbolisant le gap
	lenI = len (textI)
	aliMatrix =[]
	for char in textA:
		aliMatrix.append ([])	# initier la matrice vide
		for chir in textI: aliMatrix[-1].append ((scoreGapOpen, 3))
	rangeO = range (1, len (textA))
	for a in rangeO: aliMatrix[a][0] =( aliMatrix[a-1][0][0] + scoreGapOpen, 3)
	rangeO = range (1, lenI)
	for i in rangeO: aliMatrix[0][i] =( aliMatrix[0][i-1][0] + scoreGapOpen, 3)
	return aliMatrix

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

def computeCaseScore (a,i, textA, textI, aliMatrix):
	scoreTrio =[]
	scoreTrio.append (aliMatrix[a-1][i][0] + scoreGapFill)	# gap en i aligné en face de la lettre de a
	scoreTrio.append (aliMatrix[a-1][i-1][0] + scoreMatrix [textA[a] + textI[i]])
	scoreTrio.append (aliMatrix[a][i-1][0] + scoreGapFill)	# gap en a aligné en face de la lettre de i
#	scoreTrio.append (aliMatrix[0][i][0])	# gap en a aligné en face de la lettre de i
	return getPosScoreTrioMin (scoreTrio)

def createAliMatrix (textA, textI):
	textA = '#'+ textA	## symbolise le gap
	textI = '#'+ textI
	aliMatrix = initAliMatrix (textA, textI)
	lenA = len (textA)
	lenI = len (textI)
	rangeA = range (1, lenA)
	rangeI = range (1, lenI)
	for a in rangeA:
		for i in rangeI: aliMatrix[a][i] = computeCaseScore (a,i, textA, textI, aliMatrix)
	return aliMatrix

def upwalkAliMatrix (textA, textI, aliMatrix):
	textA = '#'+ textA	## symbolise le gap
	textI = '#'+ textI
	a= len (textA) -1
	i= len (textI) -1
	textAnv =""
	textInv =""
	while a>0 and i>0:
		if aliMatrix[a][i][1] ==1:	# alignement
			textAnv = textA[a] + textAnv
			textInv = textI[i] + textInv
			a-=1
			i-=1
		elif aliMatrix[a][i][1] ==0:	# gap dans i
			textAnv = textA[a] + textAnv
			textInv = '#'+ textInv
			a-=1
		elif aliMatrix[a][i][1] ==2:	# gap dans a
			textAnv = '#'+ textAnv
			textInv = textI[i] + textInv
			i-=1
	return textAnv, textInv

def alignText (textA, textI):
	print (textA, '\n', textI, '\n')
	aliMatrix = createAliMatrix (textA, textI)
	textAnv, textInv = upwalkAliMatrix (textA, textI, aliMatrix)
	print (textAnv, '\n', textInv)

alignText ('zrzog,el', 'nanczk,vl;')