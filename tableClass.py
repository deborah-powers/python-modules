=	#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileClass import FilePerso
help ="""
ce script peut etre appele dans d'autres scripts
"""
def dictGetKeyByValue (dictionnary, value):
	return list(dictionnary.keys())[list(dictionnary.values()).index(value)]
def rangeNb (nb, start=0, step=1):
	rangeListTmp = range (start, nb, step)
	rangeList = ListPerso()
	for r in rangeListTmp: rangeList.append (r)
	return rangeList
class ListPerso (list):
	def iterate (self, function):
		rangeList = self.range()
		newList =ListPerso()
		for i in rangeList: newList.append (function (self[i]))
		return newList
	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = len (self)
		if end > lenList: end =0
		else: lenList -= end
		return rangeNb (lenList, start, step)
	def delDuplicates (self):
		""" transformer la liste [ a b b a c d e a f g ] en [ a b c d e f g ] """
		rangeList = self.range()
		rangeList.reverse()
		for i in rangeList:
			nb= self.count (self[i])
			if nb>1: self.pop(i)
	def fromList (self, otherLst):
		for item in otherLst: self.append (item)
	def fromText (self, text, word):
		tmpList = text.split (word)
		self.fromList (tmpList)
	def __str__(self):
		newList =[]
		for item in self: newList.append (str (item))
		return 'n'.join (newList)
class ListText (FilePerso):
	def __init__ (self, file=None, separator='n'):
		FilePerso.__init__ (self, file)
		self.list = ListPerso()
		self.separator = separator
	def append (self, item):
		self.list.append (item)
	def extend (self, tmpList):
		self.list.extend (tmpList)
	def reverse (self):
		self.list.reverse()
	def pop (self, pos):
		trash = self.list.pop (pos)
	def __getitem__ (self, pos):
		return self.list[pos]
	def __setitem__ (self, pos, value):
		self.list[pos] = value
	def range (self, start=0, end=0, step=1):
		return self.list.range (start, end, step)
	def length (self):
		return len (self.list)
	def fromStr (self, text=None):
		if text: self.text = text
		while self.separator + self.separator in self.text: self.replace (self.separator + self.separator, self.separator)
		self.extend (self.text.split (self.separator))
	def fromFile (self):
		FilePerso.fromFile (self)
		ListText.fromStr (self)
	def toFile (self, mode='w'):
		self.text = self.toStr()
		FilePerso.toFile (self, mode)
	def toStr (self):
		string =""
		for item in self.list: string = string + str (item) + self.separator
		return string
	def fromFilePerso (self, ftext):
		self.copyFile (ftext)
		self.fromStr()
	def sortFile (self, fileName):
		""" trier un fichier contenant une liste """
		self.fromFile (fileName)
		self.list.sort()
		self.toFile ('w')
	def compare (self, newList):
		listF = ListText ('b/compare %s - %s.txt' % (self.title, newList.title))
		nbAdd =0; nbDel =0; nbCom =0
		while self.list:
			if self.list[0] in newList.list:
				pos = newList.list.index (self.list[0])
				if pos >0:
					rpos = range (pos)
					for p in rpos:
						listF.append ('<t'+ newList.list.pop(0))
						nbDel +=1
				listF.append (self.list.pop(0))
				nbCom +=1
				trash = newList.list.pop(0)
			else:
				listF.append ('>t'+ self.list.pop(0))
				nbAdd +=1
		while newList.list:
			listF.append ('<t'+ newList.list.pop(0))
			nbDel +=1
		if nbAdd ==0 and nbDel ==0: print ('les fichiers %s et %s sont identiques' % (self.title, newList.title))
		elif nbCom ==0: print ("les fichiers %s et %s n'ont rien de commun" % (self.title, newList.title))
		else:
			listF.title = self.title +' - '+ newList.title
			print ('il y a %d additions et %d délétions entre les fichiers "%s" et "%s", cf "%s"' % (nbAdd, nbDel, self.title, newList.title, listF.title))
			listF.toFile()
""" ____________________________________ fonctions pour les tableaux 2d ____________________________________ """
class TablePerso (ListPerso):
	def __str__ (self):
		fnlList = ListPerso()
		for line in self:
			tmpList =[]
			for item in line: tmpList.append (str (item))
			fnlList.append ('t'.join (tmpList))
		return fnlList.__str__()
	def emptyTable (self, nlin, ncol, filling=None):
		rlin= range (nlin)
		rcol= range (ncol)
		for l in rlin:
#			creer une ligne
			self.append (ListPerso())
			for c in rcol:
#				creer une case
				self[-1].append (filling)
	def revert (self):
		newTable = table()
		rangeCol = self[0].range()
		for c in rangeCol:
			newTable.append ([])
			for line in self: newTable[-1].append (line[c])
		return newTable
	""" fonctions pour traiter les colonnes """
	def col (self, nb):
		""" récupérer tous les éléments de la colone nb """
		liste =[]
		for line in self:
#			si la ligne est courte, n'a pas de case nb
			if len (line) <=nb: liste.append (None)
			else: liste.append (line[nb])
		return liste
	def colPop (self, nb):
		rangeTab = self.range()
		for i in rangeTab:
#			repere si la ligne est asssez longue pour avoir une case nb
			if len (self[i]) >nb: trash = self[i].pop (nb)
	def colAppend (self, col):
		rangeCol = range (len (col))
		for i in rangeCol: self[i].append (col[i])
	def colInsert (self, pos, col):
		rangeCol = range (len (col))
		for i in rangeCol: self[i].insert (pos, col[i])
class TableText (ListText):
	def __init__ (self, file=None, separator='n', separatorCol='t'):
		ListText.__init__(self, file, separator)
		self.separatorCol = separatorCol
	def fromList (self):
		rangeList = self.range()
		for l in rangeList:
			while self.separatorCol + self.separatorCol in self.list[l]:
				self.list[l] = self.list[l].replace (self.separatorCol + self.separatorCol, self.separatorCol)
			newLine = ListPerso()
			newLine.extend (self.list[l].split (self.separatorCol))
			self.list[l] = newLine
	def fromFile (self):
		ListText.fromFile (self)
		self.fromList()
	def toFile (self, mode='w'):
		self.text = self.toStr()
		FilePerso.toFile (self, mode)
	def toStr (self):
		string =""
		for line in self.list:
			for item in line:
				string = string + str (item) + self.separatorCol
			string = string + self.separator
		string = string.replace (self.separatorCol + self.separator, self.separator)
		return string
	def fromStr (self, text=None):
		ListText.fromStr (self, text)
		self.fromList()
class TableBdd (TableText):
	def __init__ (self, file=None):
		TableText.__init__(self, file, 'n', 't')
		self.colNames = ListPerso()
		self.colNames.separator ='t'
	def fromCsv (self):
		self.separatorCol = '","'
		self.fromFile()
		self.colNames.pop(0)
		self.colNames[-1] = self.colNames[-1][:-1]
		rangeTab = self.range()
		for l in rangeTab:
			self[l].pop(0)
			self[l][-1] = self[l][-1][:-1]
		self.list.sort()
		self.separatorCol ='t'
		self.extension = 'tsv'
		self.toFile()
	def fromFile (self):
		TableText.fromFile (self)
		self.colNames = self.list.pop(0)
	def toFile (self, mode='w'):
	#	self.list.sort()
		self.list.insert (0, self.colNames)
		TableText.toFile (self)
	def get (self, colName, value, contains='full'):
		""" les valeurs de contains:
			full: la case contient exactement la valeur recherchée
			none: la case ne contient pas la valeur recherchéé
			part: la valeur recherchéé est un mot-clef contenu dans la case
		"""
		pos = self.colNames.index (colName)
		newTable = TableBdd()
		if contains == 'full':
			for line in self.list:
				if line[pos] == value: newTable.append (line)
		if contains == 'part':
			for line in self.list:
				if value in line[pos]: newTable.append (line)
		elif contains == 'none':
			for line in self.list:
				if line[pos] != value: newTable.append (line)
		return newTable
	def order (self, orderedCol):
		# ordonner les colonnes dans une liste temporaire
		newTable = TableBdd (self.file)
		newTable.dataFromfile()
		TablePerso.emptyTable (newTable.list, len (self.list), 0)
		rangeList = self.range()
		for colName in orderedCol:
			id= self.colNames.index (colName)
			newTable.colNames.append (colName)
			for l in rangeList:
				newTable.list[l].append (self.list[l][id])
		# remplacer l'objet original par le nouveau
		self.colNames =[]
		self.colNames.extend (newTable.colNames)
		for l in rangeList:
			self.list[l] = ListPerso()
			self.list[l].extend (newTable.list[l])
	def __str__(self):
		string = FilePerso.__str__(self)
		string = string +'ncolonnes: '+ ', '.join (self.colNames)
		return string