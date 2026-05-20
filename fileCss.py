#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
import loggerFct as log

class RuleCss():
	def __init__ (self):
		self.query =""	# div.class-name
		self.rules ={}		# color: red

	def fromText (self, text):
		# text = div{color:red;font-size:1em;
		d= text.find ('{')
		self.query = text[:d]
		text = text[d+1:-1]
		if text[-1] ==';': text = text[:-1]
		text = text.replace (';',':')
		textList = text.split (':')
		rangeList = range (0, len (textList) -1, 2)
		for c in rangeList: self.rules [textList[c]] = textList[c+1]

class QueryCss():
	def __init__ (self):
		self.query =""	# (max-width: 768px) ou print
		self.rules =[]	# RuleCss()

	def fromText (self, text):
		# text = myQuery{...}
		d= text.find ('{')
		self.query = text[:d]
		text = text[d+1:-1]
		# les règles
		textList = text.split ('}')
		rangeList = range (len (textList) -1)
		for c in rangeList:
			self.rules.append (RuleCss())
			self.rules[-1].fromText (textList[c])

class FileCss (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.queries =[]	# QueryCss
		self.rules =[]		# RuleCss

	def read (self):
		File.read (self)
		self.replace ('\n'," ")
		self.replace ('\t'," ")
		self.replace ('\r'," ")
		self.cleanForStandarding()
		self.deleteComments()
		self.listMediaQueries()
		self.listRules()

	def listMediaQueries (self):
		if '@media' not in self.text: return
		textList = self.text.split ('@media')
		rangeList = range (1, len (textList))
		for c in rangeList:
			d= textList[c].find ('}')
			nOpening = textList[c][:d].count ('{')
			nClosing =1
			while nOpening > nClosing:
				d= textList[c].find ('}',d+1)
				nOpening = textList[c][:d].count ('{')
				nClosing =1+ textList[c][:d].count ('}')
			d+=1
			self.queries.append (QueryCss())
			self.queries[-1].fromText (textList[c][:d])
			textList[c] = textList[c][d:]
		self.text = " ".join (textList)
		self.cleanForStandarding()

	def listRules (self):
		textList = text.split ('}')
		rangeList = range (len (textList) -1)
		for c in rangeList:
			self.rules.append (RuleCss())
			self.rules[-1].fromText (textList[c])
		self.text =""

	def deleteComments (self):
		if '/*' not in self.text: return
		textList = self.text.split ('/*')
		rangeList = range (1, len (textList))
		for c in rangeList:
			f=2+ textList[c].find ('*/')
			textList[c] = textList[c][f:]
		self.text = "".join (textList)
		self.cleanForStandarding()

	def cleanForStandarding (self):
		while "  " in self.text: self.replace ("  "," ")
		marquers ='{}:;'
		for mark in marquers:
			self.replace (" "+ mark, mark)
			self.replace (mark +" ", mark)

fileName = 's/library-css\\structure.css'
fileCss = FileCss (fileName)
fileCss.read()