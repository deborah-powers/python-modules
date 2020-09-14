#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from htmlClean import ArticleHtml, help

class Fffic (ArticleHtml):
	def getText (self):
		start = self.text.find ('<p>')
		end = self.text.rfind ('</p>') +4
		self.text = self.text [start:end]

	def getMeta (self):
		# trouver l'auteur
		start = self.text.find ('By:<a target=')
		start = self.text.find ('>', start) +1
		end = self.text.find ('<', start)
		self.author = self.text [start:end]
		# trouver le genre
		start = self.text.find ('Fiction ') +16
		start = self.text.find (' - ', start) +3
		end = self.text.find (' - ', start +1)
		self.subject = self.text [start:end]

	def getChapter (self):
		start = self.text.find ("<SELECT id=chap_select")
		start = self.text.find ('<option value', start)
		start = self.text.find (' selected>', start) +10
		end = self.text.find ('<', start)
		chapter = self.text [start:end]
		if ':' in chapter:
			start = chapter.find (': ') +2
			chapter = chapter[start:]
		return chapter

	def multiPage (self, maxNb):
		# première page
		self.fromUrl()
		self.clean()
		self.getMeta()
		tmpUrl = self.url
		tmpText =""
		# itérer sur les autres
		rangeUrl = range (1, maxNb+1)
		for u in rangeUrl:
			self.url = tmpUrl.replace ('/1/', '/%d/' %u)
			self.fromUrl()
			self.clean()
			chapter = self.getChapter()
			self.getText()
			tmpText = tmpText + '\n<h1>%s</h1>\n%s' % (chapter, self.text)
		self.text = tmpText[1:]
		self.toFile()

	def monoPage (self):
		self.fromUrl()
		self.clean()
		self.getMeta()
		self.getText()
		self.toFile()






