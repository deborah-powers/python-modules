#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
import loggerFct as log

"""
dans un fichier js, il y a
fonction simple, function truc()
fonction d'objet, Truc.prototype.machin = function()
variable globale
classe, class Truc
isoler
les fonctions des deux types
les classes
les blocs libres
"""

def maskBracketInString (text, quote):
	croches =( '{~', '}^')
	if text.count (quote) %2 ==0:
		textList = text.split (quote)
		rangeList = range (1, len (textList), 2)
		for l in rangeList:
			for b,a in croches: textList[l] = textList[l].replace (b, a)
		text = quote.join (textList)
	else: print ('nombre inpaire de', quote)
	return text

class FileJs (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.classes ={}
		self.functions ={}
		self.blocs =[]

	def read (self):
		self.readPrep()
		self.createBlock()

	def readPrep (self):
		File.read (self)
		self.text = self.text.replace ('\r'," ")
		self.text = self.text.replace ('\n','\t')
		# supprimer les commentaires
		if '\t//' in self.text:
			textList = self.text.split ('\t//')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f= textList[c].find ('\t')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)
		self.text = self.text.replace ('\t'," ")
		self.cleanForStandarding()
		if '/*' in self.text:
			textList = self.text.split ('/*')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f=2+ textList[c].find ('*/')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)
		self.cleanForStandarding()

	def cleanForStandarding (self):
		self.text = self.text.replace ("()"," ()")
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		marquers ='{}:;"\''
		for mark in marquers:
			self.text = self.text.replace (" "+ mark, mark)
			self.text = self.text.replace (mark +" ", mark)

	def createBlock (self):
		self.text =" "+ self.text +" "
		textLen = len (self.text)
		# isoler les classes
		d=0
		f=-1
		while d< textLen and "class " in self.text[d:] and '{' in self.text[d:] and '}' in self.text[d:]:
			d= self.text.find ("class ",d)
			f= min (self.text.find (" ",d+7), self.text.find ('{',d))
			name = self.text[d+6:f]
			f= self.text.find ('{',f)
			f= self.findComplementaryBracket (f)
			self.classes[name] =(d,f)
			d=f+1
		# isoler les fonctions d'objet
		d=0
		f=-1
		while d< textLen and " = function " in self.text[d:] and '{' in self.text[d:] and '}' in self.text[d:]:
			f= self.text.find (" = function ",d)
			d=1+ max (self.text[:f].rfind (" "), self.text[:f].rfind (';'), self.text[:f].rfind ('}'))
			name = self.text[d:f]
			f= name.rfind ('.')
			parent = name[:f]
			name = name[f+1:]
			f= self.text.find ('{',d)
			f= self.findComplementaryBracket (f)
			self.functions[name] =(d,f, parent)
			d=f+1
		# isoler les fonctions simples
		self.text = self.text.replace (' = function ', ' = function$')
		d=0
		f=-1
		while d< textLen and "function " in self.text[d:] and '{' in self.text[d:] and '}' in self.text[d:]:
			d= self.text.find ("function ",d)
			f= self.text.find (" ",d+10)
			name = self.text[d+9:f]
			f= self.text.find ('{',f)
			f= self.findComplementaryBracket (f)
			self.functions[name] =(d,f, self.inClass (d))
			d=f+1
		self.text = self.text.replace (' = function$', ' = function ')
		# isoler les blocs libres
		# récupérer toutes les positions prises dans les structures
		structuPos = list (self.classes.values())
		structuPos.extend (list (self.functions.values()))
		structuPos.sort()
		"""
		print (self.text[structuPos[2][0]:structuPos[2][1]])
		print (self.text[structuPos[2][1]:structuPos[3][0]])
		"""
		# les blocs
		if structuPos[0][0] >0 and structuPos[0][1] > structuPos[0][0]: self.blocs.append ((0, structuPos[0][0]))
		structuRange = range (len (structuPos) -1)
		for s in structuRange:
			if structuPos[s][1] +1 < structuPos[s+1][0]: self.blocs.append ((structuPos[s][1], structuPos[s+1][0]))
		if structuPos[-1][1] +1 < textLen: self.blocs.append ((structuPos[-1][1], textLen))

	def findComplementaryBracket (self, pStart):
		textLen = len (self.text)
		# masquer les croches dans une string
		croches =( '{~', '}^')
		guillemets =( '"', "'", '\\n', '\\t' )
		for g in guillemets:
			for b,a in croches:
				self.text = self.text.replace (g+b, g+a)
				self.text = self.text.replace (b+g, a+g)
		# rechercher
		pClose = self.text.find ('}', pStart)
		nStart = self.text[pStart +1:pClose].count ('{')
		nClose = self.text[pStart +1:pClose].count ('}')
		while nStart > nClose and pClose >0 and '}' in self.text[pClose +1:]:
	#	while nStart > nClose and pClose >=0 and pClose < textLen :
			pClose = self.text.find ('}', pClose +1)
			nStart = self.text[pStart +1:pClose].count ('{')
			nClose = self.text[pStart +1:pClose].count ('}')
		if nClose < nStart:
			print (pStart, pClose, nStart, nClose, self.text[pStart +1:pStart +61], '---', self.text[pClose -60:pClose +1])
		pClose +=1	# inclure la } dans les limites
		# afficher les croches dans une string
		for g in guillemets:
			for b,a in croches:
				self.text = self.text.replace (g+a, g+b)
				self.text = self.text.replace (a+g, b+g)
		return pClose

	def inClass (self, pos):
		names = self.classes.keys()
		isin =""
		for name in names:
			if pos >= self.classes[name][0] and pos <= self.classes[name][1]: isin = name
		return isin

	def inFunc (self, pos):
		names = self.functions.keys()
		isin =""
		for name in names:
			if pos >= self.functions[name][0] and pos <= self.functions[name][1]: isin = name
		return isin

	def __str__ (self):
		self.toPath()
		strInfos = self.path
		if self.classes:
			strInfos = strInfos + '\nclasses:'
			names = self.classes.keys()
			for name in names: strInfos = strInfos +" "+ name
		if self.functions:
			strInfos = strInfos + '\nfunctions:'
			names = self.functions.keys()
			for name in names:
				if not self.functions[name][2]: strInfos = strInfos + "\n%d %d %s" % (self.functions[name][0], self.functions[name][1], name)
				elif 'prototype' in self.functions[name][2]:
					strInfos = strInfos + "\n%d %d %s (%s)" % (self.functions[name][0], self.functions[name][1], name, self.functions[name][2][:-10])
		elif self.functions and 1==2:
			strInfos = strInfos + '\nfunctions:'
			names = self.functions.keys()
			for name in names:
				if not self.functions[name][2]: strInfos = strInfos +" "+ name +','
				elif 'prototype' in self.functions[name][2]:
					strInfos = strInfos +" "+ name +" ("+ self.functions[name][2][:-10] +'),'
		if self.blocs:
			strInfos = strInfos + '\nblocs:'
			for blocA, blocB in self.blocs:
				strInfos = strInfos +"\n%d %d %s --- %s" % (blocA, blocB, self.text[blocA:blocA +80], self.text[blocB -80:blocB])
		return strInfos

