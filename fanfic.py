#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from list import List
from htmlFile import FileHtml, findTextBetweenTag, listTags
from htmlArticle import ArticleHtml
from listFiles import ListArticle
import logger

class Fanfic (ArticleHtml):
	def ficWeb (self, url, subject=None):
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
		if 'http://www.gutenberg.org/' in url:				self.ficGutemberg (subject)
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ficEbg (subject)
		elif 'https://archiveofourown.org/works/' in url:	self.ficAooo()
		elif 'https://www.dev.com/' in url:				self.ficDev()
		elif 'https://menace-theoriste.fr/' in url:			self.ficTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.ficReddit()
		elif 'https://www.therealfemaledatingstrategy.com/' in url:	self.ficFds()
		elif 'https://www.abcBourse.com/' in url:			self.ficBourse()
		elif 'http://uel.unisciel.fr/' in url:			self.ficUnisciel (subject)
		elif 'gtb'		in url: self.ficGutemberg (subject)
		elif 'egb'		in url: self.ficEbg (subject)
		elif 'b/aooo.html' == url: self.ficAoooLcl (subject)
		elif 'ficFfn'	in url: self.ficFfn (subject)
		elif 'medium'	in url: self.ficMedium (subject)
		elif 'adapt'	in url: self.adapt()
		elif 'jmdoudoux.fr'	in url: self.jmdoudoux()
		else: self.cleanWeb()
		self.metas = {}
		self.replace (' <', '<')
		self.replace ('><', '>\n<')
		if self.contain ('</a>') or self.contain ('<img'): self.toFile()
		else: self.toFileText()

	def findSubject (self, subject=None):
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		if subject:
			subject = subject.replace ('/', ', ')
			subject = subject.replace (', ', ', ')
			subject = subject.replace ('-', ', ')
			subjectList = subject
		subjectDict = {
			'romance': ('romance', ' sex', 'x reader', 'rasmus', 'ville valo', 'jyrki', 'him (band)'),
			'rockers': ('rasmus', 'ville valo', 'jyrki', 'him (band)'),
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

	""" ________________________ pour chaque site ________________________ """

	def ficBourse (self):
		self.subject = 'argent'
		self.author = 'abc bourse'
		d= self.index ('<h1>')
		f= self.index ('<p>Vous avez aimé cet article')
		self.text = self.text[d:f]
		if self.contain ('suivant.gif'):
			f= self.index ('suivant.gif')
			self.text = self.text[0:f]
			f= self.rindex ('</p>') +4
			self.text = self.text[0:f]

	def ficVg (self):
		self.subject = 'sortie'
		self.author = 'vide-grenier'
		d= self.index ('<h2>')
		f= self.rindex ('<span>Voir les prochaines')
		self.text = self.text[d:f]
		toReplace =( ('<h2><span>', '<h2>'), ('</span></h2>', '</h2>'), ('<span><span>', '<span>'), ('</span></span>', '</span>') )
		for i,j in toReplace: self.replace (i,j)
		textList = List()
		textList.fromText ('<h3>', self.text)
		textRange = textList.range (1)
		"""
		for t in textRange:
			logger.log (str(t) +'\t'+ textList[t])

		self.replace ('><span>', '>')
		self.replace ('</span><', '<')
		"""

	def ficReddit (self):
		if 'FemaleDatingStrategy' in self.link:
			self.subject = 'feminisme'
			self.title = 'fds '+ self.title
		else: self.subject = 'opinion'
		self.cleanWeb()
		self.cleanLink()
		d= self.index ('<h1>')
		d= self.index ('<p>', d)
		f= self.index ('<div>ficReddit Inc')
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
		f= self.rindex ('<hr>Created')
		self.text = self.text [:f]
		# zapper les commentaires
		f= self.index ('<button>share</button>')
		self.text = self.text [:f]
		f= self.rindex ('</p>') +4
		self.text = self.text [:f]

	def ficUnisciel (self, subject):
		self.subject = 'cours'
		self.author = 'ficUnisciel'
		self.text = findTextBetweenTag (self.text, 'body')
		self.cleanWeb()
		self.delScript()
		d= self.index ('<td>') +4
		f= self.index ('</td>', d)
		self.title = self.text [d:f].lower()
		d= self.index ('<p>')
		f= self.rindex ('</p>') +4
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
		self.styles.append ('ficUnisciel.css')

	def ficGutemberg (self, subject=None):
		# le titre
		d= self.index ('Title:') +7
		f= self.index ('Author:', d) -1
		self.title = self.text [d:f]
		# l'auteur
		d= f+9
		f= self.index ('Release', d) -1
		self.author = self.text [d:f]
		# le sujet est impossible à trouver
		self.findSubject (subject)
		# le texte
		d= self.index ('<h1>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]
		# cas spécifiques
		if (self.contain ('<p>CONTENTS</p>')):
			d= self.index ('<p>CONTENTS</p>')
			d= self.index ('<hr>', d)
			self.text = self.text [d:]
		if (self.contain ('<h2>Footnotes:</h2>')):
			f= self.index ('<h2>Footnotes:</h2>')
			self.text = self.text [:f]
		self.delImgLink()
		self.metas = {}

	def ficEbg (self, subject=None):
		self.delImgLink()
		# l'auteur
		d= self.index ('<p class=Auteur>') +16
		f= self.index ('</p>', d)
		self.author = self.text [d:f].lower()
		# le titre
		d= self.index ('<title>') +7
		f= self.index ('</title>', d)
		self.title = self.text [d:f].lower()
		# le texte
		self.cleanWeb()
		f= self.index ('<h1>À propos de cette édition électronique</h1>')
		self.text = self.text [:f]
		# le sujet
		self.findSubject (subject)

	def ficDev (self, subject=None):
		self.findSubject (subject)
		self.cleanWeb()
		self.replace ('<br>', '</p><p>')
		self.delScript()
		f= self.title.rfind (' ')
		self.title = self.title [:f]
		d= self.index ("By<a href=") +11
		f= self.index ("'", d)
		self.autlink = self.text [d:f]
		d= self.index ('>', f) +1
		f= self.index ('<', d)
		self.author = self.text [d:f]
		d= self.index ('<p>', f)
		self.text = self.text [d:]
		self.replace ('<div>',"")
		self.replace ('</div>',"")
		f= self.index ('>See More by')
		self.text = self.text [:f]
		f= self.rindex ('</p>') +4
		self.text = self.text [:f]
	#	if self.text [-1] != '>': self.text = self.text +'</p>'

	def ficAoooLcl (self, subject=None):
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
		d= self.index ("<a href='/downloads/") +20
		f= self.index ('/', d)
		self.link = 'https://archiveofourown.org/works/' + self.text[d:f]
		self.ficAoooCommon (subject)
		
	def ficAooo (self, subject=None):
		if 'This work could have adult content. If you proceed you have agreed that you are willing to see such content' in self.text:
			print ('fichier protégé', self.title)
			return
		self.cleanWeb()
		self.replace ('<br>', '</p><p>')
		self.text = findTextBetweenTag (self.text, 'body')
		# le titre
		d= self.index ('<h2>') +4
		f= self.index ('</h2>', d)
		self.title = self.text [d:f]
		self.title = self.title.strip()
		self.title = self.title.strip ('.')
		self.ficAoooCommon (subject)

	def ficAoooCommon (self, subject=None):
		# le sujet
		if subject and subject not in self.subject: self.subject = self.subject +', '+ subject
		d= self.index ('Category:<ul><li><a') +20
		d= self.index ('>', d) +1
		f= self.index ('</a>', d)
		if self.text[d:f] in ('F/M', 'F/F') and 'romance' not in self.subject: self.subject = ', romance'+ self.subject
		self.findSubject (subject)
		"""
		d= self.index ('Fandoms:<ul><li><a', f) +20
		d= self.index ('>', d) +1
		f= self.index ('</a>', d)
		if self.text[d:f] not in self.subject: self.subject = self.subject +', '+ self.text[d:f]
		"""
		self.subject = self.subject.replace (' - Fandom', "")
	#	self.subject = self.subject[2:]
		# l'auteur
		d= self.index ("<h3><a href='/users/") +13
		f= self.index ('>', d) -1
		self.autlink = self.text[d:f]
		d= f+2
		f= self.index ('<', d)
		self.author = self.text [d:f]
		self.author = self.author.replace ('-',' ')
		self.author = self.author.replace ('_',' ')
		self.author = self.author.strip()
		self.replace ('<h3>Chapter Text</h3>')
		# le texte ne compte qu'un seul chapître
		d= self.index ('<h3>Work Text:</h3>') +19
		# le texte compte plusieurs chapîtres
		if d==18: d= self.index ("<h3><a href='/works/")
		f= self.rindex ('<h3>Actions</h3>')
		self.text = self.text [d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		if self.contain ("<h3><a href='/works/"):
			chapters = List()
			chapters.fromText ("<h3><a href='/works/", self.text)
			chapterRange = chapters.range (1)
			for c in chapterRange:
				d= chapters [c].find ('>') +1
				chapters [c] = chapters [c] [d:]
			self.text = '<h2>'.join (chapters)
			self.replace ('</a></h3>', '</h2>')
		if self.contain ('<h2>Chapter ') and not self.contain ('</h2>'):
			chapters = List()
			chapters.fromText ('<h2>Chapter ', self.text)
			chapterRange = chapters.range (1)
			for c in chapterRange:
				d= chapters [c].find ('</a>: ') +6
				chapters [c] = chapters [c] [d:]
				chapters [c] = chapters [c].replace ('</h3>', '</h2>', 1)
			self.text = '<h2>'.join (chapters)
		# nettoyer le texte
		if self.contain ('<h3>Notes:</h3>'):
			halfText = self.length() /2
			d= self.index ('<h3>Notes:</h3>')
			if d> halfText: self.text = self.text [:d]
		self.usePlaceholders()
		self.replace ('h2>', 'h1>')

	def ficFfn (self, subject=None):
		# trouver les meta
		data = self.title.split (', ')
		self.title = data [0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title [:f]
		d= self.index ('https://www.fanfiction.net/u/')
		if d<0:
			d= self.index ('https://www.fictionpress.com/u/')
			self.link = 'https://www.fictionpress.com/s/'
		f= self.index ('>', d) -1
		self.autlink = self.text [d:f]
		d= self.index ('<', f)
		self.author = self.text [f+2:d]
		if subject: self.subject = subject
		else:
			self.subject = data [1] [2:]
			if ' fanfic' in self.subject:
				f= self.subject.find (' fanfic')
				self.subject = self.subject [:f]
			d= self.index ('Rated: <a')
			d= self.index ('</a>', d) +8
			f= self.index ('Reviews: <a', d)
			data = self.text [d:f].split (' - ')
			self.subject = self.subject +', '+ data [1].replace ('/', ', ')
		if 'fictionpress' in self.link:
			d= self.index ('/s/') +3
			f= self.index ('/', d) +1
			self.link = self.link + self.text [d:f] +'1/'
			d= self.index ('/', f) +1
			f= self.index ("'", d)
			self.link = self.link + self.text [d:f]
		else: self.link = self.metas ['canonical']
		self.metas = {}
		# trouver le texte
		d= self.index ('<p>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text [d:f]

	def ficMedium (self, subject):
		# récupérer les metadonnées
		self.link = self.title
		d= self.index ('"creator":') +12
		f= self.index ('"', d)
		self.author = self.text [d:f]
		d-=15
		f= self.text [:d].rfind ('@') +1
		self.autlink = 'https://gen.medium.com/@' + self.text [f:d]
		d= self.link.rfind ('/') +1
		f= self.link.rfind ('-')
		self.title = self.link [d:f].replace ('-', ' ')
		if subject: self.subject = subject
		# récupérer le texte
		d= self.index ('<p>')
		f= self.text.rfind ('<h2>GEN</h2>')
		self.text = self.text [d:f]
		f= self.text.rfind ('</p>') +4
		self.text = self.text [:f]
		self.replace ('<div>')
		self.replace ('</div>')
	#	self.delImgLink()

	def ficTheoriste (self):
		self.subject = 'sciences'
		self.cleanWeb()
		self.replace ('<div>')
		self.replace ('</div>')
		d= self.index ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.index ('>', d) -1
		self.autlink = self.text [d:f]
		d=f+2
		f= self.index ('</a>', d)
		self.author = self.text [d:f]
		d= self.index ('</h1>')
		d= self.index ('</header>', d) +9
		f= self.index ('<footer>', d)
		self.text = self.text [d:f]
		f= self.index ('#comments')
		f= self.text [:f].rfind ('<a')
		f= self.text [:f].rfind ('>') +1
		self.text = self.text [:f]

	def ficFds (self):
		self.subject = 'feminisme'
		# self.title = 'fds '+ findTextBetweenTag (self.text, 'title').lower()
		self.title = 'fds '+ self.title
		self.text = findTextBetweenTag (self.text, 'article')
		self.author = findTextBetweenTag (self.text, 'li')
		d= self.index ('<article>') +9
		d= self.index ('<', d)
		self.text = self.text [d:]
		self.replace ('<div>')
		self.replace ('</div>')

	def jmdoudoux (self):
		self.subject = 'programmation'
		self.author = 'jean-michel doudoux'
		self.autlink = 'http://www.jmdoudoux.fr/'
		self.text = self.text.lower()
		d= self.index ('</h1>') +5
		f= self.rindex ('<hr>')
		self.text = self.text[d:f]
