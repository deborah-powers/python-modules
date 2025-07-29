#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
from fileList import FileTable
import loggerFct as log
log.logDate = True
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
invenspecForge = FileTable (invenspecPath % 'forge tout')
invenspecSharepoint = FileTable (invenspecPath % 'sharepoint tout')
invenspecCosmose = FileTable (invenspecPath % 'cosmose tout')
invenspecForge.read()
invenspecForge.pop (0)
invenspecSharepoint.read()
invenspecSharepoint.pop(0)
invenspecCosmose.read()
invenspecCosmose.pop(0)

# fichiers contenant les données triées
invenspecCFS = File (invenspecPath % 'cosmose forge sharepoint')
invenspecCFS.text = '\t'.join ([ 'titre cosmose', 'comparaison date forge', 'comparaison date sharepoint', 'modif cosmose', 'titre forge', 'modif forge', 'chemin forge', 'titre sharepoint', 'modif sharepoint', 'chemin sharepoint' ])
invenspecCF = File (invenspecPath % 'cosmose forge')
invenspecCF.text = '\t'.join ([ 'titre cosmose', 'comparaison date', 'modif cosmose', 'titre forge', 'modif forge', 'chemin forge' ])
invenspecCS = File (invenspecPath % 'cosmose sharepoint')
invenspecCS.text = '\t'.join ([ 'titre cosmose', 'comparaison date', 'modif cosmose', 'titre sharepoint', 'modif sharepoint', 'chemin sharepoint' ])
invenspecFonly = File (invenspecPath % 'forge uniquement')
invenspecFonly.read()
invenspecSonly = File (invenspecPath % 'sharepoint uniquement')
invenspecSonly.read()
invenspecConly = File (invenspecPath % 'cosmose uniquement')
invenspecConly.read()

def dateEquals (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO and len (datA) >10: return '=='
	elif datA in datO or datO in datA: return '~~'
	datA = datA[6:10] +'/'+ datA[3:5] +'/'+ datA[:2] + datA[10:]
	datO = datO[6:10] +'/'+ datO[3:5] +'/'+ datO[:2] + datO[10:]
	if datA > datO:
		if datO[:10] in datA: return '>~'
		else: return '>>'
	elif datO[:10] in datA: return '<~'
	else: return '<<'

def dateEquals_va (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO and len (datA) >10: return '='
	elif datA in datO or datO in datA: return '~'
	elif datA[:10] in datO: return '~'
	elif datO[:10] in datA: return '~'
	elif datA > datO: return '>'
	else: return '<'

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
	if typeC not in ('document', 'média', 'page wiki'): continue
	elif titleC in invenspecConly.text: continue
	elif len (titleC) <5:
		invenspecConly.text = invenspecConly.text +'\n'+ titleC
		continue
	# repérer les fichiers similaires
	titleCb = cleanTitle (titleC)
	pForge =-1
	pSharepoint =-1
	dateCompF ='--'
	dateCompS ='--'
	p=0
	while p< forgeLen:
		if invenspecForge[p][0] not in invenspecFonly.text and invenspecForge[p][1] not in invenspecFonly.text and (titlesIdem (titleCb, invenspecForge[p][0]) or titlesIdem (titleCb, invenspecForge[p][1])):
			pForge =p
			p= forgeLen
		p+=1
	p=0
	while p< sharepointLen:
		# if invenspecSharepoint[p][0] not in invenspecSonly.text and titlesIdem (titleCb, invenspecSharepoint[p][0]):
		if titlesIdem (titleCb, invenspecSharepoint[p][0]):
			pSharepoint =p
			p= sharepointLen
		p+=1
	# comparer les dates de modification entre cosmose, la forge et le sharepoint
	log.log (titleC, pForge, pSharepoint)
	print (invenspecForge[pForge])
	print (invenspecSharepoint[pSharepoint])
	if pForge >=0: dateCompF = dateEquals (modifC, invenspecForge[pForge][2])
	if pSharepoint >=0: dateCompS = dateEquals (modifC, invenspecSharepoint[pSharepoint][1])
	# log.log (pForge, pSharepoint)
	if pForge <0 and pSharepoint <0: invenspecConly.text = invenspecConly.text +'\n'+ titleC
	elif pSharepoint <0: invenspecCF.text = invenspecCF.text + '\n' + '\t'.join ([ titleC, dateCompF, modifC, invenspecForge[p][1], invenspecForge[p][2], invenspecForge[p][3] ])
	elif pForge <0: invenspecCS.text = invenspecCS.text + '\n' + '\t'.join ([ titleC, dateCompS, modifC, invenspecSharepoint[p][0], invenspecSharepoint[p][1], invenspecSharepoint[p][3] ])
	else: invenspecCFS.text = invenspecCFS.text + '\n' + '\t'.join ([ titleC, dateCompF, dateCompS, modifC, invenspecForge[p][1], invenspecForge[p][2], invenspecForge[p][3], invenspecSharepoint[p][0], invenspecSharepoint[p][1], invenspecSharepoint[p][3] ])

invenspecConly.write()
invenspecCFS.write()
invenspecCF.write()
invenspecCS.write()
