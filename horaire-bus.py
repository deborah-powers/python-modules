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
horaireLigneTemplate = '<tr><th>$heure</th><td>$minutes</td></tr>'

def extractHours (horaireList, posFin):
	horaireRange = range (0, posFin, 2)
	horaireLigneData =""
	for h in horaireRange:
		horaireLigneData = horaireLigneData + horaireLigneTemplate.replace ('$heure', horaireList[h])
		horaireList[h+1] = horaireList[h+1].replace (" ", '</td><td>')
		horaireLigneData = horaireLigneData.replace ('$minutes', horaireList[h+1])
	return horaireLigneData

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
	horaireList = horaireList[11:]
	d= horaireList.index ('samedi')
	horaireLigneData = extractHours (horaireList, d)
	horaireTemplateFile.replace ('$semaine', horaireLigneData)
	horaireList = horaireList[d+1:]
	d= horaireList.index ('dimanche et férié')
	horaireLigneData = extractHours (horaireList, d)
	horaireTemplateFile.replace ('$samedi', horaireLigneData)
	horaireList = horaireList[d+1:]
	horaireLigneData = extractHours (horaireList, len (horaireList))
	horaireTemplateFile.replace ('$dimanche', horaireLigneData)
	horaireTemplateFile.write()
