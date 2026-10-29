#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import path
path.append ('C:\\Users\\LENOVO\\Desktop\\python')
from datetime import datetime, timedelta
from fileCls import File
from fileList import FileTable
import loggerFct as log

# ============ récupérer les règles de l'année passée ============

dataFull = FileTable ('b/perso\\regles.tsv')
dataFull.read()
dataFull.pop (0)

# récupération des données de deux ans
year = dataFull[0][0][:4]
periodYears = '-'+ year
r=0
while dataFull[r][0][:4] == year: r+=1
year = dataFull[r][0][:4]
periodYears = year + periodYears
while dataFull[r][0][:4] == year: r+=1
dataRafined = FileTable()
dataRafined.extend (dataFull[:r])

# début du graphe
dateStart = datetime.strptime (dataRafined[-1][0][:8] +'01', '%Y/%m/%d')
averageStartGap =0

# transformer les dates
dataRange = range (len (dataRafined))
dateEcart = None
for r in dataRange:
	dateEcart = datetime.strptime (dataRafined[r][0], '%Y/%m/%d')
	dateEcart = dateEcart - dateStart
	dataRafined[r][0] = str (dateEcart.days)
	averageStartGap += dateEcart

averageStartGap /= (len (dataRafined) -1)

# créer les données
# templateLine = "<line y1='0' y2='300' x1='$' x2='$' />"
templateRect = "<rect y='0' height='300' x='$debut' width='$large' />"
graphic =""

for r in dataRange:
	graphic = graphic + templateRect
	graphic = graphic.replace ('$debut', dataRafined[r][0])
	graphic = graphic.replace ('$large', dataRafined[r][1])

# remplir le modèle html
templateHtml = File ('b/perso\\regles template.html')
templateHtml.read()
templateHtml.title = 'regles recentes'
templateHtml.toPath()
templateHtml.replace ('$graphic', graphic)
templateHtml.replace ('$periodYears', periodYears)
templateHtml.replace ('$averageStartGap', str (averageStartGap))
templateHtml.write()

# remplir le modèle svg
templateSvg = File ('b/perso\\regles template.svg')
templateSvg.read()
templateSvg.title = 'regles recentes'
templateSvg.toPath()
templateSvg.replace ('$graphic', graphic)
templateSvg.write()
