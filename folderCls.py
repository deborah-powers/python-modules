#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import listFct
import textFct
from fileLocal import *
from fileCls import File, Article
from htmlCls import Html
import loggerFct

class Folder():
	def __init__ (self, path='b/'):
		path = shortcut (path)
		self.path = path
		self.list =[]
		if self.path[-1] != os.sep: self.path = self.path + os.sep

	# ________________________ agir sur les fichiers ________________________

	def rename (self, wordOld, wordNew=""):
		for file in self.list:
			if wordOld not in file.title: continue
			file.fromPath()
			newPath = file.title.replace (wordOld, wordNew)
			newPath = file.path.replace ('\t', newPath)
			file.toPath()
			os.rename (file.path, newPath)

	def renameDate (self):
		self.get ('202')
		for file in self.list: file.renameDate()

	def move (self, newPath):
		# newPath est une string
		if newPath[-1] != os.sep: newPath = newPath + os.sep
		newPath = shortcut (newPath)
		for file in self.list:
			file.toPath()
			os.rename (file.path, newPath + file.path)
		self.path = newPath

	def replace (self, wordOld, wordNew):
		""" remplacer un motif dans le texte """
		for file in self.list:
			if wordOld in file.text:
				file.replace (wordOld, wordNew)
				file.write()

	# ________________________ fonctions de base ________________________

	def get (self, tagName=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			if tagName and sens:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if tagName not in subList[i]: trash = subList.pop(i)
			elif tagName:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if tagName in subList[i]: trash = subList.pop(i)
			if subList:
				for file in subList:
					if '.' not in file: continue
					elif 'index.' in file: continue
					fileTmp = File (os.path.join (dirpath, file))
					fileTmp.fromPath()
					# fileTmp.path = fileTmp.path.replace (self.path, "")
					self.list.append (fileTmp)
		self.list.sort()

	def filter (self, tagName, sens=True):
		""" quand on a besoin de ré-exclure certains fichiers après le get.
		quand je veux exclure sur plusieurs mots-clefs """
		rangeFile = listFct.range (self.list)
		rangeFile.reverse()
		if sens:
			for f in rangeFile:
				if tagName not in self.list[f].path and tagName not in self.list[f].title: trash = self.list.pop(f)
		else:
			for f in rangeFile:
				if tagName in self.list[f].path or tagName in self.list[f].title: trash = self.list.pop(f)

	def createIndex (self):
		index = Html (self.path + 'index.html')
		index.text = '<h1>index du dossier ' + self.path +'</h1>\n'
		self.get()
		for file in self.list:
			index.text = index.text + "<a href='" + file.path +"'>"+ file.title +'</a>\n'
		index.styles.append ('C:\\wamp64\\www\\site-dp\\library-css\\structure.css')
		index.styles.append ('C:\\wamp64\\www\\site-dp\\library-css\\perso.css')
		index.styles.append ('C:\\wamp64\\www\\site-dp\\library-css\\index-dossier.css')
		index.write()

	def read (self):
		rangeList = listFct.range (self.list)
		for i in rangeList: self[i].read()

	def write (self):
		rangeList = listFct.range (self.list)
		for i in rangeList: self[i].write()

	def iterate (self, function):
		newList = Folder()
		for file in self.list:
			res = function (file)
			if res: newList.append (res)
		return newList

	def append (self, file):
		file.shortcut()
		self.list.append (file)

	def __str__ (self):
		strList = 'Dossier: '+ self.path +'\nListe:'
		for file in self:
			file.toPath()
			strList = strList +'\n'+ file.path.replace (self.path, "")
		return strList

	def __len__(self):
		return len (self.list)

	def __setitem__ (self, pos, item):
		lenList = len (self.list)
		if type (pos) == int:
			while pos <0: pos += lenList
			if pos < lenList: self.list[pos] = item
			else: self.append (item)

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex[0], posIndex[1], posIndex[2])
			if type (item) in (tuple, list) and len (item) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = item[i]
					i+=1
			elif type (item) == Folder and len (item.list) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = item.list[i]
					i+=1

	def __getitem__ (self, pos):
		lenList = len (self.list)
		if type (pos) == int:
			while pos <0: pos += lenList
			while pos >= lenList: pos -= lenList
			return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex[0], posIndex[1], posIndex[2])
			newList = Folder (self.path)
			for l in rangeList: newList.append (self.list[l])
			return newList
		else: return None

	def test (self):
		self.path = shortcut ('a/')
		self.get ('built on')
		"""
		print (self)
		print (self[1])
		self[0] = self[3]
		self.rename ('built', 'dodo')
		print (self)
		"""
		file = File ('fanfics/a doctor calls.txt')
		self.append (file)
		self.move ('b/temp/')
		self.filter ('the')
		print (self)
		"""
		self[0].path = self[0].path
		self[0].read()
		print (len (self[0].text), 'caractères')
		"""
"""
folder = Folder()
folder.test()
"""
class FolderArticle (Folder):
	def __init__ (self, path='a/', subject=""):
		Folder.__init__(self, path)
		self.subject = subject
		if subject == 'fanfic' or subject == 'romance': self.path = 'a/fanfics/'
		elif subject == 'cour': self.path = 'a/cours/'
		elif subject == 'education': self.path = 'a/education/'
		elif subject == 'roman': self.path = 'a/romans/'
		self.path = shortcut (self.path)

	def createIndex (self):
		index = File (self.path + 'index.tsv')
		self.get()
		self.read()
		self.list.sort()
		for file in self.list:
			file.toPath()
			index.text = index.text + file.subject +'\t'+ file.author +'\t'+ file.title +'\t'+ file.path +'\n'
		print (self.path)
		index.text = index.text.replace (self.path, "")
		index.write()

	def createIndex_va (self):
		index = Html (self.path + 'index.html')
		index.text = '<h1>index du dossier ' + self.path +'</h1>\n<table>\n'
		self.get()
		self.read()
		self.list.sort()
		for file in self.list:
			file.toPath()
			index.text = index.text + "<tr><td>"+ file.subject + "</td><td>" + file.author + "</td><td><a href='" + file.path +"'>"+ file.title + "</a></td></tr>\n"
		index.text = index.text + '</table>'
		index.styles.append ('C:\\wamp64\\www\\site-dp\\library-css\\structure.css')
		index.styles.append ('C:\\wamp64\\www\\site-dp\\library-css\\perso.css')
		index.write()

	def get (self, tagName=None, sens=True):
		tmpList = Folder (self.path)
		tmpList.get (tagName, sens)
		for file in tmpList.list:
			article = Article (file.path)
			if article.type in ('html', 'txt'): self.append (article)
		self.list.sort()

	def __getitem__ (self, pos):
		lenList = len (self.list)
		if type (pos) == int:
			if pos <0: pos += lenList
			if pos > lenList or pos <0: return None
			else: return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
			newList = FolderArticle (self.path)
			for l in rangeList: newList.append (self.list[l])
			return newList
		else: return None
