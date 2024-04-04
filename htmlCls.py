#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from os import remove
import urllib as ul
from urllib import request as urlRequest
import codecs
import textFct
from fileCls import File
import loggerFct as log

listTags =( 'i', 'b', 'em', 'span', 'strong', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol', 'td', 'th', 'tr', 'caption', 'table', 'nav', 'div', 'label', 'button', 'textarea', 'fieldset', 'form', 'figcaption', 'figure', 'section', 'article', 'body' )
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta' )
listAttributes =( 'href', 'src', 'colspan', 'rowspan', 'value', 'type', 'name', 'id', 'class', 'method', 'content', 'onclick', 'ondbclick' )
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

class TagHtml():
	def __init__ (self, text):
		self.tag =""
		self.className =""
		self.id =""
		self.innerHtml =""
		self.attributes ={}
		# trouver le tag
		text = text.strip ('<')
		d= text.find ('>')
		if " " in text[:d]: d= text.find (" ")
		self.tag = text[:d]
		text = text[d:]
		d= text.find ('>')
		# trouver le texte
		if self.tag not in listTagsSelfClosing:
			self.innerHtml = text[d+1:]
			text = text[:d]
		# trouver les attributs
		text = text.strip()
		if text:
			attributes = text.split (" ")
			rattr = reversed (range (1, len (attributes)))
			for a in rattr:
				if '=' not in attributes[a]:
					end = attributes.pop (a)
					attributes[a-1] = attributes[a-1] +" "+ end
			for attr in attributes:
				if attr[:3] == 'id=': self.id = attr[4:-1]
				elif attr[:6] == 'class=': self.id = attr[7:-1]
				else:
					d= attr.find ('=')
					if attr[:d] in listAttributes: self.attributes[attr[:d]] = attr[d+2:-1]

	def containAttribute (self, attribut):
		if attribut == 'id' and self.id: return self.id
		elif attribut == 'class' and self.className: return self.className
		elif attribut in self.attributes.keys(): return self.attributes[attribut]
		else: return None

	def __str__ (self):
		tagStr = self.tag +" "+ self.className +" "+ self.id
		if len (self.attributes.keys()) >0:
			tagStr = tagStr +'\t'
			for attr in self.attributes.keys(): tagStr = tagStr + attr +': '+ self.attributes[attr] +", "
		if self.innerHtml: tagStr = tagStr +'\nil y a du texte'
		return tagStr

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

	""" ________________________ récupérer des balises ________________________ """

	def getById (self, index):
		text = self.text.replace ('"', "'")
		if " id='" + index +"'" in text:
			posStart = text.find (" id='" + index +"'")
			posStart = self.text [:posStart].rfind ('<')
			return self.getByPos (posStart)
		else: return None

	def getByClass (self, className):
		if 'class=' not in self.text: return []
		# repérer les balises
		textList = self.text.split ("class='")
		textRange = range (1, len (textList))
		for t in textRange:
			f= textList[t].find ("'")
			if className in textList[t][:f]: textList[t-1] = textList[t-1] +'$'
		self.text = "class='".join (textList)
		textList = self.text.split ('class="')
		textRange = range (1, len (textList))
		for t in textRange:
			f= textList[t].find ('"')
			if className in textList[t][:f]: textList[t-1] = textList[t-1] +'$'
		self.text = 'class="'.join (textList)
		# récupérer les balises
		tagList =[]
		d=0
		while '$<' in self.text[d:]:
			d=1+ self.text.find ('$<',d)
			tagList.append (self.getByPos (d))
			d=d+2
		self.text = self.text.replace ('$<', '<')
		return tagList

	def getByTag (self, tagName):
		tagStart = '<'+ tagName
		if tagStart not in self.text: return []
		tagList =[]
		d=0
		while tagStart in self.text[d:]:
			d= self.text.find (tagStart, d)
			tagList.append (self.getByPos (d))
			d=d+2
		return tagList

	def getByTagAndClass (self, tagName, className):
		tagStart = '<'+ tagName +" "
		if tagStart not in self.text or className not in self.text: return []
		# identifier les balises d'intérêt
		tagList = self.text.split (tagStart)
		reta = range (1, len (tagList))
		for m in reta:
			fBracket= tagList[m].find ('>')
			if 'class=' not in tagList[m][:fBracket]: continue
			d= 7+ tagList[m].find ('class=')
			f= tagList[m].find ("'",d)
			if 'class="' in tagList[m]: f= tagList[m].find ('"',d)
			if className in tagList[m][d:f]: tagList[m-1] = tagList[m-1] +'$'
		self.text = tagStart.join (tagList)
		# récupérer les balises
		d=1+ self.text.find ('$'+ tagStart)
		tagList =[]
		while '$'+ tagStart in self.text[d:]:
			tagList.append (self.getByPos (d))
			d= 1+ self.text.find ('$'+ tagStart, d)
			d=d+2
		self.text = self.text.replace ('$'+ tagStart, tagStart)
		return tagList

	def getByPos (self, posStart):
		# posStart = pos <tag
		f= self.text.find ('>', posStart)
		# balise auto-fermante
		if self.text[f-1] == '/': return TagHtml (self.text [posStart:f-1])
		else:
			# balise contenant du texte
			if " " in self.text[:f]:
				f= self.text.find (" ", posStart)
			tagStart = self.text[posStart:f]
			tagEnd = '</'+ tagStart[1:] +'>'
			d= self.text.find (tagStart, posStart)
			f= self.text.find (tagEnd, posStart)
			nbEnd =0
			nbStart = self.text[d+1:f].count (tagStart)
			lenText = len (self.text) -3
			while nbEnd < nbStart and f< lenText:
				f= self.text.find (tagEnd, f+3)
				nbStart = self.text[d+1:f].count (tagStart)
				nbEnd = nbEnd +1
			return TagHtml (self.text[d:f])

	""" ________________________ nettoyer le texte ________________________ """

	def delAttributes (self):
		# éffacer les attributs inutiles
		listeCoins = self.text.split ('<')
		rangeCoins = range (1, len (listeCoins))
		for c in rangeCoins:
			if '>' not in listeCoins[c]: continue
			f= listeCoins[c].find ('>')
			if " " not in listeCoins[c][:f]: continue
			# examiner les attributs
			attributes = listeCoins[c][:f].split (" ")
			rattr = reversed (range (2, len (attributes)))
			for a in rattr:
				if '=' in attributes[a]:
					d= attributes[a].find ('=')
					if attributes[a][:d] not in listAttributes: end = attributes.pop (a)
				else:
					end = attributes.pop (a)
					attributes[a-1] = attributes[a-1] +" "+ end
			# examiner le premier attribut
			d= attributes[1].find ('=')
			if attributes[1][:d] not in listAttributes: end = attributes.pop (1)
			listeCoins[c] = " ".join (attributes) + listeCoins[c][f:]
		self.text = '<'.join (listeCoins)

	def delClasses (self):
		self.text = self.text.replace (' id=', ' class=')
		textList = self.text.split (' class="')
		textRange = range (1, len (textList))
		for t in textRange:
			f= 1+ textList[t].find ('"')
			textList[t] = textList[t][f:]
		self.text = "".join (textList)
		textList = self.text.split (" class='")
		textRange = range (1, len (textList))
		for t in textRange:
			f= 1+ textList[t].find ("'")
			textList[t] = textList[t][f:]
		self.text = "".join (textList)
		for tag in listTags:
			while '<'+ tag + '></'+ tag + '>' in self.text: self.text = self.text.replace ('<'+ tag + '></'+ tag + '>', "")

	def setBody (self):
		d= self.text.find ('<body')
		d= self.text.find ('>',d) +1
		f= self.text.rfind ('</body>')
		self.text = self.text[d:f]

	def setTitle (self):
		d= self.text.find ('<title')
		d= self.text.find ('>',d) +1
		f= self.text.rfind ('</title>')
		self.title = self.text[d:f]
		self.cleanTitle()

	def setMetas (self):
		self.meta ={}
		metaList = self.text.split ('<meta ')
		reta = range (1, len (metaList))
		for m in reta:
			fBracket= metaList[m].find ('>')
			if 'name=' not in metaList[m][:fBracket] or 'content=' not in metaList[m][:fBracket] or 'viewport' in metaList[m][:fBracket]: continue
			d= 6+ metaList[m].find ('name=')
			f= metaList[m].find ("'",d)
			if 'name="' in metaList[m]: f= metaList[m].find ('"',d)
			name = metaList[m][d:f]
			d= 9+ metaList[m].find ('content=')
			f= metaList[m].find ("'",d)
			if 'content="' in metaList[m]: f= metaList[m].find ('"',d)
			if name and metaList[m][d:f]: self.meta[name] = metaList[m][d:f]

	def getMetas (self):
		metas =""
		for meta in self.meta.keys(): metas = metas + "<meta name='%s' content='%s'/>" % (meta, self.meta[meta])
		return metas

	""" ________________________ texte du web ________________________ """

	def fromUrlVa (self, params=None):
		# récupérer le texte. les params servent à remplir les formulaires
		myRequest = None
		response = None
		paramsUrl = None
		res = True
		if params:
			paramsUrl = ul.parse.urlencode (params).encode ('utf-8')
			myRequest = urlRequest.Request (self.link, method='POST')
		else: myRequest = urlRequest.Request (self.link)
		try:
			response = urlRequest.urlopen (myRequest, paramsUrl)
			tmpByte = response.read()
			self.text = codecs.decode (tmpByte, 'utf-8', errors='ignore')
			if not self.text: self.text = tmpByte.decode ('utf-8')
			response.close()
			# self.titleFromUrl()
			self.clean()
			self.setTitle()
			self.setMetas()
			self.setBody()
			self.delAttributes()
			return True
		except Exception as e: return False

	def fromUrlVb (self):
		res = False
		self.title = 'tmp'
		self.toPath()
		try: urlRequest.urlretrieve (self.link, self.path)
		except Exception as e:
			print (e)
			return False
		else:
			self.read()
			self.delAttributes()
			remove (self.path.replace ('\t', 'tmp'))
			return True

	def fromUrl (self, params=None):
		self.toPath()
		res = False
		if params: res = self.fromUrlVa (params)
		else:
			res = self.fromUrlVa()
			if not res: res = self.fromUrlVb()
		if not res: print ('la récupération à échoué, impossible de récupérer les données')

	def titleFromUrl (self):
		title = self.link.strip ('/')
		pos = title.rfind ('/') +1
		title = title [pos:]
		endTitle = '?.'
		for end in endTitle:
			if end in title:
				pos = title.rfind (end)
				title = title [:pos]
		if title.count ('-') >1: title = title.replace ('-', ' ')
		title = title.replace ('_', ' ')
		title = title.lower()
		self.title = title
		self.cleanTitle()

	""" ________________________ lire et écrire dans un fichier html ________________________ """

	def toText (self):
		if '</a>' in self.text or '<img' in self.text: return
		article = Article()
		article.text = textFct.fromHtml (self.text)
		if '</' in article.text: return
		article.path = self.path.replace ('.html', '.txt')
		if self.type == 'xhtml': article.path = self.path.replace ('.xhtml', '.txt')
		article.title = self.title
		article.subject = self.subject
		article.type = 'txt'
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		article.write()
		print ('article créé:\n' + article.path)

	def read (self):
		File.read (self)
		self.clean()
		self.setTitle()
		self.setMetas()
		self.setBody()
		# self.delAttributes()

	def write (self, mode='w'):
		# self.text ne contient plus que le corps du body
		self.text = self.text.replace ('><', '>\n<')
		self.text = self.text.replace ('>\n</', '></')
		self.cleanTitle()
		self.clean()
		self.text = templateHtml % (self.title, self.getMetas(), self.text)
		File.write (self, mode)

	def clean (self):
		# nettoyage de base
		self.text = textFct.cleanBasic (self.text)
		self.text = self.text.replace ('\n', ' ')
		self.text = self.text.replace ('\t', ' ')
		for i, j in textFct.weirdChars: self.text = self.text.replace (i, j)
		self.text = self.text.strip()
		while '  ' in self.text: self.text = self.text.replace ('  ', ' ')
		self.text = self.text.replace ('> ', '>')
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace (' >', '>')
		self.text = self.text.replace (' />', '/>')
		# standardiser tags
		for tag in listTags:
			self.text = self.text.replace ('<'+ tag.upper(), '<'+ tag)
			self.text = self.text.replace ('</'+ tag.upper(), '</'+ tag)
		for tag in listTagsSelfClosing:
			self.text = self.text.replace ('<'+ tag.upper(), '<'+ tag)
			self.text = self.text.replace ('<'+ tag +'>', '<'+ tag +'>')

	def cleanTitle (self):
		self.title = self.title.lower()
		for i, j in textFct.weirdChars: self.title = self.title.replace (i, j)
		charToErase = '-_.:;,?/\\'
		for char in charToErase: self.title = self.title.replace (char," ")
		self.title = self.title.strip()
		while '  ' in self.title: self.title = self.title.replace ('  ', ' ')
