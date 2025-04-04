#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
import json
import listFct
import textFct
import htmlFct
from fileLocal import *
from fileTemplate import *
from htmlFromText import toHtml
import loggerFct as log

dateFormatFull = '%Y/%m/%d %H:%M:%S'
dateFormatDay = '%Y-%m-%d'
dateFormatHour = dateFormatDay + '-%H-%M'

def comparerText (textA, textB):
	textA = textA.replace ('\t'," ")
	textA = textFct.cleanBasic (textA)
	listA = textA.split ('\n')
	textB = textB.replace ('\t'," ")
	textB = textFct.cleanBasic (textB)
	listB = textB.split ('\n')
	listCommon = listFct.comparer (listA, listB)
	textCommon =""
	for line in listCommon:
		textCommon = textCommon +'\n'+ line[1] +'\t'+ line[0]
	return textCommon

class File():
	def __init__ (self, file =None):
		self.path =""
		self.title =""
		self.text =""
		if file:
			self.path = file
			self.fromPath()

	def comparer (self, fileB):
		# self et fileB sont ouverts
		title = 'b/comparer %s et %s.txt' %( self.title, fileB.title)
		fileCommon = File (title)
		if (self.path[:-4] == '.css' and fileB.path[:-4] == '.css') or (self.path[:-3] == '.js' and fileB.path[:-3] == '.js'):
			self.text = self.text.replace ('{',"")
			self.text = self.text.replace ('}',"")
			self.text = self.text.replace (';',"")
			fileB.text = fileB.text.replace ('{',"")
			fileB.text = fileB.text.replace ('}',"")
			fileB.text = fileB.text.replace (';',"")
		fileCommon.text = comparerText (self.text, fileB.text)
		fileCommon.write()

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
		self.path = self.path [:posS] +'\t'+ self.path [posE:]
	#	self.path = self.path.replace (self.title, '\t')

	def toPath (self):
		if '\t' in self.path:
			self.path = self.path.replace ('\t', self.title)
			self.path = shortcut (self.path)

	def remove (self):
		self.toPath()
		if os.path.exists (self.path): os.remove (self.path)

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
		chars = '/\\\t\n><'; c=0
		while chars != 'error' and c<6:
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

	def copy (self):
		newFile = File (self.path)
		newFile.title = self.title
		newFile.type = self.type
		return newFile

	def toMarkdown (self):
		self.text = textFct.toMarkdown (self.text)
		self.path = self.path.replace ('.txt', '.md')

	def readJson (self):
		if not self.text: self.read()
		self.replace ('\n')
		self.replace ('\t')
		self.replace (',]', ']')
		d= self.text.find ('{')
		f= self.text.rfind (';')
		self.text = self.text[d:f]
		jsonData = json.loads (self.text)
		return jsonData

	def divide (self):
		self.fromPath()
		self.text = textFct.shape (self.text)
		if len (self.text) < 420000: self.write()
		else:
			sep = '\n'
			if '============ ' in self.text: sep = '============ '
			elif '************ ' in self.text: sep = '************ '
			elif '<h1>' in self.text and self.text.count ('<h1>') >1: sep = '<h1>'
			elif '<h2>' in self.text: sep = '<h2>'

			newFile = self.copy()
			counter =1
			newFile.title = self.title +' %02d' % counter

			lines = self.text.split (sep)
			newFile.text = lines.pop (0)

			for line in lines:
				if len (newFile.text) >300000:
					newFile.write()
					counter +=1
					newFile = self.copy()
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

	def __setitem__ (self, pos, item):
		lenList = len (self.text)
		if type (pos) == int:
			itemStr = str (item)
			if len (itemStr) ==1:
				while pos <0: pos += lenList
				if pos < lenList: self.text[pos] = str (item)
				else: self.text = self.text + str (item)

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex[0], posIndex[1], posIndex[2])
			if type (item) in (tuple, list, str) and len (item) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = str (item[i])
					i+=1

	def __getitem__ (self, pos):
		lenList = len (self.text)
		if type (pos) == int:
			while pos <0: pos += lenList
			while pos >= lenList: pos -= lenList
			return self.text [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (lenList)
			rangeList = self.range (posIndex[0], posIndex[1], posIndex[2])
			newList =""
			for l in rangeList: newList = newList + self.text[l]
			return newList
		else: return None

	def __len__(self):
		return len (self.text)

	def find (self, word, posStart=0):
		pos =-1
		if word in self.text[posStart:]: pos = self.text.find (word, posStart)
		elif "'" in word:
			word = word.replace ("'",'"')
			if word in self.text[posStart:]: pos = self.text.find (word, posStart)
		elif '"' in word:
			word = word.replace ('"',"'")
			if word in self.text[posStart:]: pos = self.text.find (word, posStart)
		if pos >-1: pos += posStart
		return pos

	def rfind (self, word, posEnd=0):
		if posEnd <1: posEnd += len (self.text)
		pos =-1
		if word in self.text[:posEnd]: pos = self.text[:posEnd].rfind (word)
		elif "'" in word:
			word = word.replace ("'",'"')
			if word in self.text[:posEnd]: pos = self.text[:posEnd].rfind (word)
		elif '"' in word:
			word = word.replace ('"',"'")
			if word in self.text[:posEnd]: pos = self.text[:posEnd].rfind (word)
		return pos

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

class Article (File):
	# classe pour les fichiers txt et html
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.author =""
		self.subject =""
		self.link =""
		self.type =""
		self.meta ={}
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
			ficNew.type = self.type
			ficNew.path = self.path
			ficNew.meta = self.meta
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
				ficRange = listFct.rangeList (ficList)
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

	def metaToText (self):
		metaTemplate = '%s:\t%s\n'
		text =""
		for meta in self.meta: text = text + metaTemplate % (meta, self.meta[meta])
		return text

	def metaFromText (self, text):
		if 'style:\n' in text:
			text = text +'\n'
			d= text.find ('style:\n')
			f=1+ text.rfind ('}\n')
			if 'script:\n' in text[:f]:
				f= text.rfind ('script:\n')
				f=1+ text[:f].rfind ('}\n')
			self.meta['style'] = text[d+7:f]
			text = text[:d] + text[f:].strip()
		if 'script:\n' in text:
			text = text +'\n'
			d= text.find ('script:\n')
			e=1+ text.rfind ('}\n')
			f=1+ text.rfind (';\n')
			if e>f: f=e
			self.meta['script'] = text[d+8:f]
			text = text[:d] + text[f:].strip()
		textList = text.split ('\n')
		for line in textList:
			d= line.find (':\t')
			self.meta [line[:d]] = line[d+2:]

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] == 'xhtml': self.type = 'xhtml'
		elif self.path[-4:] == 'html': self.type = 'html'

	def read (self):
		File.read (self)
		metadata =[]
		self.text = textFct.cleanText (self.text)
		self.text = textFct.shape (self.text)
		self.text = self.text.strip()
		d= self.text.rfind ('\n======')
		metaText = self.text[d:].lower()
		metaText = metaText.replace (': ',':\t')
		metaText = metaText +'\n'
		self.text = self.text[:d]
		metadata = textFct.fromModel (metaText, templateTextMeta)
		self.subject = metadata[0]
		self.author = metadata[1]
		self.link = metadata[2]
		if len (metadata) >3:
			self.metaFromText (metadata[3])
			"""
			metaList = metadata[3].split ('\n')
			for meta in metaList:
				d= meta.find (':')
				self.meta[meta[:d]] = meta[d+2:]
			"""

	def write (self):
		self.title = self.title.lower()
		meta = self.metaToText()
		self.text = textFct.cleanText (self.text)
		self.text = textFct.shape (self.text, 'reset upper')
		self.text = templateText % (self.text, self.subject, self.author, self.link, meta)
		File.write (self, 'w')

	def copy (self):
		article = Article (self.path)
		article.subject = self.subject
		article.title = self.title
		article.type = self.type
		article.link = self.link
		article.author = self.author
		self.meta = self.meta
		return article

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
		self.text = htmlFct.toHtml (self.text)
		self.type = 'html'
		print ('text html\t', self.text)
		self.write()

class FileList (File):
	def __init__(self, file=None, sep='\n'):
		File.__init__(self, file)
		self.list =[]
		self.sep = sep
		self.length =0

	def write (self, upper=False):
		self.text = self.sep.join (self.list)
		if upper: self.text = textFct.shape (self.text, 'reset upper')
		else: self.text = textFct.shape (self.text, 'reset')
		File.write (self)

	def read (self):
		File.read (self)
		self.fromText()

	def toText (self):
		# self.text = listFct.toText (self.list, self.sep)
		self.text = self.sep.join (self.list)

	def fromText (self, text=None):
		if text: self.text = text
		while self.sep + self.sep in self.text: self.text = self.text.replace (self.sep + self.sep, self.sep)
		self.list = self.text.split (self.sep)
		self.length = len (self.list)

	def range (self, start=0, end=0, step=1):
		return listFct.rangeList (self.list, start, end, step)

	def iterate (self, function):
		return listFct.iterate (self.list, function)

	def __str__(self):
		self.text = self.sep.join (self.list)
		return self.path +'\n'+ self.text

	def __len__(self):
		self.length = len (self.list)
		return self.length

	def __setitem__ (self, pos, item):
		if type (pos) == int:
			if pos <0: pos += self.length
			if pos < self.length: self.list[pos] = item
			else: self.append (item)

		elif type (pos) == slice:
			posIndex = pos.indices (self.length)
			rangeList = range (posIndex [0], posIndex [1], posIndex [2])
			if type (item) in (tuple, list) and len (item) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = item[i]
					i+=1

	def __getitem__ (self, pos):
		if type (pos) == int:
			while pos <0: pos += self.length
			while pos >= self.length: pos -= self.length
			return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (self.length)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
			newList =[]
			for l in rangeList: newList.append (self.list[l])
			return newList
		else: return None

	def reverse (self):
		self.list.reverse()

	def append (self, item):
		self.list.append (item)
		self.length +=1

	def extend (self, liste):
		for item in liste: self.append (item)

	def insert (self, pos, item):
		while pos <0: pos += self.length
		self.list.insert (pos, item)
		self.length +=1

	def pop (self, pos):
		length = len (self.list)
		if pos <0: pos += self.len
		elif pos >= self.len: pos -= self.len
		trash = self.list.pop (pos)
		self.length -=1

	def replace (self, wordOld, wordNew):
		rfile = self.range()
		for l in self.range:
			if wordOld in self[l]: self[l] = self[l].replace (wordOld, wordNew)

class FileTable (FileList):
	def __init__(self, file=None, sep='\n', sepCol='\t'):
		FileList.__init__(self, file, sep)
		self.sepCol = sepCol
		self.lenCol =0

	def getByCol (self, pos, value):
		newTab = FileTable()
		newTab.path = self.path
		newTab.title = self.title +' bis'
		newTab.toPath()
		for line in self.list:
			if line[pos] == value: newTab.append (line)
		return newTab

	def getCol (self, ncol):
		rangeList = self.range()
		newList =[]
		for i in rangeList: newList.append (self.list[i][ncol])
		return newList

	def popCol (self, ncol):
		rangeList = self.range()
		for i in rangeList: trash = self.list[i].pop (ncol)
		self.lenCol -=1

	def addCol (self, item):
		typeItem = type (item)
		typeList = type (self.list[0][0])
		action = 'inconnu'
		# item est une liste de la même taille que la liste principale, une colonne. je rajoute un élément par ligne
		if typeItem in (list, tuple) and len (item) == self.length and typeList == type (item[0]): action = 'unique'
		# item est un objet simple, à rajouter partout
		elif typeItem == typeList: action = 'commun'
		if action in 'unique commun': self.lenCol +=1
		return action

	def appendCol (self, item):
		action = self.addCol (item)
		if action == 'unique':
			for l in rangeList: self.list[l].append (item[l])
		elif action == 'commun':
			for l in rangeList: self.list[l].append (item)

	def insertCol (self, pos, item):
		action = self.addCol (item)
		if action == 'unique':
			for l in rangeList: self.list[l].insert (pos, item[l])
		elif action == 'commun':
			for l in rangeList: self.list[l].insert (pos, item)

	def toText (self):
		newList =[]
		for line in self.list: newList.append (self.sepCol.join (line))
		self.text = self.sep.join (newList)

	def fromText (self, text=None):
		if text: self.text = text
		while self.sepCol + self.sepCol in self.text: self.text = self.text.replace (self.sepCol + self.sepCol, self.sepCol)
		FileList.fromText (self)
		rangeList = range (self.length)
		for l in rangeList: self.list[l] = self.list[l].split (self.sepCol)
		self.lenCol = len (self.list[0])

