#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

def listMethodsSort_va (itemA, itemO):
	voyelles = 'aeiouy'
	if itemA in voyelles and itemO in voyelles: return itemA > itemO
	elif itemA not in voyelles and itemO not in voyelles: return itemA > itemO
	elif itemA in voyelles and itemO not in voyelles: return True
	else: return False

def listMethodsSort (itemA, itemO):
	voyelles = 'aeiouy'
	if itemA == itemO: return 0
	if itemA in voyelles and itemO in voyelles:
		if itemA > itemO: return 1	# itemA est après itemO
		else: return -1
	elif itemA not in voyelles and itemO not in voyelles:
		if itemA > itemO: return 1
		else: return -1
	elif itemA in voyelles and itemO not in voyelles: return -1
	else: return 1

def listMethods():
	from functools import cmp_to_key
	myList =[ 'a', 'b', 'c', 'd' ]
	b= myList.pop (1)
	myList.remove ('c')
	myList.append ('e')
	myList.extend ([ 'i', 'j', 'k' ])
	myList = myList + [ 'f', 'g', 'h' ]
	myList.sort()
	myList.insert (2, 'l')
	print (myList)
	myList = sorted (myList, key=cmp_to_key (listMethodsSort))
	print (myList)
	yList =[]
	for l in myList: yList.append (l+'y')
	print (yList)
	zList =[ l+ 'z' for l in myList ]
	print (zList)
	for (a,b) in yList: print (a, ':', b)

listMethods()

Reference = list	# nécessaire pour faire tourner le scipt. Reference peut-être n'importe quelle classe pré-existente
class Custom (Reference):
	# https://realpython.com/operator-function-overloading/#the-internals-of-operations-like-len-and
	def __init__(self, parameter):
		# custom = Custom (myParameter)
		self.field = parameter

	def __str__(self):
		# print (custom)
		return "parameter: "+ parameter

	def __repr__(self):
		# déconseillé. peut être utilisé à la place de str.
		return "objet Custom (Reference). parameter = "+ self.parameter

	def __len__(self):
		# len (custom)
		return parameter.__len__()

	def __add__ (self, itemStr):
		# newCustom = self + "grenouille"
		# aussi sub -, mul *, pow **, abs abs(nb),
		newCustom = Custom (self.parameter +" "+ itemStr)
		return newCustom

	def __radd__ (self, itemStr):
		# newCustom = "grenouille" + self
		# aussi rsub, rmul
		newCustom = Custom (itemStr +" "+ self.parameter)
		return newCustom

	def __iadd__ (self, itemStr):
		# custom += "grenouille"
		# aussi isub
		self.parameter +" "+ itemStr
		return self

	def __bool__(self):
		# if custom: do code
		if self.parameter: return True
		else: return False

	def __eq__(self, itemCustom):
		# custom == itemCustom
		# également ne !=, gt >, lt <, ge >=, le <=
		if self.parameter == itemCustom.parameter: return True
		else: return False
	"""
	def __or__ (self, item):
		# également not
	"""

	def __setitem__ (self, pos, item):
		# custom[2] = 'a'
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
		# print (custom[2])
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