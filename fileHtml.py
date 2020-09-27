#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from htmlCreate import textToHtml, htmlToText
from fileClass import *

help ="""lancer le script
	python fileHtml.py url"""

listTagsIntern =[ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button']
listTagsSpecial =[ 'a', 'img', 'form', 'input']
listTagsKeep =[ 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'header', 'footer', 'section', 'div', 'body']
listTagsKeep.extend (listTagsIntern)
listTagsKeep.extend (listTagsSpecial)
listTags =[]
listTags.extend (listTagsKeep)
listTags.extend (listTagsSpecial)

htmlTemplate ="""<!DOCTYPE html><html><head>
	<title>%s</title>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	%s
	<link rel='stylesheet' type='text/css' href='/home/lenovo/Bureau/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='/home/lenovo/Bureau/site-dp/library-css/perso.css'/>
	<base target='_blank'>
</head><body>
%s
</body></html>"""

def findTextBetweenTag (originalText, tag):
	lTag = len (tag)
	d= originalText.find ('<'+ tag) +1+ lTag
	d= originalText.find ('>', d) +1
	f= originalText.find ('</'+ tag +'>', d)
	phrase = originalText[d:f]
	phrase = phrase.strip()
	return phrase

class ArticleHtml (Article):
	# classe pour les fichiers html
	def __init__(self, file =None):
		if file and file[:4] == 'http':
			Article.__init__(self)
			self.link = file
		elif file: Article.__init__(self, file)
		else: Article.__init__(self)
		self.extension = 'html'
		self.styles =[]
		self.metas ={}

	""" ________________________ manipuler les fichiers ________________________ """

	def fromFile (self):
		FilePerso.fromFile (self)
		self.clean()
		tmpTitle = findTextBetweenTag (self.text, 'title')
		if tmpTitle and '>' not in tmpTitle and '<' not in tmpTitle: self.title = tmpTitle
		self.styles =[]
		self.getCss()
		self.getMetadata()
		if 'link' in self.metas.keys(): self.link = self.metas['link']
		if 'author' in self.metas.keys(): self.author = self.metas['author']
		if 'subject' in self.metas.keys(): self.subject = self.metas['subject']
		if 'autlink' in self.metas.keys(): self.autlink = self.metas['autlink']
		self.text = findTextBetweenTag (self.text, 'body')

	def toFile (self):
	#	pas de text, ""
		if not self.text:
			print ('rien a ecrire pour', self.title)
			print (self.file)
			return
		self.title = self.title.lower()
		self.author = self.author.lower()
		self.subject = self.subject.lower()
		self.metas['author'] = self.author
		self.metas['subject'] = self.subject
		self.metas['link'] = self.link
		self.metas['autlink'] = self.autlink
		textInfos = self.setMetadata()
		textCss = self.setCss()
		textInfos = textInfos + textCss
		textInfos = textInfos.strip()
		# le nouveau fichier
		for tag in listTagsIntern:
			self.replace ('<'+ tag +'>\n<', '<'+ tag +'><')
			self.replace ('>\n</'+ tag +'>', '></'+ tag +'>')
		self.text = htmlTemplate %( self.title, textInfos, self.text)
		FilePerso.toFile (self)

	def clean (self):
		self.replace ('\t', ' ')
		self.replace ('\n', ' ')
		FilePerso.clean (self)
		self.replace ('  ', ' ')
		self.replace ('> ', '>')
		self.replace (' <', '<')
		self.replace (' />', '/>')
		self.text = self.text.strip()
		self.replace ('"', "'")
		# rajouter des espaces autour des liens
		self.replace ('</a>', ' </a>')
		self.replace ('">', '"> ')
		self.replace ("'>", "'> ")

	def __str__ (self):
		strFic = 'Titre: %s, Fichier: %s' %( self.title, self.file)
		if self.metas:
			strFic = strFic + '\nMeta:'
			for meta in self.metas.keys(): strFic = strFic +'\n\t%s\t%s' %( meta, self.metas[meta])
		if self.styles:
			strFic = strFic + '\nStyle:'
			for css in self.styles: strFic = strFic +'\n\t%s' %css
		return strFic

	""" ________________________ récupérer les métadonnées ________________________ """

	def getCss (self):
		# styles par défaut
		defaultCss =[
			'/home/lenovo/Bureau/site-dp/library-css/structure.styles',
			'/home/lenovo/Bureau/site-dp/library-css/perso.styles'
		]
		listText = self.text.split ('<link ')
		for line in listText[1:]:
			d= line.find ('href=') +6
			f= line.find ('.css', d) +4
			if line[d:f] not in self.styles and line[d:f] not in defaultCss: self.styles.append (line[d:f])

	def setCss (self):
		textCss =""
		if self.styles:
			textCss = "'/>\n\t<link rel='stylesheet' type='text/css' href='".join (self.styles)
			textCss = "<link rel='stylesheet' type='text/css' href='%s'/>" % textCss
		return textCss

	def getMetadata (self):
		"""
		tmpText = self.text.replace ('<link rel=', '<meta name=')
		tmpText = tmpText.replace (' href=', ' content=')
			elif 'stylesheet' in metaTmp[0]: continue			# artéfact
		"""
		listText = self.text.split ('<meta ')
		for line in listText[1:]:
			d= line.find ('name=') +6
			if d<6: continue						# ligne charset
			f= line.find ('>', d) -1
			if 'content' not in line[d:f]: continue
			metaTmp = line[d:f].split (' content=')
			metaTmp[0] = metaTmp[0][:-1]
			if metaTmp[0] in ('stylesheet', 'viewport'): continue	# ligne viewport
			if '"' in metaTmp[0]:
				f= metaTmp[0].find ('"')
				metaTmp[0] = metaTmp[0][:f]
			elif "'" in metaTmp[0]:
				f= metaTmp[0].find ("'")
				metaTmp[0] = metaTmp[0][:f]
			metaTmp[1] = metaTmp[1][1:]
			if '"' in metaTmp[1]:
				f= metaTmp[1].find ('"')
				metaTmp[1] = metaTmp[1][:f]
			elif "'" in metaTmp[1]:
				f= metaTmp[1].find ("'")
				metaTmp[1] = metaTmp[1][:f]
			self.metas[metaTmp[0]] = metaTmp[1]

	def setMetadata (self):
		textInfos =""
		if self.metas.keys():
			for meta in self.metas.keys():
				tmpMeta = "<meta name='%s' content='%s'/>\n\t" %( meta, self.metas[meta])
				textInfos = textInfos + tmpMeta
		return textInfos

	""" ________________________ convertir en texte ________________________ """

	def fromArticle (self, ftext):
		# file est un fichier txt utilisant ma mise en forme
		if not ftext.text: ftext.fromFile()
		ftext.shape()
		self.copyFile (ftext)
		self.text = textToHtml (ftext.text)
		self.toFile()

	def fromArticleName (self, fileName):
	#	ftext = FilePerso (fileName)
		ftext = Article (fileName)
		self.fromArticle (ftext)

	def toArticle (self):
		# fileHtml a été cré avec textToHtml
		# récupérer le texte
		if not self.text: self.fromFile()
		self.clean()
		ftext = Article()
		ftext.copyFile (self)
		ftext.extension = 'txt'
		ftext.fileFromData()
		# les titres
		ftext.replace ('<h1>', '\n______\n______ ')
		ftext.replace ('<h2>', '\n______ ')
		ftext.replace ('<h3>', '\n------ ')
		ftext.replace ('<h4>', '\n--- ')
		ftext.replace ('</h4>', ' ---\n')
		ftext.replace ('</h3>', ' ------\n')
		ftext.replace ('</h2>', ' ______\n')
		ftext.replace ('</h1>', ' ______\n')
		# les conteneurs
		container =[ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
		for tag in container:
			ftext.replace ('</'+ tag +'>')
			ftext.replace ('<'+ tag +'>')
		# les tableaux
		ftext.replace ('th>', 'td>')
		ftext.replace ('</td><td>', '\t')
		ftext.replace ('</td></tr><tr><td>', '\n')
		ftext.replace ('<tr>', '\n')
		ftext.replace ('</tr>', '\n')
		# les listes
		ftext.replace ('</li><li>', '\n\t')
		ftext.replace ('<li>', '\n\t')
		ftext.replace ('</li>', '\n')
		# les lignes
		ftext.replace ('</p><p>', '\n')
		lines =[ 'p', 'caption', 'figcaption' ]
		for tag in lines:
			ftext.replace ('</'+ tag +'>', '\n')
			ftext.replace ('<'+ tag +'>', '\n')
		# les phrases
		inner =[ 'span', 'em', 'strong' ]
		for tag in inner:
			ftext.replace ('</'+ tag +'>', ' ')
			ftext.replace ('<'+ tag +'>', ' ')
		ftext.replace (' \n', '\n')
		ftext.replace ('\n ', '\n')
		# autres
		ftext.replace ('<hr>', '\n________________________\n')
		ftext.replace ('<hr/>', '\n________________________\n')
		ftext.replace ('<br>', '\n')
		ftext.replace ('<br/>', '\n')
		ftext.clean()
		ftext.toFile()

	""" ________________________ texte du web ________________________ """

	def fromUrl (self, params=None):
		# récupérer le texte. les params servent à remplir les formulaires
		myRequest = None
		if params:
			paramsUrl = ul.urlencode (params).encode ('utf-8')
			myRequest = urlRequest.Request (self.link, paramsUrl)
		else: myRequest = urlRequest.Request (self.link)
		try: response = urlRequest.urlopen (myRequest)
		except Exception as e:
			print ("le fichier n'est pas téléchargeable:\n", self.link)
			return
		else:
			tmpByte = response.read()
			self.text = codecs.decode (tmpByte, 'utf-8', errors='ignore')
			response.close()
			# récupérer le titre
			title = self.link.strip ('/')
			pos = title.rfind ('/') +1
			title = title[pos:]
			endTitle = '?.'
			for end in endTitle:
				if end in title:
					pos = title.rfind (end)
					title = title[:pos]
			if title.count ('-') >1: title = title.replace ('-', ' ')
			self.title = title.replace ('_', ' ')
			self.clean()

	def cleanLocal (self):
		FileHtml.clean()
		self.text = findTextBetweenTag (self.text, 'body')

	def cleanWeb (self):
		self.clean()
		# supprimer les commentaires
		textList = ListPerso()
		textList.extend (self.text.split ('<!--'))
		textRange = textList.range (1)
		for t in textRange:
			f= textList[t].find ('-->') +3
			textList[t] = textList[t][f:]
			self.text = "".join (textList)
		# effacer certaines balises
		self.cleanSpan()
		self.cleanTags()
	#	self.cleanTags()
		self.text = findTextBetweenTag (self.text, 'body')
		self.clean()

	def cleanTags (self):
		# supprimer les attributs inutiles
		tagList = ListPerso()
		textList = ListPerso()
		textList.extend (self.text.split ('<'))
		textRange = textList.range (1)
		textRange.reverse()
		for t in textRange:
			if len (textList[t]) ==0: continue
			elif '>' not in textList[t] or textList[t][0] in '/!': continue
			f= textList[t].find ('>')
			tag = textList[t][:f].lower()
			textList[t] = textList[t][f:]
			if ' ' in tag:
				f= tag.find (' ')
				attributes = tag[f:]
				tag = tag[:f]
				if tag in ('a', 'img'): tag = self.cleanTagsSpecial (tag, attributes)
				elif tag not in tagList: tagList.append (tag)
			elif tag not in tagList and tag not in ('a', 'img'): tagList.append (tag)
			textList[t] = tag+ textList[t]
		self.text = '<'.join (textList)
		self.replace (' <', '<')
		# supprimer les balises inutiles
		self.replace ('<img>')
		while '<br><br>' in self.text: self.replace ('<br><br>', '<br>')
		self.replace ('><br>', '>')
		self.replace ('<br><', '<')
		for tag in tagList:
			if tag not in listTagsKeep:
				self.replace ('</'+ tag +'>')
				self.replace ('<'+ tag +'>')
		if self.contain ('<a>'):
			textList = ListPerso()
			textList.extend (self.text.split ('<a>'))
			textRange = textList.range (1)
			for a in textRange:
				d= textList[a].find ('</a>')
				textList[a] = textList[a][:d].strip() +' '+ textList[a][d+4:].strip()
			#	textList[a] = textList[a][d+4:].strip()
			self.text = ' '.join (textList)
		# retrouver les balises vides
		for tag in tagList: self.replace ('<'+ tag +'></'+ tag +'>')

	def cleanTagsSpecial (self, tag, attributeList):
		if tag == 'a':
			return self.keepAttribute ('a', 'href', attributeList)
		elif tag == 'img': return self.keepAttribute ('img', 'src', attributeList)

	def keepAttribute (self, tag, attr, attributeList):
		if attr in attributeList:
			tag = tag +' '+ attr +"='"
			d= attributeList.find (attr) +2+ len (attr)
			quote = attributeList[d-1]
			if quote in '"\'':
				f= attributeList.find (quote, d)
				tag = tag + attributeList[d:f] +"'"
			else:
				d-=1
				tag = tag + attributeList[d:] +"'"
		return tag

	def delScript (self):
		if not self.contain ('</script>'): return
		txtList = self.text.split ('</script>')
		rangeTxt = range (len (txtList) -1)
		for t in rangeTxt:
			pos = txtList[t].rfind ('<script')
			txtList[t] = txtList[t][:pos]
		self.text = "".join (txtList)

	def cleanSpan (self):
		# supprimer les span en trop
		self.replace ('<SPAN', '<span')
		self.replace ('</SPAN', '</span')
		textList = ListPerso()
		textList.extend (self.text.split ('<span '))
		textRange = textList.range (1)
		textRange.reverse()
		for t in textRange:
			f= textList[t].find ('>')
			textList[t] = textList[t][f:]
		self.text = '<span'.join (textList)
		self.replace ('</span>=', '=')
		self.replace ('<</span>', '<')
		self.replace ('<span>>', '>')
		self.replace ('<span>', ' ')
		self.replace ('</span>', ' ')
		# supprimer les liens en trop
		textList = ListPerso()
		textList.extend (self.text.split ('="<a '))
		textRange = textList.range (1)
		textRange.reverse()
		for t in textRange:
			f= textList[t].find ('</a>"') +4
			textList[t] = textList[t][f:]
		self.text = '="'.join (textList)
		self.replace (' href=""')
		# nettoyer
		while self.contain ('  '): self.replace ('  ', ' ')
		self.replace (' >', '>')
		self.replace ('< ', '<')
		self.replace ('> ', '>')
		self.replace (' <', '<')
		self.replace ('</ ', '</')
		self.replace (' />', '/>')
		self.text = self.text.strip()

	def delImgLink (self):
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('<div>', "")
		# supprimer les liens
		if self.contain ('<a href='):
			textList = ListPerso()
			textList.extend (self.text.split ('<a href='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList[i].find ('>') +1
				textList[i] = textList[i][d:]
			self.text = "".join (textList)
			self.text = self.text.replace ('</a>', "")
		# supprimer les images
		if self.contain ('<img src='):
			textList = ListPerso()
			textList.extend (self.text.split ('<img src='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList[i].find ('>') +1
				textList[i] = textList[i][d:]
			self.text = "".join (textList)

	def test (self):
		self.file = 'b/coucou.html'
		self.dataFromFile()
		self.author = 'deborah powers'
		self.subject = 'test'
		self.autlink = 'http://deborah-powers.fr/'
		self.link = 'http://www.mon/histoire.com'
		self.text = 'coucou je suis deborah'
		self.toFile()
		self.fromFile()
		print (self)

# on appele ce script dans un autre script
if __name__ != '__main__': pass
# mettre des majuscules dans un text
elif len (argv) >=2:
	fhtml = ArticleHtml()
	fhtml.fromArticleName (argv[1])
# le nom du fichier n'a pas ete donne
else: print (help)
