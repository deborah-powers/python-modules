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
class FileJs (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.classes ={}
		self.functions ={}
		self.blocs =[]

	def read (self):
		File.read (self)
		self.clean()
		self.delComments()
		# masquer les croches dans une string
		croches =( '{~', '}^')
		guillemets =( '"', "'", '\\n', '\\t')
		keepEnd =( '\n', '\t', ';\n', ';\t')
		for g in guillemets:
			for b,a in croches:
				self.text = self.text.replace (g+b, g+a)
				self.text = self.text.replace (b+g, a+g)
				for e in keepEnd: self.text = self.text.replace (g+a+e, g+b+e)
		self.listClass()
		self.listFuncPrototype()
		self.listFuncClassic()
		self.listBlock()
		# afficher les croches dans une string
		for g in guillemets:
			for b,a in croches:
				self.text = self.text.replace (g+a, g+b)
				self.text = self.text.replace (a+g, b+g)

	def listClass (self):
		d=0
		while '\nclass ' in self.text[d:]:
			d=1+ self.text.find ('\nclass ',d)
			f= self.text.find (" ",d+9)
			name = self.text[d+9:f]
			f=1+ self.text.find ('}\n', d)
			while self.text[d:f].count ('{') > self.text[d:f].count ('}') and '}\n' in self.text[f+1:]:
				f=2+ self.text.find ('}\n', f+1)
			self.classes[name] =(d,f,"")
			d=f

	def listFuncClassic (self):
		d=0
		while '\nfunction ' in self.text[d:]:
			d=1+ self.text.find ('\nfunction ',d)
			f= self.text.find (" ",d+9)
			name = self.text[d+9:f]
			f=1+ self.text.find ('}\n', d)
			while self.text[d:f].count ('{') > self.text[d:f].count ('}') and '}\n' in self.text[f+1:]:
				f=2+ self.text.find ('}\n', f+1)
			self.functions[name] =(d,f,"")
			d=f

	def listFuncPrototype (self):
		d=0
		while '.prototype.' in self.text[d:]:
			e=10+ self.text.find ('.prototype.', d)
			d=1+ self.text[:e].rfind ('\n')
			parent = self.text[d:e]
			f= self.text.find (" ",e)
			name = self.text[e+1:f]
			f=1+ self.text.find ('}\n', d)
			while self.text[d:f].count ('{') > self.text[d:f].count ('}') and '}\n' in self.text[f+1:]:
				f=2+ self.text.find ('}\n', f+1)
			self.functions[name] =(d,f, parent)
			d=f

	def listBlock (self):
		textLen = len (self.text)
		# récupérer toutes les positions prises dans les structures
		structuPos = list (self.classes.values())
		structuPos.extend (list (self.functions.values()))
		structuPos.sort()
		for a,b,c in structuPos: log.log (a,b,c)
		print (structuPos[2], self.text[structuPos[2][0]:structuPos[2][1]])
		log.message ('---')
		print (structuPos[3], self.text[structuPos[2][1]:structuPos[3][0]])
		# les blocs
		if structuPos[0][0] >0 and structuPos[0][1] > structuPos[0][0]: self.blocs.append ((0, structuPos[0][0]))
		structuRange = range (len (structuPos) -1)
		for s in structuRange:
			if structuPos[s][1] +1 < structuPos[s+1][0]: self.blocs.append ((structuPos[s][1], structuPos[s+1][0]))
		if structuPos[-1][1] +1 < textLen: self.blocs.append ((structuPos[-1][1], textLen))

	def clean (self):
		self.text = self.text.replace ('\r'," ")
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		self.text = self.text.replace ('\t ','\t')
		while '\t\t' in self.text: self.text = self.text.replace ('\t\t','\t')
		while '\n\n' in self.text: self.text = self.text.replace ('\n\n','\n')
		self.text = self.text.replace ('\n\t','\n')
		self.text = self.text.replace ('\n ','\n')
		self.text = self.text.replace ('\n\t','\n')
		while '\n\n' in self.text: self.text = self.text.replace ('\n\n','\n')
		self.text = self.text.replace ("()"," ()")
		while "  " in self.text: self.text = self.text.replace ("  "," ")
		marquers ='{}:;"\''
		blankSpaces = '\n\t '
		for space in blankSpaces:
			for mark in marquers:
				self.text = self.text.replace (space + mark, mark)
				self.text = self.text.replace (mark + space, mark)
		self.text = '\n'+ self.text +'\n'

	def delComments (self):
		if '\n//' in self.text:
			textList = self.text.split ('\n//')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f= textList[c].find ('\n')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)
		if '\t//' in self.text:
			textList = self.text.split ('\t//')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f= textList[c].find ('\n')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)
		if '/*' in self.text:
			textList = self.text.split ('/*')
			rangeList = range (1, len (textList))
			for c in rangeList:
				f=2+ textList[c].find ('*/')
				textList[c] = textList[c][f:]
			self.text = "".join (textList)

	def findComplementaryBracket (self, pStart):
		textLen = len (self.text)
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
			print (pStart, pClose, nStart, nClose, self.text[pStart +1:pStart +91], '---', self.text[pClose -30:pClose +1])
		pClose +=1	# inclure la } dans les limites
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

