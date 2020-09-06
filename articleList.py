#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from os import sep
from sys import argv
from fileList import FileList, fc
from htmlArticle import ArticleHtml
from fileClass import FileText

help ="""lancer le script
	python %s genre
""" % __file__

articlePath = fc.pathDesktop + 'articles' + sep

class ArticleList (FileList):
	def __init__ (self):
		FileList.__init__ (self, articlePath)

	def modify (self):
		""" utilise ArticleHtml.modify() """
		rangeArticle = self.range()
		for a in rangeArticle:
			self[a].modify()

	def openHtml (self):
		FileList.get (self, '.html')
		rangeArticle = self.range()
		for a in rangeArticle:
			titleTmp = self[a].title
			articleTmp = ArticleHtml()
			articleTmp.file = self[a].file
			self[a] = articleTmp
			self[a].getMetadata()
			self[a].fromFile()
		self.sort()

	def open (self):
		FileList.get (self, '.txt')
		rangeArticle = self.range()
		for a in rangeArticle:
			titleTmp = self[a].title
			articleTmp = FileText (self[a].file)
			self[a] = articleTmp
			self[a].fromFile()
		self.sort()

	def show (self, genre=None):
		if genre:
			print (len (self), 'histoires de', genre)
			for article in self: print ('%s\t%s' %( article.author, article.title))
		else:
			print (len (self), 'histoires')
			for article in self: print ('%s\t%s\t%s' %( article.subject, article.author, article.title))

	def getByGenre (self, genre=None):
		if not genre: return self
		else:
			aList = ArticleList()
			for article in self:
				if genre in article.subject: aList.append (article)
			return aList

# on appele ce script dans un autre script
if __name__ != '__main__': pass
aList = ArticleList()
aList.open()
if len (argv) >=2:
	genre = argv[1]
	if genre == 'modif': aList.modify()
	else:
		newList = aList.getByGenre (genre)
		newList.show (genre)
else: aList.show()

