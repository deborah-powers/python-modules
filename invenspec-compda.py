#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileTable
import loggerFct as log
invenspecPath = 'b/fouille-spec\\invenspec cosmose %s.tsv'


"""
invenspecFile = FileTable (invenspecPath % 'forge')
invenspecFile.read()
invenspecFile.pop (0)

categorie2 =[]
categorie1 =[]
categorie0 =[]

for nameC, nameF, compD in invenspecFile.list:
	if compD == '2': categorie2.append ((nameC, nameF))
	elif compD == '1': categorie1.append ((nameC, nameF))
	elif compD == '0': categorie0.append ((nameC, nameF))

if categorie2: print (len (categorie2), "fichiers ont la même date à l'heure près entre cosmose et la forge")
else: print ("aucun fichier n'a la même date à l'heure près entre cosmose et la forge")
if categorie1: print (len (categorie1), "fichiers ont la même date au jour près entre cosmose et la forge")
else: print ("aucun fichier n'a la même date au jour près entre cosmose et la forge")
if categorie0: print (len (categorie0), "fichiers ont des dates différentes entre cosmose et la forge")
else: print ("aucun fichier n'a de dates différentes entre cosmose et la forge")

invenspecFile = FileTable (invenspecPath % 'sharepoint')
invenspecFile.read()
invenspecFile.pop (0)

categorie2 =[]
categorie1 =[]
categorie0 =[]

for nameC, nameF, compD in invenspecFile.list:
	if compD == '2': categorie2.append ((nameC, nameF))
	elif compD == '1': categorie1.append ((nameC, nameF))
	elif compD == '0': categorie0.append ((nameC, nameF))

if categorie2: print (len (categorie2), "fichiers ont la même date à l'heure près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date à l'heure près entre cosmose et le sharepoint")
if categorie1: print (len (categorie1), "fichiers ont la même date au jour près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date au jour près entre cosmose et le sharepoint")
if categorie0: print (len (categorie0), "fichiers ont des dates différentes entre cosmose et le sharepoint")
else: print ("aucun fichier n'a de dates différentes entre cosmose et le sharepoint")
"""

invenspecFile = FileTable (invenspecPath % 'forge sharepoint')
invenspecFile.read()
invenspecFile.pop (0)

categorie22 =[]
categorie21 =[]
categorie20 =[]
categorie12 =[]
categorie11 =[]
categorie10 =[]
categorie02 =[]
categorie01 =[]
categorie00 =[]

for nameC, nameF, nameS, compF, compS in invenspecFile.list:
	if compF == '2' and compS == '2': categorie22.append ((nameC, nameF, nameS))
	elif compF == '2' and compS == '1': categorie21.append ((nameC, nameF, nameS))
	elif compF == '2' and compS == '0': categorie20.append ((nameC, nameF, nameS))
	elif compF == '1' and compS == '2': categorie12.append ((nameC, nameF, nameS))
	elif compF == '1' and compS == '1': categorie11.append ((nameC, nameF, nameS))
	elif compF == '1' and compS == '0': categorie10.append ((nameC, nameF, nameS))
	elif compF == '0' and compS == '2': categorie02.append ((nameC, nameF, nameS))
	elif compF == '0' and compS == '1': categorie01.append ((nameC, nameF, nameS))
	elif compF == '0' and compS == '0': categorie00.append ((nameC, nameF, nameS))

if categorie22: print (len (categorie22), "fichiers ont la même date à l'heure près entre les trois plate-formes")
else: print ("aucun fichier n'a la même date à l'heure près entre les trois plate-formes")

if categorie21: print (len (categorie21), "fichiers ont la même date à l'heure près entre cosmose et la forge, et au jour près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date à l'heure près entre cosmose et la forge, et au jour près entre cosmose et le sharepoint")
if categorie20: print (len (categorie20), "fichiers ont la même date à l'heure près entre cosmose et la forge, et pas la même date du tout entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date à l'heure près entre cosmose et la forge, et pas la même date du tout entre cosmose et le sharepoint")
if categorie12: print (len (categorie12), "fichiers ont la même date au jour près entre cosmose et la forge, et la même date à l'heure près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date au jour près entre cosmose et la forge, et la même date à l'heure près entre cosmose et le sharepoint")
if categorie11: print (len (categorie11), "fichiers ont la même date au jour près entre les trois plate-formes")
else: print ("aucun fichier n'a la même date au jour près entre les trois plate-formes")
if categorie10: print (len (categorie10), "fichiers ont la même date au jour près entre cosmose et la forge, et pas la même date du tout entre cosmose et le sharepoint")
else: print ("aucun fichier n'a la même date au jour près entre cosmose et la forge, et pas la même date du tout entre cosmose et le sharepoint")
if categorie02: print (len (categorie02), "fichiers ont pas la même date du tout entre cosmose et la forge, et à l'heure près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a pas la même date du tout entre cosmose et la forge, et à l'heure près entre cosmose et le sharepoint")
if categorie01: print (len (categorie01), "fichiers ont pas la même date du tout entre cosmose et la forge, et au jour près entre cosmose et le sharepoint")
else: print ("aucun fichier n'a pas la même date du tout entre cosmose et la forge, et au jour près entre cosmose et le sharepoint")
if categorie00: print (len (categorie00), "fichiers ont des dates différentes entre les trois plate-formes")
else: print ("aucun fichier n'a de dates différentes entre les trois plate-formes")


