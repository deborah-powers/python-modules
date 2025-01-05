#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

from sys import argv
from os import remove
import listFct
import textFct
from fileCls import Article
import htmlCls
import loggerFct as log

"""
cour de biologie végétale chez unisciel
cours d'évolution
https://uel.unisciel.fr/biologie/module1/module1/co/module1_1.html
"""

refUrl = 'https://uel.unisciel.fr/biologie/module1/module1_ch%02d/co/apprendre_ch%s.html'	# num-module et portion de page
refPage = 'a/unisciel\\bv-%s-%s-%02d.html'	# livre, chapître et numéro de page

class Unisciel (htmlCls.Html, Article):
	def __init__ (self, urlRef, urlPart, localRef, localNb):
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, urlRef % urlPart)
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.path = localRef % localNb
		self.fromPath()
		self.setByTag ('section')
		self.delAttributes()
		self.replace ('<div>')
		self.replace ('</div>')
		self.replace ('><span>')
		self.replace ('</span><')
	#	self.replace ('../res/', 'evo/')
		self.delAttributes()
		article = self.toText()
		log.logMsg (article)
		if article: article.write()
		else: self.write()

class UniChapter():
	def __init__ (self, bookNum, book, chapter, fragmentsUrl):
		self.fragments = fragmentsUrl
		self.url = refUrl % (bookNum, '%s')
		self.path = refPage % (book, chapter, '%02d')
		fragRange = range (len (self.fragments))
		for pageNum in uniRange:
			article = Unisciel (self.url, self.fragments[pageNum], self.path, pageNum +1)

bookChap = UniChapter (1, 'evo', 'cycle-biologique', ( '01_1_1', '1_01', '1_02', '1_03', '1_04', '1_05', '1_06' ))
bookChap = UniChapter (1, 'evo', 'phycophytes', ( '01_2_1', '1_07', '1_08', '1_09', '1_11', '1_12', '1_13', '1_14', '1_15' ))
bookChap = UniChapter (1, 'evo', 'mycophytes', ( '01_3_1', '1_16', '1_17', '1_18', '1_19', '1_20', '1_21' ))
bookChap = UniChapter (1, 'evo', 'bryophytes', ( '01_5_1', '1_25', '1_26', '1_27', '1_28', '1_29' ))
bookChap = UniChapter (1, 'evo', 'pteridophytes', ( '01_6_1', '1_30', '1_31', '1_32', '1_33', ))
bookChap = UniChapter (1, 'evo', 'spermaphytes', ( '01_7_1', '1_37', '1_38', '1_39', '1_40', '1_41', '1_42', '1_43', '1_44', '1_45' ))
bookChap = UniChapter (1, 'evo', 'prespermaphytes', ( '01_7_1', '1_34', '1_35', '1_36' ))
bookChap = UniChapter (1, 'evo', 'plantes-terrestres', ( '01_4_1', '1_22', '1_23', '1_24' ))

bookChap = UniChapter (1, 'evo', '', ())


