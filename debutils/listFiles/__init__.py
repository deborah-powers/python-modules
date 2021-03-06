#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import fileSimple as fs
from debutils.list import List
import debutils.logger as logger

class ListFile (List):
	def __init__ (self, path='b/'):
		List.__init__ (self)
		if path: path = fs.shortcut (path)
		self.path = path


	def get (self, TagNomfile=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			if TagNomfile and sens:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if TagNomfile not in subList[i]: trash = subList.pop(i)
			elif TagNomfile:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if TagNomfile in subList[i]: trash = subList.pop(i)
			if subList:
				for file in subList:
					d=1+ file.rfind ('.')
					if d<=1: continue
					if file[d:] not in fs.extensions: continue
					fileTmp = fs.File (os.path.join (dirpath, file))
					# fileTmp.dataFromFile()
					self.add (fileTmp)

		self.sort()
		# eliminer les fichiers de format inconnu
		rangeFile = self.range()
		rangeFile.reverse()
		for f in rangeFile:
			if self[f].extension not in fs.extensions: trash = self.pop(f)

	def filter (self, TagNomfile, sens=True):
		""" quand on a besoin de ré-exclure certains fichiers après le get.
		quand je veux exclure sur plusieurs mots-clefs """
		rangeFile = self.range()
		rangeFile.reverse()
		if sens:
			for f in rangeFile:
				if TagNomfile not in self[f].file: trash = self.list.pop(f)
		else:
			for f in rangeFile:
				if TagNomfile in self[f].file: trash = self.list.pop(f)

	def openAll (self):
		rangeFile = self.range()
		rangeFile.reverse()
		for f in rangeFile: self[f].fromFile()

	def closeAll (self):
		rangeFile = self.range()
		rangeFile.reverse()
		for f in rangeFile: self[f].toFile()

	def doublons (self, inText=False):
		listDbl = ListFile (self.path)
		rangeFile = self.range()
		for f in rangeFile:
			for g in rangeFile [f+1:]:
				if self[f].title == self[g].title:
					# print ('doublons pour', self[f].title, '\n\t', self[f].path, '\n\t', self[g].path)
					listDbl.add (self[f])
			if inText:
				for f in rangeFile:
					self[f].fromFile()
					if self[f].text:
						for g in rangeFile [f+1:]:
							if self[f].text == self[g].text:
								# print ('doublons pournt', self[f].file, '\n\t', self[g].file)
								listDbl.add (self[f])
		return listDbl


	def compareGit (self, pathNew):
		# identifier les fichiers modifiés par rapport à la référence
		fnote = fs.File ('b/comparaison des dossiers.txt')
		listNew = ListFile (pathNew)
		listNew.get()
		listNew.openAll()
		if not self.list:
			self.get()
			self.openAll()
		a= self.length() -1
		while a>=0:
			b= listNew.length() -1
			while b>=0:
				if self[a].title == listNew[b].title and self[a].extension == listNew[b].extension:
					if self[a].text != listNew[b].text:
						print ('modification dans', self[a].file.replace (self.path, ""))
						fnote.text = fnote.text + 'modification dans %s\n' % self[a].file.replace (self.path, "")
					self.pop (a)
					listNew.pop (b)
					b=0
				b-=1
			a-=1
		a= self.length() -1
		while a>=0:
			b= listNew.length() -1
			while b>=0:
				if self[a].title == listNew[b].title:
					if self[a].text != listNew[b].text:
						print ('modification dans', self[a].file.replace (self.path, ""), "/", listNew[b].extension)
						fnote.text = fnote.text + 'modification dans %s / %s\n' %( self[a].file.replace (self.path, ""), listNew[b].extension)
					self.pop (a)
					listNew.pop (b)
					b=0
				b-=1
			a-=1
		a= self.length() -1
		while a>=0:
			b= listNew.length() -1
			while b>=0:
				if self[a].extension == listNew[b].extension and self[a].text == listNew[b].text:
					print ('fichiers identiques:', self[a].file.replace (self.path, ""), '\t', listNew[b].file.replace (listNew.path, ""))
					fnote.text = fnote.text + 'fichiers identiques: %s\t%s\n' %( self[a].file.replace (self.path, ""), listNew[b].file.replace (listNew.path, ""))
					self.pop (a)
					listNew.pop (b)
					b=0
				b-=1
			a-=1
		fnote.toFile()

	def compare (self, pathNew):
		# identifier les films présents dans pathNew mais absent de la référence
		listNew = ListFile (pathNew)
		listNew.get()
		listDbl = ListFile()
		listUnq = ListFile()
		rangeTmp = listNew.range()
		rangeTmp.reverse()
		for fref in self:
			for f in rangeTmp:
				if fref.title == listNew[f].title:
					# print ('doublons pour', fref.title, '\n\t', fref.path, '\n\t', listNew[f].path)
					listDbl.add (listNew[f])
		for fnew in listNew:
			if fnew not in listDbl: listUnq.add (fnew)
		return listUnq

	def move (self, newPath):
		# newPath est une string
		newPath = fs.shortcut (newPath)
		for file in self:
			nvfile = file.file.replace (self.path, newPath, 1)
			os.rename (file.file, nvfile)
			file.file = nvfile
			file.extractData()
		self.path = newPath

	def clean (self):
		numbers = '0123456789'
		for fref in self:
			newFile = fref.title.replace ('.', ' ')
			newFile = newFile.replace ('_', ' ')
			newFile = newFile.replace ('\t', ' ')
			newFile = newFile.replace ('-', ' - ')
			while ' ' in newFile: newFile = newFile.replace (' ', ' ')
			newFile = newFile.strip()
			newFile = newFile.lower()
			for n in numbers:
				newFile = newFile.replace (n+' - ', n+' ')
				newFile = newFile.replace (' - '+n, ' '+n)
			newFile = fref.path + newFile +'.'+ fref.extension.lower()
			os.rename (fref.file, newFile)

	def rename (self, wordOld, wordNew=""):
		for file in self:
			if wordOld not in file.title: continue
			newFile = file.title.replace (wordOld, wordNew)
			newFile = file.path + newFile +'.'+ file.extension
			os.rename (file.file, newFile)

	def replace (self, wordOld, wordNew, close=True):
		""" remplacer un motif dans le texte """
		for file in self:
			if close: file.fromFile()
			file.replace (wordOld, wordNew)
			if close: file.toFile()

	def modify (self, funcText, close=True):
		for file in self:
			if close: file.fromFile()
			funcText (file)
			if close: file.toFile()

	def __str__ (self):
		strList = 'Dossier: '+ self.path +'\nListe:'
		for file in self: strList = strList +'\n'+ file.title
		return strList

class ListArticle (ListFile):

	def __init__ (self, genre=""):
		ListFile.__init__ (self)
		self.genre = genre
		if genre == 'fanfic' or genre == 'romance': self.path = 'a/fanfics/'
		elif genre == 'cour': self.path = 'a/cours/'
		elif genre == 'education': self.path = 'a/education/'
		elif genre == 'roman': self.path = 'a/romans/'
		self.path = fs.shortcut (self.path)

	def get (self):
		tmpList = ListFile (self.path)
		tmpList.get ('.txt')
		lRange = tmpList.range()
		for f in lRange:
			self.add (fs.Article())
			self[f].title = tmpList[f].title
			self[f].path = tmpList[f].path
			self[f].fileFromData()
			self[f].fromFile()
		self.sort()

	def __str__ (self):
		string =""
		for article in self: string = string +'\n%s\t%s\t%s' % (article.subject, article.author, article.title)
		return string [1:]

	def show (self, genre=None):
		if genre:
			print (self.length(), 'histoires de', genre)
			for article in self: print ('%s\t%s' % (article.author, article.title))
		else:
			print (self.length(), 'histoires')
			print (self)

	def getBySubject (self, subject=None):
		if not subject: return self
		else:
			aList = ListArticle()
			for article in self:
				if subject in article.subject: aList.add (article)
			return aList