#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import fileClass as fc
from listClass import ListPerso

help ="""
ce script peut être appelé dans un autre script
python %s fileName action oldArg (newArg)
les valeurs de action:
	n	renommer les fichiers en remplacant un motif par un autre
	c	remplacer un motif par un autre dans le contenu du fichier
	m	déplacer les fichiers
	l	lister les fichiers
	d	vérifier s'il y a des doublons
""" % __file__

class ListFile (ListPerso):
	def __init__(self, path='b/'):
		ListPerso.__init__(self)
		if path: path = fc.shortcut (path)
		self.path = path

	def get (self, TagNomfile=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			if TagNomfile and sens:
				range_tag = range (len (subList) -1,-1,-1)
				for i in range_tag:
					if TagNomfile not in subList[i]: trash = subList.pop (i)
			elif TagNomfile:
				range_tag = range (len (subList) -1,-1,-1)
				for i in range_tag:
					if TagNomfile in subList[i]: trash = subList.pop (i)
			if subList:
				for file in subList:
					fileTmp = fc.FilePerso (os.path.join (dirpath, file))
					# fileTmp.dataFromFile()
					self.add (fileTmp)
		self.sort()
		# eliminer les fichiers de format inconnu
		rangeFile = self.range()
		rangeFile.reverse()
		for f in rangeFile:
			if self[f].extension not in fc.extensions: trash = self.pop (f)

	def filter (self, TagNomfile, sens=True):
		""" quand on a besoin de ré-exclure certains fichiers après le get.
		quand je veux exclure sur plusieurs mots-clefs """
		rangeFile = self.range()
		rangeFile.reverse()
		if sens:
			for f in rangeFile:
				if TagNomfile not in self[f].file: trash = self.list.pop (f)
		else:
			for f in rangeFile:
				if TagNomfile in self[f].file: trash = self.list.pop (f)

	def doublons (self, inText=False):
		listDbl = ListFile (self.path)
		rangeFile = self.range()
		for f in rangeFile:
			for g in rangeFile[f+1:]:
				if self[f].title == self[g].title:
					# print ('doublons pour', self[f].title, '\n\t', self[f].path, '\n\t', self[g].path)
					listDbl.add (self[f])
			if inText:
				for f in rangeFile:
					self[f].fromFile()
					if self[f].text:
						for g in rangeFile[f+1:]:
							if self[f].text == self[g].text:
								# print ('doublons pour\n\t', self[f].file, '\n\t', self[g].file)
								listDbl.add (self[f])
		return listDbl

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
		newPath = fc.shortcut (newPath)
		for file in self:
			nvfile = file.file.replace (self.path, newPath, 1)
			os.rename (file.file, nvfile)
			file.file = nvfile
			file.extractData()
		self.path = newPath

	def clean (self):
		numbers = '0123456789'
		for fref in self:
			newFile = fref.title.replace ('.',' ')
			newFile = newFile.replace ('_',' ')
			newFile = newFile.replace ('\t',' ')
			newFile = newFile.replace ('-',' - ')
			while '  ' in newFile: newFile = newFile.replace ('  ',' ')
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

	def __str__(self):
		strList = 'Dossier: '+ self.path +'\nListe:'
		for file in self: strList = strList +'\n'+ file.title
		return strList

class ArticleList (ListFile):
	def __init__(self, genre=""):
		ListFile.__init__(self)
		self.path = fc.shortcut ('a/')
		self.genre = genre
		if genre == 'fanfic' or genre == 'romance': self.path = 'a/fanfics/'
		elif genre == 'cour': self.path = 'a/cours/'
		elif genre == 'education': self.path = 'a/education/'
		elif genre == 'roman': self.path = 'a/romans/'
		self.path = fc.shortcut (self.path)

	def get (self):
		tmpList = ListFile (self.path)
		tmpList.get ('.html')
		lRange = tmpList.range()
		for f in lRange:
			self.add (FileHtml())
			self[f].title = tmpList[f].title
			self[f].path = tmpList[f].path
			self[f].fileFromData()
			self[f].fromFile()
		self.sort()

	def __str__(self):
		string =""
		for article in self: string = string +'\n%s\t%s\t%s' %( article.subject, article.author, article.title )
		return string[1:]

	def show (self, genre=None):
		if genre:
			print (len (self), 'histoires de', genre)
			for article in self: print ('%s\t%s' %( article.author, article.title))
		else:
			print (len (self), 'histoires')
			print (self)

	def getByGenre (self, genre=None):
		if not genre: return self
		else:
			aList = ArticleList()
			for article in self:
				if genre in article.subject: aList.add (article)
			return aList

if __name__ != '__main__': pass
elif len (argv) <3: print (help)
else:
	flist = ListFile (argv[1])
	action = argv[2]
	if action in 'd l':
		if len (argv) >3: flist.get (argv[3])
		else: flist.get()
		if action == 'd': flist.doublons()
		else: print (flist)
	elif len (argv) <4: print (help)
	else:
		wordOld = argv[3]
		wordNew =""
		if len (argv) >4: wordNew = argv[4]
		if action =='n':
			flist.get (wordOld)
			flist.rename (wordOld, wordNew)
		elif action =='c':
			if (len (argv) >5): flist.get (argv[5])
			else: flist.get()
			flist.replace (wordOld, wordNew)
		elif action =='m':
			if (wordNew): flist.get (wordNew)
			else: flist.get()
			flist.move (wordOld)
		else: print (help)
