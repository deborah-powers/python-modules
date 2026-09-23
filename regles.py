#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from fileCls import File
from fileList import FileTable
import loggerFct as log

# ============ récupérer les règles de l'année passée ============

dataFull = FileTable ('b/perso\\regles.tsv')
dataFull.read()
dataFull.pop (0)

# la récupération
month = dataFull[0][0][:4]
r=0
while dataFull[r][0][:4] == month: r+=1
month = dataFull[r][0][:4]
while dataFull[r][0][:4] == month: r+=1
dataRafined = FileTable()
dataRafined.extend (dataFull[:r])

# début du graphe
dateStart = datetime.strptime (dataRafined[-1][0][:8] +'01', '%Y/%m/%d')

# transformer les dates
dataRange = range (len (dataRafined))
dateEcart = None
for r in dataRange:
	dateEcart = datetime.strptime (dataRafined[r][0], '%Y/%m/%d')
	dateEcart = dateEcart - dateStart
	dataRafined[r][0] = str (dateEcart.days)

# ============ entrer les données dans le svg ============

# créer les données
templateLine = "<line y1='0' y2='300' x1='$' x2='$' />"
templateRect = "<rect y='0' height='300' x='$debut' width='$large' />"
dataSvg =""

for r in dataRange:
	dataSvg = dataSvg + templateRect
	dataSvg = dataSvg.replace ('$debut', dataRafined[r][0])
	dataSvg = dataSvg.replace ('$large', dataRafined[r][1])

# ouvrir le modèle
templateSvg = File ('b/perso\\regles template.svg')
templateSvg.read()
templateSvg.title = 'regles recentes'
templateSvg.toPath()
templateSvg.replace ('$content', dataSvg)
templateSvg.write()
