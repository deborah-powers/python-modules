#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.list import List
from fileHtml import FileHtml, findTextBetweenTag, listTagsKeep, listTags
from fileHtml.htmlArticle import ArticleHtml
from listFiles import ListArticle
import debutils.logger as logger

help = """
récupérer les pages de certains sites que j'aime beaucoup
utilisation: python %s url
l'url peut correspondre à une page ou un fichier local
""" % __file__


class Fanfic (ArticleHtml):
	def ficWeb (self, url, subject=None):
		self.extension = 'html'
		if url[:4] == 'http':
			self.link = url
			FileHtml.fromUrl (self)
		else:
			self.file = url
			self.fromFile()
		self.clean()
		# self.cleanWeb()
		if 'http://www.gutenberg.org/' in url:				self.ficficGutemberg (subject)
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ficEbg (subject)
		elif 'https://archiveofourown.org/works/' in url:	self.ficAooo()
		elif 'https://www.ficDev.com/' in url:			self.ficDev()
		elif 'https://menace-theoriste.fr/' in url:			self.ficTheoriste()
		elif 'https://www.ficReddit.com/r/' in url:			self.ficficReddit()
		elif 'https://www.therealfemaledatingstrategy.com/' in url:	self.ficFds()
		elif 'https://www.ficBourse.com/' in url:			self.ficBourse()
		elif 'http://uel.ficUnisciel.fr/' in url:				self.ficficUnisciel (subject)
		elif 'gtb'		in url: self.ficficGutemberg (subject)
		elif 'egb'		in url: self.ficEbg (subject)
		elif 'aooo'		in url: self.ficAoooLcl (subject)
		elif 'ficFfn'	in url: self.ficFfn (subject)
		elif 'medium'	in url: self.ficMedium (subject)
		elif 'logimmo'	in url: self.logicImmo()
		elif 'seloger'	in url: self.seLoger()
		elif 'adapt'	in url: self.adapt()
		self.metas = {}
		self.replace (' <', '<')
		self.replace ('><', '>\n<')
		if self.contain ('</a>') or self.contain ('<img'): self.toFile()
		else: self.toFileText()

	def findSubject (self):
		self.subject = self.subject.lower()
		if 'pokemon' in self.subject:
			self.subject = 'romance, pokemon'

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
		for tag in listTags: self.replace ('<'+tag+'></'+tag+'>',"")
		self.delImgLink()
		self.metas = {}
		self.toFile()

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
		if len (data) >3:
			print ('trop de blocks dans le titre', self.title)
			if 'hapter' in data[1]: self.author = data.pop (1)
		self.title = data[0]
		self.author = data[1]
		self.subject = data[2]
		self.subject = self.subject.replace (' [Archive of Our Own]', "")
		self.findSubject()
		self.cleanWeb()
		d= self.index ("archiveofourown.org/works") +26
		f= self.index (" ", d)
		self.link = 'https://archiveofourown.org/works/' + self.text [d:f]
		if "'" in self.link: f= self.link.find ("'")
		else: f= self.link.find ('"')
		self.link = self.link[:f]
		self.autlink = 'https://archiveofourown.org/users/' + self.author
		# trouver le texte
		self.delScript()
		d= self.index ('<h2>')
		d= self.index ('</h3>', d) +5
		f= self.rindex ('<h3>Actions</h3>')
		self.text = self.text [d:f]
		self.delImgLink()
		self.replace ('<div>')
		self.replace ('</div>')
		"""
		if self.contain ('<h3>Chapter Text</h3>'):
			chapters = List()
			chapters.fromText ('<h3>Chapter Text</h3>', self.text)
			chapterRange = chapters.range()
			for c in chapterRange:
				logger.log (str(c) +'\t'+ chapters[c][:100])
				if '<h3>Notes:</h3>' in chapters[c]:
					f= chapters[c].rfind ('<h3>Notes:</h3>')
					chapters[c] = chapters[c][:f]
					if '<h3>Notes:</h3>' in chapters[c]:
						f= chapters[c].rfind ('<h3>Notes:</h3>')
						if f>500: chapters[c] = chapters[c][:f]
			self.text = chapters.toText ("")
		"""
		self.replace ('</blockquote><h3>Notes:</h3><blockquote>')
		self.replace ('</h3><hr>', '</h3>')
		self.replace ('</h2><hr>', '</h2>')
		if not self.contain ('</h2>'): self.replace ('h3>', 'h2>')
		self.usePlaceholders()

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
		# l'auteur et sa page
		d= self.index ("<a href='/users/", f) +9
		f= self.index ("'", d)
		self.autlink = self.text [d:f]
		d= self.index ('>', d) +1
		f= self.index ('</a>', d)
		self.author = self.text [d:f]
		# le sujet
		self.findSubject (subject)
		if self.subject == 'histoire':
			d= self.index ('Additional Tags:<ul>') +24
			d= self.index ('>', d) +1
			f= self.index ('<', d)
			self.subject = self.text [d:f]
		# le texte ne compte qu'un seul chapître
		d= self.index ('<h3>Work Text:</h3>') +19
		# le texte compte plusieurs chapîtres
		if d==18: d= self.index ("<h3><a href='/works/")
		f= self.rindex ('<h3>Actions</h3>')
		self.text = self.text [d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		self.replace ('<h3>Chapter Text</h3>')
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
	#	self.title = 'tmp'

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

	def logicImmo (self):
		# https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1/pricemin=40000/pricemax=200000/areamin=30
		self.subject = 'immobilier'
		self.author = 'logic immo'
		self.autlink = 'https://www.logic-immo.com/'
		self.styles =[]
		self.metas ={}
		self.delScript()
		self.delStyle()
		d= self.index ('<div id="header-offer-')
		f= self.rindex ('<i class="li-icon li-icon--telephone">')
		self.text = self.text[d:f]
		"""
		self.replace ("Vous souhaitez investir en Pinel ?</p>")
		self.cleanWeb()
		self.replace ('<div>')
		self.replace ('</div>')
		f= self.index ('</section>', d)
		annonceList = List()
		annonceList.fromText (" Voir l'annonce", self.text)
		annonceList.pop (-1)
		annonceRange = annonceList.range()
		self.text = annonceList.toText ('<p></p>')
		"""

	def seLoger (self):
		# https://www.seloger.com/list.htm?projects=2,5&types=1&natures=1,2,4&places=[{%22subDivisions%22:[%2275%22]}]&price=NaN/200000&surface=30/NaN&enterprise=0&qsVersion=1.0&m=search_refine
		self.subject = 'immobilier'
		self.author = 'se loger'
		self.autlink = 'https://www.seloger.com/'
		self.title = 'se-loger'
		self.fileFromData()
		self.styles =[]
		self.metas ={}
		d= self.index ('<div data-test="sl.title')
		d= self.index ('<ul', d)
		f= self.rindex ('</div>')
		self.text = self.text[d:f]
		self.cleanWeb()
		self.text = self.text[4:]
		logeList = List()
		logeList.fromText ('Appartement<ul>', self.text)
		logeRang = logeList.range()
		self.text =""
		for l in logeRang:
			text = seLogerUnite (logeList[l])
			if text: self.text = self.text + text

def seLogerUnite (text):
	if 'viager' in text or 'bouquet' in text: return ""
	template = "<hr><p>ville: %s</p><p>prix: %s</p><p>surface: %s</p>"
	f= text.find (' m²')
	d= text[:f].rfind ('>') +1
	surface = text[d:f]
	f= text.find ('€<')
	d= text[:f].rfind ('>') +1
	prix = text[d:f]
	d= text.find ('<span>', d) +6
	f= text.find ('</span>', d)
	adresse = text[d:f] +' - '
	d= f+13
	f= text.find ('</span>', d)
	adresse = adresse + text[d:f]
	template = template %( adresse, prix, surface)
	return template

"""
lfic = ListArticle ('fanfic')
lfic.get()
nfic = lfic.getBySubject ('batverse')
nfic.show ('batman')
"""
if len (argv) >=2:
	url = argv[1]
	subject = None
	page = Fanfic()
	if len (argv) >=3: subject = argv[2]
	page.ficWeb (url, subject)
# le nom du fichier n'a pas ete donne
else: print (help)
