#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileList, FileTable
import loggerFct as log
invenspecPath = 'b/fouille-spec\\invenspec %s.tsv'

""" types sans date de publication: événement local, communauté d'espace de conversations, projet tâches
dans cosmose, date-modif > date-publi: je néglige date-publi et prend date-modif
les dates dans cosmose:
1 le doc est créé ou modifié. il y a création d'une nouvelle version.
2 sa nouvelle version est masquée au public. seules les personnes ayant les droits de modification dessus peuvent y accéder. elle a juste des dates de création et de modification.
3 la version est publiée. tous les utilisateurs du sharepoint peuvent la lire. elle reçoit une date de publication.
https://support-microsoft-com.translate.goog/en-gb/office/what-happens-when-i-publish-a-page-e5e070be-00bd-4a74-84c2-67aafddb6c19?_x_tr_sl=en&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=rq
je me base sur la date de modification.
"""

# fichiers contenant les données originelles
invenspecForge = FileTable (invenspecPath % 'forge 07-09')
invenspecSharepoint = FileTable (invenspecPath % 'sharepoint 07-09')
invenspecCosmose = FileTable (invenspecPath % 'cosmose 07-09')
invenspecForge.read()
invenspecForge.pop (0)
# invenspecForge.deleteDoublons()
invenspecSharepoint.read()
invenspecSharepoint.pop(0)
invenspecCosmose.read()
invenspecCosmose.pop(0)

# fichiers contenant les données triées
invenspecConly = FileList (invenspecPath % 'cosmose uniquement')
invenspecConly.sepCol = '\t'
invenspecCFS = FileTable (invenspecPath % 'cfs')
invenspecCFS.append ([ 'titre cosmose', 'titre forge', 'titre sharepoint', 'comparaison date forge', 'comparaison date sharepoint', 'modif cosmose', 'modif forge', 'modif sharepoint' ])
invenspecCF = FileTable (invenspecPath % 'cf')
invenspecCF.append ([ 'titre cosmose', 'titre forge', 'comparaison date', 'modif cosmose', 'modif forge' ])
invenspecCS = FileTable (invenspecPath % 'cs')
invenspecCS.append ([ 'titre cosmose', 'titre sharepoint', 'comparaison date', 'modif cosmose', 'modif sharepoint' ])

def dateEquals (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO: return 2
	elif datA in datO: return 1
	elif datO in datA: return 1
	else: return 0

def dateCompare (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO: return 0
	elif datA in datO: return -1
	elif datO in datA: return 1
	datA = datA[6:10] +'/'+ datA[3:5] +'/'+ datA[:2] + datA[10:]
	datO = datO[6:10] +'/'+ datO[3:5] +'/'+ datO[:2] + datO[10:]
	if datA > datO: return 2
	else: return -2

def cleanTitle (title):
	title = title.lower()
	charToErase = '-_'
	for char in charToErase: title = title.replace (char," ")
	if '.' in title:
		nbPoint = title.count ('.') -1
		if nbPoint >0: title = title.replace ('.'," ", nbPoint)
	title = title.strip()
	while "  " in title: title = title.replace ("  "," ")
	return title

def titlesIdem (titleA, titleO):
#	titleA = cleanTitle (titleA)
	titleO = cleanTitle (titleO)
	if titleA == titleO: return True
	idems = False
	lenA = len (titleA)
	lenO = len (titleO)
	if lenA > lenO and '.' in titleA:
		f= titleA.rfind ('.')
		if titleA[:f] == titleO: idems = True
	elif lenO > lenA and '.' in titleO:
		f= titleO.rfind ('.')
		if titleO[:f] == titleA: idems = True
	return idems

forgeLen = invenspecForge.len()
sharepointLen = invenspecSharepoint.len()

for titleC, typeC, categorie, etravail, modifC in invenspecCosmose.list:
	log.message (titleC)

"""
	if len (titleC) <5:
		invenspecConly.append (titleC)
		continue
	# repérer les fichiers similaires
	titleCb = cleanTitle (titleC)
	pForge =-1
	pSharepoint =-1
	dateCompF =0
	dateCompS =0
	p=0
	while p< forgeLen:
		if titlesIdem (titleCb, invenspecForge[p][0]) or titlesIdem (titleCb, invenspecForge[p][0]):
			pForge =p
			p= forgeLen
		p+=1
	p=0
	while p< sharepointLen:
		if titlesIdem (titleCb, invenspecSharepoint[p][0]):
			pSharepoint =p
			p= sharepointLen
		p+=1
	# comparer les dates de modification entre cosmose, la forge et le sharepoint
	if pForge >=0: dateCompF = dateEquals (modifC, invenspecForge[pForge][2])
	if pSharepoint >=0: dateCompS = dateEquals (modifC, invenspecSharepoint[pSharepoint][1])
	if pForge <0 and pSharepoint <0: invenspecConly.append (titleC)
	elif pSharepoint <0:
		invenspecCF.append ([ titleC, invenspecForge[pForge][0], dateCompF, modifC, invenspecForge[pForge][2] ])
	elif pForge <0:
		invenspecCS.append ([ titleC, invenspecSharepoint[pSharepoint][0], dateCompS, modifC, invenspecSharepoint[pSharepoint][1] ])
	else: invenspecCFS.append ([ titleC, invenspecForge[pForge][0], invenspecSharepoint[pSharepoint][0], dateCompF, dateCompS, modifC, invenspecForge[pForge][2], invenspecSharepoint[pSharepoint][1] ])
invenspecConly.write()
invenspecCFS.write()
invenspecCF.write()
invenspecCS.write()
"""

