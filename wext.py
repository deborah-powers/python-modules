#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from os import sep
from folderCls import Folder
import loggerFct as log

pathRefCss = 'C:\\wamp64\\www\\site-dp\\library-css\\'
pathRefJs = 'C:\\wamp64\\www\\site-dp\\library-js\\'
PathExt = 'C:\\Users\\deborah.powers\\Desktop\\webext\\'
wext =( 'all-clean-article', 'all-md-perso', 'rgaa vb' )

# récupérer les fichiers css et js
folderRefCss = Folder (pathRefCss)
folderRefCss.get ('.css')
folderRefJs = Folder (pathRefJs)
folderRefJs.get ('.js')
folderRefJs.filter ('.json', False)
folderExtJs = Folder (PathExt)
folderExtJs.get ('.js')
folderExtJs.filter ('service-worker', False)
folderExtJs.filter ('.json', False)
folderExtJs.filter ('code', False)
folderExtCss = Folder (PathExt)
folderExtCss.get ('.css')
# vérifier la présence de certaines références
def groupByRef (folderRef, folderExt):
	dicoFiles ={}
	for ref in folderRef.list:
		dicoFiles[ref.title] = Folder (PathExt)
		dicoFiles[ref.title].append (ref)	# la référence est faussement considérée comme le premier élément du folder
		f=0
		nbFile = len (folderExt.list)
		while f< nbFile:
			if ref.title == folderExt.list[f].title:
				dicoFiles[ref.title].append (folderExt.list[f])
				folderExt.list.remove (folderExt.list[f])
				f= nbFile
			f+=1
	refKeys = dicoFiles.keys()
	delKeys =[]
	for ref in refKeys:
		if len (dicoFiles[ref]) ==1: delKeys.append (ref)
	for ref in delKeys: dicoFiles.pop (ref)
	return dicoFiles

def findModif (pathRef, folderIdem):
	# le premier élément du dossier contient la référence
	fileRef = folderIdem.list.pop (0)
	fileRef.path = pathRef + fileRef.path
	fileRef.read()
	folderIdem.read()
	for fidem in folderIdem.list:
		if fidem.text != fileRef.text:
			f= fidem.path.find (sep)
			fidem.title = fidem.path[:f]
		#	print ('modification possible dans', fileRef.title, fidem.title)
			fileRef.comparer (fidem)

# print ('\t=== comparer les fichiers css ===\n')
groups = groupByRef (folderRefCss, folderExtCss)
refList = groups.keys()
for ref in refList: findModif (pathRefCss, groups [ref])

groups = groupByRef (folderRefJs, folderExtJs)
refList = groups.keys()
for ref in refList: findModif (pathRefJs, groups [ref])