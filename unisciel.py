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
class UniscielBook():
	def __init__ (self, number, trigram):
		self.number = number
		self.trigram = trigram
		self.urlCours = 'https://uel.unisciel.fr/biologie/module1/module1_ch0%2d/co/apprendre_ch%s.html' % (number, '%s')
		self.imgUrl = 'https://uel.unisciel.fr/biologie/module1/module1_ch0%2d/res/' % number
		self.pageCours = 'a/unisciel\\bv-%s-%s.html' % (trigram, '%s') # trigramme, chapître
	#	self.pageCours = 'a/unisciel\\bv-%s-%s-%s.html' % (trigram, '%s', '%02d') # trigramme, chapître, numéro de page
		self.imgFolder = 'a/unisciel\\%s\\' % trigram
		self.imgFolder = shortcut (self.imgFolder)

	def __str__ (self):
		return str (self.number) +" "+ self.trigram

UniscielBook.evolution = UniscielBook (1, 'evo')
UniscielBook.nutrition = UniscielBook (2, 'nut')
UniscielBook.cellule = UniscielBook (3, 'cel')
UniscielBook.developpement = UniscielBook (4, 'dev')

def imgFromWeb (imgFolder, imgUrl, imgTitle):
	try: urlRequest.urlretrieve (imgUrl + imgTitle, imgFolder + imgTitle)
	except Exception as e:
		print (e)
		return False
	else: return True

class UniscielPage (htmlCls.Html, Article):
	def __init__ (self, url, imgTrigram, imgFolder, imgUrl):
		htmlCls.Html.__init__ (self, url)
		Article.__init__ (self)
		self.meta ={}
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.setByTag ('section')
		self.delAttributes()
		self.cleanFigure()
		self.cleanText()
		self.getImg (imgTrigram, fileImage)

	def cleanText (self):
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('><span>', '>')
		self.text = self.text.replace ('</span><', '<')

	def getImg (imgTrigram, imgFolder, imgUrl):
		if "<img src='../res/" in self.text:
			imgList = self.text.split ("<img src='../res/")
			imgRange = range (1, len (imgList))
			for i in imgRange:
				f= imgList[i].find ("'")
				res = imgFromWeb (imgFolder, imgUrl, imgList[i][:f])
			self.text = ("<img src='" + imgTrigram + "/").join (imgList)

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

class UniscielChapter_va():
	def __init__ (self, book, number, fileTitle, title, start, end):
		self.book = book
		self.number = number
		self.title = title
		self.urlIntro = '0%d_%d_1' % (book.number, number)
		self.urlIntro = book.urlCours % self.pageIntro
		self.pagesNumbers = range (start, end +1)
		self.urlCours = str (book.number) + '_%02d'
		self.urlCours = book.urlCours % self.urlCours

class UniscielChapter (htmlCls.Html, Article):
	def __init__ (self, book, number, fileTitle, title, start, end):
		Article.__init__ (self)
		htmlCls.Html.__init__ (self)
		self.meta ={}
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.book = book
		self.number = number
		self.title = title
		self.link = '0%d_%d_1' % (book.number, number)
		self.link = book.urlCours % self.link
		self.path = book.pageCours % self.fileTitle
		self.pagesNumbers = range (start, end +1)
		self.urlCours = str (book.number) + '_%02d'
		self.urlCours = book.urlCours % self.urlCours
		# récupérer les pages
		pageTmp = UniscielPage (self.link, book.trigram, book.imgFolder, book.imgUrl)
		self.text = pageTmp.text
		for n in self.pagesNumbers:
			pageTmp = UniscielPage (self.urlCours % n, book.trigram, book.imgFolder, book.imgUrl)
			self.text = self.text + pageTmp.text

def readUniChapter (bookNum, book, chapter, fragmentsUrl):
	localUrl = refUrlCours % (bookNum, '%s')
	localPage = refPageCours % (book, chapter, '%02d')
	fragRange = range (len (fragmentsUrl))
	for pageNum in fragRange: article = Unisciel (book, bookNum, localUrl, fragmentsUrl[pageNum], localPage, pageNum +1)

chap = UniscielChapter (book.evolution, 1, 'cycle-biologique', 'les cycles biologiques', 1, 6)
chap = UniscielChapter (book.evolution, 2, 'phycophytes', 'les phycophytes', 7, 15)
chap = UniscielChapter (book.evolution, 3, 'mycophytes', 'les mycophytes', 16, 21)
chap = UniscielChapter (book.evolution, 4, 'plantes-terrestres', 'les plantes terrestres', 22, 24)
chap = UniscielChapter (book.evolution, 5, 'bryophytes', 'les bryophytes', 25, 29)
chap = UniscielChapter (book.evolution, 6, 'pteridophytes', 'les ptéridophytes', 30, 33)
chap = UniscielChapter (book.evolution, 7, 'prespermaphytes', 'les pré-spermaphytes', 34, 36)
chap = UniscielChapter (book.evolution, 8, 'spermaphytes', 'les spermaphytes', 37, 45)
chap = UniscielChapter (book.nutrition, 1, 'metabolisme', 'le métabolisme', 1, 4)
chap = UniscielChapter (book.nutrition, 2, 'glycolyse', 'la glycolyse', 5, 11)
chap = UniscielChapter (book.nutrition, 3, 'photochimie', 'la photochimie', 12, 16)
chap = UniscielChapter (book.nutrition, 4, 'biochimie', 'la biochimie', 17, 20)
chap = UniscielChapter (book.nutrition, 5, 'cellule', 'la cellule', 21, 22)
chap = UniscielChapter (book.nutrition, 6, 'organisme', "l'organisme", 23, 25)
chap = UniscielChapter (book.cellule, 1, 'generalites', 'generalités', 1, 3)
chap = UniscielChapter (book.cellule, 2, 'plastes', 'les plastes', 4, 8)
chap = UniscielChapter (book.cellule, 3, 'vaccuole', 'les vaccuoles', 9, 11)
chap = UniscielChapter (book.cellule, 4, 'paroi', 'la paroi', 12, 18)
chap = UniscielChapter (book.developpement, 1, 'processus', 'les processus', 1, 3)
chap = UniscielChapter (book.developpement, 2, 'meristeme', 'les meristemes', 4, 7)
chap = UniscielChapter (book.developpement, 3, 'embryogenese', "l'embryogenese", 8, 10)
chap = UniscielChapter (book.developpement, 4, 'graine', 'la graine', 11, 15)
chap = UniscielChapter (book.developpement, 5, 'avg1', 'la phytomérisation', 16, 17)
chap = UniscielChapter (book.developpement, 6, 'avg2', 'la tige feuillée', 18, 19)
chap = UniscielChapter (book.developpement, 7, 'avg3', 'la racine', 20, 22)
chap = UniscielChapter (book.developpement, 8, 'reproduction', 'la reproduction', 23)
chap = UniscielChapter (book.developpement, 9, 'mouvement', 'le mouvement', 24, 26)

print (UniscielBook.nutrition)