#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from functools import cmp_to_key
from fileCls import File
from fileList import FileList, FileTable
import loggerFct as log

def comparPhotoByCity (photoA, photoI):
	if photoA[1] > photoI[1]: return 1
	elif photoA[1] < photoI[1]: return -1
	elif photoA[2] > photoI[2]: return 1
	elif photoA[2] < photoI[2]: return -1
	elif photoA[0] > photoI[0]: return 1
	elif photoA[0] < photoI[0]: return -1
	elif photoA[4] > photoI[4]: return 1
	elif photoA[4] < photoI[4]: return -1
	elif photoA[3] > photoI[3]: return 1
	elif photoA[3] < photoI[3]: return -1
	elif photoA[5] > photoI[5]: return 1
	elif photoA[5] < photoI[5]: return -1

def comparPhotoByDate (photoA, photoI):
	if photoA[0] > photoI[0]: return 1
	elif photoA[0] < photoI[0]: return -1
	elif photoA[1] > photoI[1]: return 1
	elif photoA[1] < photoI[1]: return -1
	elif photoA[2] > photoI[2]: return 1
	elif photoA[2] < photoI[2]: return -1
	elif photoA[4] > photoI[4]: return 1
	elif photoA[4] < photoI[4]: return -1
	elif photoA[3] > photoI[3]: return 1
	elif photoA[3] < photoI[3]: return -1
	elif photoA[5] > photoI[5]: return 1
	elif photoA[5] < photoI[5]: return -1


"""
sorted (mylist, key=cmp_to_key (comparPhotoByCity))
fileA = FileTable ('b/diaporama.txt')
"""
fileA = FileTable ('s/portfolio\\diaporama\\photos-data.tsv')
fileA.read()
fileA.sort()

def cleanFsimple():
	while "   " in fileA.text: fileA.replace ("   ","  ")
	fileA.replace ("  ","\t")
	fileA.replace (' 201', '\t201')
	fileA.replace (' 202', '\t202')
	eraseWords =( ' (1)', ' (2)', ' (3)', '-s-no-gm' )
	for word in eraseWords: fileA.replace (word)
	nombres = '0123456789'
	for nba in nombres:
		for nbo in nombres: fileA.replace ('-'+ nba + nbo +" ", '-'+ nba + nbo +'\t')
	cities = ('paris', 'chtd', 'ftb', 'fontainebleau', 'avon', 'rueil', 'angers', 'cmaman', 'cpapa', 'issy', 'blr', 'jplantes', 'parc balzac', 'balzac' 'bagatelle', 'teiffel', 'boulogne', 'bboulogne', 'chateau', 'château', 'lengelen')
	for city in cities:
		fileA.replace (city +" ", city +'\t')
		fileA.replace (" "+ city, '\t'+ city)
	pronoms = ('de', 'du', 'au', 'aux')
	for pronom in pronoms:
		fileA.replace ('\t'+ pronom +'\t'," "+ pronom +" ")
		fileA.replace (" "+ pronom +'\t'," "+ pronom +" ")
		fileA.replace ('\t'+ pronom +" "," "+ pronom +" ")
	citiesAbreviation ={ 'chateau': 'château', 'chtd': 'châteaudun', 'ftb': 'fontainebleau', 'cmaman': 'intérieur', 'cpapa': 'intérieur', 'blr': 'bois le rois', 'jplantes': 'paris\tjardin des plantes', 'teiffel': 'paris\ttour eiffel', 'bboulogne': 'boulogne\tbois' }
	citiesKey = citiesAbreviation.keys()
	for abbr in citiesKey: fileA.replace (abbr, citiesAbreviation[abbr])
	fileA.replace ('paris\tparis', 'paris')
	fileA.replace ('paris paris', 'paris')
	photoList = fileA.text.split ('\n')
	photoList.sort()
	fileA.text = '\n'.join (photoList)

def findDatePos (line):
	d=-1
	rangeCell = range (len (line))
	for c in rangeCell:
		if line[c][:2] == '20': d=c
	return d

def cleanDates():
	rangeLines = range (len (fileA))
	for l in rangeLines:
		if fileA[l][0][:2] == '20': continue
		else:
			d= findDatePos (fileA[l])
			if d>0:
				cellDate = fileA[l].pop (d)
				fileA[l].insert (0, cellDate)
	fileA.sort()

def cleanCities():
	cities = ('paris', 'fontainebleau', 'avon', 'rueil', 'angers', 'beaucouzé', 'intérieur', 'issy', 'boulogne', 'châteaudun')
	rangeLines = range (len (fileA))
	for l in rangeLines:
		if fileA[l][1] in cities: continue
		else:
			nbCells = len (fileA[l])
			rangeCells = range (2, nbCells -1)
			c=0
			posCity =0
			while c< nbCells and posCity:
				if fileA[l][c] in cities: posCity =c
				c+=1
			if c>0:
				cellCity = fileA[l].pop (posCity)
				fileA[l].insert (1, cellCity)
	fileA.sort()

def eraseUrlDoubles():
	fileRef = File ('s/portfolio\\diaporama\\photos-data.csv')
	fileRef.read()
	rangeLines = reversed (range (len (fileA)))
	trash =[]
	for l in rangeLines:
		if fileA.list[l][-1] in fileRef.text:
		#	print (fileA.list[l][:3], fileA.list[l][-1][-9:])
			print (fileA.list[l])
			trash = fileA.list.pop (l)

def findDatePlaceDoubles():
	fileRef = File ('s/portfolio\\diaporama\\photos-data.csv')
	fileRef.read()
	print ('doublons de lieux et de dates')
	for line in fileA.list:
		if line[0] +'\t'+ line[1] in fileRef.text: print (line[0], line[1])

def findDatePlaceDoublesBis():
	fileRef = FileTable ('s/portfolio\\diaporama\\photos-data.csv')
	fileRef.read()
	print ('doublons de lieux et de dates')
	for line in fileA.list:
		for ref in fileRef.list:
			if line[0] in ref[0] and line[1] == ref[1]: print (line[0], ref[0], line[1])

def listThemes():
	themes =[]
	for line in fileA.list:
		if line[3] not in themes: themes.append (line[3])
	themes.sort()
	for theme in themes: print (theme)

def sortThemes():
	themes =[]
	rangeLines = range (len (fileA.list))
	for l in rangeLines:
		themes = fileA.list[l][3].split (", ")
		themes.sort()
		fileA.list[l][3] = ", ".join (themes)


colPlace = fileA.getCol (4)
fileA.popCol (4)
fileA.insertCol (2, colPlace)
fileA.list = sorted (fileA.list, key=cmp_to_key (comparPhotoByCity))

"""
listThemes()
def findShortDates():
	rangeLines = reversed (range (len (fileA)))
	trash =[]
	for l in rangeLines:
		if fileA.list[l][7] !="\t":
		#	print (fileA.list[l])
			trash = fileA.list.pop (l)

"""
fileA.title = fileA.title +" bis"
fileA.write()
