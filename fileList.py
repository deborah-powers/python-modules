#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import textFct
import listFct
from fileCls import File
import loggerFct as log

class FileList (File):
	def __init__(self, file=None, sep='\n'):
		File.__init__(self, file)
		self.list =[]
		self.sep = sep
		self.length =0

	def write (self, upper=False):
		self.toText()
		if upper: self.text = textFct.shape (self.text, 'reset upper')
		else: self.text = textFct.shape (self.text, 'reset')
		File.write (self)

	def write_va (self, upper=False):
		self.text = self.sep.join (self.list)
		if upper: self.text = textFct.shape (self.text, 'reset upper')
		else: self.text = textFct.shape (self.text, 'reset')
		File.write (self)

	def read (self):
		File.read (self)
		self.text = textFct.cleanBasic (self.text)
		self.fromText()

	def toText (self):
		# self.text = listFct.toText (self.list, self.sep)
		self.text = self.sep.join (self.list)

	def fromText (self, text=None):
		if text: self.text = text
		lsep = len (self.sep)
		# éliminer les commentaires
		if '/*' in self.text:
			self.list = self.text.split ('/*')
			rangeList = self.range (1)
			for l in rangeList:
				d=2+ self.list[l].find ('*/')
				self.list[l] = self.list[l][d:]
			self.text = "".join (self.list)
		if '// ' in self.text:
			self.list = self.text.split ('// ')
			rangeList = self.range (1)
			for l in rangeList:
				d= lsep + self.list[l].find (self.sep)
				self.list[l] = self.list[l][d:]
			self.text = "".join (self.list)
			self.list =[]
		# préparer le texte
		while self.sep + self.sep in self.text: self.text = self.text.replace (self.sep + self.sep, self.sep)
		if self.text[:lsep] == self.sep: self.text = self.text[lsep:]
		if self.text[-lsep:] == self.sep: self.text = self.text[:-lsep]
		# créer la liste
		self.list = self.text.split (self.sep)
		self.length = len (self.list)

	def fromFile (self, fileSimple):
		self.title = fileSimple.title
		self.path = fileSimple.path
		self.text = fileSimple.text

	def range (self, start=0, end=0, step=1):
		return listFct.rangeList (self.list, start, end, step)

	def len (self):
		return self.__len__()

	def iterate (self, function):
		return listFct.iterate (self.list, function)

	def deleteDoublons (self):
		self.list = listFct.deleteDoublons (self.list)

	def __str__(self):
		text = 'liste '
		if self.length ==0: text = text + 'vide dans '+ self.path
		text = text = text + 'de %d éléments dans %s\n' % (self.length, self.path)
		text = text + self.sep.join (self.list[:5])
		return text

	def __len__(self):
		self.length = len (self.list)
		return self.length

	def __setitem__ (self, pos, item):
		if type (pos) == int:
			if pos <0: pos += self.length
			if pos < self.length: self.list[pos] = item
			else: self.append (item)

		elif type (pos) == slice:
			posIndex = pos.indices (self.length)
			rangeList = range (posIndex [0], posIndex [1], posIndex [2])
			if type (item) in (tuple, list) and len (item) >= len (rangeList):
				i=0
				for l in rangeList:
					self.list[l] = item[i]
					i+=1

	def __getitem__ (self, pos):
		if type (pos) == int:
			while pos <0: pos += self.length
			while pos >= self.length: pos -= self.length
			return self.list [pos]

		elif type (pos) == slice:
			posIndex = pos.indices (self.length)
			rangeList = self.range (posIndex [0], posIndex [1], posIndex [2])
			newList =[]
			for l in rangeList: newList.append (self.list[l])
			return newList
		else: return None

	def sort (self):
		self.list.sort()

	def reverse (self):
		self.list.reverse()

	def append (self, item):
		self.list.append (item)
		self.length +=1

	def extend (self, liste):
		for item in liste: self.append (item)

	def insert (self, pos, item):
		while pos <0: pos += self.length
		self.list.insert (pos, item)
		self.length +=1

	def pop (self, pos):
		length = len (self.list)
		if pos <0: pos += self.length
		elif pos >= self.length: pos -= self.length
		trash = self.list.pop (pos)
		self.length -=1

	def replace (self, wordOld, wordNew):
		rfile = self.range()
		for l in self.range:
			if wordOld in self[l]: self[l] = self[l].replace (wordOld, wordNew)

class FileTable (FileList):
	def __init__(self, file=None, sep='\n', sepCol='\t'):
		FileList.__init__(self, file, sep)
		self.sepCol = sepCol
		self.lenCol =0

	def getByCol (self, pos, value):
		newTab = FileTable()
		newTab.path = self.path
		newTab.title = self.title +' bis'
		newTab.toPath()
		for line in self.list:
			if line[pos] == value: newTab.append (line)
		return newTab

	def getCol (self, ncol):
		rangeList = self.range()
		newList =[]
		for i in rangeList: newList.append (self.list[i][ncol])
		return newList

	def popCol (self, ncol):
		rangeList = self.range()
		for i in rangeList: trash = self.list[i].pop (ncol)
		self.lenCol -=1

	def addCol (self, item):
		typeItem = type (item)
		typeList = type (self.list[0][0])
		action = 'inconnu'
		# item est une liste de la même taille que la liste principale, une colonne. je rajoute un élément par ligne
		if typeItem in (list, tuple) and len (item) == self.length and typeList == type (item[0]): action = 'unique'
		# item est un objet simple, à rajouter partout
		elif typeItem == typeList: action = 'commun'
		if action in 'unique commun': self.lenCol +=1
		return action

	def appendCol (self, item):
		action = self.addCol (item)
		if action == 'unique':
			for l in rangeList: self.list[l].append (item[l])
		elif action == 'commun':
			for l in rangeList: self.list[l].append (item)

	def insertCol (self, pos, item):
		action = self.addCol (item)
		if action == 'unique':
			for l in rangeList: self.list[l].insert (pos, item[l])
		elif action == 'commun':
			for l in rangeList: self.list[l].insert (pos, item)

	def toText (self):
		newList =[]
		for line in self.list: newList.append (self.sepCol.join (line))
		self.text = self.sep.join (newList)

	def fromText (self, text=None):
		if text: self.text = text
		while self.sepCol + self.sepCol in self.text: self.text = self.text.replace (self.sepCol + self.sepCol, self.sepCol)
		self.text = self.text.replace (self.sepCol + self.sep, self.sep)
		FileList.fromText (self)
		rangeList = range (self.length)
		for l in rangeList: self.list[l] = self.list[l].split (self.sepCol)
		self.lenCol = len (self.list[0])

	def __str__(self):
		text = 'table '
		if self.length ==0: text = text + 'vide dans '+ self.path
		else:
			text = text + 'de %d éléments à %d cases dans %s\n' % (self.length, len (self.list[0]), self.path)
			for line in self.list[:5]: text = text + self.sepCol.join (line) + self.sep
		return text

