#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileList, FileTable

dateRef = '2024/04/'
typeRef = 'courses'

# préparer les lignes
fileSrc = FileTable ('b/perso\\depenses.tsv')
fileSrc.read()
header = fileSrc.list.pop (0)

def extractByDate (dateRef, depenseTable):
	depenseDateeTable =[]
	l=0
	lenTable = len (depenseTable)
	while l< lenTable and dateRef not in depenseTable[l][0]: l+=1
	while l< lenTable and dateRef in depenseTable[l][0]:
		depenseDateeTable.append (depenseTable[l])
		l+=1
	return depenseDateeTable

def extractByType_va (typeRef, depenseTable):
	depenseTypeeTable =[]
	for line in depenseTable:
		if typeRef == line[2]: depenseTypeeTable.append (line)
	return depenseTypeeTable

def resetType (depenseTable):
	rangeTable = range (len (depenseTable))
	for d in rangeTable:
		if depenseTable[d][3] == 'avon' and (depenseTable[d][2] == 'friandise' or depenseTable[d][2] == 'courses'):
			depenseTable[d][2] = 'cadeau'
		elif depenseTable[d][2] == 'friandise': depenseTable[d][2] = 'courses'
	return depenseTable

def organiseByType (depenseTable):
	depDict ={}
	for line in depenseTable:
		if line[2] in depDict.keys(): depDict [line[2]] += float (line[1])
		else: depDict [line[2]] = float (line[1])
	dicoKeys = depDict.keys()
	depTotal =0.0
	for key in dicoKeys: depTotal += depDict[key]
#	depDict['total'] = depTotal
	print ('dépenses totale de', dateRef, ':', depTotal)
	print ('dépenses par thème:')
	for key in dicoKeys: print (key, ':', depDict[key])
#	return depDict

def extractByType (typeRef, depenseTable):
	depenseTypeeTable =[]
	depTotal =0.0
	for line in depenseTable:
		if typeRef == line[2]:
			depenseTypeeTable.append (line)
			depTotal += float (line[1])
	print ('dépenses de', dateRef, 'pour', typeRef, ':', depTotal)
	for line in depenseTypeeTable: print (line[3], line[1], line[4])
#	return depenseTypeeTable

depenseTable =[]
if dateRef:
	depenseTable = extractByDate (dateRef, fileSrc.list)
	depenseTable = resetType (depenseTable)
	if typeRef: extractByType (typeRef, depenseTable)
	else: organiseByType (depenseTable)
elif typeRef: extractByType (typeRef, fileSrc.list)
else:
	for line in fileSrc.list: depenseTable.append (line)
