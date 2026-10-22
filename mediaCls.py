#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import win32com.client as wclient
from urllib import request as urlRequest
import fileLocal
from folderCls import Folder
import loggerFct as log

""" classe et fonctions communes pour les médias, imageCls et videoCls """

dateFormatDay = '%Y-%m-%d'
dateFormatHour = dateFormatDay + '-%H-%M'
metadataWindow =[
	'Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type',
	'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating',
	'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
	'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords'
]
alpabet = 'abcdefghijklmnopqrstuvwxyz'
extensions =[ 'jpg', 'bmp', 'gif', 'png', 'mp4', 'avi', 'mov', 'heic', 'heif' ]

def mediaAtraiter (imgTitle):
	imgTitle = imgTitle.lower()
	if imgTitle[:4] in ('img_', 'img-', 'vid_') or imgTitle[:6] == 'video_': return True
	else:
		l=0
		while l<26:
			if alpabet[l] in imgTitle: l=27
			l+=1
		if l==28: return False
		else: return True

def getNameSpace (pathWindow):
	if pathWindow[-1] == os.sep: pathWindow = pathWindow[:-1]
	shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
	nameSpace = shellApp.NameSpace (pathWindow)
	return nameSpace

def getDateCreation (nameImg, nameSpace, addHour=False):
	fileData = nameSpace.ParseName (nameImg)
	# repérer la date de création. Date taken ou Date created
	dateCreation = nameSpace.GetDetailsOf (fileData, 12).replace (" ","")
	if dateCreation and '202' in dateCreation:
		dateCreation = dateCreation.replace ('‎', "")
		dateCreation = dateCreation.replace ('‏', '/')
	else: dateCreation = nameSpace.GetDetailsOf (fileData, 4).replace (" ",'/')
	# mettre en forme la date de création
	dateCreation = dateCreation.replace (':', '-')
	dateList = dateCreation.split ('/')
	dateCreation = dateList[2] +'-'+ dateList[1] +'-'+ dateList[0]
	if addHour: dateCreation = dateCreation +'-'+ dateList[3]
	return dateCreation

def createDatedName (pathImg, extImg, dateCreation):
	newName =""
	l=0
	while l<26:
		newName = pathImg + dateCreation +" "+ alpabet[l] +'.'+ extImg
		if not os.path.exists (newName): l=27
		l+=1
	if l<27:
		newName =""
		print ("je n'ai pas réussi à renommer l'image:", pathImg)
	return newName

def fromWeb (imgUrl, imgFile):
	try: urlRequest.urlretrieve (imgUrl, imgFile)
	except Exception as e:
		print (e)
		return False
	else: return True

class MediaFile():
	def __init__ (self, filePath=""):
		self.path =""
		self.title =""
		self.extension =""
		self.pathRoot =""
		if filePath:
			self.path = filePath
			self.fromPath()

	def renameDate (self, nameSpace, addHour=False):
		nameCreation = self.renameDateEtape1 (nameSpace, addHour);
		if nameCreation: os.rename (self.path, nameCreation)

	def renameDateEtape1 (self, nameSpace, addHour=False):
		""" renommer un fichier en prenant en compte la date
		la fonction utilise les métadonnées de window
		"""
		if mediaAtraiter (self.title):
			self.toPath()
			dateCreation = getDateCreation (self.title +'.'+ self.extension, nameSpace, addHour)
			nameCreation = createDatedName (self.pathRoot, self.extension, dateCreation)
			if nameCreation:
				self.open()
				return nameCreation
			else: return None
		else: return None

	def draw (self):
		self.toPath()
		chars = '/\\\t\n'; c=0
		while chars != 'error' and c<4:
			if chars[c] in self.title:
				print ('le fichier est mal formé:', self.title [:100])
				print (c, chars[c])
				chars = 'error'
			c+=1
		if chars == 'error': return False
		else:
			self.toPath()
			return True

	def remove (self):
		self.toPath()
		if os.path.exists (self.path): os.remove (self.path)

	def fromPath (self):
		if self.pathRoot: return
		self.path = fileLocal.shortcut (self.path)
		if os.sep not in self.path or '.' not in self.path:
		#	print ('fichier malformé:\n' + self.path)
			return
		elif self.path.rfind (os.sep) > self.path.rfind ('.'):
			# print ('fichier malformé:\n' + self.path)
			return
		posS = self.path.rfind (os.sep) +1
		posE = self.path.rfind ('.')
		self.title = self.path [posS:posE]
		self.extension = self.path[posE+1:]
		self.pathRoot = self.path [:posS]

	def toPath (self):
		self.path = self.pathRoot + self.title +'.'+ self.extension

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		self.toPath()
		newFile.toPath()
		return self.path < newFile.path

	def __str__ (self):
		self.toPath()
		return self.path


class MediaFolder (Folder):
	def __init__ (self, path='i/'):
		Folder.__init__(self, path)

	def renameDate (self, addHour=False):
		nameSpace = getNameSpace (self.path[:-1])
		self.get ('new')
		for image in self.list:
			if os.sep not in image.path: image.path = self.path + image.path
			image.renameDate (nameSpace, addHour)
		#	image.path = image.path.replace (self.path, "")

	def get (self, detail=""):
		self.fromPath()
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			range_tag = range (len (subList) -1, -1, -1)
			for i in range_tag:
				if subList[i][-3:] not in extensions or subList[i][-4] !='.': trash = subList.pop(i)
			if detail == 'new':
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if not mediaAtraiter (subList[i][:-4]): trash = subList.pop(i)
			elif detail:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if detail not in subList[i]: trash = subList.pop(i)
			if subList:
				for image in subList:
				#	fileTmp = MediaFile (os.path.join (dirpath, image))
					self.list.append (os.path.join (dirpath, image))
		self.list.sort()

	def __str__ (self):
		strText = 'liste à %d éléments dans le dossier %s' %( len (self.list), self.path)
		self.fromPath()
		for image in self.list[:6]: strText = strText + '\n\t' + str (image).replace (self.path, "")
		return strText