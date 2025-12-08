#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
import json
from urllib import request as urlRequest
import pdfplumber
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

# ------ fonctions basiques ------

def decodeFileContent (textBrut):
	tmpByte = textBrut.read()
	encodingList = ('utf-8', 'ascii', 'ISO-8859-1', 'ISO8859-1')
	text =""
	for encoding in encodingList:
		try: text = codecs.decode (tmpByte, encoding=encoding)
		except UnicodeDecodeError: pass
		else: break
	if not text:
		for encoding in encodingList:
			try: text = codecs.decode (tmpByte, encoding=encoding, errors='ignore')
			except UnicodeDecodeError: pass
			else: break
	textBrut.close()
	return text

def fromFile (fileName):
	if not os.path.exists (fileName):
		print ("ce fichier n'existe pas:", fileName)
		return ""
	else:
		textBrut = open (fileName, 'rb')
		text = decodeFileContent (textBrut)
		return text

def toFile (fileName, text, mode='w'):
	if not text:
		print ('rien a ecrire pour:', fileName)
		return
	d=1+ fileName.rfind (os.sep)
	title = fileName[d:]
	chars = '/\\\t\n><';
	toWrite = True
	for c in chars:
		if c in title: toWrite = False
	if toWrite:
		if mode == 'a': text = '\n'+ text
		textBrut = open (fileName, mode +'b')
		textBrut.write (text.encode ('utf-8'))
		textBrut.close()
	else: print ('le titre du fichier est mal formé', title)

def fromUrl (url, params=None):
	text =""
	try:
		myRequest = None
		if params:
			paramsUrl = ul.parse.urlencode (params).encode ('utf-8')
			myRequest = urlRequest.Request (url, method='POST', headers={ 'User-Agent': 'Mozilla/5.0' })
		else: myRequest = urlRequest.Request (url, headers={ 'User-Agent': 'Mozilla/5.0' })
		textBrut = urlRequest.urlopen (myRequest)
		text = decodeFileContent (textBrut)
	except Exception as e:
		text =""
		print (e)
	if not text:
		try: urlRequest.urlretrieve (url, 'tmp.txt')
		except Exception as e: print (e)
		else:
			textBrut = open ('tmp.txt', 'rb')
			text = decodeFileContent (textBrut)
			os.remove ('tmp.txt')
	else: print ('la récupération à échoué, impossible de récupérer les données pour\n' + url)
	return text

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
		if (self.path[-4:] == '.css' and fileB.path[-4:] == '.css') or (self.path[-3:] == '.js' and fileB.path[-3:] == '.js'):
			toClean = '{}();"\''
			for item in toClean:
				self.text = self.text.replace (item,"")
				fileB.text = fileB.text.replace (item,"")
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
		self.text = fromFile (self.path)
		self.fromPath()

	def write (self, mode='w'):
		self.toPath()
		toFile (self.path, self.text, mode)

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
			if '== ' in self.text: sep = '== '
			elif '** ' in self.text: sep = '** '
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

	def toList (self, sep='\n'):
		if sep not in self.text: return []
		textTmp = self.text.replace (sep + sep, sep)
		while sep + sep in textTmp: textTmp = textTmp.replace (sep + sep, sep)
		textList = self.split (textTmp)
		return textList

	def fromList (self, textList, sep='\n'):
		if textList: self.text = sep.join (textList)

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

class FileCss (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.blocs =[]

	def toSelection (self, tagList=[]):
		text =""
		for bloc in self.blocs:
			if '*' in bloc[0] or ':root' in bloc[0] or 'body' in bloc[0] or 'html' in bloc[0]:
				text = text + bloc[0] +' { '+ bloc[1].replace (':', ': ') +'}\n'
		for tag in tagList:
			for bloc in self.blocs:
				if tag in bloc[0] and bloc[0] not in text:
					text = text + bloc[0] +' { '+ bloc[1].replace (':', ': ') +'}\n'
		text = text.replace (';', '; ')
		return text

	def read (self):
		File.read (self)
		self.text = self.text.replace ('\n'," ")
		self.text = self.text.replace ('\t'," ")
		self.text = self.text.replace ('\r'," ")
		self.cleanForStandarding()
		# supprimer les commentaires
		if '/*' in self.text:
			textList = self.text.split ('/*')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f=2+ textList[c].find ('*/')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)
			self.cleanForStandarding()
		# repérer les média queries
		if '@media' in self.text:
			textList = self.text.split ('@media')
			rangeList = range (1, len (textList))
			for c in rangeList:
				d= textList[c].find ('}')
				nOpening = textList[c][:d].count ('{')
				nClosing =1
				while nOpening > nClosing:
					d= textList[c].find ('}',d+1)
					nOpening = textList[c][:d].count ('{')
					nClosing =1+ textList[c][:d].count ('}')
				text = textList[c][:d].replace ('}',']]')
				text = text.replace ('{','[[')
				text = text.replace ('[[','{',1)
				textList[c] = text + textList[c][d:]
			self.text = '@media'.join (textList)
			self.cleanForStandarding()
		# créer les blocks
		textList = self.text.split ('}')
		trash = textList.pop (-1)
		rangeList = range (len (textList))
		for c in rangeList:
			textList[c] = textList[c].strip()
			textList[c] = textList[c].split ('{')
			if 2!= len (textList[c]): log.message (textList[c])
			textList[c][0] = textList[c][0].strip()
			textList[c][1] = textList[c][1].strip()
			textList[c][1] = textList[c][1].replace ('[[','{ ')
			textList[c][1] = textList[c][1].replace (']]','}')
			self.blocs.append (( textList[c][0], textList[c][1] ))

	def cleanForStandarding (self):
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		marquers ='{}:;'
		for mark in marquers:
			self.text = self.text.replace (" "+ mark, mark)
			self.text = self.text.replace (mark +" ", mark)

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
				if '** ' in self.text: sep = '** '
				elif '== ' in self.text: sep = '== '
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

	def fromPath (self):
		File.fromPath (self)
		if self.path[-3:] == 'txt': self.type = 'txt'
		elif self.path[-5:] == 'xhtml': self.type = 'xhtml'
		elif self.path[-4:] == 'html': self.type = 'html'

	def write (self):
		self.title = self.title.lower()
		meta = self.metaToText()
		self.text = textFct.cleanText (self.text)
		self.text = textFct.shape (self.text, 'reset upper')
		self.text = templateText % (self.text, self.subject, self.author, self.link, meta)
		File.write (self, 'w')

	def read (self):
		File.read (self)
		self.getMeta()

	def fromFile (self, fileObj):
		self.title = fileObj.title
		self.path = fileObj.path
		self.text = fileObj.text
		self.subject = 'o'
		self.author = 'o'
		self.link = 'o'
		if '\n==\n' in self.text and '\nSujet: ' in self.text: self.getMeta()

	def getMeta (self):
		metadata =[]
		self.text = textFct.cleanText (self.text)
		self.text = textFct.shape (self.text)
		self.text = self.text.strip()
		d= self.text.rfind ('\n==')
		metaText = self.text[d:].lower()
	#	metaText = metaText.replace (':\t',': ')
		metaText = metaText +'\n'
		self.text = self.text[:d]
		metadata = textFct.fromModel (metaText, templateTextMeta)
		self.subject = metadata[0]
		self.author = metadata[1]
		self.link = metadata[2]
		if len (metadata) >3: self.metaFromText (metadata[3])
		"""
			metaList = metadata[3].split ('\n')
			for meta in metaList:
				d= meta.find (':')
				self.meta[meta[:d]] = meta[d+2:]
		"""

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
			d= line.find (': ')
			self.meta [line[:d]] = line[d+2:]

	def metaToText (self):
		metaTemplate = '%s: %s\n'
		text =""
		for meta in self.meta: text = text + metaTemplate % (meta, self.meta[meta])
		return text

	def copy (self):
		article = Article (self.path)
		article.subject = self.subject
		article.title = self.title
		article.type = self.type
		article.link = self.link
		article.author = self.author
		self.meta = self.meta
		return article

	def fromPdf (self, getImg=True):
		# le fichier d'origine est un pdf, path.pdf. https://pypi.org/project/pdfplumber/#command-line-interface
		self.subject = 'o'
		self.author = 'o'
		self.toPath()
		self.link = self.path
		filePdf = pdfplumber.open (self.path)
		# pour chaque page, récupérer le texte
		self.path = self.path.replace ('.pdf', '.txt')
		for page in filePdf.pages:
			self.text = self.text +'\n/ img / page %02d\n' % page.page_number
			self.text = self.text + page.extract_text()
		# nettoyer le texte
		self.text = self.text.replace ('-\n', "")
		self.text = textFct.cleanText (self.text)
		midleChars = '?!:;,. -_abcdefghijklmnopqrstuvwxyz'
		for char in midleChars: self.text = self.text.replace ('\n'+ char, " "+ char)
		startChars = 'ABCDEFGIJKLMNOPQRSTUVWXYZ0123456789/\\-_0123456789'
		endChars = '?!:./\\0123456789'
		for char in startChars: self.text = self.text.replace ('\n'+ char, '\t'+ char)
		for char in endChars: self.text = self.text.replace (char +'\n', char +'\t')
		self.text = self.text.replace ('\n', " ")
		for char in startChars: self.text = self.text.replace ('\t'+ char, '\n'+ char)
		for char in endChars: self.text = self.text.replace (char +'\t', char +'\n')
		# pour chaque page, récupérer les images
		if getImg: self.fromPdfImg (filePdf.pages)
		else: self.text = self.text.replace ('/ img / ', '== ')
		# récupérer d'éventuelles métadonnées
		metaKeys = filePdf.metadata.keys()
		if 'subject' in metaKeys: self.subject = filePdf.metadata['subject']
		elif 'Subject' in metaKeys: self.subject = filePdf.metadata['Subject']
		elif 'sujet' in metaKeys: self.subject = filePdf.metadata['sujet']
		elif 'Sujet' in metaKeys: self.subject = filePdf.metadata['Sujet']
		if 'author' in metaKeys: self.author = filePdf.metadata['author']
		elif 'Author' in metaKeys: self.author = filePdf.metadata['Author']
		elif 'auteur' in metaKeys: self.author = filePdf.metadata['auteur']
		elif 'Auteur' in metaKeys: self.author = filePdf.metadata['Auteur']
		if 'ModDate' in metaKeys: self.meta['date'] = filePdf.metadata['ModDate']
		elif 'ModificationDate' in metaKeys: self.meta['date'] = filePdf.metadata['ModificationDate']
		elif 'CreationDate' in metaKeys: self.meta['date'] = filePdf.metadata['CreationDate']

	def fromPdfImg (self, pages):
		# créer un dossier pour contenir les éventuelles images. pages = filePdf.pages
		self.fromPath()
		i= self.path.find ('\t')
		imgPathShort = self.title + os.sep
		imgPath = self.path[:i] + imgPathShort
		if not os.path.exists (imgPath): os.mkdir (imgPath)
		images =[]
		# pour chaque page, récupérer les images
		for page in pages:
			images.append ("")
			for img in page.images:
				bbox = [img['x0'], page.cropbox[3] - img['y1'], img['x1'], page.cropbox[3] - img['y0']]
				if bbox[0] < page.cropbox[0]: bbox[0] = page.cropbox[0]
				if bbox[1] < page.cropbox[1]: bbox[1] = page.cropbox[1]
				if bbox[2] > page.cropbox[2]: bbox[2] = page.cropbox[2]
				if bbox[3] > page.cropbox[3]: bbox[3] = page.cropbox[3]
				imgPage = page.crop (bbox=bbox)
				imgObj = imgPage.to_image (resolution=100)
				imgNameShort = "%s%02d %s.png" % (imgPathShort, img['page_number'], img['name'])
				imgName = "%s%02d %s.png" % (imgPath, img['page_number'], img['name'])
				imgObj.save (imgName)
				images[-1] = images[-1] + imgNameShort +'\n'
		# rajouter les images dans le texte
		textList = self.text.split ('/ img / ')
		textRange = range (1, len (textList))
		for t in textRange: textList[t] = textList[t] + images[t-1]
		self.text = '== '.join (textList)

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
