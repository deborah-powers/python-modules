#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import win32com.client as wclient
from fileCls import File
from folderCls import Folder
import loggerFct as log

metadataWindow =[
	'Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type',
	'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating',
	'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
	'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords'
]
imgExtensions =[ 'jpg', 'bmp', 'gif', 'png', 'mp4' ]
alpabet = 'abcdefghijklmnopqrstuvwxyz'

def imageAtraiter (imageTitle):
	aTraiter = True
	if os.sep in imageTitle: aTraiter = False
	if imageTitle[:4] not in 'img_ img- vid_' and imageTitle[:6] != 'video_':
		l=0
		while l<26:
			if alpabet[l] in imageTitle:
				aTraiter = False
				l=27
			l+=1
	return aTraiter

class FolderImg (Folder):
	def __init__ (self, path='i/'):
		Folder.__init__(self, path)
	#	self.date = '2012-12-12'

	def renameDate (self, addHour=False):
		pathWindow = self.path[:-1]
		shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
		nameSpace = shellApp.NameSpace (pathWindow)
		self.get()
		for file in self.list:
			# repérer les fichiers traitables par cette méthode
			if imageAtraiter (file.path.replace ('\t', file.title)):
				fileData = nameSpace.ParseName (file.title + file.path[-4:])
				# repérer la date de création
				dateCreation = nameSpace.GetDetailsOf (fileData, 12).replace (" ","")
				if dateCreation:
					dateCreation = dateCreation.replace ('‎', "")
					dateCreation = dateCreation.replace ('‏', '/')
				else: dateCreation = nameSpace.GetDetailsOf (fileData, 4).replace (" ",'/')
				# mettre en forme la date de création
				dateCreation = dateCreation.replace (':', '-')
				dateList = dateCreation.split ('/')
				dateCreation = dateList[2] +'-'+ dateList[1] +'-'+ dateList[0]
				if addHour: dateCreation = dateCreation +'-'+ dateList[3]
				# renommer le fichier
				file.path = self.path + file.path
				file.fromPath()
				l=0
				while l<26:
					newPath = file.path.replace ('\t', dateCreation +" "+ alpabet[l])
					if not os.path.exists (newPath):
						file.toPath()
						os.rename (file.path, newPath)
						l=27
					l+=1
				file.path = file.path.replace (self.path, "")

	def get (self, tagName=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			range_tag = range (len (subList) -1, -1, -1)
			for i in range_tag:
				if subList[i][-3:] not in imgExtensions or subList[i][-4] !='.': trash = subList.pop(i)
			range_tag = range (len (subList) -1, -1, -1)
			if tagName and sens:
				for i in range_tag:
					if tagName not in subList[i]: trash = subList.pop(i)
			elif tagName:
				for i in range_tag:
					if tagName in subList[i]: trash = subList.pop(i)
			if subList:
				for file in subList:
					fileTmp = File (os.path.join (dirpath, file))
					fileTmp.fromPath()
					# fileTmp.path = fileTmp.path.replace (self.path, "")
					self.list.append (fileTmp)
		self.list.sort()
		self.fromPath()