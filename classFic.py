#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from classFile import Article
from classHtml import Html

class FicHtml (Html):
	def fromWeb (self, url, subject=None):
		if url[:4] == 'http':
			self.link = url
			html = Html()
			html.link = url
			html.fromWeb()
			self.toPath()
		else:
			if url[-5:] != '.html': url = 'b/' + url + '.html'
			self.file = url
			self.fromPath()
			self.read()
		self.clean()
		if subject: self.subject = subject
		if 'http://www.gutenberg.org/' in url:				self.gutemberg()
		elif 'https://www.ebooksgratuits.com/html/' in url:	self.ebGratuit()
		elif 'https://archiveofourown.org/works/' in url:	self.aoooWeb()
		elif 'https://menace-theoriste.fr/' in url:			self.menaceTheoriste()
		elif 'https://www.reddit.com/r/' in url:			self.reddit()
		elif 'https://www.therealfemaledatingstrategy.com/' in url:	self.fDatingS()
		elif 'https://www.abcBourse.com/' in url:			self.bourse()
		elif 'http://uel.unisciel.fr/' in url:				self.unisciel()
		elif 'gtb'		in url: self.gutemberg()
		elif 'egb'		in url: self.ebGratuit()
		elif 'b/aooo.html' == url: self.aoooLocal()
		elif 'ffNet'	in url: self.ffNet()
		elif 'medium'	in url: self.medium()
		elif 'adapt'	in url: self.adapt()
		elif 'jmdoudoux.fr'	in url: self.jmdoudoux()
		else: self.cleanWeb()
		self.metas = {}
		self.text = self.text.replace (' <', '<')
		self.text = self.text.replace ('><', '>\n<')
		article = self.toArticle()
		article = article.toText()
		article.write()

	def findSubject (self):
		if self.subject:
			self.subject = self.subject.replace ('/', ', ')
			self.subject = self.subject.replace (', ', ', ')
			self.subject = self.subject.replace ('-', ', ')
		storyData = self.title.lower() +'\t'+ self.subject.lower() +'\t'+ self.author.lower()
		subjectList =""
		subjectDict = {
			'romance': ('romance', ' sex', 'x reader', 'rasmus', 'ville valo', 'jyrki', 'him (band)'),
			'rockers': ('rasmus', 'ville valo', 'jyrki', 'him (band)'),
			'monstres': ('mythology', 'vampire', 'naga', 'pokemon'),
			'sf': ('mythology', 'vampire', 'scify', 'lovecraft', 'stoker', 'conan doyle', 'naga'),
			'tricot': ('tricot', 'point', 'crochet')
		}
		subjectKeys = subjectDict.keys()
		for subject in subjectKeys:
			for word in subjectDict [subject]:
				if word in storyData:
					subjectList = subjectList +', '+ subject
					break
		if subjectList: self.subject = subjectList[2:]
		else: self.subject = 'histoire'







class Fanfic (Article):
	pass

