#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from classList import List
from classText import Text
from classFile import Article
from classHtml import Html, findTextBetweenTag
import logger

help = """
récupérer les pages de certains sites que j'aime beaucoup
utilisation: python fanfic url
l'url peut correspondre à une page ou un fichier local
"""
class Fanfic (Html):
	def fromWeb (self, url, subject=None):
		if url[:4] == 'http':
			self.link = url
			html = Html()
			html.link = url
			html.fromWeb()
			self.toPath()
		else:
			if url[-5:] != '.html': url = 'b/' + url + '.html'
			self.path = url
			self.fromPath()
			self.read()
		self.clean()
		if subject: self.subject = subject
		if 'http://www.gutenberg.org/' in url:				self.gutemberg()
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebGratuit()
		elif 'https://archiveofourown.org/works/' in url:	self.aoooWeb()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.reddit()
		elif 'http://uel.unisciel.fr/' in url:				self.unisciel()
		elif 'gtb'		in url: self.gutemberg()
		elif 'egb'		in url: self.ebGratuit()
		elif 'b/aooo.html' == url: self.aoooLocal()
		elif 'ffNet'	in url: self.ffNet()
		elif 'medium'	in url: self.medium()
		self.metas = {}
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace ('><', '>\n<')
		article = self.toArticle()
		logger.log (article.autlink)
		logger.log (article.link)
		article.write()

	def findSubject (self):
		if self.subject:
			self.subject = self.subject.replace ('/', ', ')
			self.subject = self.subject.replace (', ', ', ')
			self.subject = self.subject.replace ('-', ', ')
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		subjectDict = {
			'romance': ('romance', ' sex', 'x reader', 'rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars'),
			'rockers': ('rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars'),
			'monstres': ('mythology', 'vampire', 'naga', 'pokemon'),
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

	def usePlaceholders (self):
		placeholders = ('y/n', 'e/c', 'h/c', 'l/n')
		for ph in placeholders:
			self.text = self.text.replace (ph.upper(), ph)
			self.text = self.text.replace ('('+ ph +')', ph)
			self.text = self.text.replace ('['+ ph +']', ph)
		self.text = self.text.replace ('y/n', 'Deborah')
		self.text = self.text.replace ('e/c', 'grey')
		self.text = self.text.replace ('h/c', 'dark blond')
		self.text = self.text.replace ('l/n', 'Powers')

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
		self.text = self.text.replace ('<div>')
		self.text = self.text.replace ('</div>')
		self.text = self.text.replace ('<img', '</p><img')
		self.text = self.text.replace ("png'>","png'><p>")
		self.text = self.text.replace ('<p><p>', '<p>')
		self.text = self.text.replace ('</p></p>', '</p>')
		self.text = self.text.replace ('<p>', '</p><p>')
		self.text = self.text.replace ('</p>', '</p><p>')
		self.text = self.text.replace ('<p></p>')
		self.text = self.text.replace ('<p><p>', '<p>')
		self.text = self.text.replace ('<p><img', '<img')
		self.text = self.text.replace ("png'></p>","png'>")
		self.text = self.text [4:-3]
		self.text = self.text.replace ('../res/', 'bv-'+ subject +'/')
		self.text = self.text.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01.png'><p>", ' <b>ADP +P --> ATP</b> ')
		self.text = self.text.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01_1.png'><p>", ' <b>ATP --> ADP +P</b> ')
		self.styles.append ('unisciel.css')

	def gutemberg (self):
		# le titre
		d= self.text.find ('Title:') +7
		f= self.text.find ('Author:', d) -1
		self.title = self.text [d:f]
		# l'auteur
		d= f+9
		f= self.text.find ('Release', d) -1
		self.author = self.text [d:f]
		# le sujet est impossible à trouver
		self.text.findSubject()
		# le texte
		d= self.text.find ('<h1>')
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
		self.delImgLink()
		self.metas = {}

	def ebGratuit (self):
		self.delImgLink()
		# l'auteur
		d= self.text.find ('<p class=Auteur>') +16
		f= self.text.find ('</p>', d)
		self.author = self.text [d:f].lower()
		# le titre
		d= self.text.find ('<title>') +7
		f= self.text.find ('</title>', d)
		self.title = self.text [d:f].lower()
		# le texte
		self.clean()
		f= self.text.find ('<h1>À propos de cette édition électronique</h1>')
		self.text = self.text [:f]
		# le sujet
		self.text.findSubject()

	def menaceTheoriste (self):
		self.subject = 'sciences'
		self.clean()
		self.text = self.text.replace ('<div>')
		self.text = self.text.replace ('</div>')
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
		self.text = self.text.replace ('<div>')
		self.text = self.text.replace ('</div>')
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
		self.text = self.text.replace ('<div>')
		self.text = self.text.replace ('</div>')
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

	def ffNet (self):
		# trouver les meta
		data = self.title.split (', ')
		self.title = data [0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title [:f]
		d= self.text.find ('https://www.fanfiction.net/u/')
		if d<0:
			d= self.text.find ('https://www.fictionpress.com/u/')
			self.link = 'https://www.fictionpress.com/s/'
			f= self.text.find ('>', d) -1
			self.autlink = self.text [d:f]
			d= self.text.find ('<', f)
			self.author = self.text [f+2:d]
		else:
			self.subject = data [1] [2:]
			if ' fanfic' in self.subject:
				f= self.subject.find (' fanfic')
				self.subject = self.subject [:f]
			d= self.text.find ('Rated: <a')
			d= self.text.find ('</a>', d) +8
			f= self.text.find ('Reviews: <a', d)
			data = self.text [d:f].split (' - ')
			self.subject = self.subject +', '+ data [1].replace ('/', ', ')
		if 'fictionpress' in self.link:
			d= self.text.find ('/s/') +3
			f= self.text.find ('/', d) +1
			self.link = self.link + self.text [d:f] +'1/'
			d= self.text.find ('/', f) +1
			f= self.text.find ("'", d)
			self.link = self.link + self.text [d:f]
		else: self.link = self.metas ['canonical']
		self.metas = {}
		# trouver le texte
		d= self.text.find ('<p>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]

	def aoooLocal (self):
		self.styles =[]
		self.metas ={}
		self.title = self.title.replace (' [Archive of Our Own]', "")
		data = self.title.split (' - ')
		self.title = data[0]
		if len (data) >3 and 'hapter' in data[1]: self.author = data.pop (1)
		self.author = data[1]
		self.subject = data[2]
		self.subject = self.subject.replace (' (band)', "")
		self.clean()
		# le lien
		d= self.text.find ("<a href='/downloads/") +20
		f= self.text.find ('/', d)
		self.link = 'https://archiveofourown.org/works/' + self.text[d:f]
		self.aoooCommon()
		
	def aoooWeb (self):
		if 'This work could have adult content. If you proceed you have agreed that you are willing to see such content' in self.text:
			print ('fichier protégé', self.title)
			return
		self.clean()
		self.text = self.text.replace ('<br>', '</p><p>')
		self.text = findTextBetweenTag (self.text, 'body')
		# le titre
		d= self.text.find ('<h2>') +4
		f= self.text.find ('</h2>', d)
		self.title = self.text [d:f]
		self.title = self.title.strip()
		self.title = self.title.strip ('.')
		self.aoooCommon()

	def aoooCommon (self):
		# le sujet
		d= self.text.find ('Category:<ul><li><a') +20
		d= self.text.find ('>', d) +1
		f= self.text.find ('</a>', d)
		if self.text[d:f] in ('F/M', 'F/F') and 'romance' not in self.subject: self.subject = ', romance'+ self.subject
		self.findSubject()
		"""
		d= self.text.find ('Fandoms:<ul><li><a', f) +20
		d= self.text.find ('>', d) +1
		f= self.text.find ('</a>', d)
		if self.text[d:f] not in self.subject: self.subject = self.subject +', '+ self.text[d:f]
		"""
		self.subject = self.subject.replace (' - Fandom', "")
	#	self.subject = self.subject[2:]
		# l'auteur
		d= self.text.find ("<h3><a href='/users/") +13
		f= self.text.find ('>', d) -1
		self.autlink = self.text[d:f]
		d= f+2
		f= self.text.find ('<', d)
		self.author = self.author.replace ('-',' ')
		self.author = self.author.replace ('_',' ')
		self.author = self.author.strip()
		self.text = self.text.replace ('<h3>Chapter Text</h3>')
		# le texte ne compte qu'un seul chapître
		d= self.text.find ('<h3>Work Text:</h3>') +19
		# le texte compte plusieurs chapîtres
		if d==18: d= self.text.find ("<h3><a href='/works/")
		f= self.text.rfind ('<h3>Actions</h3>')
		self.text = Text (self.text [d:f])
		self.text = self.text.replace ('<div>')
		self.text = self.text.replace ('</div>')
		if "<h3><a href='/works/" in self.text:
			chapters = List()
			chapters.fromText ("<h3><a href='/works/", self.text)
			chapterRange = chapters.range (1)
			for c in chapterRange:
				d= chapters [c].find ('>') +1
				chapters [c] = chapters [c] [d:]
			self.text = '<h2>'.join (chapters)
			self.text = self.text.replace ('</a></h3>', '</h2>')
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
			d= self.text.find ('<h3>Notes:</h3>')
			if d> halfText: self.text = self.text [:d]
		self.usePlaceholders()
		self.text = self.text.replace ('h2>', 'h1>')
		if '<h3>Series this work belongs to:</h3>' in self.text:
			f= self.text.find ('<h3>Series this work belongs to:</h3>')
			self.text = self.text[:f]

if len (argv) >=2:
	url = argv[1]
	subject = None
	page = Fanfic()
	if len (argv) >=3: subject = argv[2]
	page.fromWeb (url, subject)
# le nom du fichier n'a pas ete donne
else: print (help)


