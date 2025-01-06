#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from urllib import request as urlRequest
from fileLocal import shortcut
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
refUrl = 'https://uel.unisciel.fr/biologie/module1/module1_ch%02d/'	# num-module
refUrlCours = refUrl + 'co/apprendre_ch%s.html'	# num-module et portion de page
refUrlImage = refUrl + 'res/%s'	# num-module et titre de l'image
# refPage = 'a/unisciel\\bv-%s-%s-%s.html'	# livre, chapître et numéro de page
refPageCours = 'b/unisciel\\bv-%s-%s-%s.html'
refPageImage = 'b/unisciel\\%s\\%s'	# livre et titre de l'image
refPageImage = shortcut (refPageImage)

def imgFromWeb (book, bookNum, imgTitle):
	imgFile = refPageImage % (book, imgTitle)
	imgUrl = refUrlImage % (bookNum, imgTitle)
	try: urlRequest.urlretrieve (imgUrl, imgFile)
	except Exception as e:
		print (e)
		return False
	else: return True

class Unisciel (htmlCls.Html, Article):
	def __init__ (self, book, bookNum, localUrl, urlPart, localPage, localNb):
		Article.__init__ (self)
		htmlCls.Html.__init__ (self, localUrl % urlPart)
		self.meta ={}
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.path = localPage % localNb
		self.fromPath()
		self.setByTag ('section')
		self.delAttributes()
		self.cleanFigure()
		self.cleanText()
		self.getImg (book, bookNum)
		self.write()

	def cleanText (self):
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('><span>', '>')
		self.text = self.text.replace ('</span><', '<')

	def getImg (self, book, bookNum):
		if "<img src='../res/" in self.text:
			imgList = self.text.split ("<img src='../res/")
			imgRange = range (1, len (imgList))
			for i in imgRange:
				f= imgList[i].find ("'")
				res = imgFromWeb (book, bookNum, imgList[i][:f])
			self.text = ("<img src='" + book + "/").join (imgList)

	def cleanFigure (self):
		if '</figure>' in self.text and '</figcaption>' not in self.text:
			self.text = self.text.replace ('<figure>', "")
			self.text = self.text.replace ('</figure>', "")
		elif '</figure>' in self.text:
			imgList = self.text.split ('</figure>')
			imgRange = range (len (imgList) -1)
			for i in imgRange:
				d=8+ imgList[i].find ('<figure>')
				if '</figcaption>' in imgList[i][d:]: imgList[i] = imgList[i] + '</figure>'
				else: imgList[i] = imgList[i][d:]
			self.text = "".join (imgList)

def readUniChapter (bookNum, book, chapter, fragmentsUrl):
	localUrl = refUrlCours % (bookNum, '%s')
	localPage = refPageCours % (book, chapter, '%02d')
	fragRange = range (len (fragmentsUrl))
	for pageNum in fragRange: article = Unisciel (book, bookNum, localUrl, fragmentsUrl[pageNum], localPage, pageNum +1)

readUniChapter (1, 'evo', 'cycle-biologique', ( '01_1_1', '1_01', '1_02' ))
"""
readUniChapter (1, 'evo', 'cycle-biologique', ( '01_1_1', '1_01', '1_02', '1_03', '1_04', '1_05', '1_06' ))
readUniChapter (1, 'evo', 'phycophytes', ( '01_2_1', '1_07', '1_08', '1_09', '1_11', '1_12', '1_13', '1_14', '1_15' ))
readUniChapter (1, 'evo', 'mycophytes', ( '01_3_1', '1_16', '1_17', '1_18', '1_19', '1_20', '1_21' ))
readUniChapter (1, 'evo', 'bryophytes', ( '01_5_1', '1_25', '1_26', '1_27', '1_28', '1_29' ))
readUniChapter (1, 'evo', 'pteridophytes', ( '01_6_1', '1_30', '1_31', '1_32', '1_33', ))
readUniChapter (1, 'evo', 'spermaphytes', ( '01_7_1', '1_37', '1_38', '1_39', '1_40', '1_41', '1_42', '1_43', '1_44', '1_45' ))
readUniChapter (1, 'evo', 'prespermaphytes', ( '01_7_1', '1_34', '1_35', '1_36' ))
readUniChapter (1, 'evo', 'plantes-terrestres', ( '01_4_1', '1_22', '1_23', '1_24' ))
readUniChapter (2, 'nutri', '', ())
"""


