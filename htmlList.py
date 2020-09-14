#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileList
from fileClass import shortcut

class HtmlList (FileList):
	def __init__(self):
		FileList.__init__(self)
		self.path = shortcut ('a/fanfics/')

	def get (self):
		tmpList = FileList (self.path)
		tmpList.get ('.html')
		lRange = tmpList.range()
		for f in lRange:
			self.append (FileHtml())
			self[f].title = tmpList[f].title
			self[f].path = tmpList[f].path
			self[f].fileFromData()
			self[f].fromFile()
		self.sort()

	def __str__(self):
		string =""
		for article in self: string = string +'\n%s\t%s\t%s' %( article.subject, article.author, article.title )
		return string[1:]