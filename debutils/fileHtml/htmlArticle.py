#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileHtml import FileHtml, findTextBetweenTag
from fileSimple import File, Article
from debutils.list import List
import debutils.logger as logger

class ArticleHtml (FileHtml, Article):
	def __init__ (self, file =None):
		FileHtml.__init__ (self)
		Article.__init__ (self)
		if file:
			self.file = file
			self.shortcut()
			self.dataFromFile()

	""" ________________________ manipuler des fichiers ________________________ """

	def fromFile (self):
		FileHtml.fromFile (self)
		if 'link' in self.metas.keys(): self.link = self.metas ['link']
		if 'author' in self.metas.keys(): self.author = self.metas ['author']
		if 'subject' in self.metas.keys(): self.subject = self.metas ['subject']
		if 'autlink' in self.metas.keys(): self.autlink = self.metas ['autlink']

	def toFile (self):
		self.author = self.author.lower()
		self.subject = self.subject.lower()
		self.title = self.title.lower()
		self.metas ['author'] = self.author
		self.metas ['subject'] = self.subject
		self.metas ['link'] = self.link
		self.metas ['autlink'] = self.autlink
		FileHtml.toFile (self)

	def toFileText (self):
		self.author = self.author.lower()
		self.subject = self.subject.lower()
		self.title = self.title.lower()
		self.clean()
		# récupérer les metadonnées
		self.text = """<table>
	<tr><td>Sujet:</td><td>%s</td></tr>
	<tr><td>Auteur:</td><td>%s</td></tr>
	<tr><td>Lien:</td><td>%s</td></tr>
	<tr><td>Laut:</td><td>%s</td></tr>
</table>
%s""" % (self.subject, self.author, self.link, self.autlink, self.text)
		FileHtml.toFileText (self)

	def fromFileText (self):
		ftext = Article (self.file)
		ftext.fromFile()
		ftext.toHtml()
		self.text = ftext.text
		self.author = ftext.author
		self.autlink = ftext.autlink
		self.link = ftext.link
		self.extension = 'html'
		self.fileFromData()
		self.toFile()

	""" ________________________ récupérer et nettoyer les fichiers ________________________ """

	def fromUrl (self, url, subject=None):
		self.extension = 'html'
		if url[:4] == 'http':
			self.link = url
			FileHtml.fromUrl (self)
		else:
			self.file = url
			self.fromFile()
		self.clean()
		toText = True
		self.cleanWeb()
		if self.contain ('</a>') or self.contain ('<img'): toText = False
		self.metas = {}
		self.replace (' <', '<')
		self.replace ('><', '>\n<')
		if toText: self.toFileText()
		else: self.toFile()

	def findSubject (self, subject=None):
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		if subject:
			subject = subject.replace ('/', ', ')
			subject = subject.replace (', ', ', ')
			subject = subject.replace ('-', ', ')
			subject = subject.replace (' ', ' ')
			subjectList = subject
		subjectDict = {
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
		if subjectList: self.subject = subjectList [2:]
		else: self.subject = 'histoire'

	def delImgLink (self):
		self.replace ('</div>',"")
		self.replace ('<div>',"")
		# supprimer les liens
		if self.contain ('<a href='):
			textList = List()
			textList.addList (self.text.split ('<a href='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = "".join (textList)
			self.replace ('</a>',"")
		# supprimer les images
		if self.contain ('<img src='):
			textList = List()
			textList.addList (self.text.split ('<img src='))
			textRange = textList.range (1)
			for i in textRange:
				d= textList [i].find ('>') +1
				textList [i] = textList [i] [d:]
			self.text = "".join (textList)

	def usePlaceholders (self):
		placeholders = ('y/n', 'e/c', 'h/c', 'l/n')
		for ph in placeholders:
			self.replace (ph.upper(), ph)
			self.replace ('('+ ph +')', ph)
			self.replace ('['+ ph +']', ph)
		self.replace ('y/n', 'Deborah')
		self.replace ('e/c', 'grey')
		self.replace ('h/c', 'dark blond')
		self.replace ('l/n', 'Powers')
