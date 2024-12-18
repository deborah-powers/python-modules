#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import win32com.client as wclient
from fileCls import File
from folderCls import Folder
import loggerFct as log

metadataWindows =[ 'Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected', 'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords' ]
imgExtensions =[ 'jpg', 'bmp', 'gif', 'png' ]
alpabet = 'abcdefghijklmnopqrstuvwxyz'

def imageDejaTraitee (imageTitle):
	dejaTraitee = False
	for l in alpabet:
		if l in imageTitle: dejaTraitee = True
	return dejaTraitee

class FolderImg (Folder):
	def __init__ (self, path='i/'):
		Folder.__init__(self, path)
	#	self.date = '2012-12-12'

	def renameDate (self):
		self.get ('202')
		for file in self.list:
			file.path = self.path + file.path
			file.renameDate()
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