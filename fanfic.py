#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

from sys import argv
from os import remove
import listFct
import textFct
from fileCls import Article
import htmlCls
import loggerFct as log

help = """
récupérer les pages de certains sites que j'aime beaucoup
utilisation: python fanfic.py url
l'url peut correspondre à une page ou un fichier local
"""

class Fanfic (htmlCls.Html, Article):
	def __init__ (self, url, subject=None):
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, url)
		self.delAttributes()
		if subject: self.subject = subject
		if 'http://archiveofourown.org/' in self.text:	self.fromAooo()
		elif '://www.gutenberg.org/' in url:	self.gutemberg()

		elif 'b/ffnet.html' == url:		self.ffNet()
		elif 'b/fpress.html' == url:	self.fPress()
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebGratuit()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.reddit()
		elif 'http://uel.unisciel.fr/' in url:				self.unisciel()
		elif 'egb'		in url: self.ebGratuit()
		elif 'medium'	in url: self.medium()
		elif '</article>' in self.text:
			article = htmlCls.getByTagFirst (self.text, 'article')
			self.text = article
		self.meta ={ 'link': self.link, 'author': self.author, 'autlink': self.autlink, 'subject': self.subject }
		self.delClasses()
		article = self.toText()
		if article: article.divide()
		else: self.divide()

	def findSubject (self):
		if self.subject:
			self.subject = self.subject.replace ('/', ', ')
			self.subject = self.subject.replace (', ', ', ')
			self.subject = self.subject.replace ('-', ', ')
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		subjectDict = {
			'romance': ('romance', ' sex', 'x reader', 'rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars', 'integra', 'axi', 'damned caeli'),
			'rocker': ('rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars'),
			'tstm': ('30 seconds to mars', ), 'him': ('him (band)', 'ville valo'), '69eyes': ('jyrki', ),
			'hellsing': ('integra', 'axi', 'damned caeli'),
			'monstre': ('mythology', 'vampire', 'naga', 'pokemon'),
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
		else: self.subject = 'fiction'

	def usePlaceholders (self):
		placeholders = ('y/n', 'e/c', 'h/c', 'l/n')
		for ph in placeholders:
			self.text = self.text.replace (ph.upper(), ph)
			self.text = self.text.replace ('('+ ph +')', ph)
			self.text = self.text.replace ('['+ ph +']', ph)
			self.text = self.text.replace ('{'+ ph +'}', ph)
		self.text = self.text.replace ('y/n', 'Deborah')
		self.text = self.text.replace ('e/c', 'grey')
		self.text = self.text.replace ('h/c', 'dark blond')
		self.text = self.text.replace ('l/n', 'Powers')

	def ebGratuit (self):
		# l'auteur
		tag = htmlCls.getByTagAndClassFirst (self.text, 'p', 'Auteur')
		d= self.text.find ('<p class=>') +16
		f= self.text.find ('</p>', d)
		self.author = self.text [d:f].lower()
		self.title = htmlCls.getTitle (self.text)
		# le texte
		self.clean()
		f= self.text.find ('<h1>À propos de cette édition électronique</h1>')
		self.text = self.text [:f]
		# le sujet
		self.findSubject()

	def gutemberg (self):
		# le titre
		if 'dc.title' in self.meta.keys(): self.title = htmlCls.cleanTitle (self.meta['dc.title'])
		else:
			d= self.text.find ('Title:') +7
			f= self.text.find ('Author:', d) -1
			self.title = self.text [d:f]
		# l'auteur
		if 'dc.creator' in self.meta.keys():
			authlist = self.meta['dc.creator'].split (', ')
			self.author = authlist[1] +" "+ authlist[0]
			self.author = htmlCls.cleanTitle (self.author)
		else:
			d= self.text.find ('Title:') +7
			f= self.text.find ('Author:', d) -1
			d= f+9
			f= self.text.find ('Release', d) -1
			self.author = self.text [d:f]
		# le sujet est impossible à trouver
		if 'dc.subject' in self.meta.keys(): self.subject = htmlCls.cleanTitle (self.meta['dc.subject'])
		self.findSubject()
		# le texte
		d= self.text.find ('<h1')
		if d==-1: d= self.text.find ('<h2')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]
		# cas spécifiques
		if '<p>CONTENTS</p>' in self.text:
			d= self.text.find ('<p>CONTENTS</p>')
			d= self.text.find ('<hr>', d)
			self.text = self.text [d:]
		if '<h2>Footnotes:</h2>' in self.text:
			f= self.text.find ('<h2>Footnotes:</h2>')
			self.text = self.text [:f]
	#	self.delImgLink()

	def fromAooo (self):
		# fanfic enregistrée via le bouton télécharger en html
		self.meta ={}
		# le lien de la fanfic
		tag = htmlCls.getByTagAndClassFirst (self.text, 'p', 'message')
		tag = htmlCls.getByTag (tag.innerHtml, 'a')[1]
		self.link = tag.attributes['href']
		# le titre
		self.title = htmlCls.getcontentByTag (self.text, 'h1')
		self.title = htmlCls.cleanTitle (self.title)
		# l'auteur
		tag = htmlCls.getByTagAndClassFirst (self.text, 'div', 'byline')
		tag = htmlCls.getByTagFirst (tag.innerHtml, 'a')
		self.autlink = tag.attributes['href']
		f= self.autlink.find ('/pseuds/')
		self.autlink = self.autlink[:f]
		self.author = tag.innerHtml
		# le sujet
		tag = htmlCls.getByTagAndClassFirst (self.text, 'dl', 'tags')
		tag.innerHtml = tag.innerHtml.replace ('http://archiveofourown.org/tags/', "")
		tags = htmlCls.getByTag (tag.innerHtml, 'a')
		for link in tags: self.subject = self.subject +'\t'+ link.innerHtml
		self.findSubject()
		# le texte
		tag = htmlCls.getById (self.text, 'chapters')
		self.text = tag.innerHtml
		self.delClasses()
		self.text = self.text.replace ('<div>',"")
		self.text = self.text.replace ('</div>',"")

	def fromAoooVa (self):
		# fanfic enregistrée en faisant un ctl+ click
		self.meta ={}
		# le titre
		tag = htmlCls.getByTagAndClassFirst (self.text, 'h2', 'title heading')
		self.title = htmlCls.cleanTitle (tag.innerHtml)
		# l'auteur
		tag = htmlCls.getByTagAndClassFirst (self.text, 'h3', 'byline heading')
		tag = htmlCls.getByTagFirst (tag.innerHtml, 'a')
		self.autlink = 'https://archiveofourown.org' + tag.attributes['href']
		self.author = htmlCls.cleanTitle (tag.innerHtml)
		# le sujet
		tag = htmlCls.getByTagAndClassFirst (self.text, 'dd', 'fandom tags')
		tag = htmlCls.getByTagFirst (tag.innerHtml, 'a')
		self.subject = htmlCls.cleanTitle (tag.innerHtml)
		self.findSubject()
		# le lien de la fanfic
		tag = htmlCls.getByTagAndClassFirst (self.text, 'dd', 'bookmarks')
		tag = htmlCls.getByTagFirst (tag.innerHtml, 'a')
		self.link = 'https://archiveofourown.org' + tag.attributes['href'].replace ('bookmarks', "")
		# le texte
		tag = htmlCls.getById (self.text, 'chapters')
		self.text = tag.innerHtml

	def unisciel (self, subject):
		self.subject = 'cours'
		self.author = 'unisciel'
		self.text = findTextBetweenTag (self.text, 'body')
		self.clean()
		self.delScript()
		d= self.text.find ('<td>') +4
		f= self.text.find ('</td>', d)
		self.title = self.text [d:f].lower()
		d= self.text.find ('<p>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('<img', '</p><img')
		self.text = self.text.replace ("png'>","png'><p>")
		self.text = self.text.replace ('<p><p>', '<p>')
		self.text = self.text.replace ('</p></p>', '</p>')
		self.text = self.text.replace ('<p>', '</p><p>')
		self.text = self.text.replace ('</p>', '</p><p>')
		self.text = self.text.replace ('<p></p>', "")
		self.text = self.text.replace ('<p><p>', '<p>')
		self.text = self.text.replace ('<p><img', '<img')
		self.text = self.text.replace ("png'></p>","png'>")
		self.text = self.text [4:-3]
		self.text = self.text.replace ('../res/', 'bv-'+ subject +'/')
		self.text = self.text.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01.png'><p>", ' <b>ADP +P --> ATP</b> ')
		self.text = self.text.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01_1.png'><p>", ' <b>ATP --> ADP +P</b> ')
		self.styles.append ('unisciel.css')

	def menaceTheoriste (self):
		self.subject = 'sciences'
		self.clean()
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		d= self.text.find ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.text.find ('>', d) -1
		self.autlink = self.text [d:f]
		d=f+2
		f= self.text.find ('</a>', d)
		self.author = self.text [d:f]
		d= self.text.find ('</h1>')
		d= self.text.find ('</header>', d) +9
		f= self.text.find ('<footer>', d)
		self.text = self.text [d:f]
		f= self.text.find ('#comments')
		f= self.text [:f].rfind ('<a')
		f= self.text [:f].rfind ('>') +1
		self.text = self.text [:f]

	def medium (self, subject):
		# récupérer les metadonnées
		self.link = self.title
		d= self.text.find ('"creator":') +12
		f= self.text.find ('"', d)
		self.author = self.text [d:f]
		d-=15
		f= self.text [:d].rfind ('@') +1
		self.autlink = 'https://gen.medium.com/@' + self.text [f:d]
		d= self.link.rfind ('/') +1
		f= self.link.rfind ('-')
		self.title = self.link [d:f].replace ('-', ' ')
		# récupérer le texte
		d= self.text.find ('<p>')
		f= self.text.rfind ('<h2>GEN</h2>')
		self.text = self.text [d:f]
		f= self.text.rfind ('</p>') +4
		self.text = self.text [:f]
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
	#	self.delImgLink()

	def reddit (self):
		if 'FemaleDatingStrategy' in self.link:
			self.subject = 'feminisme'
			self.title = 'fds '+ self.title
		else: self.subject = 'opinion'
		self.clean()
		self.cleanLink()
		d= self.text.find ('<h1>')
		d= self.text.find ('<p>', d)
		f= self.text.find ('<div>reddit Inc')
		self.text = self.text [d:f]
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		# auteur
		f= self.link.find ('/', 26)
		self.autlink = self.link [:f]
		self.author = self.autlink [25:]
		self.title = self.title.replace ('#', ' ')
		# finir le texte
		self.text = self.text.replace ('<li><p>', '<li>')
		self.text = self.text.replace ('</p></li>', '</li>')
		f= self.text.rfind ('<hr>Created')
		self.text = self.text [:f]
		# zapper les commentaires
		f= self.text.find ('<button>share</button>')
		self.text = self.text [:f]
		f= self.text.rfind ('</p>') +4
		self.text = self.text [:f]

	def fPress (self):
		# les métadonnées
		data = self.title.split (', ')
		self.title = data[0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title [:f]
		d= textFct.find (self.text, '/u/') +3
		f= textFct.find (self.text, "'>", d)
		self.autlink = 'https://www.fictionpress.com/u/' + self.text[d:f]
		self.link = 'https:' + self.metas ['canonical']
		d= self.autlink.rfind ('/') +1
		self.author = cleanTitle (self.autlink[d:])
		# le sujet
		if '- Romance/' in self.text: self.subject = 'romance'
		self.findSubject()
		# le texte
		self.replace ('<br>', '</p><p>')
		d= self.text.find ("<div class='storytext")
		d= self.text.find ('>',d) +1
		f= self.text.find ("</div>", d)
		self.text = self.text[d:f]
		self.text = self.text.strip()
		self.text = '<p>'+ self.text +'</p>'

	def ffNet (self):
		# les métadonnées
		data = self.title.split (', ')
		self.title = data[0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title [:f]
		d= textFct.find (self.text, '/u/') +3
		f= textFct.find (self.text, "'>", d)
		self.autlink = 'https://www.fanfiction.net/u/' + self.text[d:f]
		self.link = 'https:' + self.metas ['canonical']
		d= self.autlink.rfind ('/') +1
		self.author = cleanTitle (self.autlink[d:])
		# le sujet
		if '- Romance/' in self.text: self.subject = 'romance'
		self.findSubject()
		# le texte
		self.replace ('<br>', '</p><p>')
		d= self.text.find ("<div class='storytext")
		d= self.text.find ('>',d) +1
		f= self.text.find ("<div style='height: 5px'>", d)
		self.text = self.text[d:f]
		self.text = self.text.strip()
		self.text = '<p>'+ self.text +'</p>'

if len (argv) >=2:
	url = argv[1]
	subject = None
	if len (argv) >=3: subject = argv[2]
	page = Fanfic (url, subject)
# le nom du fichier n'a pas ete donne
else: print (help)