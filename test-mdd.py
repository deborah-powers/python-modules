#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import htmlFct
from fileCls import File
import loggerFct as log

fileName = 'C:\\wamp64\\www\\html\\md-maison-test.mdd'

class Mdd (File):
	def __init__ (self):
		File.__init__ (self, fileName)

	def toHtml (self):
		article = File()
		article.text = htmlFct.toHtml (self.text)
		if '</' in article.text:
			article.path = self.path.replace ('.mdd', '.html')
			article.title = self.title
			return article
		else: return self

mdd = Mdd()
mdd.read()
mddHtml = mdd.toHtml()
mddHtml.write()