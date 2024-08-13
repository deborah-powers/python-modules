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

	# ________________________ manipuler les noeuds ________________________

	def delAttributes (self):
		attributes = self.attributes.keys()
		for attr in attributes:
			if attr not in listAttributes: self.attributes.pop (attr)
		for child in self.children: child.delAttributes()
		self.toInnerHtml()

	def delId (self):
		self.className =""
		self.id =""
		for child in self.children: child.delId()
		self.toInnerHtml()

	def delScript (self):
		tags = self.getAllByTag ('script')
		for tag in tags: self.delete (tag)
		tags = self.getAllByTag ('style')
		for tag in tags: self.delete (tag)

	def delete (self, childToDel):
		if len (self.children) ==0: return None
		elif childToDel in self.children:
			d= self.children.index (childToDel)
			return self.children.pop (d)
		else:
			c=0
			lenChildren = len (self.children)
			res = None
			while c< lenChildren and not res:
				res = self.children[c].delete (childToDel)
				c+=1
			return res
	# ________________________ récupérer les noeuds d'intérêt ________________________

	def getOneByTag (self, tagName):
		tagok = lambda tag: tag.tag == tagName
		return self.getOne (tagok)

	def getOneById (self, index):
		idok = lambda tag: tag.id == index
		return self.getOne (idok)

	def getOneByClass (self, className):
		classok = lambda tag: tag.className == className
		return self.getOne (classok)

	def getOneByTagClass (self, tagName, className):
		tagok = lambda tag: tag.tag == tagName and tag.className == className
		return self.getOne (tagok)

	def getOneByAttribute (self, attributeName, attributeValue):
		attrok = lambda tag: attributeName in tag.attributes.keys() and tag.attributes[attributeName] == attributeValue
		return self.getOne (attrok)

	def getOne (self, funcFound):
		if funcFound (self): return self
		elif len (self.children) ==0: return None
		else:
			c=0
			nbChildren = len (self.children)
			newTag = None
			while newTag == None and c< nbChildren:
				newTag = self.children[c].getOne (funcFound)
				c+=1
			return newTag

	def getAllByTag (self, tagName):
		tagok = lambda tag: tag.tag == tagName
		return self.getAll (tagok)

	def getAllByClass (self, className):
		classok = lambda tag: tag.className == className
		return self.getAll (classok)

	def getAllByTagClass (self, tagName, className):
		tagok = lambda tag: tag.tag == tagName and tag.className == className
		return self.getAll (tagok)

	def getAllByAttribute (self, attributeName, attributeValue):
		attrok = lambda tag: attributeName in tag.attributes.keys() and tag.attributes[attributeName] == attributeValue
		return self.getAll (attrok)

	def getAll (self, funcFound):
		tags =[]
		if funcFound (self): tags.append (self)
		for child in self.children:
			newTags = child.getAll (funcFound)
			tags.extend (newTags)
		return tags

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
			self.setChildren()

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

	def setChildren (self):
		self.children =[]
		if '<' not in self.innerHtml or '>' not in self.innerHtml or self.tag == 'text': return
		elif '<' not in self.innerHtml: return
		d= self.innerHtml.find ('<')
		if d>0: self.children.append (HtmlTag (self.innerHtml[:d]))
		lenHtml = self.lenght()
		while d< lenHtml and '<' in self.innerHtml[d:]:
			if self.innerHtml[d] =='<' and self.innerHtml[d+1] in 'abcdefghilmnopqrstv':
				newTag = HtmlTag (self.innerHtml[d:])
				d= self.innerHtml.find (newTag.innerHtml, d+1)
				d= d+ len (newTag.innerHtml)
				d=1+ self.innerHtml.find ('>',d+1)
				self.children.append (newTag)
				if d< lenHtml and self.innerHtml[d] !='<':
					f= self.innerHtml.find ('<',d)
					if f<0: f= self.lenght()
					self.children.append (HtmlTag (self.innerHtml[d:f]))
			else: d= self.innerHtml.find ('<', d+1)
		# éliminer les emboîtements inutiles
		if len (self.children) ==1:
			if self.children[0].tag == 'text': self.children =[]
			elif self.tag == 'a':
				if self.children[0].tag not in listTagsSelfClosing and self.children[0].tag != 'svg': self.unnestOneChild()
			elif self.children[0].tag == 'span': self.unnestOneChild()
			elif self.tag != 'svg':
				self.tag = self.children[0].tag
				self.attributes ={}
				attributes = self.children[0].attributes.keys()
				for attr in attributes: self.attributes[attr] = self.children[0].attributes[attr]
				self.unnestOneChild()

	def unnestOneChild (self):
		self.innerHtml = self.children[0].innerHtml
		if not self.id and self.children[0].id: self.id = self.children[0].id
		if self.children[0].className:
			if self.className: self.className = self.className +" "+ self.children[0].className
			else: self.className = self.children[0].className
		for child in self.children[0].children: self.children.append (child)
		self.children.pop (0)

	# ________________________ manipulations basiques ________________________

	def lenght (self):
		return len (self.innerHtml)

	def __lt__ (self, other):
		if self.tag < other.tag: return True
		elif self.className < other.className: return True
		elif self.id < other.id: return True
		elif self.tag == 'a' and other.tag == 'a':
			if self.attributes['href'] < other.attributes['href']: return True
			elif self.innerHtml < other.innerHtml: return True
			else: return False
		elif self.tag == 'img' and other.tag == 'img':
			if self.attributes['src'] < other.attributes['src']: return True
			if self.attributes['alt'] < other.attributes['alt']: return True
			else: return False
		elif self.innerHtml < other.innerHtml: return True
		else: return False

	def toInnerHtml (self):
		if not self.children: return
		self.innerHtml =""
		for child in self.children: self.innerHtml = self.innerHtml + child.__str__()

	def __str__ (self):
		if self.tag == 'text': return self.innerHtml
		tagStr = '<'+ self.tag
		if self.className: tagStr = tagStr +" class='"+ self.className +"'"
		if self.id: tagStr = tagStr +" id='"+ self.id +"'"
		if self.attributes:
			attributes = self.attributes.keys()
			for attr in attributes: tagStr = tagStr +" "+ attr +"='"+ self.attributes[attr] +"'"
		if self.tag in listTagsSelfClosing: tagStr = tagStr +'/>'
		else: tagStr = tagStr +'>'+ self.innerHtml +'</'+ self.tag +'>'
		return tagStr

	# ________________________ auxilières ________________________

def cleanTitle (title):
	title = title.lower()
	charToErase = '-_.:;,?/\\'
	for char in charToErase: title = title.replace (char," ")
	title = textFct.cleanBasic (title)
	return title

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
		return self.tree.getOneByTag (tagName)

	def getOneByClass (self, className):
		return self.tree.getOneByClass (className)

	def getOneById (self, index):
		return self.tree.getOneById (index)

	def getOneByTagClass (self, tagName, className):
		return self.tree.getOneByTagClass (tagName, className)

	def getOneByAttribute (self, attributeName, attributeValue):
		return self.tree.getOneByAttribute (attributeName, attributeValue)

	def getAllByTag (self, tagName):
		return self.tree.getAllByTag (tagName)

	def getAllByClass (self, className):
		return self.tree.getAllByClass (className)

	def getAllByTagClass (self, tagName, className):
		return self.tree.getAllByTagClass (tagName, className)

	def getAllByAttribute (self, attributeName, attributeValue):
		return self.tree.getAllByAttribute (attributeName, attributeValue)

	def setByTag (self, tagName):
		node = self.tree.getOneByTag (tagName)
		self.setFromTag (node)

	def setByClass (self, className):
		node = self.tree.getOneByClass (className)
		self.setFromTag (node)

	def setById (self, index):
		node = self.tree.getOneById (index)
		self.setFromTag (node)

	def setByTagClass (self, tagName, className):
		node = self.tree.getOneByTagClass (tagName, className)
		self.setFromTag (node)

	def setByAttribute (self, attributeName, attributeValue):
		node = self.tree.getOneByAttribute (attributeName, attributeValue)
		self.setFromTag (node)

	def setFromTag (self, node):
		if node != None:
			self.tree = node
			self.text = node.innerHtml
			self.tree.tag = 'body'

	# ________________________ finir la lecture, préparer l'écriture ________________________

	def setHtml (self):
		d= self.text.find ('<html')
		f=7+ self.text.rfind ('</html>')
		self.tree = HtmlTag (self.text[d:f])
		self.text = self.tree.innerHtml

	def setTitle (self):
		if '</title>' in self.text: self.title = cleanTitle (self.getOneByTag ('title').innerHtml)
		elif '</h1>' in self.text: self.title = cleanTitle (self.getOneByTag ('h1').innerHtml)

	def setMain (self):
		if '</main>' in self.text: self.setByTag ('main')
		if self.text.count ('</article>') ==1: self.setByTag ('article')
	#	if self.text.count ('</section>') ==1: self.setByTag ('section')

	def setMetas (self):
		metaList = self.tree.getAllByTag ('meta')
		self.meta ={}
		for meta in metaList:
			attributes = meta.attributes.keys()
			if 'content' in attributes and 'name' in attributes and meta.attributes['name'][:5] != 'csrf-':
				self.meta [meta.attributes['name']] = meta.attributes['content']
			self.tree.delete (meta)

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

	def write (self, mode='w'):
		# self.text ne contient plus que le corps du body
		self.addIndentation()
		self.meta['link'] = self.link
		self.title = cleanTitle (self.title)
		self.text = templateHtml % (self.title, self.getMetas(), self.text)
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

	def delId (self):
		self.tree.delId()
		self.text = self.tree.innerHtml

	def delScript (self):
		while '</script>' in self.text:
			d= self.text.find ('<script')
			f=9+ self.text.find ('</script>')
			self.text = self.text[:d] + self.text[f:]
		while '</style>' in self.text:
			d= self.text.find ('<style')
			f=8+ self.text.find ('</style>')
			self.text = self.text[:d] + self.text[f:]
		while '<!--' in self.text:
			d= self.text.find ('<!--')
			f=3+ self.text.find ('-->')
			self.text = self.text[:d] + self.text[f:]

	def cleanBody (self):
		self.text = textFct.cleanHtml (self.text)
		# standardiser tags
		for tag in listTags:
			self.replace ('<'+ tag.upper(), '<'+ tag)
			self.replace ('</'+ tag.upper(), '</'+ tag)
		for tag in listTagsSelfClosing:
			self.replace ('<'+ tag.upper(), '<'+ tag)
			self.replace (tag +'>', tag +'/>')
		self.setHtml()
		self.setTitle()
		self.setMetas()
		self.setByTag ('body')
	#	self.delScript()
