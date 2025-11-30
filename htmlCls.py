#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
import os
import urllib as ul
from urllib import request as urlRequest
import codecs
from fileLocal import pathDesktop, pathCard
import textFct
import htmlFct
from fileCls import File, Article, FileCss
from fileTemplate import templateHtml, templateHtmlEreader
from htmlToText import fromHtml
from htmlFromText import toHtml
import loggerFct as log

listTags = htmlFct.listTagsIntern + ( 'a', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'tr', 'caption', 'label', 'button', 'textarea', 'figcaption' ) + htmlFct.listTagsContainer
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta', 'link', 'base' )
listAttributes =( 'href', 'src', 'alt', 'colspan', 'rowspan', 'value', 'type', 'name', 'id', 'class', 'method', 'content', 'onclick', 'ondbclick' )
listTagsLocal =[]

# ________________________ auxilières ________________________

def cleanTitle (title):
	title = title.lower()
	charToErase = '-_.:;,?/\\|'
	for char in charToErase: title = title.replace (char," ")
	title = textFct.cleanBasic (title)
	return title

def getAttribute (text, attrName):
	# récupérer un attribut d'un texte tranformé par getFromPos
	if '>' in text:
		f= text.find ('>')
		text = text[:f]
	if attrName +'=' not in text: return ""
	else:
		d=1+ len (attrName) + text.find (attrName +'=')
		f= text.find (text[d], d+1)
		return text[d+1:f]

def getInnerHtml (text):
	# récupérer le innerHtml d'un texte tranformé par getFromPos
	# if text[:2] == 'a ': return getAttribute (text, 'href')
	if text[:4] == 'img ': return getAttribute (text, 'src')
	elif text[:6] == 'input ': return getAttribute (text, 'value')
	elif '>' not in text: return ""
	else:
		d=1+ text.find ('>')
		return text[d:]

def endFromPos (text, pos, tagName=""):
	""" pos est la postion de <tag ...
	renvoyer la position après la balise fermante
	<tag attr='value'>content</tag>posRenvoyee
	ou
	<img src='path.img'/>posRenvoyee
	"""
	# retrouver le tag
	if not tagName:
		f= text.find ('>', pos)
		if " " in text[pos:f]: f= text.find (" ", pos)
		tagName = text[pos +1:f]
	# tag auto-fermant
	if tagName in listTagsSelfClosing: return 1+ text.find ('>', pos)
	# erreur, pas de tag fermant
	elif '</'+ tagName +'>' not in text[pos:]: return -1
	# une seule occurence du tag
	elif text.count ('</'+ tagName +'>') ==1: return 3+ len (tagName) + text.find ('</'+ tagName +'>')
	# plusieurs tags similaires. retrouver la balise fermante associé au mien
	else:
		tagStart = '<'+ tagName
		tagEnd = '</'+ tagName +'>'
		# if text.count (tagStart) != text.count (tagEnd): log.logLst ('pas assez de tag', tagName)
		f= text.find (tagEnd, pos)
		nbEnd =1
		nbStart = text[pos:f].count (tagStart)
		lenText = len (text) -3
		while nbEnd < nbStart and tagEnd in text[f+3:]:
			f= text.find (tagEnd, f+3)
			nbStart = text[pos:f].count (tagStart)
			nbEnd = nbEnd +1
		if f<0: return -1
		else: return f+3+ len (tagName)

def singleChild (text):
	""" vérifier si le texte transformé par getFromPos ne contient qu'un seul enfant
	que faire avec les tables encapsulées, celles contenant thead et tbody ?
	"""
	if '>' not in text or 'svg' == text[:3]: return text
	d= text.find ('>')
	if " " in text[:d]: d= text.find (" ")
	if text[:d] in listTagsSelfClosing: return text
	d=1+ text.find ('>')
	if len (text) ==d or text[d] != '<': return text
	elif len (text) > endFromPos (text, d): return text
	tagStart = text[:d]
	d=1+ text.find ('>', d)
	f= text.rfind ('<')
	if d>f:
		# tag auto-fermant à l'intérieur
		if 'a' == tagStart[0] and tagStart[1] in "> ": return text
		elif tagStart[:2] in ('td', 'th', 'li') and tagStart[2] in "> ": return text
		else:
			d=2+ text.find ('><')
			text = text[d:-1]
			if '/' == text[-1]: text = text[:-1]
			return text
	elif tagStart[:5] != 'table' and tagStart[:2] not in ('a ', 'tr', 'ul', 'ol', 'dl'):
		c= 1+ len (tagStart)
		if text[c:c+2] in ('a ', 'tr', 'th', 'td') or text[c:c+5] == 'table': tagStart = text[c:d]
		text = tagStart + text[d:f]
		text = singleChild (text)
		return text
	else: return text

def getFromPos (text, pos):
	""" pos est la postion de <tag ...
	renvoi tag attr='value'>content
	ou
	img src='path.img'
	"""
	# retrouver le tag
	f= text.find ('>', pos)
	if " " in text[pos:f]: f= text.find (" ", pos)
	tagName = text[pos+1:f]
	f= endFromPos (text, pos, tagName)
	pos +=1
	f-=1
	# erreur, pas de tag fermant
	if f<1: return ""
	# tag auto-fermant
	elif tagName in listTagsSelfClosing or '>' not in text[pos:f]:
		if text[f-1] =='/': f-=1
		return text[pos:f]
	# tag avec du innerHtml
	elif tagName in listTags or tagName in listTagsLocal:
		f= text[:f].rfind ('<')
		return singleChild (text[pos:f])
	# cas inconnu, erreurs
	else:
		print ('erreur pour:', tagName, pos, f)
		return text

def simplifyNesting (text):
	if '<' not in text or '>' not in text: return text
	d=0
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	while '<' in text[d:]:
		d= text.find ('<', d)
		f= text.find ('>', d)
		if text[d+1] in alphabet and text[f-1] != '/':
			if text[d+1:f] not in listTagsSelfClosing:
				f= endFromPos (text, d)
				f= text[:f].rfind ('<')
				textBis = getFromPos (text, d)
				if ""== textBis: f=1+ text.find ('<',d+1)
				# gérer les tableaux imbriqués dans un conteneur
				elif textBis[0] != text[f+2]:
					c=1+ textBis.find ('>')
					textBis = textBis +'</'+ textBis[:c]
					f=1+ text.find ('>', f+1)
				text = text[:d] +'<'+ textBis + text[f:]
		d+=1
	return text

def getOneByTag (text, tagName):
	if '<'+ tagName not in text: return ""
	d= text.find ('<'+ tagName)
	return getFromPos (text, d)

def getOneById (text, tagId):
	if tagId not in text or 'id=' not in text: return ""
	textBis = text.replace ('"',"'")
	if "id='"+ tagId +"'" not in textBis: return ""
	d= textBis.find ("id='"+ tagId +"'")
	d= textBis[:d].rfind ('<')
	return getFromPos (text, d)

def getOneByClass (text, className):
	if className not in text or 'class=' not in text: return ""
	lenText = len (text)
	index =-1
	d=0
	while d< lenText and className in text[d:] and 'class=' in text[d:]:
		d=6+ text.find ('class=', d)
		f= text.find (text[d], d+1)
		if className in text[d:f]:
			index = text[:d].rfind ('<')
			d=1+ lenText
	if index ==-1: return ""
	else: return getFromPos (text, index)

def getOneByTagClass (text, tagName, className):
	if '<'+ tagName +" " not in text or className not in text or 'class=' not in text: return ""
	lenText = len (text)
	index =-1
	d=0
	while d< lenText and '<'+ tagName +" " in text[d:] and 'class=' in text[d:] and className in text[d:]:
		d=7+ text.find ('class=', d)
		f= text.find (text[d-1], d)
		# if className in text[d:f]:
		if className == text[d:f] or " "+ className +" " in text[d:f]:
			index = text[:d].rfind ('<')
			if tagName == text [index +1:d-8]: d=1+ lenText
		elif className in text[d:f]:
			classLen =1+ len (className)
			if text[d:d+ classLen] == className +" " or text[f- classLen:f] == " "+ className:
				index = text[:d].rfind ('<')
				if tagName == text[index +1:d-8]: d=1+ lenText
	if index ==-1: return ""
	else: return getFromPos (text, index)

def getOneByAttribute (text, attrName, attrValue):
	if attrValue not in text or attrName +'=' not in text: return ""
	textBis = text.replace ('"',"'")
	if attrName +"='"+ attrValue +"'" not in textBis: return ""
	d= textBis.find (attrName +"='"+ attrValue +"'")
	d= textBis[:d].rfind ('<')
	return getFromPos (text, d)

def getAllByTag (text, tagName):
	if '<'+ tagName not in text: return []
	tagList =[]
	while '<'+ tagName in text:
		d= text.find ('<'+ tagName)
		tagList.append (getFromPos (text, d))
		text = text[d+1:]
	return tagList

def getAllByClass (text, className):
	if className not in text or 'class=' not in text: return []
	# repérer les tags intéressants
	textBis = text.replace ('"',"'")
	textList = textBis.split ('class=')
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ("'")
		if className in textList[t][:f]:
			d= textList[t-1].rfind ('<')
			textList[t-1] = textList[t-1][:d] +'$'+ textList[t-1][d:]
		t+=1
	textBis = textList.join ('class=')
	# récupérer les tags
	tagList =[]
	while '$<' in textBis:
		d= textBis.find ('$<')
		tagList.append (getFromPos (text, d))
		textBis = textBis.replace ('$<', '<', 1)
	return tagList

def getAllByTagClass (text, tagName, className):
	if '<'+ tagName +" " not in text or className not in text or 'class=' not in text: return []
	# repérer les tags intéressants
	textBis = text.replace ('"',"'")
	textList = textBis.split ('<'+ tagName +" ")
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ('>')
		if 'class=' in textList[t][:f]:
			d=7+ textList[t].find ('class=')
			f= textList[t].find ("'",d)
			if className in textList[t][d:f]:
				d= textList[t-1].rfind ('<')
				textList[t-1] = textList[t-1][:d] +'$'+ textList[t-1][d:]
		t+=1
	textJoin = '<'+ tagName +" "
	textBis = textJoin.join (textList)
	# récupérer les tags
	tagList =[]
	while '$<' in textBis:
		d= textBis.find ('$<')
		tagList.append (getFromPos (text, d))
		textBis = textBis.replace ('$<', '<', 1)
	return tagList

def getAllByAttribute (text, attrName, attrValue):
	if attrValue not in text or attrName +'=' not in text: return []
	# repérer les tags intéressants
	textBis = text.replace ('"',"'")
	textList = textBis.split (attrName +"='")
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ("'",d)
		if attrValue in textList[t][:f]:
			d= textList[t-1].rfind ('<')
			textList[t-1] = textList[t-1][:d] +'$'+ textList[t-1][d:]
		t+=1
	textJoin = attrName +"='"
	textBis = textJoin.join (textList)
	# récupérer les tags
	tagList =[]
	while '$<' in textBis:
		d= textBis.find ('$<')
		tagList.append (getFromPos (text, d))
		textBis = textBis.replace ('$<', '<', 1)
	return tagList

class Html (Article):
	def __init__ (self, file =None):
		Article.__init__ (self)
		self.meta ={}
		self.link =""

		if file and file[:4] == 'http':
			file = file.replace ('!', '&')
			self.link = file
			self.path = 'b/tmp.html'
			self.fromPath()
			self.fromUrl()
		elif file:
			self.path = file
			self.fromPath()
		#	self.read()

	# ________________________ récupérer les noeuds d'intérêt ________________________

	def getOneByTag (self, tagName):
		return getOneByTag (self.text, tagName)
	def getOneByClass (self, className):
		return getOneByClass (self.text, className)
	def getOneById (self, index):
		return getOneById (self.text, index)
	def getOneByTagClass (self, tagName, className):
		return getOneByTagClass (self.text, tagName, className)
	def getOneByAttribute (self, attributeName, attributeValue):
		return getOneByAttribute (self.text, attributeName, attributeValue)
	def getAllByTag (self, tagName):
		return getAllByTag (self.text, tagName)
	def getAllByClass (self, className):
		return getAllByClass (self.text, className)
	def getAllByTagClass (self, tagName, className):
		return getAllByTagClass (self.text, tagName, className)
	def getAllByAttribute (self, attributeName, attributeValue):
		return getAllByAttribute (self.text, attributeName, attributeValue)

	def setByTag (self, tagName):
		tagStr = getOneByTag (self.text, tagName)
		self._setOne (tagStr)
	def setById (self, index):
		tagStr = getOneById (self.text, index)
		self._setOne (tagStr)
	def setByClass (self, className):
		tagStr = getOneByClass (self.text, className)
		self._setOne (tagStr)
	def setByTagClass (self, tagName, className):
		tagStr = getOneByTag (self.text, tagName, className)
		self._setOne (tagStr)
	def setByAttribute (self, attributeName, attributeValue):
		tagStr = getOneByAttribute (self.text, attributeName, attributeValue)
		self._setOne (tagStr)

	def _setOne (self, tagStr):
		if not tagStr: return
		# balise ouvrante
		elif '>' in tagStr:
			d=1+ tagStr.find ('>')
			self.text = tagStr[d:]
		# balise auto-fermante
		else:
			tagStr = tagStr +'/>'
			self.text = tagStr

	def _setByTagSimple (self, tagName):
		if '</'+ tagName +'>' not in self.text or self.text.count ('</'+ tagName +'>') >1: return
		d= self.text.find ('<'+ tagName)
		d=1+ self.text.find ('>',d)
		f= self.text.find ('</'+ tagName +'>', d)
		self.text = self.text[d:f]

	def setByHtml (self):
		self._setByTagSimple ('html')
	def setByBody (self):
		self._setByTagSimple ('body')
	def setByMain (self):
		self._setByTagSimple ('main')
		self.setById ('main')
		self._setByTagSimple ('article')

	# ________________________ finir la lecture, préparer l'écriture ________________________

	def getAttribute (self, attrName):
		return getAttribute (self.text, attributeName)

	def setTitle (self):
		if '</title>' in self.text: self.title = cleanTitle (self.getOneByTag ('title'))
		elif '</h1>' in self.text: self.title = cleanTitle (self.getOneByTag ('h1'))
		d=1+ self.title.find ('>')
		self.title = self.title[d:]

	def simplifyNesting (self):
		self.text = simplifyNesting (self.text)

	def delIcons (self):
		# les balises ont encore leurs attributs et leurs classes
		iconWords =( 'icon', 'icone', 'logo', 'emoji' )
		endingLetters = '/ "\''
		# les images
		textList = self.text.split ('<img ')
		textRange = range (1, len (textList))
		for i in textRange:
			f= textList[i].find ('>')
			isIcon = False
			for word in iconWords:
				for letter in endingLetters:
					if word + letter in textList[i][:f]: isIcon = True
			if isIcon: textList[i] = textList[i][f+1:]
			else: textList[i] = '<img '+ textList[i]
		self.text = "".join (textList)
		# les span
		textList = self.text.split ('<span ')
		textRange = range (1, len (textList))
		for i in textRange:
			f= textList[i].find ('</span>')
			isIcon = False
			for word in iconWords:
				for letter in endingLetters:
					if word + letter in textList[i][:f]: isIcon = True
			if isIcon: textList[i] = textList[i][f+7:]
			else: textList[i] = '<span '+ textList[i]
		self.text = "".join (textList)

	def findTagsLocals (self):
		text = self.text.strip()
		for tag in listTags:
			text = text.replace ('</'+ tag +'>', '$')
			text = text.replace ('<'+ tag +'>', '$')
			text = text.replace ('<'+ tag +" ", '$ ')
		for tag in listTagsSelfClosing:
			text = text.replace ('</'+ tag +'>', '$')
			text = text.replace ('<'+ tag +'>', '$')
			text = text.replace ('<'+ tag +" ", '$ ')
		textList = text.split ('</')
		for line in textList[1:]:
			if line[0] in 'abcdefghijklmnopqrstuvwxyz' and '>' in line:
				f= line.find ('>')
				if line[:f] not in listTagsLocal:
					listTagsLocal.append (line[:f])
					text = text.replace ('</'+ line[:f] +'>', '$')
					text = text.replace ('<'+ line[:f] +'>', '$')
					text = text.replace ('<'+ line[:f] +" ", '$ ')
		textList = text.split ('<')
		for line in textList[1:]:
			if line[0] in 'abcdefghijklmnopqrstuvwxyz' and '>' in line and " " in line:
				f= line.find ('>')
				if " " in line[:f]: f= line.find (" ")
				if line[:f] not in listTagsLocal:
					listTagsLocal.append (line[:f])
					text = text.replace ('<'+ line[:f] +'>', '$')
					text = text.replace ('<'+ line[:f] +" ", '$ ')

	def setMetas (self):
		if '<meta ' not in self.text and '<link ' not in self.text: return
		metaList = getAllByTag (self.text, 'meta')
		self.meta ={}
		for meta in metaList:
			if 'csrf-' in meta or 'content=' not in meta or 'viewport' in meta: continue
			elif 'og:url' in meta:
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d+1)
				self.link = meta[d+1:f]
			elif 'name' in meta:
				d=5+ meta.find ('name=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]
			elif 'property' in meta:
				d=9+ meta.find ('property=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]
		metaList = getAllByTag (self.text, 'link')
		for meta in metaList:
			if 'rel="canonical"' in meta or "rel='canonical" in meta:
				d=5+ meta.find ('href=')
				f= meta.find (meta[d], d+1)
				self.link = meta[d+1:f]
			elif 'stylesheet' not in meta and 'icon' not in meta:
				d=4+ meta.find ('rel=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=5+ meta.find ('href=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]
		if 'link' in self.meta: self.link = self.meta.pop ('link')
		elif 'lien' in self.meta: self.link = self.meta.pop ('lien')
		if 'subject' in self.meta: self.subject = self.meta.pop ('subject')
		elif 'sujet' in self.meta: self.subject = self.meta.pop ('sujet')
		if 'author' in self.meta: self.author = self.meta.pop ('author')
		elif 'auteur' in self.meta: self.author = self.meta.pop ('auteur')

	def getMetas (self):
		metaTemplate = "<meta name='%s' content='%s'/>"
		cssTemplate = "<link rel='stylesheet' type='text/css' href='%s'/>"
		jsTemplate = "<script type='text/javascript' src='%s'></script>"
		styleTemplate = "<style type='text/css'>%s</style>"
		scriptTemplate = "<script type='text/javascript'>%s</script>"
		text =""
		metaKeys = self.meta.keys()
		for meta in metaKeys:
			if meta not in 'css js style script subject author link': text = text + metaTemplate % (meta, self.meta[meta])
		if 'css' in metaKeys: text = text + (cssTemplate % self.meta.pop ('css'))
		if 'js' in metaKeys: text = text + (jsTemplate % self.meta.pop ('js'))
		if 'style' in metaKeys: text = text + (styleTemplate % self.meta.pop ('style'))
		if 'script' in metaKeys: text = text + (scriptTemplate % self.meta.pop ('script'))
		return text

	# ________________________ lire et écrire dans un fichier html ________________________

	def toText (self):
		# if '</a>' in self.text or '<img' in self.text: return None
		self.replace ('\n')
		self.replace ('\t')
		article = Article()
		self.replace (" class='arrow'>", '>--> ')
		self.delAttributes()
		article.text = fromHtml (self.text)
		if '</' in article.text:
		#	print (article.text)
			d= article.text.find ('</')
			log.log ('présence de balise html', article.text.count ('</'), article.text[d-6:d+8])
			return None
		article.path = self.path.replace ('.html', '.txt')
		if self.type == 'xhtml': article.path = self.path.replace ('.xhtml', '.txt')
		article.type = 'txt'
		article.title = self.title
		article.subject = self.subject
		article.author = self.author
		article.link = self.link
	#	if 'link' in self.meta.keys(): article.link = self.meta['link']
		keys = self.meta.keys()
		for key in keys: article.meta[key] = self.meta[key]
		return article

	def fromText (self, fileTxt):
		self.text = toHtml (fileTxt.text)
		self.title = fileTxt.title
		self.path = fileTxt.path.replace ('.txt', '.html')

	def fromArticle (self, article):
		self.fromText (article)
		self.subject = article.subject
		self.author = article.author
		self.link = article.link
		keys = article.meta.keys()
		for key in keys: self.meta[key] = article.meta[key]

	def read (self):
		File.read (self)
		self.cleanBody()

	def read_va (self):
		File.read (self)
		metadata = textFct.fromModel (textTmp, templateHtml)
		self.subject = metadata[1].strip()
		self.author = metadata[2].strip()
		self.link = metadata[3].strip()
		self.metaFromHtml (metadata[4].strip())
		"""
		if '</script>' in metadata[6]: print ('la page contient du code js, qui est peut-être modifié par la mise en forme')
		self.text = metadata[6].strip()
		"""
		f= self.text.rfind ('</body>')
		self.text = self.text[:f]
		f= self.text.find ('<body')
		f=1+ self.text.find ('>',f)
		self.text = self.text[f:]
		self.cleanBody()

	def addIndentation (self):
		if '</xmp>' in self.text:
			while '\n\n' in self.text: self.text = self.text.replace ('\n\n', '\n')
			while '\t\t' in self.text: self.text = self.text.replace ('\t\t', '\t')
			self.text = self.text.replace ('\t\n', '\n')
		else:
			self.replace ('\n'," ")
			self.replace ('\t'," ")
		self.text = textFct.simpleSpace (self.text)
		self.replace ("> ",'>')
		self.replace (" <",'<')
		# rajouter les espaces autour des balises internes
		for tag in htmlFct.listTagsIntern:
			self.replace ('<'+ tag +'>', ' <'+ tag +'>')
			self.replace ('</'+ tag +'>', '</'+ tag +'> ')
		self.replace ("<a ", " <a ")
		tagPoint = '<.:;'
		for tag in htmlFct.listTagsIntern:
			self.replace ('</'+ tag +'>', '</'+ tag +'> ')
			for point in tagPoint: self.replace ('</'+ tag +'> '+ point, '</'+ tag +'>'+ point)
			for tig in htmlFct.listTagsIntern: self.replace ('</'+ tag + '><'+ tig +'>', '</'+ tag + '> <'+ tig +'>')
		self.text = textFct.simpleSpace (self.text)
		# rajouter les sauts de ligne
		self.replace ('><', '>\n<')
		for tag in htmlFct.listTagsIntern:
			self.replace ('\n<' + tag, '<'+ tag)
			self.replace ('</' + tag + '>\n', '</' + tag +'>')
		self.replace ('><img', '>\n\t<img')
		self.replace ('><meta', '>\n\t<meta')
		self.replace ('><base', '>\n\t<base')
		self.replace ('\n<td>', '<td>')
		self.replace ('</td>\n', '</td>')
		self.replace ('\n<th>', '<th>')
		self.replace ('</th>\n', '</th>')
		self.replace ('</tr>\n<tr>', '\n</tr><tr>\n\t')
		self.replace ('\n<tr>', '<tr>\n\t')
		self.replace ('</tr>\n', '\n</tr>')
		self.replace ('<li>', '\t<li>')
		self.replace ('<dt>', '\t<dt>')
		self.replace ('</dt>\n<dd>', '</dt><dd>')
		self.replace ('</a>\n', '</a>')
		self.replace ('> ', '>')
		self.replace (' <', '<')

	def write (self, independant=False):
		# self.text ne contient plus que le corps du body
		self.toPath()
		meta = self.getMetas()
		self.title = cleanTitle (self.title)
		self.text = htmlFct.cleanHtmlForWritting (self.text)
		self.text = templateHtml % (self.title, self.subject, self.author, self.link, meta, self.text)
		self.addIndentation()
		File.write (self, 'w')

	def toEreader (self):
		if os.path.exists (pathCard): self.path = pathCard + self.title + '.html'
		else:
			self.title = self.title +" reader"
			self.path = pathDesktop + self.title +".html"
		self.replace ('file:///')
		self.text = htmlFct.imgToB64 (self.text)
		self.text = htmlFct.cleanHtmlForWritting (self.text)
	#	self.createSummary()
		meta = self.getMetas()
		self.text = templateHtmlEreader % (self.title, self.subject, self.author, self.link, meta, self.text)
		File.write (self, 'w')

	def getCssFromFileForEreader (self):
		tagList =[]
		for tag in listTags:
			if len (tag) >2 and tag +'>' in self.text: tagList.append (tag)
		for tag in listTagsSelfClosing:
			if len (tag) >2 and (tag +'>' in self.text or tag +'/>' in self.text or tag +' />' in self.text): tagList.append (tag)
		for tag in listTagsLocal:
			if len (tag) >2 and tag +'>' in self.text: tagList.append (tag)
		fileCss = FileCss ('s/library-css\\structure.css')
		fileCss.read()
		# dimensions de ma liseuse kobo aura
		style = "\n<style type='text/css' media='(width: 295px) and (height: 380px)'>\n" + fileCss.toSelection (tagList) + '</style>'
		return style

	def createSummary (self):
		if '</h1>' in self.text and "<section id='sommaire'>" not in self.text and self.text.count ('</h1>') >4:
			sommaire = "<section id='sommaire'>"
			numero =1
			textList = self.text.split ('<h1')
			textRange = range (1, len (textList))
			for t in textRange:
				d=1+ textList[t].find ('>')
				f= textList[t].find ('<')
				chapid = 'chap-' + str(t)
				sommaire = sommaire + "<a href='%s'>%s</a>" %( '#'+ chapid, textList[t][d:f])
				textList[t] =" id='" + chapid +"'"+ textList[t]
			sommaire = sommaire + '</section>'
			self.text = '<h1'.join (textList)
			self.text = sommaire + self.text

	def createSummary_vb (self):
		if '</h1>' in self.text and "<section id='sommaire'>" not in self.text and self.text.count ('</h1>') >4:
			sommaire = "<section id='sommaire'>"
			numero =1
			if '</h2>' in self.text:
				numeroSub =1
				self.text = self.text.replace ('<h1', '<hxx1')
				self.text = self.text.replace ('<h2', '<hxx2')
				textList = self.text.split ('<hxx')
				textRange = range (1, len (textList))
				for t in textRange:
					d=1+ textList[t].find ('>')
					f= textList[t].find ('<')
					chapid = 'chap-' + str(t)
					sommaire = sommaire + "<a href='%s'>%s</a>" %( '#'+ chapid, textList[t][d:f])
					textList[t] =" id='" + chapid +"'"+ textList[t]
				sommaire = sommaire + '</section>'
				self.text = '<h1'.join (textList)

			else:
				textList = self.text.split ('<h1')
				textRange = range (1, len (textList))
				for t in textRange:
					d=1+ textList[t].find ('>')
					f= textList[t].find ('<')
					chapid = 'chap-' + str(t)
					sommaire = sommaire + "<a href='%s'>%s</a>" %( '#'+ chapid, textList[t][d:f])
					textList[t] =" id='" + chapid +"'"+ textList[t]
				sommaire = sommaire + '</section>'
				self.text = '<h1'.join (textList)
			self.text = sommaire + self.text

	def imgToB64 (self):
		if 'src=' in self.text:
			self.text = htmlFct.imgToB64 (self.text)
			self.text = self.text.replace ("src='data", "scr='data")
			self.text = self.text.replace ('src="data', 'scr="data')
			self.text = self.text.replace ("src='http", "scr='http")
			self.text = self.text.replace ('src="http', 'scr="http')
			if 'src=' in self.text:
				textList = self.text.split ('src=')
				self.textRange = range (1, len (textList))
				for t in self.textRange:
					f= textList[t].find (textList[t][0], 2)
					if textList[t][f-4:f] not in '.bmp .png .gif .jpg': continue
					imageName = textList[t][1:f]
					d= self.path.rfind (os.sep)
					pathTmp = self.path[:d]
					while imageName[:3] == '../':
						d= pathTmp.rfind (os.sep)
						pathTmp = pathTmp[:d]
						imageName = imageName[3]
					if imageName[:2] == './': imageName = imageName[2:]
					elif imageName[0] == '/': imageName = imageName[1:]
					elif imageName[:2] == 'C:' and '/' in imageName: imageName = imageName.replace ('/','\\')
					if imageName[:2] != 'C:': imageName = pathTmp + os.sep + imageName
					imgStr = htmlFct.imgToB64One (imageName)
					textList[t] = textList[t][0] + imgStr + textList[t][f:]
				self.text = 'src='.join (textList)
			self.text = self.text.replace ('scr=', 'src=')

	# ________________________ texte du web ________________________

	def fromUrlVa (self, params=None):
		# récupérer le texte. les params servent à remplir les formulaires
		myRequest = None
		response = None
		paramsUrl = None
		if params:
			paramsUrl = ul.parse.urlencode (params).encode ('utf-8')
			myRequest = urlRequest.Request (self.link, method='POST', headers={ 'User-Agent': 'Mozilla/5.0' })
		else: myRequest = urlRequest.Request (self.link, headers={ 'User-Agent': 'Mozilla/5.0' })
		try:
			response = urlRequest.urlopen (myRequest, paramsUrl)
			tmpByte = response.read()
			self.text = codecs.decode (tmpByte, 'utf-8', errors='ignore')
			if not self.text: self.text = tmpByte.decode ('utf-8')
			response.close()
			return True
		except Exception as e: return False

	def fromUrlVb (self):
		self.title = 'tmp'
		self.toPath()
		try: urlRequest.urlretrieve (self.link, self.path)
		except Exception as e:
			print (e)
			return False
		else:
			self.read()
			os.remove (self.path.replace ('\t', 'tmp'))
			return True

	def fromUrl (self, params=None):
		pathTmp = self.path
		self.toPath()
		res = False
		if params: res = self.fromUrlVa (params)
		else:
			res = self.fromUrlVa()
			if not res: res = self.fromUrlVb()
		self.path = pathTmp
		if res: self.cleanBody()
		else: print ('la récupération à échoué, impossible de récupérer les données pour\n' + self.link)

	""" ________________________ nettoyer le texte ________________________ """

	def cleanRead (self):
		self.delIcons()
		self.text = textFct.cleanHtml (self.text)
		self.cleanList()
		self.cleanTable()
		self.cleanFigure()

	def cleanList (self):
		self.replace ('<li><p>', '<li>')
		self.replace ('</p></li>', '</li>')
		self.replace ('<li><p>', '<li>')
		self.replace ('</li></ul><ul><li>', '</li><li>')
		self.replace ('</li></ol><ol><li>', '</li><li>')
		tabList = self.text.split ('li>')
		tabRange = range (1, len (tabList), 2)
		for t in tabRange: tabList[t] = tabList[t].replace ('</p><p>', '<br/>')
		self.text = 'li>'.join (tabList)

	def cleanTable (self):
		self.replace ('<td><p>', '<td>')
		self.replace ('</p></td>', '</td>')
		self.replace ('<th><p>', '<th>')
		self.replace ('</p></th>', '</th>')
		self.replace ('<tbody>')
		self.replace ('</tbody>')
		self.replace ('<thead>')
		self.replace ('</thead>')

		tabList = self.text.split ('</table>')
		textRange = range (len (tabList) -1)
		for t in textRange:
			d= tabList[t].rfind ('<table')
			textTmp = tabList[t][d:]
			if '</p><p>' in textTmp: textTmp = textTmp.replace ('</p><p>', '<br/>')
			if '<td><strong>' in textTmp and '</strong></td>' in textTmp:
				textTmp = textTmp.replace ('<td><strong>', '<th>')
				textTmp = textTmp.replace ('</strong></td>', '</th>')
			for tag in htmlFct.listTagsIntern:
				textTmp = textTmp.replace ('<'+ tag +'>', ' <'+ tag +'>')
				textTmp = textTmp.replace ('</'+ tag +'>', '</'+ tag +'> ')
			tabList[t] = tabList[t][:d] + textTmp
		self.text = '</table>'.join (tabList)
		self.replace ('<col>', "")
		self.replace ('<colgroup>', "")
		self.replace ('</colgroup>', "")

	def cleanFigure (self):
		if '</figure>' in self.text and '</figcaption>' not in self.text:
			self.replace ('<figure>', "")
			self.replace ('</figure>', "")
		elif '</figure>' in self.text:
			imgList = self.text.split ('</figure>')
			imgRange = range (len (imgList) -1)
			for i in imgRange:
				d=8+ imgList[i].find ('<figure>')
				if '</figcaption>' in imgList[i][d:]: imgList[i] = imgList[i] + '</figure>'
				else: imgList[i] = imgList[i][d:]
			self.text = "".join (imgList)

	def delAttributes (self):
		for tagName in listTags:
			if '<'+ tagName +" " in self.text:
				textList = self.text.split ('<'+ tagName +" ")
				textRange = range (1, len (textList))
				for t in textRange:
					f= textList[t].find ('>')
					# récupérer les attributs importants
					if tagName =='a' and 'href=' in textList[t][:f]:
						d=5+ textList[t].find ('href=')
						e= textList[t].find (textList[t][d], d+1)
						attribute = " href='" + textList[t][d+1:e] +"'"
						textList[t] = attribute + textList[t][f:]
					elif tagName =='button' and 'click=' in textList[t][:f]:
						d=6+ textList[t].find ('click=')
						e= textList[t].find (textList[t][d], d+1)
						attribute = " onclick='" + textList[t][d+1:e] +"'"
						textList[t] = attribute + textList[t][f:]
					elif tagName =='button' and 'method=' in textList[t][:f]:
						d=7+ textList[t].find ('method=')
						e= textList[t].find (textList[t][d], d+1)
						attribute = " method='" + textList[t][d+1:e] +"'"
						textList[t] = attribute + textList[t][f:]
					elif tagName =='td':
						attribute =""
						if 'rowspan=' in textList[t][:f]:
							d=8+ textList[t].find ('rowspan=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" rowspan='" + textList[t][d+1:e] +"'"
						if 'colspan=' in textList[t][:f]:
							d=8+ textList[t].find ('colspan=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" colspan='" + textList[t][d+1:e] +"'"
						textList[t] = attribute + textList[t][f:]
					else: textList[t] = textList[t][f:]
				textJoin = '<'+ tagName
				self.text = textJoin.join (textList)
		for tagName in listTagsSelfClosing:
			if '<'+ tagName +" " in self.text:
				textList = self.text.split ('<'+ tagName +" ")
				textRange = range (1, len (textList))
				if tagName =='img':
					for t in textRange:
						f= textList[t].find ('>')
						if 'src=' in textList[t][:f]:
							d=4+ textList[t].find ('src=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = " src='" + textList[t][d+1:e] +"'"
							textList[t] = attribute +'/'+ textList[t][f:]
				elif tagName =='input':
					for t in textRange:
						attribute =""
						f= textList[t].find ('>')
						if 'type=' in textList[t][:f]:
							d=5+ textList[t].find ('type=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" type='" + textList[t][d+1:e] +"'"
						if 'name=' in textList[t][:f]:
							d=5+ textList[t].find ('name=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" name='" + textList[t][d+1:e] +"'"
						if 'value=' in textList[t][:f]:
							d=6+ textList[t].find ('value=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" value='" + textList[t][d+1:e] +"'"
						if 'placeholder=' in textList[t][:f]:
							d=12+ textList[t].find ('placeholder=')
							e= textList[t].find (textList[t][d], d+1)
							attribute = attribute +" placeholder='" + textList[t][d+1:e] +"'"
						textList[t] = attribute +'/'+ textList[t][f:]
				textJoin = '<'+ tagName
				self.text = textJoin.join (textList)
		for tagName in listTagsLocal:
			if '<'+ tagName +" " in self.text:
				textList = self.text.split ('<'+ tagName +" ")
				textRange = range (1, len (textList))
				for t in textRange:
					f= textList[t].find ('>')
					textList[t] = textList[t][f:]
				textJoin = '<'+ tagName
				self.text = textJoin.join (textList)

	def delScript (self):
		if '<script' in self.text:
			textList = self.text.split ('<script')
			textRange = range (1, len (textList))
			for l in textRange:
				d=9+ textList[l].find ('</script>')
				textList[l] = textList[l][d:]
			self.text = "".join (textList)
		if '<style' in self.text:
			textList = self.text.split ('<style')
			textRange = range (1, len (textList))
			for l in textRange:
				d=8+ textList[l].find ('</style>')
				textList[l] = textList[l][d:]
			self.text = "".join (textList)
		if '<!--' in self.text:
			textList = self.text.split ('<!--')
			textRange = range (1, len (textList))
			for l in textRange:
				d=3+ textList[l].find ('-->')
				textList[l] = textList[l][d:]
			self.text = "".join (textList)

	def delEmptyTags (self):
		for tag in listTags: self.replace ('<'+ tag + '></' + tag +'>', "")
		for tag in listTagsLocal: self.replace ('<'+ tag + '></' + tag +'>', "")
		for tag in listTags:
			if '></' + tag +'>' in self.text:
				lenTag = len (tag)
				textList = self.text.split ('></' + tag +'>')
				textRange = range (len (textList) -1)
				for l in textRange:
					d= textList[l].rfind ('<')
					if textList[l][d+1:d+1+ lenTag] == tag: textList[l] = textList[l][:d]
					else: textList[l] = textList[l] + '></' + tag +'>'
				self.text = "".join (textList)
		for tag in listTagsLocal:
			if '></' + tag +'>' in self.text:
				lenTag = len (tag)
				textList = self.text.split ('></' + tag +'>')
				textRange = range (len (textList) -1)
				for l in textRange:
					d= textList[l].rfind ('<')
					if textList[l][d+1:d+1+ lenTag] == tag: textList[l] = textList[l][:d]
					else: textList[l] = textList[l] + '></' + tag +'>'
				self.text = "".join (textList)
		d=0
		while '></' in self.text[d:] and d< len (self.text):
			d= self.text.find ('></', d+1)
			c=1+ self.text[:d].rfind ('<')
			e= self.text.find ('>', d+1)
			if self.text[c:d] == self.text[d+3:e]: self.replace (self.text[c-1:e+1], "")

	def cleanBody (self):
		"""
		self.text = self.text.lower()
		self.cleanRead()
		"""
		self.setByHtml()
		self.setMetas()
		self.setTitle()
		self.setByBody()
		self.delScript()
		self.findTagsLocals()
		self.delEmptyTags()
