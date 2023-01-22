#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import textFct as tf

"""
https://docs.python.org/3/library/html.parser.html
https://gist.github.com/FiloSottile/2352407
"""

htmlText = """
<!DOCTYPE html><html><head>
	<title>page de test</title>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<link rel='icon' type='image/svg+xml' href='../../site-dp/data/nounours-perso.svg'/>
	<link rel='stylesheet' type='text/css' href='../../site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='../../site-dp/library-css/perso.css' media='screen'/>
<style type='text/css'>
	h1 { self.text-align: center; }
</style></head><body>
	<h1>bonjour !</h1>
	<p>je suis Deborah</p>
	<p class='coco' color='green'>je suis Deborah</p>
</body></html>
"""

htmlTemplates ={
	'all': "<%s>%s</%s>",
	'a': "<a href='%s'>%s</a>",
	'img': "<img src='%s' alt='%s'/>",
	'br': '<br/>', 'hr': '<hr/>',
	'input': "<input type='%s' value='%s'/>"
}
htmlTemplatesKeys = htmlTemplates.keys()

class HtmlTag():

	def empty (self):
		self.name =""
		self.id =""
		self.clazz =""
		self.text =""
		self.content =[]
		self.src =""
		self.attributes ={}

	def __init__(self, name, text="", src="", id="", clazz="", attributes={}):
		self.name = name
		self.id = id
		self.clazz = clazz
		self.text = text
		self.src = src
		self.attributes = attributes

	def __str__(self):
		text = htmlTemplates ['all']
		if self.name in htmlTemplatesKeys:
			text = htmlTemplates [self.name]
			if self.name not in 'br hr': text = text %( self.src, self.text)
		else: text = text %( self.name, self.text, self.name)
		attributesNames = self.attributes.keys()
		for attribute in attributesNames: text = text.replace ('<'+ self.name, '<'+ self.name +' '+ attribute +"='"+ self.attributes [attribute] +"'")
		if self.id: text = text.replace ('<'+ self.name, '<'+ self.name +" id='"+ self.id +"'")
		if self.clazz: text = text.replace ('<'+ self.name, '<'+ self.name +" class='"+ self.clazz +"'")
		return text

	def parseContent (self):
		d= self.text.find ('<')
		contentTag = HtmlTag ('text')
		if d<0:
			contentTag.text = self.text
			self.content.append (contentTag)
		elif d>0:
			contentTag.text = self.text[:d]
			self.content.append (contentTag)
		contentTag

	def parse (self, text):
		bordures =[]
		self.empty()
		# extraire le nom du tag
		d= text.find ('<') +1
		bordures.append (text[:d-1].strip())
		text = text[d:]
		f= text.find ('>')
		if text[f-1] =='/': f=f-1
		e= text.find (' ')
		if f<e or e<0: self.name = text[:f]
		else:
			# le tag a des attributs
			self.name = text[:e]
			attributes = text[e+1:f].split (' ')
			for attribute in attributes:
				d= attribute.find ('=')
				if attribute[:d] == 'id': self.id = attribute [d+2:-1]
				elif attribute[:d] == 'class': self.clazz = attribute [d+2:-1]
				elif attribute[:d] == 'src': self.src = attribute [d+2:-1]
				elif attribute[:d] == 'href': self.src = attribute [d+2:-1]
				elif attribute[:d] == 'type': self.src = attribute [d+2:-1]
				elif attribute[:d] == 'alt': self.text = attribute [d+2:-1]
				elif attribute[:d] == 'value': self.text = attribute [d+2:-1]
				else: self.attributes [attribute[:d]] = attribute [d+2:-1]
		# récupérer le texte
		if self.name not in htmlTemplatesKeys:
			f= text.find ('>') +1
			text = text[f:]
			# trouver les positions des brackets complémentaires
			d=0
			f= text.index ('</'+ self.name +'>')
			totD = text[d+1:f].count ('<'+ self.name)
			totF = text[d+1:f].count ('</'+ self.name +'>')
			while totD > totF:
				f= text.index ('</'+ self.name +'>', f+1)
				totD = text[d+1:f].count ('<'+ self.name)
				totF = text[d+1:f].count ('</'+ self.name +'>')
			self.text = text[d:f]
		f= text.find ('>',f) +1
		bordures.append (text[f:].strip())
		print (bordures)
		return bordures

mytag = HtmlTag ('hr', 'bonjour je suis Deborah', 'http://www.dodo.fr', 'dodo', 'coucou', { 'koko': 'dodo', 'dada': 'doudou' })
"""
mytag = HtmlTag ('p', 'bonjour je suis Deborah', 'http://www.dodo.fr', 'dodo', 'coucou', { 'koko': 'dodo', 'dada': 'doudou' })
mytag = HtmlTag ('img', 'bonjour je suis Deborah', 'http://www.dodo.fr', 'dodo', 'coucou', { 'koko': 'dodo', 'dada': 'doudou' })
mytag = HtmlTag ('a', 'bonjour je suis Deborah', 'http://www.dodo.fr', 'dodo', 'coucou', { 'koko': 'dodo', 'dada': 'doudou' })
mytag = HtmlTag ('input', 'bonjour je suis Deborah', 'http://www.dodo.fr', 'dodo', 'coucou', { 'koko': 'dodo', 'dada': 'doudou' })
mytag.parse ("<hr class='coco' color='green'/>")
mytag.parse ("<hr/>")
mytag.parse ("<p class='coco' color='green'>je suis Deborah</p>")
mytag.parse ("<p class='coco' color='green'>je suis Deborah. <p>j'aime le pain</p> et le nutella</p>")
"""
mytag.parse ("ohé <hr class='coco' color='green'/> cloclo")