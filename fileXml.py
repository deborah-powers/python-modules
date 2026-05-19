#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
import loggerFct as log

header = '<?xml version="1.0" encoding="utf-8"?>'

class NodeXml():
	def __init__ (self):
		self.name =""
		self.text =""
		self.children =[]
		self.attributes ={}

	def treeFromText (self, textParent):
		f= textParent.find ('>')
		self.name = textParent[1:f]
		if self.name[-1] == '/': self.name = self.name[:-1]
		if " " in self.name:
			# récupérer les attributs
			self.name = self.name.replace ('=', ':')
			tmpList = self.name.split (" ")
			self.name = tmpList.pop (0)
			for attr in tmpList:
				if ':' in attr:
					a= attr.find (':')
					self.attributes[attr[:a]] = attr[a+1:]
				else: self.attributes[attr] =""
		# la fin du bloc
		if textParent[f-1] =='/': textParent = textParent[f+1:]
		else:
			textParent = textParent[f+1:]
			f= textParent.find ('</' + self.name +'>')
		#	if '<'+ self.name in textParent[:f]: print ('nid')
			self.text = textParent[:f]
			f= textParent.find ('>', f)
			textParent = textParent[f+1:]
			while self.text !="" and self.text[0] == '<':
				self.children.append (NodeXml())
				self.text = self.children[-1].treeFromText (self.text)
		return textParent

	def __str__ (self):
		infos = self.name
		if self.attributes:
			infos = infos +'\nattributs:'
			keys = self.attributes.keys()
			for k in keys: infos = infos +" "+k+ " = "+ self.attributes[k] +','
		infos = infos +'\nenfants:'
		for child in self.children: infos = infos +" "+ child.name +','
		return infos

	def findChildPosByName (self, childName):
		nbChildren = len (self.children)
		c=0
		while c< nbChildren and self.children[c].name != childName: c+=1
		if c== nbChildren: c=-1
		return c

	def getChildrenNames (self):
		nameList =[]
		for child in self.children: nameList.append (child.name)
		return nameList

	def __eq__ (self, newNode):
		if self.name != newNode.name or self.text != newNode.text: return False
		result = self.samesAttributes (newNode)
		if result: result = self.samesChildren (newNode)
		if result:
			# comparer le contenu des noeuds enfants
			a=0
			nbChildren = len (self.children)
			while result and a< nbChildren:
				o= newNode.findChildPosByName (self.children[a].name)
				if self.children[a].text != newNode.children[o].text: result = False
				elif not self.children[a].samesAttributes (newNode.children[o]): result = False
				elif not self.children[a].samesChildren (newNode.children[o]): result = False
				elif not self.children[a].__eq__ (newNode.children[o]): result = False
				a+=1
		return result

	def __ne__ (self, newNode):
		if self.name != newNode.name or self.text != newNode.text: return True
		elif not self.samesAttributes (newNode): return True
		elif not self.samesChildren (newNode): return True
		# comparer le contenu des noeuds enfants
		a=0
		result = True
		nbChildren = len (self.children)
		while result and a< nbChildren:
			o= newNode.findChildPosByName (self.children[a].name)
			if self.children[a].text != newNode.children[o].text: result = False
			elif not self.children[a].samesAttributes (newNode.children[o]): result = False
			elif not self.children[a].samesChildren (newNode.children[o]): result = False
			elif not self.children[a].__eq__ (newNode.children[o]): result = False
			a+=1
		return (not result)

	def samesAttributes (self, newNode):
		attributesSelf = self.attributes.keys()
		attributesNew = newNode.attributes.keys()
		areSamesAttributes = True
		a=0
		nbAttributes = len (attributesSelf)
		while areSamesAttributes and a< nbAttributes:
			if attributesSelf[a] not in attributesNew: areSamesAttributes = False
			a+=1
		if areSamesAttributes:
			a=0
			nbAttributes = len (attributesNew)
			while areSamesAttributes and a< nbAttributes:
				if attributesNew[a] not in attributesSelf: areSamesAttributes = False
				elif self.attributes [attributesNew[a]] != newNode.attributes [attributesNew[a]]: areSamesAttributes = False
				a+=1
		return areSamesAttributes

	def samesChildren (self, newNode):
		# comparer seulement les noms des noeuds enfants
		childrenSelf = self.getChildrenNames()
		childrenNew = newNode.getChildrenNames()
		areSamesChildren = True
		a=0
		nbChildren = len (childrenSelf)
		while areSamesChildren and a< nbChildren:
			if childrenSelf[a] not in childrenNew: areSamesChildren = False
			a+=1
		if areSamesChildren:
			a=0
			nbChildren = len (childrenNew)
			while areSamesChildren and a< nbChildren:
				if childrenNew[a] not in childrenSelf: areSamesChildren = False
				a+=1
		return areSamesChildren

	def __gt__ (self, newNode):
		if self.name > newNode.name: return True
		elif self.name < newNode.name: return False
		if self.text !="" and newNode.text !="":
			if self.text > newNode.text: return True
			else: return False
		nbChildSelf = len (self.children)
		nbChildNew = len (newNode.children)
		if nbChildSelf > nbChildNew: return True
		else: return False

	def __lt__ (self, newNode):
		if self.name < newNode.name: return True
		elif self.name > newNode.name: return False
		if self.text !="" and newNode.text !="":
			if self.text < newNode.text: return True
			else: return False
		nbChildSelf = len (self.children)
		nbChildNew = len (newNode.children)
		if nbChildSelf < nbChildNew: return True
		else: return False

	def __ge__ (self, newNode):
		if self.name > newNode.name: return True
		elif self.name < newNode.name: return False
		if self.text !="" and newNode.text !="":
			if self.text >= newNode.text: return True
			else: return False
		nbChildSelf = len (self.children)
		nbChildNew = len (newNode.children)
		if nbChildSelf >= nbChildNew: return True
		else: return False

	def __le__ (self, newNode):
		if self.name < newNode.name: return True
		elif self.name > newNode.name: return False
		if self.text !="" and newNode.text !="":
			if self.text <= newNode.text: return True
			else: return False
		nbChildSelf = len (self.children)
		nbChildNew = len (newNode.children)
		if nbChildSelf <= nbChildNew: return True
		else: return False

class FileXml (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.tree = NodeXml()

	def comparer (self, newFile):
		self.toPath()
		newFile.toPath()
		if self.tree == newFile.tree: print ('les fichiers xml sont identiques\n', self.path, '\n', newFile.path)
		else: print ('les fichiers xml sont différents\n', self.path, '\n', newFile.path)


	def read (self):
		File.read (self)
		self.cleanText()
		self.treeFromText()

	def cleanText (self):
		self.text = self.text.replace ('\t', " ")
		self.text = self.text.replace ('\n', " ")
		self.text = self.text.replace ('\r', " ")
		while "  " in self.text: self.text = self.text.replace ("  ", " ")
		self.text = self.text.replace (" <", "<")
		self.text = self.text.replace ("> ", ">")
		self.text = self.text.replace (" >", ">")

	def treeFromText (self):
		self.text = self.text.replace (header, "")
		self.text = self.tree.treeFromText (self.text)

fileName = 'C:\\Users\\deborah.powers\\Desktop\\sian-2026\\test ciphyto flux\\ciphyto conseil lega flux.xml'
fileBisName = 'C:\\Users\\deborah.powers\\Desktop\\sian-2026\\test ciphyto flux\\ciphyto conseil npsl 05-18 flux.xml'

fileData = FileXml (fileName)
fileData.read()
fileBis = FileXml (fileBisName)
fileBis.read()
fileData.comparer (fileBis)
