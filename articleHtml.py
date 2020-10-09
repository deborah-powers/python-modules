#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileHtml import FileHtml, findTextBetweenTag
from fileClass import Article
from listClass import ListPerso

help ="""lancer le script
	python articleHtml.py url"""

class ArticleHtml (FileHtml, Article):
	def __init__(self, file =None):
		FileHtml.__init__ (self)
		Article.__init__ (self)

	""" ________________________ manipuler des fichiers ________________________ """

	def fromFile (self):
		FileHtml.fromFile (self)
		if 'link' in self.metas.keys(): self.link = self.metas['link']
		if 'author' in self.metas.keys(): self.author = self.metas['author']
		if 'subject' in self.metas.keys(): self.subject = self.metas['subject']
		if 'autlink' in self.metas.keys(): self.autlink = self.metas['autlink']

	def toFile (self):
		self.author = self.author.lower()
		self.subject = self.subject.lower()
		self.metas['author'] = self.author
		self.metas['subject'] = self.subject
		self.metas['link'] = self.link
		self.metas['autlink'] = self.autlink
		FileHtml.toFile (self)

	def toFileText (self):
		self.clean()
		ftext = Article()
		ftext.copyFile (self)
		ftext.extension = 'txt'
		ftext.fileFromData()
		# les titres
		ftext.replace ('<h1>', '\n______\n______ ')
		ftext.replace ('<h2>', '\n______ ')
		ftext.replace ('<h3>', '\n------ ')
		ftext.replace ('<h4>', '\n--- ')
		ftext.replace ('</h4>', ' ---\n')
		ftext.replace ('</h3>', ' ------\n')
		ftext.replace ('</h2>', ' ______\n')
		ftext.replace ('</h1>', ' ______\n')
		# les conteneurs
		container =[ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
		for tag in container:
			ftext.replace ('</'+ tag +'>')
			ftext.replace ('<'+ tag +'>')
		# les tableaux
		ftext.replace ('th>', 'td>')
		ftext.replace ('</td><td>', '\t')
		ftext.replace ('</td></tr><tr><td>', '\n')
		ftext.replace ('<tr>', '\n')
		ftext.replace ('</tr>', '\n')
		# les listes
		ftext.replace ('</li><li>', '\n\t')
		ftext.replace ('<li>', '\n\t')
		ftext.replace ('</li>', '\n')
		# les lignes
		ftext.replace ('</p><p>', '\n')
		lines =[ 'p', 'caption', 'figcaption' ]
		for tag in lines:
			ftext.replace ('</'+ tag +'>', '\n')
			ftext.replace ('<'+ tag +'>', '\n')
		# les phrases
		inner =[ 'span', 'em', 'strong' ]
		for tag in inner:
			ftext.replace ('</'+ tag +'>', ' ')
			ftext.replace ('<'+ tag +'>', ' ')
		ftext.replace (' \n', '\n')
		ftext.replace ('\n ', '\n')
		# autres
		ftext.replace ('<hr>', '\n________________________\n')
		ftext.replace ('<br>', '\n')
		ftext.clean()
		ftext.toFile()

	""" ________________________ récupérer et nettoyer les fichiers ________________________ """

	def fromWeb (self, url, subject=None):
		self.extension = 'html'
		self.link = url
		self.fromUrl()
		self.clean()
		toText = True
		if 'http://www.gutenberg.org/' in url:				self.gutemberg (subject)
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebg (subject)
		elif 'https://archiveofourown.org/works/' in url:	self.aooo()
		elif 'https://www.deviantart.com/' in url:			self.deviantart()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'http://uel.unisciel.fr/' in url:				self.unisciel (subject)
		else:
			self.cleanWeb()
			toText = False
		self.metas ={}
		self.cleanPunctuation()
		self.replace (' <', '<')
		if toText: self.toFileText()
		else: self.toFile()

	def fromLocal (self, file, subject=None):
		self.file = file
		self.fromFile()
		self.clean()
		self.cleanWeb()
		if 'gtb'		in self.file: self.gutemberg (subject)
		elif 'egb'		in self.file: self.egb (subject)
		elif 'aooo'		in self.file: self.aoooFromSource (subject)
		elif 'ffnet'	in self.file: self.ffnet (subject)
		elif 'medium'	in self.file: self.medium (subject)
		elif 'adapt'	in self.file: self.adapt()
		self.metas ={}
		self.styles =[]
		self.toFileText()

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

	def delImgLink (self):
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('<div>', "")
		# supprimer les liens
		if self.contain ('<a href='):
			textList = ListPerso()
			textList.addList (self.text.split ('<a href='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList[i].find ('>') +1
				textList[i] = textList[i][d:]
			self.text = "".join (textList)
			self.text = self.text.replace ('</a>', "")
		# supprimer les images
		if self.contain ('<img src='):
			textList = ListPerso()
			textList.addList (self.text.split ('<img src='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList[i].find ('>') +1
				textList[i] = textList[i][d:]
			self.text = "".join (textList)

	def usePlaceholders (self):
		placeholders = ('y/n', 'e/c', 'h/c')
		for ph in placeholders:
			self.text.replace (ph.upper(), ph)
			self.text.replace ('('+ ph.upper() +')', ph)
			self.text.replace ('('+ ph +')', ph)
		self.text = self.text.replace ('y/n', 'Deborah')
		self.text = self.text.replace ('e/c', 'grey')
		self.text = self.text.replace ('h/c', 'dark blond')

	""" ________________________ récupérer les articles des sites ________________________ """

	def unisciel (self, subject):
		self.subject = 'cours'
		self.author = 'unisciel'
		self.text = findTextBetweenTag (self.text, 'body')
		self.cleanWeb()
		self.delScript()
		d= self.index ('<td>') +4
		f= self.index ('</td>', d)
		self.title = self.text[d:f].lower()
		d= self.index ('<p>')
		f= self.rindex ('</p>') +4
		self.text = self.text[d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		self.replace ('<img', '</p><img')
		self.replace ("png'>", "png'><p>")
		self.replace ('<p><p>', '<p>')
		self.replace ('</p></p>', '</p>')
		self.replace ('<p>', '</p><p>')
		self.replace ('</p>', '</p><p>')
		self.replace ('<p></p>')
		self.replace ('<p><p>', '<p>')
		self.replace ('<p><img', '<img')
		self.replace ("png'></p>", "png'>")
		self.text = self.text[4:-3]
		self.replace ('../res/', 'bv-'+ subject +'/')
		self.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01.png'><p>", ' <b>ADP +P --> ATP</b> ')
		self.replace ("</p><img src='bv-" + subject + "/apprendre_ch2_01_1.png'><p>", ' <b>ATP --> ADP +P</b> ')
		self.styles.append ('unisciel.css')

	def gutemberg (self, subject=None):
		# le titre
		d= self.index ('Title:') +7
		f= self.index ('Author:', d) -1
		self.title = self.text[d:f]
		# l'auteur
		d= f+9
		f= self.index ('Release', d) -1
		self.author = self.text[d:f]
		# le sujet est impossible à trouver
		self.indexSubject (subject)
		# le texte
		d= self.index ('<h1>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text[d:f]
		# cas spécifiques
		if (self.inText ('<p>CONTENTS</p>')):
			d= self.index ('<p>CONTENTS</p>')
			d= self.index ('<hr>', d)
			self.text = self.text[d:]
		if (self.inText ('<h2>Footnotes:</h2>')):
			f= self.index ('<h2>Footnotes:</h2>')
			self.text = self.text[:f]
		for tag in listTags: self.text = self.text.replace ('<'+tag+'></'+tag+'>', "")
		self.delImgLink()
		self.metas ={}
		self.toFile()

	def ebg (self, subject=None):
		self.delImgLink()
		# le titre
		d= self.index ('<p>', 10) +3
		f= self.index ('</p>', d)
		self.author = self.text[d:f]
		# l'auteur
		d= self.index ('<p>', f) +3
		f= self.index ('</p>', d)
		self.title = self.text[d:f]
		# le sujet
		self.indexSubject (subject)
		# le texte
		d=f
		f= self.text.rfind ('<h1>')
		if self.inText ('propos de cette édition électronique'):
			d2= self.index ('propos de cette édition électronique')
			if d2<f: d=d2
		elif self.count ('<h1>') >1:
			d2= self.index ('<h1>')
			if d2<f: d=d2
		d= self.index ('<p>', d)
		self.text = self.text[d:f]
		self.metas ={}
		self.toFile()

	def deviantart (self, subject=None):
		self.indexSubject (subject)
		self.text = self.text.replace ('<br/>', '</p><p>')
		self.delScript()
		self.cleanWeb()
		f= self.title.rfind (' ')
		self.title = self.title[:f]
		d= self.index ("By<a href='https://www.deviantart.com/") +11
		f= self.index ("'",d)
		self.autlink = self.text[d:f]
		d= self.index ('>',f) +1
		f= self.index ('<',d)
		self.author = self.text[d:f]
		d= self.index ('<p>',f)
		self.text = self.text[d:]
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		f= self.index ('>See More by')
		self.text = self.text[:f]
		f= self.rfind ('<a')
		self.text = self.text[:f]
		if self.text[-1] != '>': self.text = self.text +'</p>'

	def aoooFromSource (self, subject=None):
		data = self.title.split (' - ')
		if len (data) >3:
			print ('trop de blocks dans le titre', self.title)
			if 'hapter' in data[1]: self.author = data.pop(1)
		self.title = data[0]
		self.author = data[1]
		self.subject = data[2]
		d= self.index ("https://archiveofourown.org/works/")
		f= self.index ("'", d)
		self.link = self.text[d:f]
		if '"' in self.link:
			f= self.link.find ('"')
			self.link = self.link[:f]
		self.autlink = 'https://archiveofourown.org/users/' + self.author
		# trouver le texte
		self.delScript()
		self.replace ('<div>')
		self.replace ('</div>')
		d= self.index ('<h2>')
		d= self.index (self.author + '</a></h3>', d)
		c= self.text[:d].rfind ('href') +6
		f= self.index ('/pseuds/', c) +1
		self.metas ['autlink'] = self.text[c:f]
		d= self.index ('</h3>', d) +5
		f= self.text.rfind ('<h3>Actions</h3>')
		self.text = self.text[d:f]
		"""
		if self.contain ('<h3>Notes:</h3>'):
			f= self.text.rfind ('<h3>Notes:</h3>')
			self.text = self.text[:f]
		"""
		self.delImgLink()
		d= self.index ('<h3>Work Text:</h3>') +19
		self.text = self.text[d:]
		self.replace ('</blockquote><h3>Notes:</h3><blockquote>')
		self.replace ('</h3><h3>', '</h2><h3>')
		self.replace ('<h3>Chapter Text</h3>', '<hr>')
		self.replace ('<h3>Chapter', '<h2>Chapter')
		self.replace ('</h2><hr>', '</h2>')
		self.usePlaceholders()

	def aooo (self, subject=None):
		if 'This work could have adult content. If you proceed you have agreed that you are willing to see such content' in self.text:
			print ('fichier protégé', self.title)
			return
		self.cleanWeb()
		self.replace ('<br>', '</p><p>')
		self.text = findTextBetweenTag (self.text, 'body')
		d= self.index ('<h2>') +4
		f= self.index ('</h2>', d)
		self.title = self.text[d:f]
		self.title = self.title.strip()
		self.title = self.title.strip ('.')
		d= self.index ("<a href='/users/", f) +9
		f= self.index ("'", d)
		self.autlink = self.text[d:f]
		d= self.index ('>', d) +1
		f= self.index ('</a>', d)
		self.author = self.text[d:f]
		self.findSubject (subject)
		if self.subject == 'histoire':
			d= self.index ('Additional Tags:<ul>') +24
			d= self.index ('>', d) +1
			f= self.index ('<', d)
			self.subject = self.text[d:f]
		d= self.index ('<h3>Work Text:</h3>') +19
		f= self.rindex ('<h3>Actions</h3>')
		self.text = self.text[d:f]
		self.replace ('<div>')
		self.replace ('</div>')
		if self.contain ('<h3>Notes:</h3>'):
			halfText = self.length() /2
			d= self.index ('<h3>Notes:</h3>')
			if d> halfText: self.text = self.text[:d]
		self.usePlaceholders()

	def ffnet (self, subject=None):
		# trouver les meta
		data = self.title.split (', ')
		self.title = data[0]
		if 'hapter' in self.title:
			f= self.title.find ('hapter') -2
			self.title = self.title[:f]
		d= self.index ('https://www.fanfiction.net/u/')
		if d<0:
			d= self.index ('https://www.fictionpress.com/u/')
			self.link = 'https://www.fictionpress.com/s/'
		f= self.index ('>',d) -1
		self.autlink = self.text[d:f]
		d= self.index ('<',f)
		self.author = self.text[f+2:d]
		if subject: self.subject = subject
		else:
			self.subject = data[1][2:]
			if ' fanfic' in self.subject:
				f= self.subject.find (' fanfic')
				self.subject = self.subject[:f]
			d= self.index ('Rated: <a')
			d= self.index ('</a>',d) +8
			f= self.index ('Reviews: <a', d)
			data = self.text[d:f].split (' - ')
			self.subject = self.subject +', '+ data[1].replace ('/', ', ')
		if 'fictionpress' in self.link:
			d= self.index ('/s/') +3
			f= self.index ('/',d) +1
			self.link = self.link + self.text[d:f] +'1/'
			d= self.index ('/',f) +1
			f= self.index ("'",d)
			self.link = self.link + self.text[d:f]
		else: self.link = self.metas['canonical']
		self.metas ={}
		# trouver le texte
		d= self.index ('<p>')
		f= self.text.rfind ('</p>') +4
		self.text = self.text[d:f]
		self.toFile()

	def medium (self, subject):
		# récupérer les metadonnées
		self.link = self.title
		d= self.index ('"creator":') +12
		f= self.index ('"',d)
		self.author = self.text[d:f]
		d-=15
		f= self.text[:d].rfind ('@') +1
		self.autlink = 'https://gen.medium.com/@' + self.text[f:d]
		d= self.link.rfind ('/') +1
		f= self.link.rfind ('-')
		self.title = self.link[d:f].replace ('-', ' ')
		if subject: self.subject = subject
		# récupérer le texte
		d= self.index ('<p>')
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
		d= self.index ("par<a href='https://menace-theoriste.fr/author/") +12
		f= self.index ('>',d) -1
		self.autlink = self.text[d:f]
		d=f+2
		f= self.index ('</a>',d)
		self.author = self.text[d:f]
		d= self.index ('</h1>')
		d= self.index ('</header>', d) +9
		f= self.index ('<footer>', d)
		self.text = self.text[d:f]
		f= self.index ('#comments')
		f= self.text[:f].rfind ('<a')
		f= self.text[:f].rfind ('>') +1
		self.text = self.text[:f]

# on appele ce script dans un autre script
if __name__ != '__main__': pass
# mettre des majuscules dans un texte
elif len (argv) >=2:
	url = argv[1]
	subject =None
	if len (argv) >=3: subject = argv[2]
	page = ArticleHtml()
	if url[:4] == 'http': page.fromWeb (url, subject)
	else: page.fromLocal (url, subject)
# le nom du file n'a pas ete donne
else: print (help)