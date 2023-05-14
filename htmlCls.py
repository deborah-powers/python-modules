#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import codecs
from os import remove
import urllib as ul
from urllib import request as urlRequest
from fileCls import File, Article, templateHtml
import listFct
import textFct
import loggerFct as log

help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python htmlClass.py fichier.html
"""

listTagsIntern = [ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button']
listTagsSpecial = [ 'a', 'img', 'form', 'input']
listTagsKeep = [ 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body']
listTagsKeep.extend (listTagsIntern)
listTagsKeep.extend (listTagsSpecial)
listTags = []
listTags.extend (listTagsKeep)
listTags.extend (listTagsSpecial)

def findTextBetweenTag (originalText, tag):
	d= originalText.find ('<'+ tag) +1+ len (tag)
	d= originalText.find ('>', d) +1
	f= originalText.find ('</'+ tag +'>', d)
	phrase = originalText [d:f]
	phrase = phrase.strip()
	return phrase

def getAttributeValue (text, attribute):
	d= text.find (attribute +'=') +2+ len (attribute)
	f= text.find (text[d-1], d)
	return text[d:f]

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

	def read (self, getMeta=False):
		File.read (self)
		self.text = textFct.cleanHtml (self.text)
		tmpTitle = findTextBetweenTag (self.text, 'title')
		if tmpTitle and '>' not in tmpTitle and '<' not in tmpTitle: self.title = tmpTitle
		self.cleanTitle()
		self.styles = []
		if getMeta:
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
		self.text = self.text.strip()
		self.text = templateHtml % (self.title, self.author, self.subject, self.link, self.autlink, textInfos, self.text)
		File.write (self)

	""" ________________________ netoyer le texte ________________________ """

	def clean (self):
		self.text = textFct.cleanHtml (self.text)
		self.text = self.text.replace ('> ', '>')
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace (' />', '/>')
		self.text = self.text.strip()
		self.text = self.text.replace ("''", '"')

	def cleanLocal (self):
		self.cleanHtml()
		self.text = findTextBetweenTag (self.text, 'body')

	def cleanWeb (self):
		for tag in listTags:
			self.text = self.text.replace ('<'+ tag.upper(), '<'+ tag)
			self.text = self.text.replace ('</'+ tag.upper(), '</'+ tag)
			while '<'+tag+'></'+tag+'>' in self.text: self.text = self.text.replace ('<'+tag+'></'+tag+'>',"")
		self.clean()
		# supprimer les commentaires
		self.text = self.text.replace ('< ! --', '<!--')
		self.text = self.text.replace ('< !--', '<!--')
		textList =[]
		textList.extend (self.text.split ('<!--'))
		textRange = listFct.range (textList, start=1)
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
		tagList =[]
		textList = (self.text.split ('<'))
		textRange = listFct.range (textList, start=1)
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
		self.text = self.text.replace ('<hr>', '<hr/>')
		# supprimer les balises inutiles
		self.text = self.text.replace ('<img>', "")
		self.text = self.text.replace ('<br/>', '<br>')
		while '<br><br>' in self.text: self.text = self.text.replace ('<br><br>', '<br>')
		self.text = self.text.replace ('><br>', '>')
		self.text = self.text.replace ('<br><', '<')
		self.text = self.text.replace ('<br>', '</p><p>')
		# les images
		self.text = self.text.replace (".jpg'>", ".jpg'/>")
		self.text = self.text.replace (".png'>", ".png'/>")
		self.text = self.text.replace (".bmp'>", ".bmp'/>")
		self.text = self.text.replace (".svg'>", ".svg'/>")
		self.text = self.text.replace ('.jpg">', '.jpg"/>')
		self.text = self.text.replace ('.png">', '.png"/>')
		self.text = self.text.replace ('.bmp">', '.bmp"/>')
		self.text = self.text.replace ('.svg">', '.svg"/>')
		for tag in tagList:
			if tag not in listTagsKeep:
				self.text = self.text.replace ('</'+ tag +'>', " ")
				self.text = self.text.replace ('<'+ tag +'>', " ")
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		if '<a>' in self.text:
			textList = self.text.split ('<a>')
			textRange = listFct.range (textList, start=1)
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
		self.title = title
		self.cleanTitle()
		self.cleanWeb()

	def cleanTitle (self):
		charToDelete = '\\/:;\n\t_'
		for char in charToDelete: self.title = self.title.replace (char, " ")
		while "  " in self.title: self.title = self.title.replace ("  ", " ")

	def fromWeb (self, url=None):
		# remove (self.path)
		self.path = 'b/tmp.html'
		self.fromPath()
		if url: self.link = url
		self.fromUrl()
		log.log (self.text)
		# self.cleanWeb()
		self.metas = {}
		self.styles = []
		self.metas ['link'] = self.link
		self.write()

	def getById (self, id):
		d= self.text.find ("id='" +id +"'")
		if d<0: d= self.text.find ('id="' +id +'"')
		if d<0: return ""
		d= self.text[:d].rfind ('<')
		f= self.text.find (' ',d)
		return self.getTag (d,f)

	def getByClass (self, className, tagName=""):
		d= self.text.find ("class='" + className +"'")
		if d<0: d= self.text.find ('class="' + className +'"')
		if d<0: return ""
		d= self.text[:d].rfind ('<')
		f= self.text.find (' ',d)
		if tagName and self.text[d+1:f] != tagName:
			while self.text[d+1:f] != tagName:
				f= self.text.find ('>',d)
				d= self.text.find ("class='" + className +"'", f)
				if d<0: d= self.text.find ('class="' + className +'"', f)
				if d<0: return ""
				d= self.text[:d].rfind ('<')
				f= self.text.find (' ',d)
		return self.getTag (d,f)

	def getByTag (self, tagName):
		d= self.text.find ('<'+ tagName +' ')
		if tagName not in ('hr', 'br', 'img', 'input'):
			f= self.text.find ('<'+ tagName +'>')
			if d<0 and f<0: return ""
			elif d<0 or (d>f and f>=0): d=f
		if d<0: return ""
		else: return self.getTag (d)

	def getTag (self, d,f=-1):
		""" exemples de résultats
			a	http://www.ref.fr	message du lien
			img	http://www.src.png
			p	le <i>contenu</i> du paragraphe
			input	text	valeur du message
			hr
		anciens exemples
			hr id='hr-id' class='hr-class'
			div id='div-id' class='div-class'><p>bonjour</p><hr id='hr-a'><hr id='hr-id' class='hr-class'/><p>me voila</p>
		"""
		d=d+1
		if f<0: f= min ( self.text.find ('>',d), self.text.find ('/',d), self.text.find (' ',d) )
		tagName = self.text[d:f]
		content =""
		if tagName in ('hr', 'br', 'img', 'input'):
			f= self.text.find ('>',d)
			content = self.text[d:f]
			if content[-1] =='/': content = content[:-1]
			# récupérer les données importantes
			if tagName in ' br hr': return tagName
			elif tagName == 'img': content = 'img\t' + getAttributeValue (content, 'src')
			elif tagName == 'input': content = 'input\t%s\t%s' %( getAttributeValue (content, 'type'), getAttributeValue (content, 'value'))
		else:
			# trouver les positions des brackets complémentaires
			f= self.text.index ('</'+ tagName +'>', d)
			totD = self.text[d:f].count ('<'+ tagName)
			totF = self.text[d:f].count ('</'+ tagName +'>')
			while totD > totF:
				f= self.text.index ('</'+ tagName +'>', f+1)
				totD = self.text[d:f].count ('<'+ tagName)
				totF = self.text[d:f].count ('</'+ tagName +'>')
			content = self.text[d:f]
			# récupérer les données importantes
			tagName = tagName +'\t'
			if tagName == 'a\t': tagName = tagName + getAttributeValue (content, 'href') +'\t'
			d=1+ content.find ('>')
			content = tagName + content[d:]
		return content

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
			if d<f and line[d:f] not in self.styles and line [d:f] not in defaultCss:
				self.styles.append (line [d:f])

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
			f= line.find ('>') -1
			if 'name=' in line[:f] and 'content=' in line[:f]:
				# éviter les lignes charset et viewport
				d= line.find ('name=') +6
				metaTmp = line [d:f].split (' content=')
				metaTmp[0] = metaTmp[0].strip()
				metaTmp[0] = metaTmp[0][:-1]
				metaTmp[1] = metaTmp[1].strip()
				metaTmp[1] = metaTmp[1][1:-1]
				if metaTmp[0] != 'viewport': self.metas [metaTmp[0]] = metaTmp[1]

		listText = self.text.split ('<link ')
		for line in listText [1:]:
			f= line.find ('>')
			styleTmp = line[:f]
			styleTmp = styleTmp.replace ('""','o')
			styleTmp = styleTmp.replace ("''",'o')
			styleTmp = styleTmp.replace ('"',"")
			styleTmp = styleTmp.replace ("'","")
			if styleTmp[-1] =='/': styleTmp = styleTmp[:-1]
			styleTmp = styleTmp.strip()
			if 'rel=stylesheet' not in styleTmp:
				styleTmp = styleTmp.replace ('='," ")
				styleTmpList = styleTmp.split (" ")
				d= styleTmpList.index ('rel') +1
				f= styleTmpList.index ('href') +1
				if styleTmpList[f] !='o' and styleTmpList[d] !='o': self.metas [styleTmpList[d]] = styleTmpList[f]

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
			textRange = listFct.range (textList, start=1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = " ".join (textList)
			self.text = self.text.replace ('</a>'," ")
		# supprimer les images
		if '<img src=' in self.text:
			textList =[]
			textList.extend (self.text.split ('<img src='))
			textRange = listFct.range (textList, start=1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = " ".join (textList)
		self.text = textFct.cleanHtml (self.text)

if __name__ == '__main__':
	if len (argv) >1:
		htmlFile = Html (argv[1])
		htmlFile.read()
		htmlFile.clean()
		htmlFile.cleanWeb()
		htmlFile.write()
	else: print (help)
