#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import codecs
from os import remove
import urllib as ul
from urllib import request as urlRequest
from classFile import File, Article, templateHtml
import funcList
import funcText
import funcLogger

listTagsIntern = [ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button']
listTagsSpecial = [ 'a', 'img', 'form', 'input']
listTagsKeep = [ 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body']
listTagsKeep.extend (listTagsIntern)
listTagsKeep.extend (listTagsSpecial)
listTags = []
listTags.extend (listTagsKeep)
listTags.extend (listTagsSpecial)

def findTextBetweenTag (originalText, tag):
	lTag = len (tag)
	d= originalText.find ('<'+ tag) +1+ lTag
	d= originalText.find ('>', d) +1
	f= originalText.find ('</'+ tag +'>', d)
	phrase = originalText [d:f]
	phrase = phrase.strip()
	return phrase

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
		self.text = funcText.clean (self.text)
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
		self.text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, self.text)
		File.write (self)

	""" ________________________ netoyer le texte ________________________ """

	def clean (self):
		self.text = self.text.replace ('\t', ' ')
		self.text = self.text.replace ('\n', ' ')
		self.text = funcText.clean (self.text)
		while '  ' in self.text: self.text = self.text.replace ('  ', ' ')
		self.text = self.text.replace ('> ', '>')
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace (' />', '/>')
		self.text = self.text.strip()
		self.text = self.text.replace ("''", '"')

	def cleanLocal (self):
		self.clean()
		self.text = findTextBetweenTag (self.text, 'body')

	def cleanWeb (self):
		self.clean()
		self.text = self.text.replace ('<br/>', '<br>')
		self.text = self.text.replace ('<hr/>', '<hr>')
		# supprimer les commentaires
		self.text = self.text.replace ('< ! --', '<!--')
		self.text = self.text.replace ('< !--', '<!--')
		textList =[]
		textList.extend (self.text.split ('<!--'))
		textRange = funcList.range (textList, start=1)
		for t in textRange:
			f= textList[t].find ('-->') +3
			textList[t] = textList[t] [f:]
			self.text = "".join (textList)
		# effacer certaines balises
		# self.cleanSpan()
		self.cleanTags()
		if '</body>' in self.text: self.text = findTextBetweenTag (self.text, 'body')
		self.clean()
		for tag in listTags:
			while '<'+tag+'></'+tag+'>' in self.text: self.text = self.text.replace ('<'+tag+'></'+tag+'>',"")

	def cleanTags (self):
		# supprimer les attributs inutiles
		self.text = self.text.replace ('<br/>', '<br>')
		self.text = self.text.replace ('<hr/>', '<hr>')
		tagList =[]
		textList = (self.text.split ('<'))
		textRange = funcList.range (textList, start=1)
		# textRange.reverse()
		for t in textRange:
			if len (textList[t]) ==0: continue
			elif textList[t] [0] in '/ !': continue
			elif '>' not in textList[t]: textList[t] = textList[t] [:f] +'>'
			f= textList[t].find ('>')
			tag = textList[t][:f].lower()
			textList[t] = textList[t][f:]
			if ' ' in tag:
				f= tag.find (' ')
				attributes = tag[f:]
				tag = tag[:f]
				if tag in ('a', 'img', 'form', 'input'): tag = self.cleanTagsSpecial (tag, attributes)
				elif tag not in tagList: tagList.append (tag)
			elif tag not in tagList: tagList.append (tag)
			textList[t] = tag + textList[t]
		self.text = '<'.join (textList)
		self.text = self.text.replace (' <', '<')
		# supprimer les balises inutiles
		self.text = self.text.replace ('<img>', "")
		while '<br><br>' in self.text: self.text = self.text.replace ('<br><br>', '<br>')
		self.text = self.text.replace ('><br>', '>')
		self.text = self.text.replace ('<br><', '<')
		for tag in tagList:
			if tag not in listTagsKeep:
				self.text = self.text.replace ('</'+ tag +'>', " ")
				self.text = self.text.replace ('<'+ tag +'>', " ")
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		if '<a>' in self.text:
			textList = self.text.split ('<a>')
			textRange = funcList.range (textList, start=1)
			for a in textRange:
				d= textList[a].find ('</a>')
				textList[a] = textList[a] [:d].strip() +' '+ textList[a] [d+4:].strip()
			#	textList[a] = textList[a] [d+4:].strip()
			self.text = ' '.join (textList)
		# retrouver les balises vides
		self.clean()
		self.text = self.text.replace ('\n', "")
		for tag in tagList: self.text = self.text.replace ('<'+ tag +'></'+ tag +'>', " ")
		while "  " in self.text: self.text = self.text.replace ("  "," ")

	def cleanTagsSpecial (self, tag, attributeList):
		if tag == 'a': return self.keepAttribute ('a', 'href', attributeList)
		elif tag == 'img': return self.keepAttribute ('img', 'src', attributeList)
		elif tag == 'input': return self.keepAttributeInput (attributeList)
		elif tag == 'form': return self.keepAttributeForm (attributeList)

	def keepAttribute (self, tag, attr, attributeList):
		if attr in attributeList:
			tag = tag +' '+ attr +"='"
			d= attributeList.find (attr) +2+ len (attr)
			quote = attributeList [d-1]
			if quote in '"\'':
				f= attributeList.find (quote, d)
				tag = tag + attributeList [d:f] +"'"
			else:
				d-=1
				tag = tag + attributeList [d:] +"'"
		return tag

	def keepAttributeInput (self, attributeList):
		tag = 'input'
		for attr in ('type', 'name', 'value', 'placeholder'):
			if attr +'=' in attributeList:
				tag = tag +' '+ attr +"='"
				d= attributeList.find (attr) +2+ len (attr)
				quote = attributeList [d-1]
				if quote in '"\'':
					f= attributeList.find (quote, d)
					tag = tag + attributeList [d:f] +"'"
				else:
					d-=1
					tag = tag + attributeList [d:] +"'"
		return tag

	def keepAttributeForm (self, attributeList):
		tag = 'form'
		for attr in ('action', 'method'):
			if attr in attributeList:
				tag = tag +' '+ attr +"='"
				d= attributeList.find (attr) +2+ len (attr)
				quote = attributeList [d-1]
				if quote in '"\'':
					f= attributeList.find (quote, d)
					tag = tag + attributeList [d:f] +"'"
				else:
					d-=1
					tag = tag + attributeList [d:] +"'"
		return tag

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
			self.titleFromUrl()
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
			remove (self.path.replace ('\t', 'tmp'))
			self.titleFromUrl()
			self.toPath()
			return True

	def fromUrl (self, params=None):
		self.toPath()
		res = False
		if params: res = self.fromUrlVa (params)
		else: res = self.fromUrlVb()
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

	def fromWeb (self, url=None):
		# remove (self.path)
		self.path = 'b/tmp.html'
		self.fromPath()
		if url: self.link = url
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
		self.text = self.text.replace ('<META NAME', '<meta name')
		self.text = self.text.replace ('<META ', '<meta ')
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

		listText = self.text.split ('<link ')
		for line in listText [1:]:
			if '.css' not in line:
				da= line.find ('rel=') +5
				fa= funcText.find (line, "'", da)
				db= line.find ('href=') +6
				fb= funcText.find (line, "'", db)
				self.metas [line [da:fa]] = line [db:fb]


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
		if '<a href=' in self.text:
			textList =[]
			textList.extend (self.text.split ('<a href='))
			textRange = funcList.range (textList, start=1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = " ".join (textList)
			self.text = self.text.replace ('</a>'," ")
		# supprimer les images
		if '<img src=' in self.text:
			textList =[]
			textList.extend (self.text.split ('<img src='))
			textRange = funcList.range (textList, start=1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = " ".join (textList)
		self.text = funcText.clean (self.text)
