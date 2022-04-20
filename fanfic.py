#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from list import List
from htmlFile import FileHtml, findTextBetweenTag, listTags
from htmlArticle import ArticleHtml
from listFiles import ListArticle
import logger

class Fanfic (ArticleHtml):
	def ficWeb (self, url):
		self.extension = 'html'
		if url[:4] == 'http':
			self.link = url
			FileHtml.fromUrl (self)
			self.fileFromData()
		else:
			if url[-5:] != '.html': url = 'b/' + url + '.html'
			self.file = url
			self.dataFromFile()
			self.fromFile()
		self.clean()
		# self.cleanWeb()
		if 'http://www.gutenberg.org/' in url:				self.gutemberg()
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebGratuit()
		elif 'https://archiveofourown.org/works/' in url:	self.aoooWeb()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.reddit()
		elif 'https://www.therealfemaledatingstrategy.com/' in url:	self.fDatingS()
		elif 'https://www.abcBourse.com/' in url:			self.bourse()
		elif 'http://uel.unisciel.fr/' in url:				self.unisciel()
		elif 'gtb'		in url: self.gutemberg()
		elif 'egb'		in url: self.ebGratuit()
		elif 'b/aooo.html' == url: self.aoooLocal()
		elif 'ffNet'	in url: self.ffNet()
		elif 'medium'	in url: self.medium()
		elif 'adapt'	in url: self.adapt()
		elif 'jmdoudoux.fr'	in url: self.jmdoudoux()
		else: self.cleanWeb()
		self.metas = {}
		self.replace (' <', '<')
		self.replace ('><', '>\n<')
		if '</a>' in self.text or '<img' in self.text: self.toFile()
		else: self.toFileText()

	""" ________________________ pour chaque site ________________________ """

	def bourse (self):
		self.subject = 'argent'
		self.author = 'abc bourse'
		d= self.find ('<h1>')
		f= self.find ('<p>Vous avez aimé cet article')
		self.text = self.text[d:f]
		if 'suivant.gif' in self.text:
			f= self.find ('suivant.gif')
			self.text = self.text[0:f]
			f= self.rfind ('</p>') +4
			self.text = self.text[0:f]

	def reddit (self):
		if 'FemaleDatingStrategy' in self.link:
			self.subject = 'feminisme'
			self.title = 'fds '+ self.title
		else: self.subject = 'opinion'
		self.cleanWeb()
		self.cleanLink()
		d= self.find ('<h1>')
		d= self.find ('<p>', d)
		f= self.find ('<div>reddit Inc')
		self.text = self.text [d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		# auteur
		f= self.link.find ('/', 26)
		self.autlink = self.link [:f]
		self.author = self.autlink [25:]
		self.title = self.title.replace ('#', ' ')
		# finir le texte
		self.replace ('<li><p>', '<li>')
		self.replace ('</p></li>', '</li>')
		f= self.rfind ('<hr>Created')
		self.text = self.text [:f]
		# zapper les commentaires
		f= self.find ('<button>share</button>')
		self.text = self.text [:f]
		f= self.rfind ('</p>') +4
		self.text = self.text [:f]

	def unisciel (self, subject):
		self.subject = 'cours'
		self.author = 'unisciel'
		self.text = findTextBetweenTag (self.text, 'body')
		self.cleanWeb()
		self.delScript()
		d= self.find ('<td>') +4
		f= self.find ('</td>', d)
		self.title = self.text [d:f].lower()
		d= self.find ('<p>')
		f= self.rfind ('</p>') +4
		self.text = self.text [d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		self.replace ('<img', '</p><img')
		self.replace ("png'>","png'><p>")
		self.replace ('<p><p>', '<p>')
		self.replace ('</p></p>', '</p>')
		self.replace ('<p>', '</p><p>')
		self.replace ('</p>', '</p><p>')
		self.replace ('<p></p>')
		self.replace ('<p><p>', '<p>')
		self.replace ('<p><img', '<img')
		self.replace ("png'></p>","png'>")
		self.text = self.text [4:-3]
		self.replace ('../res/', 'bv-'+ subject +'/')
		self.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01.png'><p>", ' <b>ADP +P --> ATP</b> ')
		self.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01_1.png'><p>", ' <b>ATP --> ADP +P</b> ')
		self.styles.append ('unisciel.css')

	def gutemberg (self):
		# le titre
		d= self.find ('Title:') +7
		f= self.find ('Author:', d) -1
		self.title = self.text [d:f]
		# l'auteur
		d= f+9
		f= self.find ('Release', d) -1
		self.author = self.text [d:f]
		# le sujet est impossible à trouver
		self.findSubject()
		# le texte
		d= self.find ('<h1>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]
		# cas spécifiques
		if '<p>CONTENTS</p>' in self.text:
			d= self.find ('<p>CONTENTS</p>')
			d= self.find ('<hr>', d)
			self.text = self.text [d:]
		if '<h2>Footnotes:</h2>' in self.text:
			f= self.find ('<h2>Footnotes:</h2>')
			self.text = self.text [:f]
		self.delImgLink()
		self.metas = {}

	def ebGratuit (self):
		self.delImgLink()
		# l'auteur
		d= self.find ('<p class=Auteur>') +16
		f= self.find ('</p>', d)
		self.author = self.text [d:f].lower()
		# le titre
		d= self.find ('<title>') +7
		f= self.find ('</title>', d)
		self.title = self.text [d:f].lower()
		# le texte
		self.cleanWeb()
		f= self.find ('<h1>À propos de cette édition électronique</h1>')
		self.text = self.text [:f]
		# le sujet
		self.findSubject()

	def ficDev (self):
		self.findSubject()
		self.cleanWeb()
		self.replace ('<br>', '</p><p>')
		self.delScript()
		f= self.title.rfind (' ')
		self.title = self.title [:f]
		d= self.find ("By<a href=") +11
		f= self.find ("'", d)
		self.autlink = self.text [d:f]
		d= self.find ('>', f) +1
		f= self.find ('<', d)
		self.author = self.text [d:f]
		d= self.find ('<p>', f)
		self.text = self.text [d:]
		self.replace ('<div>',"")
		self.replace ('</div>',"")
		f= self.find ('>See More by')
		self.text = self.text [:f]
		f= self.rfind ('</p>') +4
		self.text = self.text [:f]
	#	if self.text [-1] != '>': self.text = self.text +'</p>'

	def aoooLocal (self):
		self.styles =[]
		self.metas ={}
		data = self.title.split (' - ')
		if len (data) >3 and 'hapter' in data[1]: self.author = data.pop (1)
		self.title = data[0]
		# self.author = data[1]
		self.subject = data[2]
		self.subject = self.subject.replace (' [Archive of Our Own]', "")
		self.subject = self.subject.replace (' (band)', "")
		self.cleanWeb()
		# le lien
		d= self.find ("<a href='/downloads/") +20
		f= self.find ('/', d)
		self.link = 'https://archiveofourown.org/works/' + self.text[d:f]
		self.aoooWebCommon()
		
	def aoooWeb (self):
		if 'This work could have adult content. If you proceed you have agreed that you are willing to see such content' in self.text:
			print ('fichier protégé', self.title)
			return
		self.cleanWeb()
		self.replace ('<br>', '</p><p>')
		self.text = findTextBetweenTag (self.text, 'body')
		# le titre
		d= self.find ('<h2>') +4
		f= self.find ('</h2>', d)
		self.title = self.text [d:f]
		self.title = self.title.strip()
		self.title = self.title.strip ('.')
		self.aoooWebCommon()

	def aoooWebCommon (self):
		# le sujet
		if subject and subject not in self.subject: self.subject = self.subject +', '+ subject
		d= self.find ('Category:<ul><li><a') +20
		d= self.find ('>', d) +1
		f= self.find ('</a>', d)
		if self.text[d:f] in ('F/M', 'F/F') and 'romance' not in self.subject: self.subject = ', romance'+ self.subject
		self.findSubject()
		"""
		d= self.find ('Fandoms:<ul><li><a', f) +20
		d= self.find ('>', d) +1
		f= self.find ('</a>', d)
		if self.text[d:f] not in self.subject: self.subject = self.subject +', '+ self.text[d:f]
		"""
		self.subject = self.subject.replace (' - Fandom', "")
	#	self.subject = self.subject[2:]
		# l'auteur
		d= self.find ("<h3><a href='/users/") +13
		f= self.find ('>', d) -1
		self.autlink = self.text[d:f]
		d= f+2
		f= self.find ('<', d)
		self.author = self.text [d:f]
		self.author = self.author.replace ('-',' ')
		self.author = self.author.replace ('_',' ')
		self.author = self.author.strip()
		self.replace ('<h3>Chapter Text</h3>')
		# le texte ne compte qu'un seul chapître
		d= self.find ('<h3>Work Text:</h3>') +19
		# le texte compte plusieurs chapîtres
		if d==18: d= self.find ("<h3><a href='/works/")
		f= self.rfind ('<h3>Actions</h3>')
		self.text = self.text [d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		if "<h3><a href='/works/" in self.text:
			chapters = List()
			chapters.fromText ("<h3><a href='/works/", self.text)
			chapterRange = chapters.range (1)
			for c in chapterRange:
				d= chapters [c].find ('>') +1
				chapters [c] = chapters [c] [d:]
			self.text = '<h2>'.join (chapters)
			self.replace ('</a></h3>', '</h2>')
		if '<h2>Chapter ' in self.text and not '</h2>' in self.text:
			chapters = List()
			chapters.fromText ('<h2>Chapter ', self.text)
			chapterRange = chapters.range (1)
			for c in chapterRange:
				d= chapters [c].find ('</a>: ') +6
				chapters [c] = chapters [c] [d:]
				chapters [c] = chapters [c].replace ('</h3>', '</h2>', 1)
			self.text = '<h2>'.join (chapters)
		# nettoyer le texte
		if '<h3>Notes:</h3>' in self.text:
			halfText = self.length() /2
			d= self.find ('<h3>Notes:</h3>')
			if d> halfText: self.text = self.text [:d]
		self.usePlaceholders()
		self.replace ('h2>', 'h1>')
		if '<h3>Series this work belongs to:</h3>' in self.text:
			f= self.find ('<h3>Series this work belongs to:</h3>')
			self.text = self.text[:f]

	def ffNet (self):
		# trouver les meta
		data = self.title.split (', ')
		self.title = data [0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title [:f]
		d= self.find ('https://www.fanfiction.net/u/')
		if d<0:
			d= self.find ('https://www.fictionpress.com/u/')
			self.link = 'https://www.fictionpress.com/s/'
		f= self.find ('>', d) -1
		self.autlink = self.text [d:f]
		d= self.find ('<', f)
		self.author = self.text [f+2:d]
		if subject: self.subject = subject
		else:
			self.subject = data [1] [2:]
			if ' fanfic' in self.subject:
				f= self.subject.find (' fanfic')
				self.subject = self.subject [:f]
			d= self.find ('Rated: <a')
			d= self.find ('</a>', d) +8
			f= self.find ('Reviews: <a', d)
			data = self.text [d:f].split (' - ')
			self.subject = self.subject +', '+ data [1].replace ('/', ', ')
		if 'fictionpress' in self.link:
			d= self.find ('/s/') +3
			f= self.find ('/', d) +1
			self.link = self.link + self.text [d:f] +'1/'
			d= self.find ('/', f) +1
			f= self.find ("'", d)
			self.link = self.link + self.text [d:f]
		else: self.link = self.metas ['canonical']
		self.metas = {}
		# trouver le texte
		d= self.find ('<p>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]

	def medium (self, subject):
		# récupérer les metadonnées
		self.link = self.title
		d= self.find ('"creator":') +12
		f= self.find ('"', d)
		self.author = self.text [d:f]
		d-=15
		f= self.text [:d].rfind ('@') +1
		self.autlink = 'https://gen.medium.com/@' + self.text [f:d]
		d= self.link.rfind ('/') +1
		f= self.link.rfind ('-')
		self.title = self.link [d:f].replace ('-', ' ')
		if subject: self.subject = subject
		# récupérer le texte
		d= self.find ('<p>')
		f= self.text.rfind ('<h2>GEN</h2>')
		self.text = self.text [d:f]
		f= self.text.rfind ('</p>') +4
		self.text = self.text [:f]
		self.replace ('<div>')
		self.replace ('</div>')
	#	self.delImgLink()

	def menaceTheoriste (self):
		self.subject = 'sciences'
		self.cleanWeb()
		self.replace ('<div>')
		self.replace ('</div>')
		d= self.find ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.find ('>', d) -1
		self.autlink = self.text [d:f]
		d=f+2
		f= self.find ('</a>', d)
		self.author = self.text [d:f]
		d= self.find ('</h1>')
		d= self.find ('</header>', d) +9
		f= self.find ('<footer>', d)
		self.text = self.text [d:f]
		f= self.find ('#comments')
		f= self.text [:f].rfind ('<a')
		f= self.text [:f].rfind ('>') +1
		self.text = self.text [:f]

	def fDatingS (self):
		self.subject = 'feminisme'
		# self.title = 'fds '+ findTextBetweenTag (self.text, 'title').lower()
		self.title = 'fds '+ self.title
		self.text = findTextBetweenTag (self.text, 'article')
		self.author = findTextBetweenTag (self.text, 'li')
		d= self.find ('<article>') +9
		d= self.find ('<', d)
		self.text = self.text [d:]
		self.replace ('<div>')
		self.replace ('</div>')

	def jmdoudoux (self):
		self.subject = 'programmation'
		self.author = 'jean-michel doudoux'
		self.autlink = 'http://www.jmdoudoux.fr/'
		self.text = self.text.lower()
		d= self.find ('</h1>') +5
		f= self.rfind ('<hr>')
		self.text = self.text[d:f]
