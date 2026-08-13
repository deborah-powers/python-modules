#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import random

def compareText (itemA, itemB, aliMatrix, a, b):
	aliScore =0
	if itemA == itemB: aliScore = scoreAli
	elif itemA + itemB in scoreMatrix.keys (): aliScore = scoreMatrix [itemA + itemB ]
	elif itemB + itemA in scoreMatrix.keys (): aliScore = scoreMatrix [itemB + itemA ]
	scoreTmp =[
		aliMatrix [a-1][b] + scoreGap,
		aliMatrix [a-1][b-1] + aliScore,
		aliMatrix [a][b-1] + scoreGap
	]
	aliScore = max (scoreTmp)
	return aliScore, scoreTmp.index (aliScore) -1

def prependList (liste, item):
	listeNew =[ item ]
	for old in liste: listeNew.append (old)
	return listeNew

def newList():
	return []

def compareList (itemA, itemB, aliMatrix, a, b):
	if itemA == itemB: return scoreAli, 0
	else: return 0, random.choice (scoreChoice)

def align (anyA, anyB, funcPrepend, funcCompare, funcNew):
	# préparer les éléments
	anyA = funcPrepend (anyA, '_')
	anyB = funcPrepend (anyB, '_')
	# construire les matrices
	aliMatrix =[]
	aliPath =[]
	rangeA = range (1, len (anyA))
	rangeB = range (1, len (anyB))
	aliMatrix.append ([0])
	aliPath.append ([0])
	for b in rangeB:
		aliMatrix[0].append (scoreGap *b)
		aliPath[0].append (1)
	for a in rangeA:
		aliMatrix.append ([ scoreGap *a ])
		aliPath.append ([-1])
		for b in rangeB:
			aliMatrix[-1].append (0)
			aliPath[-1].append (0)
	# phase aller
	for a in rangeA:
		for b in rangeB: aliMatrix[a][b], aliPath[a][b] = funcCompare (anyA[a], anyB[b], aliMatrix, a, b)
	# phase retour
	anyAnew = funcNew()
	anyBnew = funcNew()
	lenA = len (anyA) -1
	lenB = len (anyB) -1
	while lenA >0 or lenB >0:
		if aliPath [lenA][lenB] ==0:
			anyAnew = funcPrepend (anyAnew, anyA [lenA])
			anyBnew = funcPrepend (anyBnew, anyB [lenB])
			lenA -=1
			lenB -=1
		elif aliPath [lenA][lenB] ==1:
			anyAnew = funcPrepend (anyAnew, '_')
			anyBnew = funcPrepend (anyBnew, anyB [lenB])
			lenB -=1
		else:
			anyAnew = funcPrepend (anyAnew, anyA [lenA])
			anyBnew = funcPrepend (anyBnew, '_')
			lenA -=1
	aliScore = aliMatrix[-1][-1] / len (anyAnew)
	return aliScore, anyAnew, anyBnew

def alignText (textA, textB):
	return align (textA, textB, prependText, compareText, newText)

def alignList (listA, listB):
	return align (listA, listB, prependList, compareList, newList)


def test():
	textA = 'abcd'
	textB = '5555'
	listA =[ 'a', 'b', 'c', 'd']
	listB =[ '5', '5', '5', '5']

	print ('textes identiques\n', alignText (textA, textA))
	print ('textes différents\n', alignText (textA, textB))
	print ('listes identiques\n', alignList (listA, listA))
	print ('listes différentes\n', alignList (listA, listB))


""" ------------------------ créer la matrice des scores ------------------------ """

def setScorePair (scoreMatrix, score, la, lo):
	scoreMatrix [la + lo] = score
	scoreMatrix [lo + la] = score

def setScoreGroup (scoreMatrix, score, letterGroup):
	for la in letterGroup:
		for lo in letterGroup: setScorePair (scoreMatrix, score, la, lo)

def createScoreMatrix():
	# renvoi un dictionnaire { appariment2char: score }, { 'ab': 5 }
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
	scoreMatrix = {}
	setScoreGroup (scoreMatrix, 5, allLetters)
	setScoreGroup (scoreMatrix, 4, alphabet)
	setScoreGroup (scoreMatrix, 3, voyels)
	setScoreGroup (scoreMatrix, 3, consomns)
	setScoreGroup (scoreMatrix, 3, numbers)
	setScoreGroup (scoreMatrix, 3, points)
	setScoreGroup (scoreMatrix, 3, tirets)
	setScoreGroup (scoreMatrix, 2, spaces)
	setScoreGroup (scoreMatrix, 2, quotes)
	# cas particuliers
	setScorePair (scoreMatrix, 2, '/', '\\')
	setScorePair (scoreMatrix, 2, '(', '[')
	setScorePair (scoreMatrix, 2, ')', ']')
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

scoreGap =6
scoreMatrix = createScoreMatrix()

def initAliMatrix (textA, textI):
	# les textes commencent déjà par un caractère symbolisant le gap
	lenI = len (textI)
	aliMatrix =[]
	for char in textA: aliMatrix.append (lenI * [ scoreGap ])	# initier la matrice vide
	rangeO = range (1, len (textA))
	for a in rangeO: aliMatrix[a][0] = aliMatrix[a-1][0] + scoreGap
	rangeO = range (1, lenI)
	for i in rangeO: aliMatrix[0][i] = aliMatrix[0][i-1] + scoreGap
	return aliMatrix

def createAliMatrix (textA, textI):
	textA = '#'+ textA	## symbolise le gap
	textI = '#'+ textI
	aliMatrix = initAliMatrix (textA, textI)




