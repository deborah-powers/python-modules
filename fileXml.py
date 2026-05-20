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

	def comparer (self, newNode, parentSelf="", parentNew=""):
		longNameSelf = parentSelf +'.'+ self.name
		longNameNew = parentNew +'.'+ newNode.name
		message = self.comparerNoeuds (newNode, longNameSelf, longNameNew)
		if 'comparer' in message and len (self.children) >0 and len (newNode.children) >0:
			messageChildren =""
			if '\n' not in message: message =""
			else: messageChildren = '\nenfants différents'
			childrenNew = newNode.getChildrenNames()
			for child in self.children:
				if child.name in childrenNew:
					childPos = newNode.findChildPosByName (child.name)
					messageChildren = messageChildren +'\n'+ child.comparer (newNode.children [childPos], longNameSelf, longNameNew)
			if '\n' in messageChildren: message = message + messageChildren
		message = message.strip()
		while '\n\n' in message: message = message.replace ('\n\n', '\n')
		message = message.replace ('\ncomparer', '\n\ncomparer')
		message = message.replace ('\ncomparer .', '\ncomparer ')
		return message

	def comparerNoeuds (self, newNode, longNameSelf="", longNameNew=""):
		if self == newNode: return ""
		else:
		#	message = 'les noeuds xml sont différents: '+ self.name
			message = "comparer "+ longNameSelf
			if longNameSelf != longNameNew: message = message +" et "+ longNameNew
			if not self.samesAttributes (newNode):
				attributesSelf = self.attributes.keys()
				attributesNew = newNode.attributes.keys()
				message = '\n\tattributs en plus:\n'
				for attr in attributesSelf:
					if attr not in attributesNew: message = message +" "+ attr +","
				message = message + '\n'+ newNode.name +':'
				for attr in attributesNew:
					if attr not in attributesSelf: message = message +" "+ attr +","
				message = message + '\n\tattributs de même nom:'
				for attr in attributesNew:
					if attr in attributesSelf and self.attributes[attr] != newNode.attributes[attr]: message = message +" "+ attr +": "+ self.attributes[attr] +" "+ newNode.attributes[attr] +','
			if self.text != newNode.text: message = message +'\nvaleurs différentes: '+ self.text +" / "+ newNode.text
			if not self.samesChildren (newNode):
				childrenSelf = self.getChildrenNames()
				childrenNew = newNode.getChildrenNames()
				message = message + '\n\tenfants en plus\n' + self.name +':'
				for child in childrenSelf:
					if child not in childrenNew: message = message +" "+ child +","
				message = message + '\n'+ newNode.name +':'
				for child in childrenNew:
					if child not in childrenSelf: message = message +" "+ child +","
		return message

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
		message = self.tree.comparer (newFile.tree)
		print (message)

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
