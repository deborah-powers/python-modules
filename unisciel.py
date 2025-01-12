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
		self.urlCours = 'https://uel.unisciel.fr/biologie/module1/module1_ch0%d/co/apprendre_ch%s.html' % (number, '%s')
		self.imgUrl = 'https://uel.unisciel.fr/biologie/module1/module1_ch0%d/res/' % number
		self.pageCours = 'a/unisciel\\bv-%s-%s.html' % (trigram, '%s') # trigramme, chapître
	#	self.pageCours = 'a/unisciel\\bv-%s-%s-%s.html' % (trigram, '%s', '%02d') # trigramme, chapître, numéro de page
		self.pageCours = shortcut (self.pageCours)
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
		self.link = url
		self.fromUrl()
		self.meta ={}
		self.subject = 'cours, biologie'
		self.author = 'unisciel'
		self.setByTag ('section')
		self.delAttributes()
		self.cleanFigure()
		self.cleanText()
		self.cleanList()
		self.cleanTable()
	#	self.getImg (imgTrigram, imgFolder, imgUrl)

	def cleanText (self):
		self.text = self.text.replace ('<div>', "")
		self.text = self.text.replace ('</div>', "")
		self.text = self.text.replace ('><span>', '>')
		self.text = self.text.replace ('</span><', '<')
		self.text = self.text.replace ('/(co_{2}/)', 'CO<sub>2</sub>')
		self.text = self.text.replace ('/(co_{2}', 'CO<sub>2</sub>')
		self.text = self.text.replace ('/(o_{2}/)', 'O<sub>2</sub>')
		self.text = self.text.replace ('/(o_{2}', 'O<sub>2</sub>')
		self.text = self.text.replace ('h_{2}o', 'H<sub>2</sub>O')
		self.text = self.text.replace ('o_{2}/)', 'O<sub>2</sub>')

	def getImg (self, imgTrigram, imgFolder, imgUrl):
		if "<img src='../res/" in self.text:
			imgList = self.text.split ("<img src='../res/")
			imgRange = range (1, len (imgList))
			for i in imgRange:
				f= imgList[i].find ("'")
				res = imgFromWeb (imgFolder, imgUrl, imgList[i][:f])
			self.text = ("<img src='" + imgTrigram + "/").join (imgList)

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
		self.path = book.pageCours % fileTitle
		self.pagesNumbers = range (start, end +1)
		self.urlCours = str (book.number) + '_%02d'
		self.urlCours = book.urlCours % self.urlCours
		# récupérer les pages
		pageTmp = UniscielPage (self.link, book.trigram, book.imgFolder, book.imgUrl)
		self.text = '<h1>' + self.title + '</h1>' + pageTmp.text
		for n in self.pagesNumbers:
			pageTmp = UniscielPage (self.urlCours % n, book.trigram, book.imgFolder, book.imgUrl)
			self.text = self.text + pageTmp.text
		htmlCls.Html.write (self)

chap = UniscielChapter (UniscielBook.evolution, 1, 'cycle-biologique', 'les cycles biologiques', 1, 6)
chap = UniscielChapter (UniscielBook.nutrition, 2, 'glycolyse', 'la glycolyse', 5, 11)
"""
chap = UniscielChapter (UniscielBook.evolution, 1, 'cycle-biologique', 'les cycles biologiques', 1, 6)
chap = UniscielChapter (UniscielBook.evolution, 2, 'phycophytes', 'les phycophytes', 7, 15)
chap = UniscielChapter (UniscielBook.evolution, 3, 'mycophytes', 'les mycophytes', 16, 21)
chap = UniscielChapter (UniscielBook.evolution, 4, 'plantes-terrestres', 'les plantes terrestres', 22, 24)
chap = UniscielChapter (UniscielBook.evolution, 5, 'bryophytes', 'les bryophytes', 25, 29)
chap = UniscielChapter (UniscielBook.evolution, 6, 'pteridophytes', 'les ptéridophytes', 30, 33)
chap = UniscielChapter (UniscielBook.evolution, 7, 'prespermaphytes', 'les pré-spermaphytes', 34, 36)
chap = UniscielChapter (UniscielBook.evolution, 8, 'spermaphytes', 'les spermaphytes', 37, 45)
chap = UniscielChapter (UniscielBook.nutrition, 1, 'metabolisme', 'le métabolisme', 1, 4)
chap = UniscielChapter (UniscielBook.nutrition, 2, 'glycolyse', 'la glycolyse', 5, 11)
chap = UniscielChapter (UniscielBook.nutrition, 3, 'photochimie', 'la photochimie', 12, 16)
chap = UniscielChapter (UniscielBook.nutrition, 4, 'biochimie', 'la biochimie', 17, 20)
chap = UniscielChapter (UniscielBook.nutrition, 5, 'cellule', 'la cellule', 21, 22)
chap = UniscielChapter (UniscielBook.nutrition, 6, 'organisme', "l'organisme", 23, 25)
chap = UniscielChapter (UniscielBook.cellule, 1, 'generalites', 'generalités', 1, 3)
chap = UniscielChapter (UniscielBook.cellule, 2, 'plastes', 'les plastes', 4, 8)
chap = UniscielChapter (UniscielBook.cellule, 3, 'vaccuole', 'les vaccuoles', 9, 11)
chap = UniscielChapter (UniscielBook.cellule, 4, 'paroi', 'la paroi', 12, 18)
chap = UniscielChapter (UniscielBook.developpement, 1, 'processus', 'les processus', 1, 3)
chap = UniscielChapter (UniscielBook.developpement, 2, 'meristeme', 'les meristemes', 4, 7)
chap = UniscielChapter (UniscielBook.developpement, 3, 'embryogenese', "l'embryogenese", 8, 10)
chap = UniscielChapter (UniscielBook.developpement, 4, 'graine', 'la graine', 11, 15)
chap = UniscielChapter (UniscielBook.developpement, 5, 'avg1', 'la phytomérisation', 16, 17)
chap = UniscielChapter (UniscielBook.developpement, 6, 'avg2', 'la tige feuillée', 18, 19)
chap = UniscielChapter (UniscielBook.developpement, 7, 'avg3', 'la racine', 20, 22)
chap = UniscielChapter (UniscielBook.developpement, 8, 'reproduction', 'la reproduction', 23)
chap = UniscielChapter (UniscielBook.developpement, 9, 'mouvement', 'le mouvement', 24, 26)
"""
print (UniscielBook.nutrition)