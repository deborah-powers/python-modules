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
		if self.path[-3:] != '.js':
			print ("ce fichier n'est pas en js")
			return None

	def comparer (self, newJs):
		self.toPath()
		newJs.toPath()
		if self.path[-3:] != '.js' and new.path[-3:] != '.js':
			print ("l'un des fichiers n'est pas en js:\n%s\n%s" % (self.path, newJs.path))
			return
		elif self.text == newJs.text:
			print ("les fichiers sont identiques:\n%s\n%s" % (self.path, newJs.path))
			return
		# fichier de comparaison
		title = 'b/comparer '+ self.title
		if self.title != newJs.title: title = title + ' et '+ newJs.title
		title = title + '.txt'
		compareFile = File (title)
		compareFile.text = 'fichier a: %s\nfichier b: %s' % (self.path, newJs.path)
		# comparer les classes
		names = self.classes.keys()
		namesNew = newJs.classes.keys()
		for name in names:
			if name not in namesNew: compareFile.text = compareFile.text + '\nnouvelle classe dans a: '+ name
			elif self.text [self.classes[name][0]:self.classes[name][1]] != newJs.text [newJs.classes[name][0]:newJs.classes[name][1]]:
				 compareFile.text = compareFile.text + '\nchangement au sein de la classe: '+ name
		for name in namesNew:
			if name not in names: compareFile.text = compareFile.text + '\nnouvelle classe dans b: '+ name
		# comparer les fonctions
		names = self.functions.keys()
		namesNew = newJs.functions.keys()
		for name in names:
			if name not in namesNew: compareFile.text = compareFile.text + '\nnouvelle fonction dans a: '+ name
			elif self.text [self.functions[name][0]:self.functions[name][1]] != newJs.text [newJs.functions[name][0]:newJs.functions[name][1]]:
				 compareFile.text = compareFile.text + '\nchangement au sein de la fonction: '+ name
		for name in namesNew:
			if name not in names: compareFile.text = compareFile.text + '\nnouvelle fonction dans b: '+ name
		# comparer les blocs
		for d,f in self.blocs:
			if self.text[d:f] in newJs.text:
				g= newJs.text.find (self.text[d:f])
				if f!=g: compareFile.text = compareFile.text + '\nbloc déplacé: %d, %d --> %d' % (d,f,g)
			else: compareFile.text = compareFile.text + '\nnouveaux blocs dans a: %d, %d' % (d,f)
		for d,f in newJs.blocs:
			if newJs.text[d:f] not in self.text: compareFile.text = compareFile.text + '\nnouveaux blocs dans b: %d, %d' % (d,f)
		compareFile.write()

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
		# les blocs
		if structuPos[0][0] >0: self.blocs.append ((0, structuPos[0][0]))
		rangeList = range (1, len (structuPos))
		for l in rangeList:
			if structuPos[l][0] - structuPos[l-1][1] >1: self.blocs.append ((structuPos[l-1][1], structuPos[l][0]))
		if structuPos[-1][1] < textLen: self.blocs.append ((structuPos[-1][1], textLen))

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
				if not self.functions[name][2]: strInfos = strInfos +" "+ name +','
				elif 'prototype' in self.functions[name][2]:
					strInfos = strInfos +" "+ name +" ("+ self.functions[name][2][:-10] +'),'
		if self.blocs:
			strInfos = strInfos + '\nblocs:'
			for blocA, blocB in self.blocs:
				if blocB - blocA <=130: strInfos = strInfos +"\nposition %d: %s" % (blocA, self.text[blocA:blocB].strip())
				else: strInfos = strInfos +"\nposition %d: %s --- %s" % (blocA, self.text[blocA:blocA +60].strip(), self.text[blocB -60:blocB].strip())
		return strInfos

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

