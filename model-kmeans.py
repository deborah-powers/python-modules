#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
modèle de tri de liste par la méthode des kmeans
scoreDifference, computeScore, computeMean sont à adapter par l'utilisateur
"""
scoreDifference =1000

def computeScore (itemA, itemO):
	return (int (itemA[0]) - int (itemO[0])) **2 + (int (itemA[1]) - int (itemO[1])) **2 + (int (itemA[2]) - int (itemO[2])) **2

def computeMean (group):
	lenGroup = len (group) -1
	newMean = [0,0,0]
	newMean[0] = (group[0][0] * lenGroup + itemList[c][0]) / (lenGroup +1)
	newMean[1] = (group[0][1] * lenGroup + itemList[c][1]) / (lenGroup +1)
	newMean[2] = (group[0][2] * lenGroup + itemList[c][2]) / (lenGroup +1)
	return newMean

def kmeans (itemList):
	groups =[[ itemList[0], itemList[0] ]]	# la case 0 contient la moyenne
	rangeItem = range (1, len (itemList))
	for c in rangeItem:
		# calculer les scores de la color étudiée avec la moyenne de chaque groupe
		groupId =0
		groupScore = 1000000
		rangeGroup = range (len (groups))
		for g in rangeGroup:
			score = computeScore (groups[g][0], itemList[c])
			if score < groupScore:
				groupScore = score
				groupId = g
		# trouver le groupe dont elle est le plus proche
		if groupScore <= scoreDifference:
			# calculer la nouvelle moyenne
			groups [groupId][0] = computeMean (groups [groupId])
			groups [groupId].append (itemList[c])
		# créer un nouveau groupe
		else: groups.append ([ itemList[c], itemList[c] ])
	return groups