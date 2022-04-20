#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from classFile import File, Article, templateHtml
from classText import Text

def findTextBetweenTag (originalText, tag):
	lTag = len (tag)
	d= originalText.find ('<'+ tag) +1+ lTag
	d= originalText.find ('>', d) +1
	f= originalText.find ('</'+ tag +'>', d)
	phrase = originalText [d:f]
	phrase = phrase.strip()
	return Text (phrase)

class Html (Article):
	def __init__ (self, file=None):
		if file and file [:4] == 'http':
			Article.__init__ (self)
			self.link = file
		elif file: Article.__init__ (self, file)
		else: Article.__init__ (self)
		self.styles = []
		self.metas = {}

	def toArticle (self):
		article = Article()
		article.text = self.text
		article.path = self.path
		article.title = self.title
		article.subject = self.subject
		article.type = self.type
		article.link = self.link
		article.author = self.author
		article.autlink = self.autlink
		return article

	def toText (self):
		article = self.toArticle()
		return article.toText()

	def read (self):
		File.read (self)
		self.text = self.text.clean()
		tmpTitle = findTextBetweenTag (self.text, 'title')
		if tmpTitle and '>' not in tmpTitle and '<' not in tmpTitle: self.title = tmpTitle
		self.styles = []
		self.getCss()
		self.getMetadata()
		self.text = findTextBetweenTag (self.text, 'body')

	def write (self):
		if not self.text:
			print ('rien a ecrire pour', self.title)
			print (self.toPath())
			return
		self.title = self.title.lower()
		textInfos = self.setMetadata()
		textCss = self.setCss()
		textCss = textCss.strip()
		textInfos = textInfos + textCss
		textInfos = textInfos.strip()
		# le nouveau fichier
		for tag in listTagsIntern:
			self.text = self.text.replace ('<'+ tag +'>\n<', '<'+ tag +'><')
			self.text = self.text.replace ('>\n</'+ tag +'>', '></'+ tag +'>')
		self.text = self.text.strip()
		self.text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, textInfos, self.text)
		File.write (self)

	def clean (self):
		self.text = self.text.replace ('\t', ' ')
		self.text = self.text.replace ('\n', ' ')
		self.text = Text.clean (self.text)
		while '  ' in self.text: self.text = self.text.replace ('  ', ' ')
		self.text = self.text.replace ('> ', '>')
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace (' />', '/>')
		self.text = self.text.strip()
		self.text = self.text.replace ("''", '"')

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
		try: response = urlRequest.urlopen (myRequest, paramsUrl)
		except Exception as e: return False
		else:
			tmpByte = response.read()
			self.text = codecs.decode (tmpByte, 'utf-8', errors='ignore')
			response.close()
			self.titleFromUrl()
			return True

	def fromUrlVb (self):
		res = False
		self.title = 'tmp'
		self.toPath()
		try: urlRequest.urlretrieve (self.link, self.path)
		except Exception as e: return False
		else:
			self.read()
			remove (self.path)
			self.titleFromUrl()
			self.toPath()
			return True

	def fromUrl (self, params=None):
		self.toPath()
		res = self.fromUrlVa (params)
		if not res:
			res = self.fromUrlVb()
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
		self.title = title.replace ('_', ' ')
		self.cleanWeb()

	def fromWeb (self, url):
		self.path = 'b/\t.html'
		self.title = 'tmp'
		self.toPath()
		self.link = url
		self.fromUrl()
		# self.cleanWeb()
		self.metas = {}
		self.styles = []
		self.metas ['link'] = self.link
		self.write()

	""" ________________________ récupérer les métadonnées ________________________ """

	def getCss (self):
		# styles par défaut
		defaultCss = [
			'/home/lenovo/Bureau/site-dp/library-css/structure.css',
			'/home/lenovo/Bureau/site-dp/library-css/perso.css'
		]
		listText = self.text.split ('<link ')
		for line in listText [1:]:
			d= line.find ('href=') +6
			f= line.find ('.css', d) +4
			if line [d:f] not in self.styles and line [d:f] not in defaultCss: self.styles.append (line [d:f])

	def setCss (self):
		textCss =""
		if self.styles:
			textCss = "'/>\n\t<link rel='stylesheet' type='text/css' href='".join (self.styles)
			textCss = "<link rel='stylesheet' type='text/css' href='%s'/>" % textCss
		return textCss

	def getMetadata (self):
		listText = self.text.split ('<meta ')
		for line in listText [1:]:
			d= line.find ('name=') +6
			if d<6: continue						# ligne charset
			f= line.find ('>', d) -1
			if 'content' not in line [d:f]: continue
			metaTmp = line [d:f].split (' content=')
			metaTmp [0] = metaTmp [0] [:-1]
			if metaTmp [0] in ('stylesheet', 'viewport'): continue	# ligne viewport
			if '"' in metaTmp [0]:
				f= metaTmp [0].find ('"')
				metaTmp [0] = metaTmp [0] [:f]
			elif "'" in metaTmp [0]:
				f= metaTmp [0].find ("'")
				metaTmp [0] = metaTmp [0] [:f]
			metaTmp [1] = metaTmp [1] [1:]
			if '"' in metaTmp [1]:
				f= metaTmp [1].find ('"')
				metaTmp [1] = metaTmp [1] [:f]
			elif "'" in metaTmp [1]:
				f= metaTmp [1].find ("'")
				metaTmp [1] = metaTmp [1] [:f]
			self.metas [metaTmp [0] ] = metaTmp [1]

	def setMetadata (self):
		textInfos =""
		if self.metas.keys():
			for meta in self.metas.keys():
				tmpMeta = "<meta name='%s' content='%s'/>\n\t" % (meta, self.metas [meta])
				textInfos = textInfos + tmpMeta
		return textInfos

	def delImgLink (self):
		self.text = self.text.replace ('</div>',"")
		self.text = self.text.replace ('<div>',"")
		# supprimer les liens
		if self.contain ('<a href='):
			textList = List()
			textList.addList (self.text.split ('<a href='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = "".join (textList)
			self.text = self.text.replace ('</a>',"")
		# supprimer les images
		if self.contain ('<img src='):
			textList = List()
			textList.addList (self.text.split ('<img src='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = "".join (textList)

