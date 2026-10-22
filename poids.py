#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from fileCls import File
from fileList import FileTable
import loggerFct as log

# ============ récupérer les pesées de l'année passée ============
"""
il y a une pesée par semaine, tous les dimanches.
la chronologie est régulière.
je récupère les 50 dernières pesées
"""
dataFull = FileTable ('b/perso\\poids.tsv')
dataFull.read()
dataFull.pop (0)
dataRafined = FileTable()
dataRafined.extend (dataFull[:50])

# ============ entrer les données dans le svg ============

# créer les données
templatePoint = "<line y1='0' y2='300' x1='$' x2='$' />"
templateRect = "<rect y='0' height='300' x='$debut' width='$large' />"
dataSvg =""

dataRange = range (50)
for r in dataRange: dataSvg = dataSvg + str(10*r) +','+ dataRafined[r][1]

# ouvrir le modèle
templateSvg = File ('b/perso\\poids template.svg')
templateSvg.read()
templateSvg.title = 'poids recent'
templateSvg.toPath()
templateSvg.replace ('$content', dataSvg)
templateSvg.write()
