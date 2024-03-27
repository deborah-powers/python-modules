#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
import textFct
from fileCls import File

listTags =( 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button', 'tr', 'table', 'figure', 'figcaption', 'textarea', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body' )
listTagsSelfClosing =( 'img', 'input', 'hr', 'br', 'meta' )

htmlText = "<html><head><title>Test</title></head><body><h1 id='parse'>Parse me!</h1><div class='cocc'>a<div color='plotplot'><span>hello</span> b</div><img src='coucoup' alt='sage comme une image'/></div></body></html>"
htmlName = 'C:\\Users\\LENOVO\\Desktop\\articles\\scene deborah abdelselem.html'
htmlFile = File (htmlName)
htmlFile.read()
print (htmlFile)

class TagHtml():
	def __init__ (self, text=""):
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
				if attr[:3] == 'id=': self.id = attr[5:-1]
				elif attr[:7] == 'class=': self.id = attr[9:-1]
				else:
					d= attr.find ('=')
					self.attributes[attr[:d]] = attr[d+2:-1]

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

class HtmlParser():
	def __init__ (self, text=""):
		self.text = text
		self.meta ={}

	def cleanBasic (self):
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

	def getBody (self):
		d= self.text.find ('<body')
		d= self.text.find ('>',d) +1
		f= self.text.rfind ('</body>')
		self.text = self.text[d:f]

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

	def getByTag (self, tagName):
		# renvoi la première balise <tag/>
		tagStart = '<'+ tagName
		if tagStart not in self.text: return None
		posStart = self.text.find (tagStart)
		return self.getByPos (posStart)

	def getById (self, index):
		text = text.replace ('"', "'")
		if " id='" + index +"'" in text:
			posStart = text.find (" id='" + index +"'")
			posStart = self.text [:posStart].rfind ('<')
			return self.getByPos (posStart)
		else: return None

	def getByClass (self, className):
		# renvoi la première balise
		text = text.replace ('"', "'")
		if " class='" + className +"'" in text:
			posStart = text.find (" class='" + className +"'")
			posStart = self.text [:posStart].rfind ('<')
			return self.getByPos (posStart)
		else: return None

	def getListByTag (self, tagName):
		tagStart = '<'+ tagName
		if tagStart not in self.text: return []
		tagList =[]
		posStart =0
		while tagStart in self.text[posStart:]:
			posStart = self.text.find (tagStart, posStart)
			tagList.append (self.getByPos (posStart))
			posStart = posStart +2
		return tagList

	def getListByClass (self, className):
		text = text.replace ('"', "'")
		if " class='" + className +"'" in text:
			tagList =[]
			posStart =0
			while " class='" + className +"'" in text[posStart:]:
				posStart = text.find (" class='" + className +"'")
				tagList.append (self.getByPos (posStart))
				posStart = posStart +2
			return self.getByPos (posStart)
		else: return []

	def getList (self, tagName, className):
		oldList = getListByTag (tagName)
		if oldList:
			tagList =[]
			for tag in oldList:
				if tag.className == className: tagList.append (tag)
			return tagList
		else: return []

	def getMetas (self):
		metas = self.getListByTag ('meta')
		reta = reversed (range (len (metas)))
		metaDict ={}
		for m in reta:
			name = metas[m].containAttribute ('name')
			if name == None or name == 'viewport': trash = metas.pop (m)
			else: metaDict[name] = metas[m].containAttribute ('content')


htmlParser = HtmlParser (htmlFile.text)
htmlParser.getMetas()
"""
text = htmlParser.getListByTag ('div')
print (len (text), text[0], text[1])
print (text)
"""