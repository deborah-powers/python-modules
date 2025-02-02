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
	newMean[0] = (group[0][0] * lenGroup + values[c][0]) / (lenGroup +1)
	newMean[1] = (group[0][1] * lenGroup + values[c][1]) / (lenGroup +1)
	newMean[2] = (group[0][2] * lenGroup + values[c][2]) / (lenGroup +1)
	return newMean

def kmeans (values):
	groups =[[ values[0], values[0] ]]	# la case 0 contient la moyenne
	rangeItem = range (1, len (values))
	for c in rangeItem:
		# calculer les scores de la color étudiée avec la moyenne de chaque groupe
		groupId =0
		groupscore = 1000000
		rangeGroup = range (len (groups))
		for g in rangeGroup:
			score = computeScore (groups[g][0], values[c])
			if score < groupscore:
				groupscore = score
				groupId = g
		# trouver le groupe dont elle est le plus proche
		if groupscore <= scoreDifference:
			# calculer la nouvelle moyenne
			groups [groupId][0] = computeMean (groups [groupId])
			groups [groupId].append (values[c])
		# créer un nouveau groupe
		else: groups.append ([ values[c], values[c] ])
	return groups

class Kmeans():
	def __init__ (self, scoreDifference, values):
		self.values =[]
		self.groups =[]
		self.scoreDifference = scoreDifference
		self.values.extend (values)
		self.groups =[[ values[0], values[0] ]]
		self.rangeValues = range (len (values))

	def BuildGroup (self):
		for c in self.rangeValues:
			# calculer les scores de la color étudiée avec la moyenne de chaque groupe
			groupId =0
			groupscore = 1000000
			rangeGroup = range (len (self.groups))
			for g in rangeGroup:
				score = self.computeScore (g, c)
				if score < groupscore:
					groupscore = score
					groupId = g
			# trouver le groupe dont elle est le plus proche
			if groupscore <= scoreDifference:
				# calculer la nouvelle moyenne
				self.groups [groupId][0] = self.computeMean (groupId)
				self.groups [groupId].append (self.values[c])
			# créer un nouveau groupe
			else: self.groups.append ([ self.values[c], self.values[c] ])

	def computeScore (self, groupId, itemId):
		raise NotImplementedError ('Please Implement this method')

	def computeMean (groupId):
		raise NotImplementedError ('Please Implement this method')

class KmeansTables (Kmeans):
	def __init__ (self, scoreDifference, table):
		values =[]
		for line in table:
			for item in line:
				if not item in values: values.append (item)
		Kmeans.__init__ (self, scoreDifference, values)

class KmeansTablesNb (KmeansTables):
	def computeScore (self, groupId, itemId):
		return (self.groups [groupId] - self.values[itemId]) **2

	def computeMean (groupId):
		lenGroup = len (self.groups [groupId]) -1
		return (self.groups [groupId][0] * lenGroup + self.values[c]) / (lenGroup +1)


