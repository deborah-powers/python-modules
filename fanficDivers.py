#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

class VideGrenier():
	def __init__ (self):
		self.title =""
		self.city =""
		self.distance =""
		self.location =""


def ficWebVg (self, url, subject=None):
	self.extension = 'html'
	if url[:4] == 'http':
		self.link = url
		FileHtml.fromUrl (self)
		self.fileFromData()
	else:
		self.file = url
		self.dataFromFile()
		self.fromFile()
	self.clean()
	# self.cleanWeb()
	if 'http://www.gutenberg.org/' in url:				self.ficficGutemberg (subject)
	elif 'https://www.ebooksgratuits.com/html/' in url:	self.ficEbg (subject)
	elif 'https://archiveofourown.org/works/' in url:	self.ficAooo()
	elif 'https://www.ficDev.com/' in url:				self.ficDev()
	elif 'https://menace-theoriste.fr/' in url:			self.ficTheoriste()
	elif 'https://www.ficReddit.com/r/' in url:			self.ficficReddit()
	elif 'https://www.therealfemaledatingstrategy.com/' in url:	self.ficFds()
	elif 'https://www.ficBourse.com/' in url:			self.ficBourse()
	elif 'http://uel.ficUnisciel.fr/' in url:			self.ficficUnisciel (subject)
	elif 'https://vide-greniers.org/' in url:			self.ficVg()
	elif 'gtb'		in url: self.ficficGutemberg (subject)
	elif 'egb'		in url: self.ficEbg (subject)
	elif 'aooo'		in url: self.ficAoooLcl (subject)
	elif 'ficFfn'	in url: self.ficFfn (subject)
	elif 'medium'	in url: self.ficMedium (subject)
	elif 'logimmo'	in url: self.logicImmo()
	elif 'seloger'	in url: self.seLoger()
	elif 'adapt'	in url: self.adapt()
	elif 'jmdoudoux.fr'	in url: self.jmdoudoux()
	else: self.cleanWeb()
	self.metas = {}
	self.replace (' <', '<')
	self.replace ('><', '>\n<')
	if self.contain ('</a>') or self.contain ('<img'): self.toFile()
	else: self.toFileText()

def logicImmo (self):
	# https://www.logic-immo.com/vente-immobilier-paris-75,100_1/options/groupprptypesids=1/pricemin=40000/pricemax=200000/areamin=30
	self.subject = 'immobilier'
	self.author = 'logic immo'
	self.autlink = 'https://www.logic-immo.com/'
	self.styles =[]
	self.metas ={}
	self.delScript()
	self.delStyle()
	d= self.index ('<div id="header-offer-')
	f= self.rindex ('<i class="li-icon li-icon--telephone">')
	self.text = self.text[d:f]
	"""
	self.replace ("Vous souhaitez investir en Pinel ?</p>")
	self.cleanWeb()
	self.replace ('<div>')
	self.replace ('</div>')
	f= self.index ('</section>', d)
	annonceList = List()
	annonceList.fromText (" Voir l'annonce", self.text)
	annonceList.pop (-1)
	annonceRange = annonceList.range()
	self.text = annonceList.toText ('<p></p>')
	"""

def seLoger (self):
	# https://www.seloger.com/list.htm?projects=2,5&types=1&natures=1,2,4&places=[{%22subDivisions%22:[%2275%22]}]&price=NaN/200000&surface=30/NaN&enterprise=0&qsVersion=1.0&m=search_refine
	self.subject = 'immobilier'
	self.author = 'se loger'
	self.autlink = 'https://www.seloger.com/'
	self.title = 'se-loger'
	self.fileFromData()
	self.styles =[]
	self.metas ={}
	d= self.index ('<div data-test="sl.title')
	d= self.index ('<ul', d)
	f= self.rindex ('</div>')
	self.text = self.text[d:f]
	self.cleanWeb()
	self.text = self.text[4:]
	logeList = List()
	logeList.fromText ('Appartement<ul>', self.text)
	logeRang = logeList.range()
	self.text =""
	for l in logeRang:
		text = seLogerUnite (logeList[l])
		if text: self.text = self.text + text

def seLogerUnite (text):
	if 'viager' in text or 'bouquet' in text: return ""
	template = "<hr><p>ville: %s</p><p>prix: %s</p><p>surface: %s</p>"
	f= text.find (' m²')
	d= text[:f].rfind ('>') +1
	surface = text[d:f]
	f= text.find ('€<')
	d= text[:f].rfind ('>') +1
	prix = text[d:f]
	d= text.find ('<span>', d) +6
	f= text.find ('</span>', d)
	adresse = text[d:f] +' - '
	d= f+13
	f= text.find ('</span>', d)
	adresse = adresse + text[d:f]
	template = template %( adresse, prix, surface)
	return template

setattr (Fanfic, 'logicImmo', logicImmo)
setattr (Fanfic, 'seLoger', seLoger)
setattr (Fanfic, 'ficWebVg', ficWebVg)
