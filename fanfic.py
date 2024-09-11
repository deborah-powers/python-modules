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

# setattr (htmlCls.HtmlTag, 'uniscielImg', uniscielImg)

class Fanfic (htmlCls.Html, Article):
	def __init__ (self, url, subject=None):
		if url in 'aooo unisciel recette': url = 'b/' + url + '.html'
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, url)
		if subject: self.subject = subject
		if 'https://archiveofourown.org/' in self.text or 'https://archiveofourown.org/' in self.link or url == 'b/aooo.html': self.fromAooo()
		elif '://uel.unisciel.fr/' in url or url == 'b/unisciel.html':				self.unisciel()
		elif '://www.gutenberg.org/' in url:	self.gutemberg()
		elif 'https://www.test-recette.fr/recette/' in url or url == 'b/recette.html':	self.testRecette()
		elif 'scoubidou'	in url: self.scoubidou()
		elif 'b/ffnet.html' == url:		self.ffNet()
		elif 'b/fpress.html' == url:	self.fPress()
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebGratuit()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.reddit()
		elif 'egb'		in url: self.ebGratuit()
		elif 'medium'	in url: self.medium()
		else: self.setByMain()
		self.meta ={ 'link': self.link, 'author': self.author, 'autlink': self.autlink, 'subject': self.subject }
		self.delAttributes()
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
			'tricot': ('tricot', 'point', 'crochet'),
			'programmation': ( 'test de recette', "test d'usine", 'cahier de test', 'cas de test' )
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
			self.replace (ph.upper(), ph)
			self.replace ('('+ ph +')', ph)
			self.replace ('['+ ph +']', ph)
			self.replace ('{'+ ph +'}', ph)
		self.replace ('y/n', 'Deborah')
		self.replace ('e/c', 'grey')
		self.replace ('h/c', 'dark blond')
		self.replace ('l/n', 'Powers')

	def fromAooo (self):
		# fanfic enregistrée via le bouton télécharger en html
		self.meta ={}
		# le lien de la fanfic
		if not self.link:
			tag = self.getOneByTagClass ('dd', 'bookmarks')
			tag = htmlCls.getOneByTag (tag, 'a')
			tag = htmlCls.getAttribute (tag, 'href')
			self.link = 'https://archiveofourown.org' + tag.replace ('bookmarks', "")
			"""
			tag = self.getOneByTagClass ('p', 'message')
			log.logMsg (tag)
			tags = htmlCls.getAllByTag (tag, 'a')
			self.link = htmlCls.getAttribute (tags[1], 'href')
			"""
		# le titre
	#	self.title = self.getOneByTag ('h1')
		self.title = self.getOneByTagClass ('h2', 'title heading')
		self.title = htmlCls.getInnerHtml (self.title)
		self.title = htmlCls.cleanTitle (self.title)
		# l'auteur
	#	tag = self.getOneByTagClass ('div', 'byline')
		tag = self.getOneByTagClass ('h3', 'byline heading')
		tag = htmlCls.getOneByTag (tag, 'a')
		self.author = htmlCls.getInnerHtml (tag)
		self.autlink = htmlCls.getAttribute (tag, 'href')
		f= self.autlink.find ('/pseuds/')
		self.autlink = self.autlink[:f]
		# le sujet
		tag = self.getOneByTagClass ('dl', 'tags')
	#	tag = self.getOneByTagClass ('dd', 'fandom tags')
		tag = tag.replace ('http://archiveofourown.org/tags/', "")
		tags = htmlCls.getAllByTag (tag, 'a')
		for link in tags: self.subject = self.subject +'\t'+ htmlCls.getInnerHtml (link)
		self.findSubject()
		# le texte
		self.setById ('workskin')
	#	self.setById ('chapters')
		self.delAttributes()
		self.replace ('<div>',"")
		self.replace ('</div>',"")

	def unisciel (self):
		self.subject = 'biologie'
		self.author = 'unisciel'
		self.autlink = 'https://uel.unisciel.fr/biologie/module1/module1/co/module1_1.html'
		if not self.link: self.link = 'https://uel.unisciel.fr/biologie/module1/module1_ch01/co/'
		self.setByTag ('section')
		self.delAttributes()
		self.replace ('<div>')
		self.replace ('</div>')
		self.replace ('../res/', 'evo/')
	#	self.replace ('../res/', 'https://uel.unisciel.fr/biologie/module1/module1_ch01/res/')
		self.title = 'unisciel-recup'
	#	self.styles.append ('unisciel.css')

	def testRecette (self):
		self.subject = 'programmation'
		self.title = self.title[8:]
		self.author = 'test-recette'
		self.autlink = 'https://www.test-recette.fr/recette/'
		if not self.link: self.link = self.meta['og:url']
		self.delScript()
		self.delAttributes()
		self.delEmptyTags()
		self.text = self.text.replace ('<div>',"")
		self.text = self.text.replace ('</div>',"")
		d= self.text.find ('<h1')
		self.text = self.text[d:]
		self.setByTag ('section')

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

	def scoubidou (self):
		# pages de lartdesscoubidous.com
		self.title = htmlCls.getTitle (self.text)
		if ' |' in self.title:
			d= self.title.find (' |')
			self.title = self.title[:d]
		self.author = 'art des scoubidous'
		self.autlink = 'https://lartdesscoubidous.com/'
		self.link = 'https://lartdesscoubidous.com/'
		self.subject = 'travaux manuels'
		self.text = htmlCls.getcontentByTag (self.text, 'section')
		d= self.text.find ('<aside')
		self.text = self.text[:d]
		self.replace ('<hr/>')
		self.replace ('<table><tbody><tr><td>', '<figure><figcaption>')
		self.replace ('</td></tr></tbody></table>', '</figure>')
		self.replace ('</td></tr><tr><td>', '</figure><figure><figcaption>')
		self.replace ('</td><td>', '</figcaption>')
		self.replace ('<br/>', '</p><p>')
		self.replace ('</strong>', "")
		self.replace ('<strong>', "")
		self.replace ('.jpg"', ".jpg'")
		self.replace (".jpg'></p>", ".jpg'>")
		self.replace ('alt=""></p>', 'alt="">')
		self.replace (".jpg'></figcaption>", ".jpg'>")
		self.replace ('alt=""></figcaption>', 'alt="">')
		self.replace ('<p><img', '<img')
		self.replace ('<figcaption><img', '<figcaption></figcaption><img')
		self.replace (' src="https://lartdesscoubidous.com/wp-content/uploads/2012/10/', " src='photos/")
		self.replace ('><h', '>\n<h')
		self.replace ('><figure', '>\n<figure')
		chiffres =( ('10', 'j'), ('11', 'k'), ('12', 'l'), ('13', 'm'), ('14', 'n'), ('15', 'o'), ('16', 'p'), ('17', 'q'), ('18', 'r'), ('19', 's'), ('20', 't'), ('21', 'u'), ('22', 'v'), ('23', 'w'), ('24', 'x'), ('25', 'y'), ('26', 'z'), ('1', 'a'), ('2', 'b'), ('3', 'c'), ('4', 'd'), ('5', 'e'), ('6', 'f'), ('7', 'g'), ('8', 'h'), ('9', 'i') )
		for c,l in chiffres: self.replace (c+ '.jpg', '-'+l+ '.jpg')

	def menaceTheoriste (self):
		self.subject = 'sciences'
		self.clean()
		self.replace ('<div>', "")
		self.replace ('</div>', "")
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

	def medium (self, subject=""):
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
		self.replace ('<div>', "")
		self.replace ('</div>', "")
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
		self.replace ('<div>', "")
		self.replace ('</div>', "")
		# auteur
		f= self.link.find ('/', 26)
		self.autlink = self.link [:f]
		self.author = self.autlink [25:]
		self.title = self.title.replace ('#', ' ')
		# finir le texte
		self.replace ('<li><p>', '<li>')
		self.replace ('</p></li>', '</li>')
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
		log.logMsg (self.text, True)
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