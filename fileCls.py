#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
import listFct
import textFct
from fileLcl import *
import loggerFct

class File():
	def __init__ (self, file =None):
		self.path =""
		self.title =""
		self.text =""
		if file:
			self.path = file
			self.fromPath()

	def renameDate (self):
		months =( '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
		days =( '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
		if '2021' in self.title or '2022' in self.title or '2023' in self.title:
			self.fromPath()
			newPath = self.title.lower()
			newPath = newPath.replace ('img_20', '20')
			newPath = newPath.replace ('vid_20', '20')
			newPath = newPath.replace ('video_20', '20')
			newPath = newPath.replace ('20210', '2021-0')
			newPath = newPath.replace ('20211', '2021-1')
			newPath = newPath.replace ('20220', '2022-0')
			newPath = newPath.replace ('20221', '2022-1')
			newPath = newPath.replace ('20230', '2023-0')
			newPath = newPath.replace ('20231', '2023-1')
			for m in months: newPath = newPath.replace ('-'+m, '-'+m+'-')
			for d in days: newPath = newPath.replace ('-'+d, '-'+d+' ')
			while '--' in newPath: newPath = newPath.replace ('--', '-')
			newPath = newPath.replace ('_', ' ')
			newPath = newPath.replace ('- ', ' ')
			newPath = newPath.replace (' -', '-')
			while '  ' in newPath: newPath = newPath.replace ('  ', ' ')
			newPath = self.path.replace ('\t', newPath)
			self.toPath()
			os.rename (self.path, newPath)

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

	def toMarkdown (self):
		self.text = textFct.toMarkdown (self.text)
		self.path = self.path.replace ('.txt', '.md')

	def divide (self):
		if len (self.text) < 420000: return
		self.fromPath()
		newFile = File (self.path)
		counter =1
		newFile.title = self.title +' %02d' % counter
		self.text = textFct.shape (self.text)

		sep = '\n'
		if '============ ' in self.text: sep = '============ '
		elif '************ ' in self.text: sep = '************ '
		elif '<h1>' in self.text and self.text.count ('<h1>') >1: sep = '<h1>'
		elif '<h2>' in self.text: sep = '<h2>'

		lines = self.text.split (sep)
		newFile.text = lines.pop (0)

		for line in lines:
			if len (newFile.text) >300000:
				newFile.write()
				counter +=1
				newFile = File (self.path)
				newFile.title = self.title +' %02d' % counter
			newFile.text = newFile.text + sep + line
		newFile.write()

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
		self.text = textFct.shape (self.text, 'reset')
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

templateXhtml ="""<?xml version='1.0' encoding='utf-8'?>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='fr'>
<head>
	<title>%s</title>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<link rel='stylesheet' type='text/css' href='/var/www/html/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='/var/www/html/site-dp/library-css/perso.css' media='screen'/>
	<link rel='stylesheet' type='text/css' href='../liseuse.css'/>
	<meta name='author' content='%s'/>
	<meta name='subject' content='%s'/>
	<meta name='link' content='%s'/>
	<meta name='autlink' content='%s'/>
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
		if file: self.fromPath()

	def explode (self):
		# découper une trop longue fanfic en morceaux
		if len (self.text) > 450000:
			# créer l'article temporaire
			idFile =1
			idText =0
			ficNew = Article()
			ficNew.subject = self.subject
			ficNew.link = self.link
			ficNew.author = self.author
			ficNew.autlink = self.autlink
			ficNew.type = self.type
			ficNew.path = self.path
			ficNew.text =""
			# récupérer le séparateur selon le type de l'article
			sep = ""
			if '<h1>' in self.text: sep = '<h1>'
			elif self.type == 'txt':
				self.text = textFct.clean (self.text)
				if '****** ' in self.text: sep = '****** '
				elif '====== ' in self.text: sep = '====== '
			if sep:
				ficList = self.text.split (sep)
				if not ficList[0]: trash = ficList.pop (0)
				ficRange = listFct.range (ficList)
				for f in ficRange:
					ficNew.text = ficNew.text + sep + ficList[f]
					if len (ficNew.text) >= 300000:
						idText =f
						ficNew.path = self.path
						ficNew.title = self.title +' '+ str (idFile)
						ficNew.write()
						ficNew.text =""
						idFile = idFile +1
				idText = idText +1
				self.text = sep.join (ficList[idText:])
				self.text = sep + self.text
				self.title = self.title +' '+ str (idFile)
				self.write()

	def toText (self):
		if self.type == 'txt': return self
		article = Article()
		article.text = self.text
		article.path = self.path.replace ('.html', '.txt')
		if self.type == 'xhtml': article.path = self.path.replace ('.xhtml', '.txt')
		article.title = self.title
		article.subject = self.subject
		article.type = 'txt'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.text = textFct.fromHtml (article.text)
		if '</' in article.text: return self
		else: return article

	def toHtml (self):
		if self.type in 'xhtml': return self
		article = Article()
		article.text = self.text
		article.path = self.path.replace ('.txt', '.html')
		article.title = self.title
		article.subject = self.subject
		article.type = 'html'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.text = textFct.toHtml (article.text)
		if '</' in article.text: return article
		else: return self

	def toXhtml (self):
		article = self.toHtml()
		article.path = article.path.replace ('.html', '.xhtml')
		article.type = 'xhtml'
		return article

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] == 'xhtml': self.type = 'xhtml'
		elif self.path[-4:] == 'html': self.type = 'html'

	def read (self):
		File.read (self)
		if self.type == 'html':
			"""
			self.text = self.text.replace ('\n', "")
			self.text = self.text.replace ('\t', "")
			"""
			metadata = textFct.fromModel (self.text, templateHtml)
			self.author = metadata[1]
			self.subject = metadata[2]
			self.link = metadata[3]
			self.autlink = metadata[4]
			self.text = metadata[6]
		elif self.type == 'xhtml':
			metadata = textFct.fromModel (self.text, templateXhtml)
			self.author = metadata[1]
			self.subject = metadata[2]
			self.link = metadata[3]
			self.autlink = metadata[4]
			self.text = metadata[5]
		elif self.type == 'txt':
			metadata = textFct.fromModel (self.text, templateText)
			self.subject = metadata[0]
			self.author = metadata[1]
			self.link = metadata[2]
			self.autlink = metadata[3]
			self.text = metadata[5]

	def write (self):
		self.title = self.title.lower()
		if self.type == 'html': self.text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, "", self.text)
		elif self.type == 'xhtml': self.text = templateXhtml % (self.title, self.author, self.subject, self.link, self.autlink, self.text)
		elif self.type == 'txt': self.text = templateText % (self.subject, self.author, self.link, self.autlink, self.text)
		File.write (self, 'w')

	def copy (self):
		article = Article (self.path)
		article.subject = self.subject
		article.title = self.title
		article.type = self.type
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		return article

	def divide (self):
		if len (self.text) < 420000: return
		self.fromPath()
		article = self.copy()
		counter =1
		article.title = self.title +' %02d' % counter
		self.text = textFct.shape (self.text)

		sep = '\n'
		if '============ ' in self.text: sep = '============ '
		elif '************ ' in self.text: sep = '************ '
		elif '<h1>' in self.text and self.text.count ('<h1>') >1: sep = '<h1>'
		elif '<h2>' in self.text: sep = '<h2>'

		lines = self.text.split (sep)
		article.text = lines.pop (0)

		for line in lines:
			if len (article.text) >300000:
				article.write()
				counter +=1
				article = self.copy()
				article.title = self.title +' %02d' % counter
			article.text = article.text + sep + line
		article.write()

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
		self.text = textFct.toHtml (self.text)
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
	#	self.text = textFct.clean (self.text)
		self.fromText()

	def toText (self):
		# self.text = listFct.toText (self.list, self.sep)
		self.text = self.sep.join (self.list)

	def fromText (self, text=None):
		if text: self.text = text
		self.list = self.text.split (self.sep)

	def range (self, start=0, end=0, step=1):
		return listFct.range (self.list, start, end, step)

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

	def delCol (self, ncol):
		rangeList = self.range()
		for i in rangeList: trash = self.list[i].pop (ncol)

	def toText (self):
		newList =[]
		for line in self.list: newList.append (self.sepCol.join (line))
		self.text = self.sep.join (newList)

	def fromText (self, text=None):
		if text: self.text = text
		newList = self.text.split (self.sep)
		for line in newList: self.append (line.split (self.sepCol))
