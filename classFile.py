#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
from classList import List
from classText import Text
from fileLocal import *
import logger

class File():
	def __init__ (self, file =None):
		self.path = file
		self.title =""
		self.text = Text()
		if file: self.fromPath()

	def fromPath (self):
		if '\t' in self.path: return
		self.path = shortcut (self.path)
		if os.sep not in self.path or '.' not in self.path:
			print ('fichier malformé:\n' + self.path)
			return
		elif self.path.rfind (os.sep) > self.path.rfind ('.'):
			print ('fichier malformé:\n' + self.path)
			return
		posS = self.path.rfind (os.sep) +1
		posE = self.path.rfind ('.')
		self.title = self.path [posS:posE]
		self.path = self.path.replace (self.title, '\t')

	def toPath (self):
		if '\t' in self.path: self.path = self.path.replace ('\t', self.title)

	def read (self):
		self.toPath()
		if not os.path.exists (self.path): return
		textBrut = open (self.path, 'rb')
		tmpByte = textBrut.read()
		encodingList = ('utf-8', 'ascii', 'ISO-8859-1')
		text =""
		for encoding in encodingList:
			try: text = codecs.decode (tmpByte, encoding=encoding)
			except UnicodeDecodeError: pass
			else: break
		textBrut.close()
		if text: self.text = Text (text)
		self.fromPath()

	def write (self, mode='w'):
		# pas de texte
		if not self.text:
			print ('rien a ecrire pour:', self.title)
			return
		chars = '/\\\t\n'; c=0
		while chars != 'error' and c<4:
			if chars[c] in self.title:
				print ('le fichier est mal formé:', self.title [:100])
				print (c, chars[c])
				chars = 'error'
			c+=1
		if chars != 'error':
			self.toPath()
			if mode == 'a' and os.path.isfile (self.path): self.text ='\n'+ self.text
			# ouvrir le fichier et ecrire le texte
			textBrut = open (self.path, mode +'b')
			textBrut.write (self.text.encode ('utf-8'))
			textBrut.close()

	def shortcut (self):
		self.path = shortcut (self.path)

	def __str__ (self):
		strShow = 'Titre: %s' % self.title
		if self.text: strShow += '.\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		self.toPath()
		newFile.toPath()
		return self.path < newFile.path

	def test (self):
		self.path = 'b/test-file.txt'
		print ('fromPath\t', self.path)
		self.fromPath()
		self.text = """nekg,ze,fmalf,al,f
fkz,fzkl,fam; v adbazjkbdafaef"""
		print ('affichage\t', self)
		print ('écriture')
		self.write()
		self.read()
		print ('lecture\t', self.text)
		self.title = 'coco'
		self.toPath()
		print ('modifier le titre\t', self.path)
		self.text = self.text.shape ('reset')
		print (self.text[:200])
		self.write()
"""
file = File ('b/ddt local\\ajout-etat-4350.sql')
file.test()
"""

templateText ="""Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""

templateHtml ="<!DOCTYPE html><html><head><title>%s</title><meta charset='utf-8'/><meta name='viewport' content='width=device-width, initial-scale=1'/><base target='_blank'><meta name='author' content='%s'/><meta name='subject' content='%s'/><meta name='link' content='%s'/><meta name='autlink' content='%s'/>%s</head><body>%s</body></html>"

class Article (File):
	# classe pour les fichiers txt et html
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.author =""
		self.subject =""
		self.link =""
		self.autlink =""
		self.type =""

	def toText (self):
		if self.type == 'txt': return self
		article = Article()
		article.text = self.text
		article.path = self.path
		article.title = self.title
		article.type = 'txt'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.text = article.text.fromHtml()
		if '</' in article.text: return self
		else: return article

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] in ('.html', 'xhtml'): self.type = 'html'

	def read (self):
		File.read (self)
		if self.type == 'html':
			self.text = self.text.replace ('\n')
			self.text = self.text.replace ('\t')
			metadata = self.text.fromModel (templateHtml)
			self.subject = metadata [2]
			self.author = metadata [1]
			self.link = metadata [3]
			self.autlink = metadata [4]
			self.text = Text (metadata [6])
		elif self.type == 'txt':
			metadata = self.text.fromModel (templateText)
			self.subject = metadata [0]
			self.author = metadata [1]
			self.link = metadata [2]
			self.autlink = metadata [3]
			self.text = Text (metadata [4])

	def write (self):
		text =""
		if self.type == 'html': text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, "", self.text)
		elif self.type == 'txt': text = templateText % (self.subject, self.author, self.link, self.autlink, self.text)
		self.text = Text (text)
		File.write (self, 'w')

	def __str__ (self):
		strShow = 'Titre: %s\tSujet: %s\tAuteur: %s' % (self.title, self.subject, self.author)
		if self.text: strShow += '\n\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		struct = '%st%st%s'
		return struct % (self.subject, self.author, self.title) < struct % (newFile.subject, newFile.author, newFile.title)

	def test (self):
		self.author = 'moi'
		self.subject = 'random'
		self.autlink = 'http://www.auteur.fr/'
		self.link = 'http://www.test.fr/'
		self.text = """nekg,ze,fmalf,al,f
fkz,fzkl,fam; v adbazjkbdafaef"""
		print ('affichage\t', self)
		self.fromPath()
		print ('fromPath\t', self.path)
		print ('écriture')
		self.write()
		self.read()
		print ('lecture\t', self.text[:200])
		print ('conversion en html')
		self.path = self.path.replace ('.txt', '.html')
		self.text = self.text.toHtml()
		self.type = 'html'
		print ('text html\t', self.text)
		self.write()
"""
file = Article ('b/artest.txt')
file.test()
"""

class FileList (File):
	def __init__(self, file=None, sep='\n'):
		File.__init__(self, file)
		self.list = List()
		self.sep = sep

	def toText (self, sep):
		self.text = self.list.toText (self.sep)

	def fromText (self, text=None):
		if text: self.text = Text (text)
		self.list = self.text.split (self.sep)

	def range (self, start=0, end=0, step=1):
		return self.list.range (start, end, step)

	def iterate (self, function):
		return self.list.iterate (function)

class Folder():
	def __init__ (self, path='b/'):
		if path: path = shortcut (path)
		self.path = path
		self.list = List()

	# ________________________ agir sur les fichiers ________________________

	def rename (self, wordOld, wordNew=""):
		for file in self.list:
			if wordOld not in file.title: continue
			file.fromPath()
			newFile = File()
			newFile.title = file.title.replace (wordOld, wordNew)
			newFile.path = file.path
			newFile.toPath()
			file.toPath()
			os.rename (self.path + file.path, self.path + newFile.path)

	def move (self, newPath):
		# newPath est une string
		if newPath[-1] != os.sep: newPath = newPath + os.sep
		newPath = shortcut (newPath)
		for file in self.list:
			file.toPath()
			os.rename (self.path + file.path, newPath + file.path)
		self.path = newPath

	def replace (self, wordOld, wordNew, close=True):
		""" remplacer un motif dans le texte """
		for file in self.list:
			if close: file.fromFile()
			if wordOld in file.text:
				file.text = file.text.replace (wordOld, wordNew)
				if close: file.toFile()

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
					fileTmp = File (os.path.join (dirpath, file))
					fileTmp.fromPath()
					fileTmp.path = fileTmp.path.replace (self.path, "")
					self.list.append (fileTmp)
				self.list.sort()

	def filter (self, tagName, sens=True):
		""" quand on a besoin de ré-exclure certains fichiers après le get.
		quand je veux exclure sur plusieurs mots-clefs """
		rangeFile = self.list.range()
		rangeFile.reverse()
		if sens:
			for f in rangeFile:
				if tagName not in self.list[f].path and tagName not in self.list[f].title: trash = self.list.pop(f)
		else:
			for f in rangeFile:
				if tagName in self.list[f].path or tagName in self.list[f].title: trash = self.list.pop(f)

	def read (self):
		rangeList = self.list.range()
		if self.path not in self[0].path:
			for i in rangeList: self[i].path = self.path + self[i].path
		for i in rangeList:
			self[i].read()
			self[i].path = self[i].path.replace (self.path, "")

	def write (self):
		rangeList = self.list.range()
		if self.path not in self[0].path:
			for i in rangeList: self[i].path = self.path + self[i].path
		for i in rangeList:
			self[i].write()
			self[i].path = self[i].path.replace (self.path, "")

	def iterate (self, function):
		newList = Folder()
		for file in self.list:
			res = function (file)
			if res: newList.append (res)
		return newList

	def append (self, file):
		file.shortcut()
		file.path = file.path.replace (self.path, "")
		self.list.append (file)

	def __str__ (self):
		strList = 'Dossier: '+ self.path +'\nListe:'
		for file in self:
			file.toPath()
			strList = strList +'\n'+ file.path
		return strList

	def __setitem__ (self, pos, item):
		lenList = len (self.list)
		if type (pos) == int:
			if pos <0: pos += lenList
			if pos < lenList: self.list[pos] = item
			else: self.append (item)

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
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
			if pos <0: pos += lenList
			if pos > lenList or pos <0: return None
			else: return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
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
		"""
		self.rename ('built', 'dodo')
		self.move ('b/temp/')
		self.filter ('the')
	#	print (self)
		file = File ('fanfics/a doctor calls.txt')
		self.append (file)
		"""
		print (self)
		self[0].path = self.path + self[0].path
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

	def get (self, tagName=None, sens=True):
		tmpList = Folder (self.path)
		tmpList.get (tagName, sens)
		for file in tmpList.list:
			file.toPath()
			article = Article (file)
			article.fromPath()
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







