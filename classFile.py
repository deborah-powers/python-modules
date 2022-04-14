#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
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

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] in ('.html', 'xhtml'): self.type = 'html'

	def read (self):
		File.read (self)
		if self.type == 'html':
			self.text = self.text.replace ('\n')
			self.text = self.text.replace ('\t')
			metadata = self.fromModel (templateHtml)
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

from classList import List

class Folder():
	def __init__ (self, path='b/'):
		if path: path = shortcut (path)
		self.path = path
		self.list = List()

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
					if '.' not in file: continue
					fileTmp = File (os.path.join (dirpath, file))
					fileTmp.fromPath()
					fileTmp.path = fileTmp.path.replace (self.path, "")
					self.list.append (fileTmp)
				self.list.sort()

	def filter (self, TagNomfile, sens=True):
		""" quand on a besoin de ré-exclure certains fichiers après le get.
		quand je veux exclure sur plusieurs mots-clefs """
		rangeFile = self.list.range()
		rangeFile.reverse()
		if sens:
			for f in rangeFile:
				if TagNomfile not in self.list[f].path and TagNomfile not in self.list[f].title: trash = self.list.pop(f)
		else:
			for f in rangeFile:
				if TagNomfile in self.list[f].path or TagNomfile in self.list[f].title: trash = self.list.pop(f)

	def iterate (self, function):
		rangeList = self.list.range()
		newList = Folder()
		for i in rangeList: newList.append (function (self.list[i]))
		return newList

	def append (self, file):
		file.shortcut()
		file.path = file.path.replace (self.path, "")
		self.list.append (file)


