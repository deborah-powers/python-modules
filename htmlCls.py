#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from os import remove
import urllib as ul
from urllib import request as urlRequest
import codecs
import textFct
import htmlFct
from fileCls import File, Article
from fileTemplate import templateHtml
import loggerFct as log

listTags =( 'i', 'b', 'em', 'span', 'strong', 'a', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'td', 'th', 'tr', 'caption', 'table', 'nav', 'div', 'label', 'button', 'textarea', 'fieldset', 'form', 'figcaption', 'figure', 'section', 'article', 'body', 'header', 'footer', 'main' )
listTagsIntern =( 'i', 'b', 'em', 'span', 'strong', 'a')
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta', 'link', 'base' )
listAttributes =( 'href', 'src', 'alt', 'colspan', 'rowspan', 'value', 'type', 'name', 'id', 'class', 'method', 'content', 'onclick', 'ondbclick' )
templateHtmlBis = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_blank'>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	%s
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/perso.css' media='screen'/>
</head><body>
%s
</body></html>"""
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
	elif '</'+ tagName +'>' not in text: return -1
	# une seule occurence du tag
	elif text.count ('</'+ tagName +'>') ==1: return 3+ len (tagName) + text.find ('</'+ tagName +'>')
	# plusieurs tags similaires. retrouver la balise fermante associé au mien
	else:
		tagStart = '<'+ tagName
		tagEnd = '</'+ tagName +'>'
		f= text.find (tagEnd, pos)
		nbEnd =1
		nbStart = text[pos:f].count (tagStart)
		lenText = len (text) -3
		while nbEnd < nbStart:
			f= text.find (tagEnd, f+3)
			nbStart = text[pos:f].count (tagStart)
			nbEnd = nbEnd +1
		return f+3+ len (tagName)

def singleChild (text):
	# vérifier si le texte transformé par getFromPos ne contient qu'un seul enfant
	if text[:3] == 'svg' or '>' not in text: return text
	d=1+ text.find ('>')
	textBis = text[d:]
	if '>' not in textBis: return text
	elif textBis[0] =='<' and textBis[-1] =='>':
		d= textBis.find ('>')
		if " " in textBis[:d]: d= textBis.find (" ")
		# nom du premier tag enfant
		tagName = textBis[1:d]
		lenTag =3+ len (tagName)
		tagStart = '<'+ tagName
		tagEnd = '</'+ tagName +'>'
		# compter les emboîtement
		lenText = len (textBis) - lenTag
		if textBis[lenText:] == tagEnd:
			if textBis.count (tagEnd) ==1:
				d= text.find (tagStart, 1)
				innerTag = getFromPos (text, d)
				# gérer les liens
				if text[:2] == 'a ':
					d=1+ text.find ('>')
					# tag contenant du innerHtml
					if '>' in innerTag: innerTag = getInnerHtml (innerTag)
					return text[:d] + getInnerHtml (innerTag)
				else: return innerTag
			else:
				f= textBis.find (tagEnd)
				nbEnd =1
				nbStart = textBis[:f].count (tagStart)
				while nbEnd < nbStart and tagEnd in textBis[f:]:
					f= textBis.find (tagEnd, f+1)
					nbStart = textBis[:f].count (tagStart)
					nbEnd = nbEnd +1
				# emboîtement
				if f== lenText:
					d= text.find (tagStart, 1)
					innerTag = getFromPos (text, d)
					# gérer les liens
					if text[:2] == 'a ':
						d=1+ text.find ('>')
						# tag contenant du innerHtml
						if '>' in innerTag: innerTag = getInnerHtml (innerTag)
						return text[:d] + getInnerHtml (innerTag)
					else: return innerTag
				else: return text
		else: return text
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
		d=6+ text.find ('class=', d)
		f= text.find (text[d], d+1)
		if className in text[d:f]:
			index = text[:d].rfind ('<')
			if tagName == text [index +1:d-7]:
				d=1+ lenText
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

class Html (File):
	def __init__ (self, file =None):
		File.__init__ (self)
		self.meta ={}
		self.link =""

		if file and file[:4] == 'http':
			self.link = file
			self.path = 'b/tmp.html'
			self.fromPath()
			self.fromUrl()
		elif file:
			self.path = file
			self.fromPath()
			self.read()

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
		f= self.text.find ('</'+ tagName +'>')
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

	def singleChild (self):
		d=0
		for tag in listTags:
			while '<'+ tag +'>' in self.text[d:]:
				d= self.text.find ('<'+ tag +'>', d)
				d=d+1

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
		metaList = getAllByTag (self.text, 'meta')
		self.meta ={}
		for meta in metaList:
			if 'content' in meta and 'name' in meta and 'csrf-' not in meta:
				d=5+ meta.find ('name=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]
			elif 'content' in meta and 'property' in meta and 'csrf-' not in meta:
				d=9+ meta.find ('property=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]
		metaList = getAllByTag (self.text, 'link')
		for meta in metaList:
			if 'stylesheet' not in meta and 'icon' not in meta:
				d=4+ meta.find ('rel=')
				f= meta.find (meta[d], d+1)
				name = meta[d+1:f]
				d=5+ meta.find ('href=')
				f= meta.find (meta[d], d+1)
				self.meta [name] = meta[d+1:f]

	def getMetas (self):
		metas =""
		for meta in self.meta.keys(): metas = metas + "<meta name='%s' content='%s'/>" % (meta, self.meta[meta])
		return metas

	# ________________________ lire et écrire dans un fichier html ________________________

	def toText (self):
		if '</a>' in self.text or '<img' in self.text: return None
		article = Article()
		article.text = htmlFct.fromHtml (self.text)
		if '</' in article.text: return None
		article.path = self.path.replace ('.html', '.txt')
		if self.type == 'xhtml': article.path = self.path.replace ('.xhtml', '.txt')
		article.type = 'txt'
		article.title = self.title
		article.subject = self.subject
		article.author = self.author
		article.link = self.link
	#	article.autlink = self.autlink
	#	if 'link' in self.meta.keys(): article.link = self.meta['link']
		keys = self.meta.keys()
		for key in keys: article.meta[key] = self.meta[key]
		return article

	def read (self):
		File.read (self)
		self.cleanBody()

	def addIndentation (self):
		self.replace ('\n'," ")
		self.replace ('\t'," ")
		self.text = textFct.simpleSpace (self.text)
		self.replace ("> ",'>')
		self.replace (" <",'<')
		# rajouter les espaces autour des balises internes
		for tag in listTagsIntern:
			self.text = self.text.replace ('<'+ tag +'>', ' <'+ tag +'>')
			self.text = self.text.replace ('</'+ tag +'>', '</'+ tag +'> ')
		self.text = self.text.replace ("<a ", " <a ")
		tagPoint = '<.:;'
		for tag in listTagsIntern:
			self.replace ('</'+ tag +'>', '</'+ tag +'> ')
			for point in tagPoint: self.replace ('</'+ tag +'> '+ point, '</'+ tag +'>'+ point)
			for tig in listTagsIntern: self.text = self.text.replace ('</'+ tag + '><'+ tig +'>', '</'+ tag + '> <'+ tig +'>')
		self.text = textFct.simpleSpace (self.text)
		# rajouter les sauts de ligne
		self.replace ('><', '>\n<')
		for tag in listTagsIntern:
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

	def write (self, mode='w'):
		# self.text ne contient plus que le corps du body
	#	self.meta['link'] = self.link
		self.toPath()
		meta = self.metaToHtml()
		self.title = cleanTitle (self.title)
		self.text = templateHtml % (self.title, self.subject, self.author, self.link, meta, self.text)
	#	self.text = templateHtml % (self.title, self.getMetas(), self.text)
		self.addIndentation()
		File.write (self, mode)

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
			remove (self.path.replace ('\t', 'tmp'))
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
		else:
			print ('la récupération à échoué, impossible de récupérer les données pour\n' + self.link)

	""" ________________________ nettoyer le texte ________________________ """

	def cleanRead (self):
		self.text = textFct.cleanBasic (self.text)
		self.text = self.text.replace ('\n', ' ')
		self.text = self.text.replace ('\t', ' ')
		for i, j in textFct.weirdChars: self.text = self.text.replace (i, j)
		self.text = self.text.strip()
		self.text = textFct.simpleSpace (self.text)
		self.text = self.text.replace ('> ', '>')
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace (' >', '>')
		self.text = self.text.replace (' />', '/>')
		self.text = textFct.simpleSpace (self.text)
		self.text = self.text.replace ('> <', '><')
		points = '.,)'
		for p in points: self.text = self.text.replace (" "+p, p)
		self.text = self.text.replace ("( ", '(')

	def cleanList (self):
		self.text = self.text.replace ('<li><p>', '<li>')
		self.text = self.text.replace ('</p></li>', '</li>')
		self.text = self.text.replace ('<li><p>', '<li>')
		self.text = self.text.replace ('</li></ul><ul><li>', '</li><li>')
		self.text = self.text.replace ('</li></ol><ol><li>', '</li><li>')
		tabList = self.text.split ('li>')
		tabRange = range (1, len (tabList), 2)
		for t in tabRange: tabList[t] = tabList[t].replace ('</p><p>', '<br/>')
		self.text = 'li>'.join (tabList)

	def cleanTable (self):
		self.text = self.text.replace ('<td><p>', '<td>')
		self.text = self.text.replace ('</p></td>', '</td>')
		self.text = self.text.replace ('<th><p>', '<th>')
		self.text = self.text.replace ('</p></th>', '</th>')
		tabList = self.text.split ('table>')
		tabRange = range (1, len (tabList), 2)
		for t in tabRange:
			tabList[t] = tabList[t].replace ('</p><p>', '<br/>')
			if '<td><strong>' in tabList[t] and '</strong></td>' in tabList[t]:
				tabList[t] = tabList[t].replace ('<td><strong>', '<th>')
				tabList[t] = tabList[t].replace ('</strong></td>', '</th>')
			elif '<strong>' in tabList[t]:
				tabList[t] = tabList[t].replace ('<strong>', "")
				tabList[t] = tabList[t].replace ('</strong>', "")
		self.text = 'table>'.join (tabList)
		self.text = self.text.replace ('<col>', "")
		self.text = self.text.replace ('<colgroup>', "")
		self.text = self.text.replace ('</colgroup>', "")

	def cleanFigure (self):
		if '</figure>' in self.text and '</figcaption>' not in self.text:
			self.text = self.text.replace ('<figure>', "")
			self.text = self.text.replace ('</figure>', "")
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
		for tag in listTags: self.text = self.text.replace ('<'+ tag + '></' + tag +'>', "")
		for tag in listTagsLocal: self.text = self.text.replace ('<'+ tag + '></' + tag +'>', "")
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
			if self.text[c:d] == self.text[d+3:e]: self.text = self.text.replace (self.text[c-1:e+1], "")

	def cleanBody (self):
		self.text = self.text.lower()
		self.cleanRead()
		self.setByHtml()
		self.setTitle()
		self.delScript()
		self.setMetas()
		self.setByBody()
		self.findTagsLocals()
		self.delEmptyTags()
