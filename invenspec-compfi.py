#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
from fileList import FileTable
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
invenspecForge = FileTable (invenspecPath % 'forge tout')
invenspecSharepoint = FileTable (invenspecPath % 'sharepoint tout')
invenspecCosmose = FileTable (invenspecPath % 'cosmose tout')
invenspecForge.read()
invenspecForge.pop (0)
# invenspecForge.deleteDoublons()
invenspecSharepoint.read()
invenspecSharepoint.pop(0)
invenspecCosmose.read()
invenspecCosmose.pop(0)

# fichiers contenant les données triées
invenspecConly = File (invenspecPath % 'cosmose uniquement')
invenspecCFS = File (invenspecPath % 'cosmose forge sharepoint')
invenspecCFS.text = '%s\t%s\t%s' % ('titre cosmose', 'comparaison date forge', 'comparaison date sharepoint')
invenspecCF = File (invenspecPath % 'cosmose forge')
invenspecCF.text = '%s\t%s' % ('titre cosmose', 'comparaison date')
invenspecCS = File (invenspecPath % 'cosmose sharepoint')
invenspecCS.text = '%s\t%s' % ('titre cosmose', 'comparaison date')

"""
invenspecCFS.text = '%s\t%s\t%s\t%s\t%s\t%s' % ('titre cosmose', 'comparaison date forge', 'comparaison date sharepoint', 'date cosmose', 'date forge', 'date sharepoint')
invenspecCF = File (invenspecPath % 'cosmose forge')
invenspecCF.text = '%s\t%s\t%s\t%s' % ('titre cosmose', 'comparaison date', 'date cosmose', 'date forge')
invenspecCS = File (invenspecPath % 'cosmose sharepoint')
invenspecCS.text = '%s\t%s\t%s\t%s' % ('titre cosmose', 'comparaison date', 'date cosmose', 'date sharepoint')

invenspecCFS.text = '%s\t%s\t%s\t%s\t%s' % ('titre cosmose', 'titre forge', 'titre sharepoint', 'comparaison date forge', 'comparaison date sharepoint')
invenspecCF = File (invenspecPath % 'cosmose forge')
invenspecCF.text = '%s\t%s\t%s' % ('titre cosmose', 'titre forge', 'comparaison date')
invenspecCS = File (invenspecPath % 'cosmose sharepoint')
invenspecCS.text = '%s\t%s\t%s' % ('titre cosmose', 'titre sharepoint', 'comparaison date')

invenspecCFS.text = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % ('titre cosmose', 'titre forge', 'titre sharepoint', 'comparaison date forge', 'comparaison date sharepoint', 'modif cosmose', 'modif forge', 'modif sharepoint')
invenspecCF = File (invenspecPath % 'cf')
invenspecCF.text = '%s\t%s\t%s\t%s\t%s' % ('titre cosmose', 'titre forge', 'comparaison date', 'modif cosmose', 'modif forge')
invenspecCS = File (invenspecPath % 'cs')
invenspecCS.text = '%s\t%s\t%s\t%s\t%s' % ('titre cosmose', 'titre sharepoint', 'comparaison date', 'modif cosmose', 'modif sharepoint')
"""
invenspecConly.read()

def dateEquals (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO and len (datA) >10: return '='
	elif datA in datO or datO in datA: return '~'
	elif datA[:10] in datO: return '~'
	elif datO[:10] in datA: return '~'
	elif datA > datO: return '>'
	else: return '<'

def dateEquals_va (datA, datO):
	# date = 04/11/2025 ou 04/11/2025 14:37
	if datA == datO and len (datA) >10: return 2
	elif datA in datO: return 1
	elif datO in datA: return 1
	elif datA[:10] in datO: return 1
	elif datO[:10] in datA: return 1
	else: return 0

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
	if titleC in invenspecConly.text: continue
	elif len (titleC) <5:
		invenspecConly.text = invenspecConly.text +'\n'+ titleC
		continue
	# repérer les fichiers similaires
	titleCb = cleanTitle (titleC)
	pForge =-1
	pSharepoint =-1
	dateCompF ='~'
	dateCompS ='~'
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
	if pForge <0 and pSharepoint <0:
		invenspecConly.text = invenspecConly.text +'\n'+ titleC
	elif pSharepoint <0:
		invenspecCF.text = invenspecCF.text + '\n%s\t%s' % (titleC, dateCompF)
#		invenspecCF.text = invenspecCF.text + '\n%s\t%s\t%s\t%s' % (titleC, dateCompF, modifC, invenspecForge[pForge][2])
	elif pForge <0:
		invenspecCS.text = invenspecCS.text + '\n%s\t%s' % (titleC, dateCompS)
#		invenspecCS.text = invenspecCS.text + '\n%s\t%s\t%s\t%s' % (titleC, dateCompS, modifC, invenspecSharepoint[pSharepoint][1])
	else:
		invenspecCFS.text = invenspecCFS.text + '\n%s\t%s\t%s' % (titleC, dateCompF, dateCompS)
#		invenspecCFS.text = invenspecCFS.text + '\n%s\t%s\t%s\t%s\t%s' % (titleC, dateCompF, dateCompS, invenspecForge[pForge][2], invenspecSharepoint[pSharepoint][1])

invenspecConly.write()
invenspecCFS.write()
invenspecCF.write()
invenspecCS.write()
