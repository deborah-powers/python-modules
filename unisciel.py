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
refPageCours = 'a/unisciel\\bv-%s-%s-%s.html'	# livre, chapître et numéro de page
# refPageCours = 'b/unisciel\\bv-%s-%s-%s.html'
refPageImage = 'a/unisciel\\%s\\%s'	# livre et titre de l'image
# refPageImage = 'b/unisciel\\%s\\%s'	# livre et titre de l'image
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

readUniChapter (1, 'evo', 'cycle-biologique', ( '01_1_1', '1_01', '1_02', '1_03', '1_04', '1_05', '1_06' ))
readUniChapter (1, 'evo', 'phycophytes', ( '01_2_1', '1_07', '1_08', '1_09', '1_11', '1_12', '1_13', '1_14', '1_15' ))
readUniChapter (1, 'evo', 'mycophytes', ( '01_3_1', '1_16', '1_17', '1_18', '1_19', '1_20', '1_21' ))
readUniChapter (1, 'evo', 'bryophytes', ( '01_5_1', '1_25', '1_26', '1_27', '1_28', '1_29' ))
readUniChapter (1, 'evo', 'pteridophytes', ( '01_6_1', '1_30', '1_31', '1_32', '1_33', ))
readUniChapter (1, 'evo', 'spermaphytes', ( '01_7_1', '1_37', '1_38', '1_39', '1_40', '1_41', '1_42', '1_43', '1_44', '1_45' ))
readUniChapter (1, 'evo', 'prespermaphytes', ( '01_7_1', '1_34', '1_35', '1_36' ))
readUniChapter (1, 'evo', 'plantes-terrestres', ( '01_4_1', '1_22', '1_23', '1_24' ))
readUniChapter (2, 'nut', 'métabolisme', ( '02_1_1', '2_01', '2_02', '2_03', '2_04' ))
readUniChapter (2, 'nut', 'glycolyse', ( '02_2_1', '2_05', '2_06', '2_07', '2_08', '2_09', '2_10', '2_11' ))
readUniChapter (2, 'nut', 'photochimie', ( '02_3_1', '2_12', '2_13', '2_14', '2_15', '2_16' ))
readUniChapter (2, 'nut', 'biochimie', ( '02_4_1', '2_17', '2_18', '2_19', '2_20' ))
readUniChapter (2, 'nut', 'cellule', ( '02_5_1', '2_20', '2_21', '2_22' ))
readUniChapter (2, 'nut', 'organisme', ( '02_6_1', '2_23', '2_24', '2_25' ))
readUniChapter (3, 'cel', 'generalites', ( '03_1_1', '3_01', '3_02', '3_03' ))
readUniChapter (3, 'cel', 'plastes', ( '03_2_1', '3_04', '3_05', '3_06', '3_07', '3_08' ))
readUniChapter (3, 'cel', 'vaccuoles', ( '03_3_1', '3_09', '3_10', '3_11' ))
readUniChapter (3, 'cel', 'paroi', ( '03_4_1', '3_12', '3_13', '3_14', '3_15', '3_16', '3_17', '3_18' ))
readUniChapter (4, 'dev', 'processus', ( '04_1_1', '4_01', '4_02', '4_03' ))
readUniChapter (4, 'dev', 'meristemes', ( '04_2_1', '4_04', '4_05', '4_06', '4_07' ))
readUniChapter (4, 'dev', 'embryogenese', ( '04_3_1', '4_08', '4_09', '4_10' ))
readUniChapter (4, 'dev', 'graine', ( '04_4_1', '4_11', '4_12', '4_13', '4_14', '4_15' ))
readUniChapter (4, 'dev', 'avg1', ( '04_5_1', '4_16', '4_17' ))
readUniChapter (4, 'dev', 'avg2', ( '04_6_1', '4_18', '4_19' ))
readUniChapter (4, 'dev', 'avg3', ( '04_7_1', '4_19', '4_20', '4_21', '4_22' ))
readUniChapter (4, 'dev', 'reproduction', ( '04_8_1', '4_23' ))
readUniChapter (4, 'dev', 'mouvement', ( '04_9_1', '4_24', '4_25', '4_26' ))
