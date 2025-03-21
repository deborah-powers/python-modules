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
		if url in 'aooo unisciel recette wiki': url = 'b/' + url + '.html'
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, url)
		if subject: self.subject = subject
		if 'https://archiveofourown.org/' in self.text or 'https://archiveofourown.org/' in self.link or url == 'b/aooo.html':
			self.fromAooo()
			self.fromAoooSpe()
		elif '://uel.unisciel.fr/' in url or url == 'b/unisciel.html': self.unisciel()
		elif '://www.gutenberg.org/' in url: self.gutemberg()
		elif '://en.wikisource.org/wiki/' in url: self.wiki()
		elif 'https://www.test-recette.fr/recette/' in url or url == 'b/recette.html': self.testRecette()
		elif 'scoubidou' in url: self.scoubidou()
		elif 'b/ffnet.html' == url: self.ffNet()
		elif 'b/fpress.html' == url: self.fPress()
		elif 'https://www.ebooksgratuits.com/html/' in url: self.ebGratuit()
		elif 'https://menace-theoriste.fr/' in url: self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url: self.reddit()
		elif 'egb' in url: self.ebGratuit()
		elif 'wiki' in url: self.wiki()
		elif 'osmose' in url: self.fromOsmose()
		else: self.setByMain()
		self.delIcons()
		self.delAttributes()
		"""
		article = self.toText()
		if article: article.divide()
		else: self.divide()
		"""
		self.divide()

	def findSubject (self):
		if self.subject:
			self.subject = self.subject.replace ('/', ', ')
			self.subject = self.subject.replace (', ', ', ')
			self.subject = self.subject.replace ('-', ', ')
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		subjectDict = {
			'romance': ('romance', ' sex', 'x reader', 'rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars', 'integra', 'axi', 'damned caeli', 'jareth'),
			'rocker': ('rasmus', 'ville valo', 'jyrki', 'him (band)', '30 seconds to mars'),
			'tstm': ('30 seconds to mars', ), 'him': ('him (band)', 'ville valo'), '69eyes': ('jyrki', ),
			'hellsing': ('integra', 'axi', 'damned caeli'),
			'labyrinth': ('jareth',),
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

	def fromOsmose (self):
		self.meta ={}
		self.subject = 'travail'
		self.author = 'synergie'
		self.setByMain()
		tag = self.getOneByTag ('h1')
		title = '<h1>' + htmlCls.getInnerHtml (tag) +'</h1>'
		tag = self.getOneByTagClass ('div', 'wysiwyg')
		self.text = htmlCls.getInnerHtml (tag)
		self.text = title + self.text
		self.title = 'osmose nettoye'
		# éffacer les images
		self.delIcons()
		self.replace ('<picture class="wysiwyg-lightbox-wrapper"><img draggable="false" class="emoji wysiwyg-lightbox" alt="♦" src="https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/2666.png" data-lg-size="17-17"></picture>', ' - ')
		"""
		textList = self.text.split ('<picture')
		textRange = range (1, len (textList))
		for t in textRange:
			d=10+ textList[t].find ('</picture>')
			textList[t] = textList[t][d:]
		self.text = "".join (textList)
		textList = self.text.split ('<img')
		textRange = range (1, len (textList))
		for t in textRange:
			d=1+ textList[t].find ('>')
			textList[t] = textList[t][d:]
		self.text = "".join (textList)
		"""
		self.replace ("<a href='jcms/290967961_dbwikipage/fr/glossaire-liste-des-abreviations'>📄</a>")
		self.replace ("<a href='jcms/290967961_dbwikipage/fr/glossaire-liste-des-abreviations'>[m'ouvrir dans une nouvelle page]</a>")
		self.replace ('jcms/', 'https://osmose.numerique.gouv.fr/jcms/')
		self.delAttributes()
		self.replace ('<tbody>')
		self.replace ('</tbody>')
		self.replace ('div>', 'p>')
		self.replace ('<p><tr>', '<table><tr>')
		self.replace ('</tr></p>', '</tr></table>')
		self.replace ('</a>', '</a></p>')
		self.replace ('<a ', '<p><a ')
		self.replace ('<p><p>', '<p>')
		self.replace ('</p></p>', '</p>')
		self.replace ('</p>-</p>', '</p>')
		self.replace ('upload/docs/image/png/', 'osmose/')
		self.cleanRead()
		for tag in htmlCls.listTagsIntern:
			self.replace ('<'+ tag +'>', " ")
			self.replace ('</'+ tag +'>', " ")
		self.simplifyNesting()
		textList = self.text.split ('a compléter plus tard[begin]')
		textRange = range (len (textList) -1)
		for t in textRange:
			d=3+ textList[t].rfind ('<p>')
			textList[t] = textList[t][:d]
			d= textList[t+1].find ('a compléter plus tard')
			d= textList[t+1].find ('</p>', d)
			textList[t+1] = textList[t+1][d:]
		self.text = 'TODO: A compléter'.join (textList)

	def fromAoooSpe (self):
		self.text = self.text.replace ("<br/>---<br/>i do not permit my work to be used by third-party websites, apps or ai-based/ai-assisted works. do not use ai to do anything with my works or create anything inspired by my works.", "")
		self.text = self.text.replace ('<h3>summary:</h3><blockquote>', "")
		self.text = self.text.replace ('</blockquote><h3>work text:</h3>', '<hr/>')

	def fromAooo (self):
		# fanfic enregistrée via le bouton télécharger en html
		self.meta ={}
		# le lien de la fanfic
		if not self.link:
			tag = self.getOneByTagClass ('dd', 'bookmarks')
		#	tag = htmlCls.getOneByTag (tag, 'a')	le a est automatiquement trouvé via la dé-nidification
			tag = htmlCls.getAttribute (tag, 'href')
			self.link = 'https://archiveofourown.org' + tag.replace ('bookmarks', "")
			"""
			tag = self.getOneByTagClass ('p', 'message')
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
	#	tag = htmlCls.getOneByTag (tag, 'a')	le a est automatiquement trouvé via la dé-nidification
		self.author = htmlCls.getInnerHtml (tag)
		autlink = htmlCls.getAttribute (tag, 'href')
		f= autlink.find ('/pseuds/')
		self.meta['lien-auteur'] = autlink[:f]
		# le sujet
		tag = self.getOneByTagClass ('dl', 'tags')
	#	tag = self.getOneByTagClass ('dd', 'fandom tags')
		tag = tag.replace ('http://archiveofourown.org/tags/', "")
		tag = tag.replace ('/tags/', "")
		tags = htmlCls.getAllByTag (tag, 'a')
		for link in tags: self.subject = self.subject +'\t'+ htmlCls.getInnerHtml (link)
		self.findSubject()
		# le texte
		self.setById ('workskin')
	#	self.setById ('chapters')
		d= self.text.find ('<a rel="author"')
		d= self.text.find ('</h3>', d) +5
		self.text = self.text[d:]
		self.delAttributes()
		self.replace ('<h3>chapter text</h3>',"")
		self.replace ('<div>',"")
		self.replace ('</div>',"")

	def unisciel (self):
		self.subject = 'biologie'
		self.author = 'unisciel'
		self.meta = { 'lien-auteur': 'https://uel.unisciel.fr/biologie/module1/module1/co/module1_1.html' }
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
		self.meta = { 'lien-auteur': 'https://www.test-recette.fr/recette/' }
		if not self.link: self.link = self.meta['og:url']
		self.delScript()
		self.delAttributes()
		self.delEmptyTags()
		self.text = self.text.replace ('<div>',"")
		self.text = self.text.replace ('</div>',"")
		d= self.text.find ('<h1')
		self.text = self.text[d:]

	def ebGratuit (self):
		# l'auteur
		tag = htmlCls.getOneByTagClass (self.text, 'p', 'Auteur')
		d= self.text.find ('<p class=>') +16
		f= self.text.find ('</p>', d)
		self.author = self.text [d:f].lower()
		# le texte
		self.text = textFct.cleanHtml (self.text)
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

	def wiki (self):
		# le titre
		d= self.title.find (' wikisource')
		self.title = self.title[:d]
		# les auteurs
		tmpText = self.getOneById ('ws-data')
		tmpText = htmlCls.getInnerHtml (tmpText)
		authlist = tmpText.split ('/wiki/author:')
		d= authlist[1].find (' ') -1
		self.meta = { 'lien-auteur': authlist[1][:d] }
		d=1+ authlist[1].find ('>',d)
		f= authlist[1].find ('<',d)
		self.author = authlist[1][d:f]
		rangeList = range (2, len (authlist))
		for i in rangeList:
			d=1+ authlist[i].find ('>')
			f= authlist[i].find ('<',d)
			self.author = self.author +', '+ authlist[i][d:f]
		self.findSubject()
		# la date
		tmpText = self.getOneById ('header-year-text')
		if not self.link: self.link = self.meta['canonical']
		self.meta['date'] = htmlCls.getInnerHtml (tmpText)
		"""
		# le texte
		d=16+ self.text.find ('ikidata item</a>')
		d= self.text.find ('<h2', d)
		f= self.text.rfind ('<p>this work is in the')
		f= self.text[:f].rfind ('<img')
		f= self.text[:f].rfind ('<p')
		self.text = self.text[d:f]
		"""
		self.delAttributes()
		self.text = self.text.replace ('<span>', "")
		self.text = self.text.replace ('</span>', "")
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		if '&action=edit&section=' in self.text:
			textList = self.text.split ("&action=edit&section=")
			rangeList = range (1, len (textList))
			for i in rangeList:
				d=1+ textList[i].find (']')
				textList[i] = textList[i][d:]
				d= textList[i-1].find ('[')
				textList[i-1] = textList[i-1][:d]
			self.text = "".join (textList)

	def scoubidou (self):
		# pages de lartdesscoubidous.com
		self.setTitle()
		if ' |' in self.title:
			d= self.title.find (' |')
			self.title = self.title[:d]
		self.author = 'art des scoubidous'
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
		self.text = textFct.cleanHtml (self.text)
		self.replace ('<div>', "")
		self.replace ('</div>', "")
		d= self.text.find ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.text.find ('>', d) -1
		self.meta = { 'lien-auteur': self.text [d:f] }
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
		self.meta = { 'lien-auteur': 'https://gen.medium.com/@' + self.text [f:d] }
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
		self.text = textFct.cleanHtml (self.text)
		self.cleanLink()
		d= self.text.find ('<h1>')
		d= self.text.find ('<p>', d)
		f= self.text.find ('<div>reddit Inc')
		self.text = self.text[d:f]
		self.replace ('<div>', "")
		self.replace ('</div>', "")
		# auteur
		f= self.link.find ('/', 26)
		autlink = self.link[:f]
		self.author = autlink[25:]
		self.meta = { 'lien-auteur': autlink }
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
		autlink = 'https://www.fictionpress.com/u/' + self.text[d:f]
		self.link = 'https:' + self.metas ['canonical']
		d= autlink.rfind ('/') +1
		self.author = cleanTitle (autlink[d:])
		self.meta = { 'lien-auteur': autlink }
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
		autlink = 'https://www.fanfiction.net/u/' + self.text[d:f]
		self.link = 'https:' + self.metas ['canonical']
		d= autlink.rfind ('/') +1
		self.author = cleanTitle (autlink[d:])
		self.meta = { 'lien-auteur': autlink }
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