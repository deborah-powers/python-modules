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
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta' )
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
		self.name =""
		self.innerHtml =""
		self.className =""
		self.id =""
		self.attributes ={}
		self.fromString (tagStr)

	def fromString (self, tagStr):
		""" tagStr est envoyée par getByPos
		<p arrt='xyz'><innerHtml>
		<img src='xyz'
		"""
		attributesExists = False
		f= tagStr.find ('>')
		if " " in tagStr[:f]:
			f= tagStr.find (" ")
			attributesExists = True
		self.name = tagStr[1:f]
		# récupérer les attributs
		if attributesExists:
			tagStr = tagStr[f+1:]
			f= tagStr.find ('>')
			attributeStr = tagStr[:f].replace ('"',"")
			attributeStr = attributeStr.replace ("'","")
			attributes = attributeStr[:f].split (" ")
			attrRge = reversed (range (1, len (attributes)))
			for a in attrRge:
				if '=' in attributes[a]:
					d= attributes[a].find ('=')
					if attributes[a][:d] == 'class': self.className = attributes[a][d+1:]
					elif attributes[a][:d] == 'id': self.id = attributes[a][d+1:]
					elif attributes[a][:d] in listAttributes: self.attributes [attributes[a][:d]] = attributes[a][d+1:]
				else:
					end = attributes.pop (a)
					attributes[a-1] = attributes[a-1] +" "+ end
			# examiner le premier attribut
			d= attributes[0].find ('=')
			if attributes[0][:d] == 'class': self.className = attributes[0][d+1:]
			elif attributes[0][:d] == 'id': self.id = attributes[0][d+1:]
			elif attributes[0][:d] in listAttributes: self.attributes [attributes[0][:d]] = attributes[0][d+1:]
		# récupérer le texte
		if self.name not in listTagsSelfClosing:
			f=1+ tagStr.find ('>')
			self.innerHtml = tagStr[f:]

	def __str__(self):
		res = '<'+ self.name
		if self.className: res = res +" class='"+ self.className +"'"
		if self.id: res = res +" id='"+ self.id +"'"
		attributes = self.attributes.keys()
		for attr in attributes: res = res +" "+ attr +"='"+ self.attributes[attr] +"'"
		if self.name in listTagsSelfClosing: res = res +'/>'
		else: res = res +'>'+ self.innerHtml +'</'+ self.name +'>'
		return res

""" ________________________ nettoyer le texte ________________________ """

def cleanTitle (title):
	title = title.lower()
	charToErase = '-_.:;,?/\\'
	for char in charToErase: title = title.replace (char," ")
	title = textFct.cleanBasic (title)
	return title

""" ________________________ récupérer des balises ________________________ """

def getAttribute (tag, attr):
	if attr +'=' not in tag: return ""
	lenAttr = len (attr)
	d=2+ lenAttr + tag.find (attr +'=')
	f= tag.find ("'",d)
	if attr +'="' in tag: f= tag.find ('"',d)
	return tag[d:f]

def getText (tag):
	""" tag à été obtenu par get by pos
	<p id='id' attr='bla bla'><inner html/>
	ou <img src='...' attr='bla bla'
	"""
	text =""
	d=-1
	f=-1
	if tag[:5] == '<img ':
		d=5+ tag.find ('src=')
		if "src='" in tag: f= tag.find ("'",d)
		elif 'src="' in tag: f= tag.find ('"',d)
		text = tag[d:f]
		if 'alt=' in tag:
			d=5+ tag.find ('alt=')
			if "alt='" in tag: f= tag.find ("'",d)
			elif 'alt="' in tag: f= tag.find ('"',d)
			text = text +'\n'+ tag[d:f]
	else:
		f=1+ tag.find ('>')
		text = tag[f:]
		if tag[:3] == '<a ':
			d=6+ tag.find ('href=')
			if 'href="' in tag: f= tag.find ('"',d)
			elif 'href="' in tag: f= tag.find ("'",d)
			text = tag[d:f] +'\n'+ text
	return text

def getByPos (text, posStart):
	# posStart = pos <tag
	f= text.find ('>', posStart)
	# balise auto-fermante
	if text[f-1] == '/': return HtmlTag (text [posStart:f-1])
	else:
		# balise contenant du texte
		if " " in text[posStart:f]: f= text.find (" ", posStart)
		tagStart = text[posStart +1:f]
		tagEnd = '</'+ tagStart +'>'
		tagStart = '<'+ tagStart
		d= text.find (tagStart, posStart)
		f= text.find (tagEnd, posStart)
		nbEnd =0
		nbStart = text[d+1:f].count (tagStart)
		lenText = len (text) -3
		while nbEnd < nbStart and f< lenText:
			f= text.find (tagEnd, f+3)
			nbStart = text[d+1:f].count (tagStart)
			nbEnd = nbEnd +1
		return HtmlTag (text[d:f])

def getById (text, index):
	text = text.replace ('"', "'")
	if " id='" + index +"'" in text:
		posStart = text.find (" id='" + index +"'")
		posStart = text [:posStart].rfind ('<')
		return getByPos (text, posStart)
	else: return None

def getByClass (text, className):
	if 'class=' not in text: return []
	# repérer les balises
	textList = text.split ("class='")
	textRange = range (1, len (textList))
	for t in textRange:
		f= textList[t].find ("'")
		if className in textList[t][:f]: textList[t-1] = textList[t-1] +'$'
	text = "class='".join (textList)
	textList = text.split ('class="')
	textRange = range (1, len (textList))
	for t in textRange:
		f= textList[t].find ('"')
		if className in textList[t][:f]: textList[t-1] = textList[t-1] +'$'
	text = 'class="'.join (textList)
	# récupérer les balises
	textList =[]
	d=0
	while '$<' in text[d:]:
		d=1+ text.find ('$<',d)
		textList.append (getByPos (text, d))
		d=d+2
	text = text.replace ('$<', '<')
	return textList

def getByTag (text, tagName):
	tagStart = '<'+ tagName
	if tagStart not in text: return []
	textList =[]
	d=0
	while tagStart in text[d:]:
		d= text.find (tagStart, d)
		textList.append (getByPos (text, d))
		d=d+2
	return textList

def getcontentByTag (text, tagName):
	tagEnd = '</' + tagName + '>'
	if tagEnd not in text: return ""
	tagStart = '<'+ tagName
	f= text.rfind (tagEnd)
	d= text[:f].find (tagStart)
	d= text.find ('>',d) +1
	return text[d:f]

def getTitle (text):
	title = getcontentByTag (text, 'title')
	if not title: title = getcontentByTag (text, 'h1')
	return cleanTitle (title)

def getByTagAndClass (text, tagName, className):
	tagStart = '<'+ tagName +" "
	if tagStart not in text or className not in text: return []
	# identifier les balises d'intérêt
	textList = text.split (tagStart)
	reta = range (1, len (textList))
	for m in reta:
		fBracket= textList[t].find ('>')
		if 'class=' not in textList[t][:fBracket]: continue
		d= 7+ textList[t].find ('class=')
		f= textList[t].find ("'",d)
		if 'class="' in textList[t]: f= textList[t].find ('"',d)
		if className in textList[t][d:f]: textList[t-1] = textList[t-1] +'$'
	text = tagStart.join (textList)
	# récupérer les balises
	d=1+ text.find ('$'+ tagStart)
	textList =[]
	while '$'+ tagStart in text[d:]:
		textList.append (getByPos (text, d))
		d= 1+ text.find ('$'+ tagStart, d)
		d=d+2
	text = text.replace ('$'+ tagStart, tagStart)
	return textList

def getByClassFirst (text, className):
	if 'class=' not in text: return None
	# repérer les balises
	textList = text.split ("class='")
	lenText = len (textList)
	t=1
	while t< lenText:
		f= textList[t].find ("'")
		if className in textList[t][:f]:
			textList[t-1] = textList[t-1] +'$'
			t= lenText
		t+=1
	text = "class='".join (textList)
	textList = text.split ('class="')
	lenText = len (textList)
	t=1
	while t< lenText:
		f= textList[t].find ('"')
		if className in textList[t][:f]:
			textList[t-1] = textList[t-1] +'$'
			t= lenText
		t+=1
	text = 'class="'.join (textList)
	# récupérer les balises
	if '$<' in text:
		d=1+ text.find ('$<',d)
		return getByPos (text, d)
	else: return None

def getByTagFirst (text, tagName):
	tagStart = '<'+ tagName
	if tagStart not in text: return None
	d= text.find (tagStart)
	return getByPos (text, d)

def getByTagAndClassFirst (text, tagName, className):
	tagStart = '<'+ tagName +" "
	if tagStart not in text or className not in text: return None
	# identifier les balises d'intérêt
	textList = text.split (tagStart)
	lenText = len (textList)
	t=1
	while t< lenText:
		fBracket= textList[t].find ('>')
		if 'class=' in textList[t][:fBracket]:
			d= 7+ textList[t].find ('class=')
			f= textList[t].find ("'",d)
			if 'class="' in textList[t][:fBracket]: f= textList[t].find ('"',d)
			if className in textList[t][d:f]:
				textList[t-1] = textList[t-1] +'$'
				t= lenText
		t+=1
	text = tagStart.join (textList)
	# récupérer les balises
	if '$<' in text:
		d=1+ text.find ('$<',d)
		return getByPos (text, d)
	else: return None

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
		self.title = cleanTitle (self.title)

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

	def cleanBody (self):
		# nettoyage de base
		self.text = self.text.replace ('\n', ' ')
		self.text = self.text.replace ('\t', ' ')
		self.text = textFct.cleanBasic (self.text)
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
			self.text = self.text.replace (tag +'>', tag +'/>')

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
			self.cleanBody()
			self.setTitle()
			self.setMetas()
			self.setBody()
			self.text = self.delAttributes()
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
			self.text = self.delAttributes()
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
		title = cleanTitle (title)
		self.title = title

	""" ________________________ lire et écrire dans un fichier html ________________________ """

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
		self.setTitle()
		self.setMetas()
		self.setBody()
		# self.text = self.delAttributes()

	def write (self, mode='w'):
		# self.text ne contient plus que le corps du body
		self.text = self.text.replace ('><', '>\n<')
		self.text = self.text.replace ('>\n</', '></')
		self.meta['link'] = self.link
		self.cleanBody()
		self.title = cleanTitle (self.title)
		self.text = templateHtml % (self.title, self.getMetas(), self.text)
		File.write (self, mode)



