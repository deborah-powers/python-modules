#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# modules python
from sys import argv
import urllib as ul
from urllib import request as urlRequest
import codecs
# modules dpowers
from tableClass import ListPerso, ListText
from htmlClass import FileHtml, findTextBetweenTag
from fileClass import FilePerso

help ="""lancer le script
	python %s url
""" % __file__

class Article (FileHtml):
	def findSubject (self, subject=None):
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		if subject:
			subject = subject.replace ('/', ', ')
			subject = subject.replace (',', ', ')
			subject = subject.replace ('-', ', ')
			subject = subject.replace ('  ', ' ')
			subjectList = subject
		subjectDict ={
			'romance': ('romance', ' sex', 'vampire', 'naga', 'x reader'),
			'sf': ('mythology', 'vampire', 'scify', 'lovecraft', 'stoker', 'conan doyle', 'naga'),
			'tricot': ('tricot', 'point', 'crochet')
		}
		subjectKeys = subjectDict.keys()
		for subject in subjectKeys:
			for word in subjectDict [subject]:
				if word in storyData:
					subjectList = subjectList +', '+ subject
					break
		if subjectList: self.subject = subjectList[2:]
		else: self.subject = 'histoire'

	def gutemberg (self, subject=None):
		# le titre
		d= self.find ('Title:') +7
		f= self.find ('Author:', d) -1
		self.title = self.text[d:f]
		# l'auteur
		d= f+9
		f= self.find ('Release', d) -1
		self.author = self.text[d:f]
		# le sujet est impossible à trouver
		self.findSubject (subject)
		# le texte
		d= self.find ('<h1>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text[d:f]
		# cas spécifiques
		if (self.inText ('<p>CONTENTS</p>')):
			d= self.find ('<p>CONTENTS</p>')
			d= self.find ('<hr>', d)
			self.text = self.text[d:]
		if (self.inText ('<h2>Footnotes:</h2>')):
			f= self.find ('<h2>Footnotes:</h2>')
			self.text = self.text[:f]
		for tag in listTags: self.text = self.text.replace ('<'+tag+'></'+tag+'>', "")
		self.delImgLink()
		self.meta ={}
		self.toFile()

	def ebg (self, subject=None):
		self.delImgLink()
		# le titre
		d= self.find ('<p>', 10) +3
		f= self.find ('</p>', d)
		self.author = self.text[d:f]
		# l'auteur
		d= self.find ('<p>', f) +3
		f= self.find ('</p>', d)
		self.title = self.text[d:f]
		# le sujet
		self.findSubject (subject)
		# le texte
		d=f
		f= self.text.rfind ('<h1>')
		if self.inText ('propos de cette édition électronique'):
			d2= self.find ('propos de cette édition électronique')
			if d2<f: d=d2
		elif self.count ('<h1>') >1:
			d2= self.find ('<h1>')
			if d2<f: d=d2
		d= self.find ('<p>', d)
		self.text = self.text[d:f]
		self.meta ={}
		self.toFile()

	def deviantart (self, subject=None):
		self.findSubject (subject)
		self.text = self.text.replace ('<br/>', '</p><p>')
		self.delScript()
		self.cleanWeb()
		f= self.title.rfind (' ')
		self.title = self.title[:f]
		d= self.find ("By<a href='https://www.deviantart.com/") +11
		f= self.find ("'",d)
		self.autlink = self.text[d:f]
		d= self.find ('>',f) +1
		f= self.find ('<',d)
		self.author = self.text[d:f]
		d= self.find ('<p>',f)
		self.text = self.text[d:]
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		f= self.find ('>See More by')
		self.text = self.text[:f]
		f= self.rfind ('<a')
		self.text = self.text[:f]
		if self.text[-1] != '>': self.text = self.text +'</p>'

	def aoooFromSource (self, subject=None):
		# trouver les metadonnées
		data = self.title.split (' - ')
		if len (data) >3:
			print ('trop de blocks dans le titre', self.title)
			if 'hapter' in data[1]: self.author = data.pop(1)
		self.title = data[0]
		self.author = data[1]
		self.subject = data[2]
		self.findSubject (subject)
		d= self.find ("https://archiveofourown.org/works/")
		f= self.find ("'", d)
		self.link = self.text[d:f]
		if '"' in self.link:
			f= self.link.find ('"')
			self.link = self.link[:f]
		self.autlink = 'https://archiveofourown.org/users/' + self.author
		# trouver le texte
		self.delScript()
		self.replace ('<div>')
		self.replace ('</div>')
		d= self.find ('<h2>')
		d= self.find (self.author + '</a></h3>', d)
		c= self.text[:d].rfind ('href') +6
		f= self.find ('/pseuds/', c) +1
		self.meta ['autlink'] = self.text[c:f]
		d= self.find ('</h3>', d) +5
		f= self.text.rfind ('<h3>Actions</h3>')
		self.text = self.text[d:f]
		"""
		if self.contain ('<h3>Notes:</h3>'):
			f= self.text.rfind ('<h3>Notes:</h3>')
			self.text = self.text[:f]
		"""
		self.delImgLink()
		self.replace ('</blockquote><h3>Notes:</h3><blockquote>')
		self.replace ('<h3>Summary:</h3>', '<h2>Notes:</h2>')
		self.replace ('</h3><h3>', '</h2><h3>')
		self.replace ('<h3>Chapter Text</h3>', '<hr>')
		self.replace ('<h3>Chapter', '<h2>Chapter')
		self.replace ('</h2><hr>', '</h2>')
		self.text = self.text.replace ('Y/N', 'y/n')
		self.text = self.text.replace ('(y/n)', 'Deborah')
		self.text = self.text.replace ('y/n', 'Deborah')

	def aooo (self, subject=None):
		if 'This work could have adult content. If you proceed you have agreed that you are willing to see such content' in self.text:
			print ('fichier protégé', self.title)
			return
		# le titre
		self.cleanWeb()
		d= self.find ("<a href='https://archiveofourown.org/")
		d= self.find ('>', d) +1
		f= self.find ('</a>', d)
		self.title = self.text[d:f]
		# l'auteur
		d= self.find ('by', f)
		d= self.find ('>', d) +1
		f= self.find ('</a>', d)
		self.author = self.text[d:f]
		# le sujet
		d= self.find ('>Additional Tags:', f) +10
		d= self.find ('<a href=', d) +9
		f= self.find ('</ul>', d)
		self.subject = self.text[d:f].lower()
		self.subject = self.subject.replace ('</a></li>', "")
		self.subject = self.subject.replace ("<li><a href='/tags/", "<'")
		textList = ListPerso()
		textList.extend (self.subject.split ("/works'>"))
		trash = textList.pop(0)
		textRange = textList.range()
		textRange.pop (-1)
		for t in textRange:
			d= textList[t].find ("<'")
			textList[t] = textList[t][:d]
		self.subject = ', '.join (textList)
		self.text = self.text[f:]
		self.findSubject (subject)
		# le texte
		self.text = self.text.replace ('<h3>Chapter Text</h3>', "")
		d= self.find ('<h3><a href=')
		d= self.find ('>Work Text:</', d) +16
		f= self.find ('<script>')
		f= self.text.rfind ('>Actions</') -3
		self.text = self.text[d:f]
		self.delImgLink()
		self.text = self.text.replace ('h3>', 'h2>')

	def fpress (self, subject=None):
		self.cleanWeb()
		# trouver les métadonnées
		d= self.find ('By:<a href=') +12
		f= self.find ('>',d) -1
		textTmp = self.text[d:f]
		self.autlink = textTmp
		f= textTmp.rfind ('/') +1
		self.author = textTmp[f:]
		self.findSubject (subject)
		# nettoyer le texte
		d= self.find ('<p>')
		f= self.rfind ('</p>') +4
		self.text = self.text[d:f]

	def fpressLocal (self, subject=None):
		self.fpress (subject)
		f=0
		if 'hapter ' in self.title: f= self.title.find ('hapter ') -2
		else: f= self.title.find (', ')
		self.title = self.title[:f]
		self.replace ('$',' ')

	def fpressSerie (self, url, pageF):
		# trouver l'url éclatée
		f= url.rfind ('/')
		d= url[:f].rfind ('/') +1
		templateUrl = url[:d] +'%d'+ url[f:]
		pageD = int (url[d:f])
		print (pageD, pageF, templateUrl)
		pageRange = range (pageD, pageF +1)
		pageText =""
		for p in pageRange:
			self.link = templateUrl %p
			self.fromUrl()
			self.clean()
			self.fpress()
			print (p, len (self.text))
			"""
			self.text = '<h1>chapître %d</h1>' %p+ self.text
			FilePerso.toFile (self, 'a')
			"""
			pageText = pageText + '<h1>chapître %d</h1>' %p
			pageText = pageText + self.text
		self.text = pageText
		self.toFile()

	def medium (self, subject):
		# récupérer les metadonnées
		self.link = self.title
		d= self.find ('"creator":') +12
		f= self.find ('"',d)
		self.author = self.text[d:f]
		d-=15
		f= self.text[:d].rfind ('@') +1
		self.autlink = 'https://gen.medium.com/@' + self.text[f:d]
		d= self.link.rfind ('/') +1
		f= self.link.rfind ('-')
		self.title = self.link[d:f].replace ('-', ' ')
		if subject: self.subject = subject
		# récupérer le texte
		d= self.find ('<p>')
		f= self.text.rfind ('<h2>GEN</h2>')
		self.text = self.text[d:f]
		f= self.text.rfind ('</p>') +4
		self.text = self.text[:f]
		self.replace ('<div>')
		self.replace ('</div>')
	#	self.delImgLink()

	def menaceTheoriste (self):
		self.subject = 'sciences'
		self.cleanWeb()
		self.replace ('<div>')
		self.replace ('</div>')
		d= self.find ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.find ('>',d) -1
		self.autlink = self.text[d:f]
		d=f+2
		f= self.find ('</a>',d)
		self.author = self.text[d:f]
		d= self.find ('</h1>')
		d= self.find ('</header>', d) +9
		f= self.find ('<footer>', d)
		self.text = self.text[d:f]
		f= self.find ('#comments')
		f= self.text[:f].rfind ('<a')
		f= self.text[:f].rfind ('>') +1
		self.text = self.text[:f]
		letters = 'dlmnst'
		for l in letters:
			self.replace (' '+l+'$',' '+l+"'")
			self.replace (l.upper() +'$',l.upper() +"'")
		self.replace ('$:',':')
		self.replace ('$',' ')
		while '  ' in self.text: self.replace ('  ',' ')

	def eduBourse (self):
		self.subject = 'finance'
		self.author = 'edu-bourse'
		self.cleanWeb()
		d= self.find ('<div><div>Mise')
		f= self.find ('</p>(adsbygoogle') +4
		self.text = self.text[d:f]
		self.replace ('<div><div>', '<p>')
		self.replace ('</div></div>', '</p>')
		self.replace ('</a>', ' </a>')
		self.replace (".php'>", ".php'> ")

	""" ________________________ récupérer et nettoyer les fichiers ________________________ """

	def fromWeb (self, url, subject=None):
		self.link = url
		self.fromUrl()
		self.clean()
		if 'http://www.gutenberg.org/' in url:				self.gutemberg (subject)
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebg (subject)
		elif 'https://archiveofourown.org/works/' in url:	self.aooo()
		elif 'https://www.deviantart.com/' in url:			self.deviantart()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.edubourse.com/' in url:			self.eduBourse()
		elif 'https://www.fictionpress.com/' in url:		self.fpressLocal (subject)
		elif 'https://www.fanfiction.net/' in url:			self.fpressLocal (subject)
	#	elif 'http://uel.unisciel.fr/biologie/' in url:		self.uniscielBiologie()
		else: self.cleanWeb()
		self.meta ={}
		self.css =[]
		self.toFileText()

	def fromLocal (self, file, subject=None):
		self.file = file
		self.fromFile()
		self.clean()
		self.cleanWeb()
		if 'gtb' in self.file:		self.gutemberg (subject)
		elif 'egb' in self.file:	self.egb (subject)
		elif 'aooo' in self.file:	self.aoooFromSource (subject)
		elif 'fpress' in self.file:	self.fpressLocal (subject)
		elif 'ffnet' in self.file:	self.fpressLocal (subject)
		elif 'medium' in self.file:	self.medium (subject)
		elif 'adapt' in self.file:	self.adapt()
		self.meta ={}
		self.css =[]
		self.toFileText()

	""" ________________________ fonctions pour gérer les fichiers ________________________ """

	def requestGet (self, params=None):
		"""
		url = 'http://localhost/site-dp/test-remplir-formulaire.php
		params ={ 'lname': 'Caroussi', 'fname': 'Claudia' }
		"""
		urlOriginal = self.link
		if params:
			self.link +='?'
			for paramName in params.keys():
				self.link += paramName +'='+ params [paramName] +'&'
			self.link = self.link.rstrip ('&')
		self.fromUrl()

# on appele ce script dans un autre script
if __name__ != '__main__': pass
# mettre des majuscules dans un texte
elif len (argv) >=2:
	url = argv[1]
	subject =None
	if len (argv) >=3: subject = argv[2]
	page = Article()
	if url[:4] == 'http':
		if subject and subject.isdigit(): page.fpressSerie (url, int (subject))
		else: page.fromWeb (url, subject)
	else: page.fromLocal (url, subject)
# le nom du file n'a pas ete donne
else: print (help)





