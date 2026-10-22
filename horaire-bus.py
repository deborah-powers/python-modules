#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from textFct import cleanBasic
from fileCls import File
from htmlCls import Html

helpData = """transformer un fichier texte en html
le fichier txt contient les horaires d'un arrêt de bus
m'inspirer du modèle b/programmes\\horaire bus template.txt
lancer le script:
python horaire-bus.py ville numligne arret
"""
horaireTemplateName = 'b/programmes\\horaire bus template.html'
horaireDataName = 'b/horaire bus $data.txt'
horaireLigneTemplate = "'$heure': '$minutes',\n"

def extractHours (horaireList):
	horaireRange = range (1, len (horaireList), 2)
	horaireLigneData =""
	for h in horaireRange:
		horaireLigneData = horaireLigneData + horaireLigneTemplate.replace ('$heure', horaireList[h])
		horaireLigneData = horaireLigneData.replace ('$minutes', horaireList[h+1])
	horaireLigneData = horaireLigneData[:-2]
	return horaireLigneData

def findPeriodHoraire (horaireBloc):
	horaireList = horaireBloc.split ('\n')
	periode = horaireList[0]
	if " " in periode:
		d= periode.find (" ")
		periode = periode[:d]
	horaire = extractHours (horaireList)
	return periode, horaire

if len (argv) !=4: print (helpData)
else:
	horaireDataData = " ".join (argv[1:])
	horaireDataName = horaireDataName.replace ('$data', horaireDataData)
	# les fichiers
	horaireDataFile = File (horaireDataName)
	horaireDataFile.read()
	horaireTemplateFile = File (horaireTemplateName)
	horaireTemplateFile.read()
	horaireTemplateFile.title = horaireDataFile.title
	horaireTemplateFile.path = horaireDataFile.path.replace ('.txt', '.html')
	horaireTemplateFile.toPath()
	# extraire les données
	horaireDataFile.text = cleanBasic (horaireDataFile.text)
	if '\n==\n' in horaireDataFile.text:
		d= horaireDataFile.text.find ('\n==\n')
		horaireDataFile.text = horaireDataFile.text[:d]
	horaireDataFile.text = horaireDataFile.text.replace (": ", '\n')
	horaireList = horaireDataFile.text.split ('\n')
	# insérer les données dans le modèle
	horaireTemplateFile.replace ('$ville', horaireList[1])
	horaireTemplateFile.replace ('$ligne', horaireList[3])
	horaireTemplateFile.replace ('$arret', horaireList[5])
	horaireTemplateFile.replace ('$direction', horaireList[7])
	horaireTemplateFile.replace ('$date', horaireList[9])
	# extraire les horaires
	horaireList = horaireList[10:]
	horaireDataFile.text = '\n'.join (horaireList)
	horaireDict ={ 'semaine': "", 'samedi': "", 'dimanche': "", 'vacance': "" }
	horaireDataFile.text = horaireDataFile.text.replace ('samedi', '\nsamedi')
	horaireDataFile.text = horaireDataFile.text.replace ('dimanche', '\ndimanche')
	horaireDataFile.text = horaireDataFile.text.replace ('vacance', '\nvacance')
	horaireList = horaireDataFile.text.split ('\n\n')
	periode, horaire = findPeriodHoraire (horaireList[0])
	horaireDict[periode] = horaire
	print (periode)
	periode, horaire = findPeriodHoraire (horaireList[1])
	horaireDict[periode] = horaire
	print (periode)
	periode, horaire = findPeriodHoraire (horaireList[2])
	horaireDict[periode] = horaire
	print (periode)
	if len (horaireList) >3:
		periode, horaire = findPeriodHoraire (horaireList[3])
		horaireDict[periode] = horaire
		print (periode)
	horaireTemplateFile.replace ('$horaireSemaine', horaireDict['semaine'])
	horaireTemplateFile.replace ('$horaireSamedi', horaireDict['samedi'])
	horaireTemplateFile.replace ('$horaireDimanche', horaireDict['dimanche'])
	horaireTemplateFile.replace ('$horaireVacance', horaireDict['vacance'])
	horaireTemplateFile.write()
