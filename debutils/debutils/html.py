#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from os import remove
import urllib as ul
from urllib import request as urlRequest
from debutils.list import List
from debutils.file import *
from debutils.fileLocal import pathCss
import debutils.logger as logger

listTagsIntern = [ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button']
listTagsSpecial = [ 'a', 'img', 'form', 'input']
listTagsKeep = [ 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body']
listTagsKeep.extend (listTagsIntern)
listTagsKeep.extend (listTagsSpecial)
listTags = []
listTags.extend (listTagsKeep)
listTags.extend (listTagsSpecial)
"""
pathCssAlt = 'C:Usersdeborah.powersDesktophtmlutils'
pathCss = '/home/lenovo/Bureau/site-dp/library-css/'
	<link rel='stylesheet' type='text/css' href='" + pathCss + "structure.css'/>
	<link rel='stylesheet' type='text/css' href='" + pathCss + "perso.css'/>
"""
htmlTemplate ="""<!DOCTYPE html><html><head>
	<title>%s</title>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<base target='_blank'>
	%s
</head><body>
%s
</body></html>"""

def findTextBetweenTag (originalText, tag):
	lTag = len (tag)
	d= originalText.find ('<'+ tag) +1+ lTag
	d= originalText.find ('>', d) +1
	f= originalText.find ('</'+ tag +'>', d)
	phrase = originalText [d:f]
	phrase = phrase.strip()
	return phrase

class FileHtml (File):
	def __init__ (self, file =None):
		if file and file [:4] == 'http':
			File.__init__ (self)
			self.link = file
		elif file: File.__init__ (self, file)
		else: File.__init__ (self)
		self.extension = 'html'
		self.styles = []
		self.metas = {}

	""" ________________________ manipuler les fichiers ________________________ """


	def fromFile (self):
		File.fromFile (self)
		self.clean()
		tmpTitle = findTextBetweenTag (self.text, 'title')
		if tmpTitle and '>' not in tmpTitle and '<' not in tmpTitle: self.title = tmpTitle
		self.styles = []
		self.getCss()
		self.getMetadata()
		self.text = findTextBetweenTag (self.text, 'body')

	def toFile (self):
		# pas de text,""
		if not self.text:
			print ('rien a ecrire pour', self.title)
			print (self.file)
			return
		"""
		if local:
			self.styles.append (pathCss + 'structure.css')
			self.styles.append (pathCss + 'perso.css')
		"""
		self.title = self.title.lower()
		textInfos = self.setMetadata()
		textCss = self.setCss()
		textCss = textCss.strip()
		textInfos = textInfos + textCss
		textInfos = textInfos.strip()
		# le nouveau fichier
		for tag in listTagsIntern:
			self.replace ('<'+ tag +'>\n<', '<'+ tag +'><')
			self.replace ('>\n</'+ tag +'>', '></'+ tag +'>')
		self.text = self.text.strip()
		self.text = htmlTemplate % (self.title, textInfos, self.text)
		File.toFile (self)

	def clean (self):
		self.replace ('\t', ' ')
		self.replace ('\n', ' ')
		File.clean (self)
		while '  ' in self.text: self.replace ('  ', ' ')
		self.replace ('> ', '>')
		self.replace (' <', '<')
		self.replace (' />', '/>')
		self.text = self.text.strip()
		self.replace ("''", '"')
		"""
		self.replace ('"',"'")
		# rajouter des espaces autour des liens
		self.replace ('</a>', ' </a>')
		self.replace ('">', '"> ')
		self.replace ("'>","'> ")
		"""

	def __str__ (self):
		strFic = 'Titre: %s, Fichier: %s' % (self.title, self.file)
		if self.metas:
			strFic = strFic + '\nMeta:'
			for meta in self.metas.keys(): strFic = strFic +'\n\t%st%s' % (meta, self.metas [meta])
		if self.styles:
			strFic = strFic + '\nStyle:'
			for css in self.styles: strFic = strFic +'\n\t%s' %css
		return strFic

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
		"""
		tmpText = self.text.replace ('<link rel=', '<meta name=')
		tmpText = tmpText.replace (' href=', ' content=')
			elif 'stylesheet' in metaTmp [0]: continue			# artéfact
		"""
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
		self.fileFromData()
		try: urlRequest.urlretrieve (self.link, self.file)
		except Exception as e: return False
		else:
			self.fromFile()
			remove (self.file)
			self.titleFromUrl()
			self.fileFromData()
			return True

	def fromUrl (self, params=None):
		res = self.fromUrlVa (params)
		if not res:
			print ('la récupération par la première méthode à échoué, éssai avec la seconde méthode')
			res = self.fromUrlVb()
			if not res: print ('la récupération par la seconde méthode à échoué, impossible de récupérer les données')

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
		self.extension = 'html'
		self.path = 'b/'
		self.title = 'tmp'
		self.fileFromData()
		self.link = url
		self.fromUrl()
		# self.cleanWeb()
		self.metas = {}
		self.styles = []
		self.metas ['link'] = self.link
		self.toFile()

	def cleanLocal (self):
		FileHtml.clean()
		self.text = findTextBetweenTag (self.text, 'body')

	def cleanWeb (self):
		self.clean()
		self.replace ('<br/>', '<br>')
		self.replace ('<hr/>', '<hr>')
		# supprimer les commentaires
		self.replace ('< ! --', '<!--')
		textList = List()
		textList.addList (self.text.split ('<!--'))
		textRange = textList.range (1)
		for t in textRange:
			f= textList [t].find ('-->') +3
			textList [t] = textList [t] [f:]
			self.text = "".join (textList)
		# effacer certaines balises
		# self.cleanSpan()
		self.cleanTags()
		self.text = findTextBetweenTag (self.text, 'body')
		self.replace ('\n')
		self.replace ('\t')
		self.clean()

	def cleanLink (self):
		if not self.contain ('</a>'): return
		listText = self.split ('</a>')
		rangeTxt = range (len (listText) -1)
		for l in rangeTxt:
			listText [l] = listText [l].strip ('/')
			d= listText [l].rfind ('<a')
			d= listText [l].rfind ('>', d) +1
			title = listText [l] [d:]
			title = title.replace (' / ', ' $ ')
			title = title.replace (' /', ' $')
			title = title.replace ('/ ', '$ ')
			title = title.replace ('. ', '% ')
			if '/' in title:
				e= title.rfind ('/') +1
				title = title [e:]
			if '.' in title:
				e= title.rfind ('.')
				title = title [:e]
			title = title.replace ('%', '.')
			title = title.replace ('$', '/')
			title = title.replace ('-', ' ')
			title = title.replace ('_', ' ')
			while '  ' in title: title = title.replace ('  ', ' ')
			listText [l] = listText [l] [:d] + title
		self.text = '</a>'.join (listText)

	def cleanTags (self):
		# supprimer les attributs inutiles
		self.replace ('<br/>', '<br>')
		self.replace ('<hr/>', '<hr>')
		tagList = List()
		textList = List()
		textList.addList (self.text.split ('<'))
		textRange = textList.range (1)
		# textRange.reverse()
		for t in textRange:
			if len (textList [t]) ==0: continue
			elif textList [t] [0] in '/ !': continue
			elif '>' not in textList [t]: textList [t] = textList [t] [:f] +'>'
			f= textList [t].find ('>')
			tag = textList [t] [:f].lower()
			textList [t] = textList [t] [f:]
			if ' ' in tag:
				f= tag.find (' ')
				attributes = tag [f:]
				tag = tag [:f]
				if tag in ('\a', 'img', 'form', 'input'): tag = self.cleanTagsSpecial (tag, attributes)
				elif tag not in tagList: tagList.add (tag)
			elif tag not in tagList: tagList.add (tag)
			textList [t] = tag + textList [t]
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
			textList = List()
			textList.addList (self.text.split ('<a>'))
			textRange = textList.range (1)
			for a in textRange:
				d= textList[a].find ('</a>')
				textList[a] = textList[a] [:d].strip() +' '+ textList[a] [d+4:].strip()
			#	textList[a] = textList[a] [d+4:].strip()
			self.text = ' '.join (textList)
		# retrouver les balises vides
		self.clean()
		self.replace ('\n')
		for tag in tagList: self.replace ('<'+ tag +'></'+ tag +'>')

	def cleanTagsSpecial (self, tag, attributeList):
		if tag == '\a':
			return self.keepAttribute ('\a', 'href', attributeList)
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

	def delScript (self):
		if not self.contain ('</script>'): return
		txtList = self.text.split ('</script>')
		rangeTxt = range (len (txtList) -1)
		for t in rangeTxt:
			pos = txtList [t].rfind ('<script')
			txtList [t] = txtList [t] [:pos]
		self.text = "".join (txtList)


	def delStyle (self):
		if not self.contain ('</style>'): return
		txtList = self.text.split ('</style>')
		rangeTxt = range (len (txtList) -1)
		for t in rangeTxt:
			pos = txtList [t].rfind ('<style')
			txtList [t] = txtList [t] [:pos]
		self.text = "".join (txtList)

	def cleanSpan (self):
		# supprimer les span en trop
		self.replace ('<SPAN', '<span')
		self.replace ('</SPAN', '</span')
		textList = List()
		textList.addList (self.text.split ('<span '))
		textRange = textList.range (1)
		textRange.reverse()
		for t in textRange:
			f= textList [t].find ('>')
			textList [t] = textList [t] [f:]
		self.text = '<span'.join (textList)
		self.replace ('</span>=', '=')
		self.replace ('<</span>', '<')
		self.replace ('<span>>', '>')
		self.replace ('<span>', ' ')
		self.replace ('</span>', ' ')
		# supprimer les liens en trop
		textList = List()
		textList.addList (self.text.split ('="<a '))
		textRange = textList.range (1)
		textRange.reverse()
		for t in textRange:
			f= textList [t].find ('</a>"') +4
			textList [t] = textList [t] [f:]
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

	# ________________________ conversion en texte simple ________________________

	def toFileText (self):
		self.fromHtml()
		self.extension = 'txt'
		self.fileFromData()
		ftext = File (self.file)
		ftext.text = self.text
		ftext.toFile()

	def fromFileText (self):
		ftext = File (self.file)
		ftext.fromFile()
		ftext.toHtml()
		self.text = ftext.text
		self.extension = 'html'
		self.fileFromData()
		self.toFile()

	# ________________________ tests ________________________

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

	def testOnline (self):
		self.link = 'https://www.tutorialspoint.com/downloading-files-from-web-using-python'
		self.fromUrl()

