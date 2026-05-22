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

	def __str__ (self):
		res = self.query +':'
		rules = self.rules.keys()
		for rule in rules: res = res +'\t' + rule +": "+ self.rules[rule]
		return res

	def __lt__ (self, otherRule):
		if self.query >= otherRule.query: return False
		ruleSelf = self.rules.keys()
		ruleOTher = otherRule.rules.keys()
		nbRules = len (ruleSelf)
		if nbRules >= len (ruleOTher): return False
		r=0
		isBefore = True
		while isBefore and r< nbRules:
			if ruleSelf[r] in ruleOTher and self.rules [ruleSelf[r]] >= ruleOTher.rules [ruleSelf[r]]: isBefore = False
			r+=1
		return isBefore

	def __gt__ (self, otherRule):
		if self.query <= otherRule.query: return False
		ruleSelf = self.rules.keys()
		ruleOTher = otherRule.rules.keys()
		nbRules = len (ruleSelf)
		if nbRules <= len (ruleOTher): return False
		r=0
		isAfter = True
		while isAfter and r< nbRules:
			if ruleSelf[r] in ruleOTher and self.rules [ruleSelf[r]] <= ruleOTher.rules [ruleSelf[r]]: isAfter = False
			r+=1
		return isAfter

	def __le__ (self, otherRule):
		return not self.__gt__ (otherRule)

	def __ge__ (self, otherRule):
		return not self.__lt__ (otherRule)

	def __eq__ (self, otherRule):
		if self.query != otherRule.query: return False
		ruleSelf = self.rules.keys()
		ruleOTher = otherRule.rules.keys()
		r=0
		nbRules = len (ruleSelf)
		isSameRule = True
		while isSameRule and r< nbRules:
			if ruleSelf[r] not in ruleOTher: isSameRule = False
			elif self.rules [ruleSelf[r]] != ruleOTher.rules [ruleSelf[r]]: isSameRule = False
			r+=1
		return isSameRule

	def __ne__ (self, otherRule):
		return not self.__eq__ (otherRule)

	def sameStructure (self, otherRule):
		if self.query != otherRule.query: return False
		ruleSelf = self.rules.keys()
		ruleOTher = otherRule.rules.keys()
		r=0
		nbRules = len (ruleSelf)
		isSameRule = True
		while isSameRule and r< nbRules:
			if ruleSelf[r] not in ruleOTher: isSameRule = False
			r+=1
		if not isSameRule: return False
		r=0
		nbRules = len (ruleOTher)
		while isSameRule and r< nbRules:
			if ruleOTher[r] not in ruleSelf: isSameRule = False
			r+=1
		return isSameRule

	def __contains__ (self, rule):
		# vérifier si un élément est dans self. rule = "nomRule" ou { nomRule: valeurRule }
		isIn = True
		ruleKeysSelf = self.rules.keys()
		if isinstance (rule, str):
			if rule not in ruleKeysSelf: isIn = False
			return isIn
		elif isinstance (rule, dict):
			ruleKeys = rule.rules.keys()
			r=0
			nbRules = len (ruleKeys)
			while isIn and r< nbRules:
				if ruleKeys[r] not in ruleKeysSelf: isIn = False
				r+=1
			return isIn
		else: return False

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

	def __str__ (self):
		res = self.query +':'
		for rule in self.rules:
			res = res +'\n\t'+ rule.__str__()
		return res

	def __contains__ (self, rule):
		if isinstance (rule, str):	# nom de règle, div, p.class-name
			isIn = False
			r=0
			nbRules = len (self.rules)
			while not isIn and r< nbRules:
				if self.rules[r].__contains__ (rule): isIn = True
				r+=1
			return isIn
		elif isinstance (rule, RuleCss):
			if not rule in self.rules: isIn = False
			return isIn
		else: return False

class FileCss (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.queries =[]	# QueryCss
		self.rules =[]		# RuleCss

	def getRulesForItem (self, item):
		rule = RuleCss()
		rule.query = item
		for ruleSelf in self.rules:
			if item not in ruleSelf.query or item +" " in ruleSelf.query: continue
			elif item +'.' in ruleSelf.query or item +'#' in ruleSelf.query or item +'[' in ruleSelf.query: continue
			elif item +':' in ruleSelf.query or item +'>' in ruleSelf.query or item +'=' in ruleSelf.query: continue
			elif ruleSelf.query == item or " "+ item +',' in ruleSelf.query or ruleSelf.query.find (item +',') ==0:
				# si la même règle est répétée plusieurs fois, la dernière occurence est gardée
				rulesNames = ruleSelf.rules.keys()
				for name in rulesNames: rule.rules[name] = ruleSelf.rules[name]
			elif ", "+ item in ruleSelf.query:
				# item est le dernier élément de la query
				pos = ruleSelf.query.rfind (", "+ item)
				if len (ruleSelf.query) -pos -2 == len (item):
					rulesNames = ruleSelf.rules.keys()
					for name in rulesNames: rule.rules[name] = ruleSelf.rules[name]
		return rule

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
		textList = self.text.split ('}')
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
rule = fileCss.getRulesForItem ('p')

print (isinstance (rule, RuleCss), isinstance ('hello', str), isinstance ({ 'a':2, 'b':4 }, dict))
