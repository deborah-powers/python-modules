#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
import funcList
import funcText
from fileLocal import *
import funcLogger

class File():
	def __init__ (self, file =None):
		self.path = file
		self.title =""
		self.text =""
		if file: self.fromPath()

	def fromPath (self):
		if '\t' in self.path: return
		self.path = shortcut (self.path)
		if os.sep not in self.path or '.' not in self.path:
			print ('fichier malformé:\n' + self.path)
			return
		elif self.path.rfind (os.sep) > self.path.rfind ('.'):
			# print ('fichier malformé:\n' + self.path)
			return
		posS = self.path.rfind (os.sep) +1
		posE = self.path.rfind ('.')
		self.title = self.path [posS:posE]
		self.path = self.path.replace (self.title, '\t')

	def toPath (self):
		if '\t' in self.path:
			self.path = self.path.replace ('\t', self.title)
			self.path = shortcut (self.path)

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
		if text: self.text = text
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

	def replace (self, wordOld, wordNew=""):
		self.text = self.text.replace (wordOld, wordNew)

	def __str__ (self):
		strShow = 'Titre: %s' % self.title
		if self.text: strShow += '.\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		self.toPath()
		newFile.toPath()
		return self.path < newFile.path

	def __len__(self):
		return len (self.text)

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
		self.text = funcText.shape (self.text, 'reset')
		print (self.text[:200])
		self.write()

templateText ="""Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""

templateHtml = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_blank'>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='author' content='%s'/>
	<meta name='subject' content='%s'/>
	<meta name='link' content='%s'/>
	<meta name='autlink' content='%s'/>
	%s
</head><body>
%s
</body></html>"""

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
		article.path = self.path.replace ('.html', '.txt')
		article.title = self.title
		article.subject = self.subject
		article.type = 'txt'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.text = funcText.fromHtml (article.text)
		if '</' in article.text: return self
		else: return article

	def toHtml (self):
		if self.type == 'html': return self
		article = Article()
		article.text = self.text
		article.path = self.path.replace ('.txt', '.html')
		article.title = self.title
		article.subject = self.subject
		article.type = 'html'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.text = funcText.toHtml (article.text)
		if '</' in article.text: return article
		else: return self

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] in ('.html', 'xhtml'): self.type = 'html'

	def read (self):
		File.read (self)
		if self.type == 'html':
			"""
			self.text = self.text.replace ('\n', "")
			self.text = self.text.replace ('\t', "")
			"""
			metadata = funcText.fromModel (self.text, templateHtml)
			self.subject = metadata [2]
			self.author = metadata [1]
			self.link = metadata [3]
			self.autlink = metadata [4]
			if len (metadata) ==6: self.text = metadata [5]
			elif len (metadata) ==7: self.text = metadata [6]
		elif self.type == 'txt':
			metadata = funcText.fromModel (self.text, templateText)
			self.subject = metadata [0]
			self.author = metadata [1]
			self.link = metadata [2]
			self.autlink = metadata [3]
			self.text = metadata [4]

	def write (self):
		self.title = self.title.lower()
		if self.type == 'html': self.text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, "", self.text)
		elif self.type == 'txt': self.text = templateText % (self.subject, self.author, self.link, self.autlink, self.text)
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
		self.text = funcText.toHtml (self.text)
		self.type = 'html'
		print ('text html\t', self.text)
		self.write()

class FileList (File):
	def __init__(self, file=None, sep='\n'):
		File.__init__(self, file)
		self.list =[]
		self.sep = sep

	def write (self):
		self.toText()
		File.write (self)

	def read (self):
		File.read (self)
		self.text = funcText.clean (self.text)
		self.fromText()

	def toText (self):
		# self.text = funcList.toText (self.list, self.sep)
		self.text = self.sep.join (self.list)

	def fromText (self, text=None):
		if text: self.text = text
		self.list = self.text.split (self.sep)

	def range (self, start=0, end=0, step=1):
		return funcList.range (self.list, start, end, step)

	def iterate (self, function):
		return iterate (self.list, function)

	def __str__(self):
		self.toText()
		return self.path +'\n'+ self.text

	def __len__(self):
		return len (self.list)

	def __setitem__ (self, pos, item):
		lenList = len (self.list)
		if type (pos) == int:
			if pos <0: pos += lenList
			if pos < lenList: self.list[pos] = item
			else: self.append (item)

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = range (posIndex [0], posIndex [1], posIndex [2])
			if type (item) in (tuple, list) and len (item) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = item[i]
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
			newList =[]
			for l in rangeList: newList.append (self.list[l])
			return newList
		else: return None

	def append (self, item):
		self.list.append (item)

	def extend (self, liste):
		for item in liste: self.append (item)

	def reverse (self):
		self.list.reverse()

	def pop (self, pos):
		length = len (self.list)
		if pos <0: pos += length
		elif pos >= length: pos -= length
		trash = self.list.pop (pos)

class FileTable (FileList):
	def __init__(self, file=None, sep='\n', sepCol='\t'):
		FileList.__init__(self, file, sep)
		self.sepCol = sepCol

	def toText (self):
		newList =[]
		for line in self.list: newList.append (self.sepCol.join (line))
		self.text = self.sep.join (newList)

	def fromText (self, text=None):
		if text: self.text = text
		newList = self.text.split (self.sep)
		for line in newList: self.append (line.split (self.sepCol))
