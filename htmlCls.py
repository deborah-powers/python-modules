#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from os import remove
import urllib as ul
from urllib import request as urlRequest
import codecs
import textFct
from fileCls import File, Article
import loggerFct as log

listTags =( 'i', 'b', 'em', 'span', 'strong', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'td', 'th', 'tr', 'caption', 'table', 'nav', 'div', 'label', 'button', 'textarea', 'fieldset', 'form', 'figcaption', 'figure', 'section', 'article', 'body' )
listTagsIntern =( 'i', 'b', 'em', 'span', 'strong', 'a')
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta', 'link', 'base' )
listAttributes =( 'href', 'src', 'alt', 'colspan', 'rowspan', 'value', 'type', 'name', 'id', 'class', 'method', 'content', 'onclick', 'ondbclick' )
templateHtml = """<!DOCTYPE html><html><head>
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

class HtmlTag():
	def __init__ (self, tagStr):
		self.tag =""
		self.innerHtml =""
		self.className =""
		self.id =""
		self.attributes ={}
		self.children =[]
		self.fromString (tagStr)

	# ________________________ création du noeud ________________________

	def fromString (self, tagStr):
		# tagStr contient l'outerHtml
		if '<' not in tagStr or '>' not in tagStr:
			self.innerHtml = tagStr
			self.tag = 'text'
		else:
			d= tagStr.find ('<')
			f=1+ tagStr.rfind ('>')
			self.innerHtml = tagStr[d:f]
			self.setAttributes()
			self.setInnerHtml()

	def setAttributes (self):
		# innerHtml contient l'outerHtml
		# récupérer le tag
		f= self.innerHtml.find ('>')
		if " " in self.innerHtml[:f]: f= self.innerHtml.find (" ")
		d=1+ self.innerHtml.find ('<')
		self.tag = self.innerHtml[d:f]
		# récupérer les attributs
		f= self.innerHtml.find ('>')
		if self.innerHtml[f-1] =='/': f-=1
		if " " in self.innerHtml[:f]:
			d=1+ self.innerHtml.find (" ")
			attriStr = self.innerHtml[d:f]
			attriStr = attriStr.replace (' =','=')
			attriStr = attriStr.replace ('= ','=')
			attriStr = attriStr.replace ('="',"='")
			attriLst = attriStr.split ("='")
			attriLst2 =[ attriLst[0], ]
			attriRge = range (1, len (attriLst) -1)
			for a in attriRge:
				d= attriLst[a].rfind (" ")
				attriLst2.append (attriLst[a][:d-1])
				attriLst2.append (attriLst[a][d+1:])
			attriLst2.append (attriLst[-1][:-1])
			attriRge = range (1, len (attriLst2), 2)
			for a in attriRge:
				if attriLst2[a-1] == 'class': self.className = attriLst2[a]
				elif attriLst2[a-1] == 'id': self.id = attriLst2[a]
				else: self.attributes [attriLst2[a-1]] = attriLst2[a]

	def setInnerHtml (self):
		# innerHtml contient l'outerHtml
		if self.tag == 'text': return
		elif self.tag in listTagsSelfClosing: self.innerHtml =""
		elif self.tag == 'svg':
			d=1+ self.innerHtml.find ('>')
			f= self.innerHtml.find ('</svg>',d)
			self.innerHtml = self.innerHtml[d:f]
		# balise contenant du texte
		else:
			tagStart = '<'+ self.tag
			tagEnd = '</'+ self.tag +'>'
			d=1+ self.innerHtml.find ('>')
			f= self.innerHtml.find (tagEnd, d)
			nbEnd =0
			nbStart = self.innerHtml[d:f].count (tagStart)
			lenText = len (self.innerHtml) -3
			while nbEnd < nbStart and f< lenText and f>=0:
				f= self.innerHtml.find (tagEnd, f+3)
				nbStart = self.innerHtml[d:f].count (tagStart)
				nbEnd = nbEnd +1
			self.innerHtml = self.innerHtml[d:f]

	def unnestOneChild (self):
		self.innerHtml = self.children[0].innerHtml
		if not self.id and self.children[0].id: self.id = self.children[0].id
		if self.children[0].className:
			if self.className: self.className = self.className +" "+ self.children[0].className
			else: self.className = self.children[0].className
		for child in self.children[0].children: self.children.append (child)
		self.children.pop (0)

# ________________________ auxilières ________________________

def cleanTitle (title):
	title = title.lower()
	charToErase = '-_.:;,?/\\'
	for char in charToErase: title = title.replace (char," ")
	title = textFct.cleanBasic (title)
	return title

def getFromPos (text, pos):
	""" pos est la postion de <tag ...
	renvoi tag attr='value'>content
	ou
	img src='path.img'
	"""
	# retrouver le tag
	text = text[pos+1:]
	f= min (text.find ('>', d), text.find (' ',d))
	tagName = text[:f]
	# tag auto-fermant
	if tagName in listTagsSelfClosing:
		f= text.find ('>')
		if text[f-1] =='/': f-=1
		return text[:f]
	# une seule occurence du tag
	elif text.count ('</'+ tagName +'>') ==1:
		f= text.find ('</'+ tagName +'>')
		return text[:f]
	# erreur, pas de tag fermant
	elif '</'+ tagName +'>' not in text: return ""
	# plusieurs tags similaires. retrouver la balise fermante associé au mien
	else:
		tagStart = '<'+ tagName
		tagEnd = '</'+ tagName +'>'
		f= text.find (tagEnd)
		nbEnd =0
		nbStart = text[:f].count (tagStart)
		lenText = len (text) -3
		while nbEnd < nbStart and f< lenText and f>=0:
			f= text.find (tagEnd, f+3)
			nbStart = text[:f].count (tagStart)
			nbEnd = nbEnd +1
		return text[:f]

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

def getOneByClass (text, tagClass):
	if tagClass not in text or 'class=' not in text: return ""
	textBis = text.replace ('"',"'")
	textList = textBis.split ('class=')
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ("'")
		if tagClass in textList[t][:f]:
			d= textList[t-1].rfind ('<')
			textList[t-1] = textList[t-1][:d] +'$'+ textList[t-1][d:]
			t=1+ lenList
		t+=1
	textJoin = 'class='
	textBis = textJoin.join (textList)
	d= textBis.find ('$<')
	return getFromPos (text, d)

def getOneByTagClass (text, tagName, className):
	if '<'+ tagName +" " not in text or tagClass not in text or 'class=' not in text: return ""
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
				t=1+ lenList
		t+=1
	textJoin = '<'+ tagName +" "
	textBis = textJoin +"='".join (textList)
	d= textBis.find ('$<')
	return getFromPos (text, d)

def getOneByAttribute (text, attrName, attrValue):
	if attrValue not in text or attrName +'=' not in text: return ""
	textBis = text.replace ('"',"'")
	textList = textBis.split (attrName +"='")
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ("'",d)
		if attrValue in textList[t][:f]:
			d= textList[t-1].rfind ('<')
			textList[t-1] = textList[t-1][:d] +'$'+ textList[t-1][d:]
			t=1+ lenList
		t+=1
	textJoin = attrName +"='"
	textBis = textJoin.join (textList)
	d= textBis.find ('$<')
	return getFromPos (text, d)

def getAllByTag (text, tagName):
	if '<'+ tagName not in text: return []
	tagList =[]
	d=-1
	lenText = len (text)
	while d< lenText:
		d= text.find ('<'+ tagName, d+1)
		if text[d+1] in "> ": tagList.append (getFromPos (text, d))
	return tagList

def getAllByClass (text, tagClass):
	if tagClass not in text or 'class=' not in text: return []
	# repérer les tags intéressants
	textBis = text.replace ('"',"'")
	textList = textBis.split ('class=')
	lenList = len (textList)
	t=1
	while t< lenList:
		f= textList[t].find ("'")
		if tagClass in textList[t][:f]:
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
	if '<'+ tagName +" " not in text or tagClass not in text or 'class=' not in text: return []
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
		self.tree = None

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

	def setFromTag (self, tagName):
		if '</'+ tagName +'>' not in self.text or self.text.count ('</'+ tagName +'>') >1: return
		d= self.text.find ('<'+ tagName)
		d=1+ self.text.find ('>',d)
		f= self.text.find ('</'+ tagName +'>')
		self.text = self.text[d:f]

	def setFromHtml (self):
		self.setFromTag ('html')
	def setFromBody (self):
		self.setFromTag ('body')
	def setFromMain (self):
		self.setFromTag ('main')

	# ________________________ finir la lecture, préparer l'écriture ________________________

	def setTitle (self):
		if '</title>' in self.text: self.title = cleanTitle (self.getOneByTag ('title').innerHtml)
		elif '</h1>' in self.text: self.title = cleanTitle (self.getOneByTag ('h1').innerHtml)

	def setMetas (self):
		metaList = getAllByTag ('meta')
		self.meta ={}
		for meta in metaList:
			if 'content' in meta and 'name' in meta and 'csrf-' not in meta:
				d=5+ meta.find ('name=')
				f= meta.find (meta[d], d)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d)
				self.meta [name] = meta[d+1:f]
			elif 'content' in meta and 'property' in meta and 'csrf-' not in meta:
				d=9+ meta.find ('property=')
				f= meta.find (meta[d], d)
				name = meta[d+1:f]
				d=8+ meta.find ('content=')
				f= meta.find (meta[d], d)
				self.meta [name] = meta[d+1:f]

	def getMetas (self):
		metas =""
		for meta in self.meta.keys(): metas = metas + "<meta name='%s' content='%s'/>" % (meta, self.meta[meta])
		return metas
	# ________________________ lire et écrire dans un fichier html ________________________

	def toText (self):
		if '</a>' in self.text or '<img' in self.text: return None
		article = Article()
		article.text = textFct.fromHtml (self.text)
		if '</' in article.text: return None
		article.path = self.path.replace ('.html', '.txt')
		if self.type == 'xhtml': article.path = self.path.replace ('.xhtml', '.txt')
		article.type = 'txt'
		article.title = self.title
		if 'link' in self.meta.keys(): article.link = self.meta['link']
		if 'subject' in self.meta.keys(): article.subject = self.meta['subject']
		if 'author' in self.meta.keys(): article.author = self.meta['author']
		if 'autlink' in self.meta.keys(): article.autlink = self.meta['autlink']
		# article.write()
		print ('article créé:\n' + article.path)
		return article

	def read (self):
		File.read (self)
		self.cleanBody()

	def addIndentation (self):
		self.replace ('\n'," ")
		self.replace ('\t'," ")
		while "  " in self.text: self.replace ("  "," ")
		self.replace ("> ",'>')
		self.replace (" <",'<')
		# rajouter les espaces autour des balises internes
		self.replace ("<a ", " <a ")
		self.replace ("> <a ", "><a ")
		for tag in listTagsIntern[:-1]:
			self.replace ('<'+ tag, ' <'+ tag)
			self.replace ('> <'+ tag, '><'+ tag)
		tagPoint = '<.:;'
		for tag in listTagsIntern:
			self.replace ('</'+ tag +'>', '</'+ tag +'> ')
			for point in tagPoint: self.replace ('</'+ tag +'> '+ point, '</'+ tag +'>'+ point)
		# rajouter les sauts de ligne
		self.replace ('><', '>\n<')
		for tag in listTagsIntern:
			self.replace ('\n<' + tag, '<'+ tag)
			self.replace ('</' + tag + '>\n', '</' + tag +'>')
		self.replace ('><img', '>\n<img')
		self.replace ('><meta', '>\n<meta')
		self.replace ('><base', '>\n<base')

	def write (self, mode='w'):
		# self.text ne contient plus que le corps du body
		self.meta['link'] = self.link
		self.title = cleanTitle (self.title)
		self.text = templateHtml % (self.title, self.getMetas(), self.text)
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
		else: print ('la récupération à échoué, impossible de récupérer les données')

	""" ________________________ nettoyer le texte ________________________ """

	def delAttributes (self):
		self.tree.delAttributes()
		self.text = self.tree.innerHtml

	def delIds (self):
		self.tree.delIds()
		self.text = self.tree.innerHtml

	def delScript (self):
		"""
		self.tree.delScript()
		self.text = self.tree.innerHtml
		"""
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
	#	self.tree = HtmlTag ('<body>' + self.text + '</body>')

	def delEmptyTags (self):
		for tag in listTags: self.text = self.text.replace ('<'+ tag + '></' + tag +'>', "")
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
		d=0
		while '></' in self.text[d:] and d< len (self.text):
			d= self.text.find ('></', d+1)
			c=1+ self.text[:d].rfind ('<')
			e= self.text.find ('>', d+1)
			if self.text[c:d] == self.text[d+3:e]: self.text = self.text.replace (self.text[c-1:e+1], "")
	#	self.tree = HtmlTag ('<body>' + self.text + '</body>')

	def cleanBody (self):
		self.text = textFct.cleanHtml (self.text)
		# standardiser tags
		self.text = self.text.lower()
		"""
		for tag in listTags:
			self.replace ('<'+ tag.upper(), '<'+ tag)
			self.replace ('</'+ tag.upper(), '</'+ tag)
		for tag in listTagsSelfClosing:
			self.replace ('<'+ tag.upper(), '<'+ tag)
			self.replace (tag +'>', tag +'/>')
		"""
		self.delScript()
		self.delEmptyTags()
		self.setHtml()
		self.setTitle()
		self.setMetas()
		self.setByTag ('body')
