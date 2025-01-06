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
refPage = 'a/unisciel\\bv-%s-%s-%s.html'	# livre, chapître et numéro de page

class Unisciel (htmlCls.Html, Article):
	def __init__ (self, book, urlRef, urlPart, localRef, localNb):
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, urlRef % urlPart)
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.path = localRef % localNb
		self.fromPath()
		self.setByTag ('section')
		self.delAttributes()
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('><span>', '>')
		self.text = self.text.replace ('</span><', '<')
		self.replace ('../res/', book +'/')
		article = self.toText()
		if article: article.write()
		else: self.write()

def readUniChapter (bookNum, book, chapter, fragmentsUrl):
	locUrl = refUrl % (bookNum, '%s')
	locPage = refPage % (book, chapter, '%02d')
	fragRange = range (len (fragmentsUrl))
	for pageNum in fragRange: article = Unisciel (book, locUrl, fragmentsUrl[pageNum], locPage, pageNum +1)


readUniChapter (1, 'evo', 'cycle-biologique', ( '01_1_1', '1_01', '1_02', '1_03', '1_04', '1_05', '1_06' ))
"""
readUniChapter (1, 'evo', 'phycophytes', ( '01_2_1', '1_07', '1_08', '1_09', '1_11', '1_12', '1_13', '1_14', '1_15' ))
readUniChapter (1, 'evo', 'mycophytes', ( '01_3_1', '1_16', '1_17', '1_18', '1_19', '1_20', '1_21' ))
readUniChapter (1, 'evo', 'bryophytes', ( '01_5_1', '1_25', '1_26', '1_27', '1_28', '1_29' ))
readUniChapter (1, 'evo', 'pteridophytes', ( '01_6_1', '1_30', '1_31', '1_32', '1_33', ))
readUniChapter (1, 'evo', 'spermaphytes', ( '01_7_1', '1_37', '1_38', '1_39', '1_40', '1_41', '1_42', '1_43', '1_44', '1_45' ))
readUniChapter (1, 'evo', 'prespermaphytes', ( '01_7_1', '1_34', '1_35', '1_36' ))
readUniChapter (1, 'evo', 'plantes-terrestres', ( '01_4_1', '1_22', '1_23', '1_24' ))
readUniChapter (2, 'nutri', '', ())
"""


