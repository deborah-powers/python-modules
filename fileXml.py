#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import textFct
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
		if textParent =="": return ""
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
		if self == newNode: return ""
		longNameSelf = parentSelf +'.'+ self.name
		longNameNew = parentNew +'.'+ newNode.name
		message =""
		if self.sameStructureNode (newNode):
			# début de la démarche
			if parentSelf =="" and not self.sameStructureTree (newNode): message = message + '\nles arbres ont des structures différentes'
		else:
			if not self.sameAttributeStructure (newNode.attributes): message = message + '\nstructure des attributs différentes'
			if not self.samesAttributes (newNode): message = message + '\nattributs différents'
			if not self.samesChildren (newNode):
				message = message + '\nnoms des enfants différents\n. '
				children = newNode.getChildrenNames()
				for child in self.children:
					if child.name not in children: message = message + child.name +", "
				message = message +'\n. '
				children = self.getChildrenNames()
				for child in newNode.children:
					if child.name not in children: message = message + child.name +", "
			message = message +'\n'
			message = message.replace ('\n. \n', '\n.\n')
			message = message.replace ('\n. ', '\n')
		messageChildren =""
		if self.text != newNode.text:
			message = message + '\ncontenu différent\n'
			if self.text: message = message + self.text +'\n'
			else: message = message +'.\n'
			if newNode.text: message = message + newNode.text
			else: message = message +'.'
		elif self.text =="":
			for child in self.children:
				o= newNode.findChildPosByName (child.name)
				if o>=0: messageChildren = messageChildren +'\n'+ child.comparer (newNode.children[o], longNameSelf, longNameNew)
		# nettoyer le message
		message = message.strip()
		while '\n\n' in message: message = message.replace ('\n\n', '\n')
		if message:
			if longNameSelf == longNameNew: message = 'comparer les noeuds xml '+ longNameSelf +'\n'+ message
			else: message = 'comparer les noeuds xml '+ longNameSelf +" et "+ longNameNew +'\n'+ message
		message = message + messageChildren
		# nettoyer le message
		message = message.strip()
		while '\n\n' in message: message = message.replace ('\n\n', '\n')
		return message

	def __eq__ (self, newNode):
		if self.name != newNode.name or self.text != newNode.text: return False
		isEquals = self.samesAttributes (newNode)
		if isEquals: isEquals = self.samesChildren (newNode)
		if not isEquals: return False
		# comparer le contenu des noeuds enfants
		a=0
		nbChildren = len (self.children)
		while isEquals and a< nbChildren:
			o= newNode.findChildPosByName (self.children[a].name)
			if self.children[a].text != newNode.children[o].text: isEquals = False
			elif not self.children[a].samesAttributes (newNode.children[o]): isEquals = False
			elif not self.children[a].samesChildren (newNode.children[o]): isEquals = False
			elif not self.children[a].__eq__ (newNode.children[o]): isEquals = False
			a+=1
		return isEquals

	def __ne__ (self, newNode):
		return not self.__eq__ (newNode)

	def sameStructureTree (self, newNode):
		isSameStructure = self.sameStructureNode (newNode)
		if not isSameStructure: return False
		# la structure des noeuds enfants
		a=0
		nbChildren = len (self.children)
		while isSameStructure and a< nbChildren:
			o= newNode.findChildPosByName (self.children[a].name)
			isSameStructure = self.children[a].sameStructureTree (newNode.children[o])
			a+=1
		return isSameStructure

	def sameStructureNode (self, newNode):
		if self.name != newNode.name: return False
		isSameStructure = self.sameAttributeStructure (newNode.attributes)
		if not isSameStructure: return False
		isSameStructure = self.samesChildren (newNode)
		return isSameStructure

	def samesAttributes (self, newNode):
		areSamesAttributes = self.sameAttributeStructure (newNode.attributes)
		if not areSamesAttributes: return False
		attributesSelf = self.attributes.keys()
		attributesNew = newNode.attributes.keys()
		areSamesAttributes = True
		a=0
		nbAttributes = len (attributesSelf)
		while areSamesAttributes and a< nbAttributes:
			if self.attributes [attributesSelf[a]] != newNode.attributes [attributesSelf[a]]: areSamesAttributes = False
			a+=1
		return areSamesAttributes

	def sameAttributeStructure (self, newNodeAttributes):
		# les noms des attributs
		attributesSelf = self.attributes.keys()
		attributesNew = newNodeAttributes.keys()
		areSamesAttributes = True
		a=0
		nbAttributes = len (attributesSelf)
		while areSamesAttributes and a< nbAttributes:
			if attributesSelf[a] not in attributesNew: areSamesAttributes = False
			a+=1
		if not areSamesAttributes: return False
		a=0
		nbAttributes = len (attributesNew)
		while areSamesAttributes and a< nbAttributes:
			if attributesNew[a] not in attributesSelf: areSamesAttributes = False
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
		if self.tree == newFile.tree: print ("les xml sont identiques:\n", self.path, '\n', newFile.path)
		else:
			# calculer le titre de la comparaison
			title = 'b/comparer '+ self.title +" et "
			d,f= textFct.commonParts (self.title, newFile.title)
			if d>3:
				title = title + newFile.title[d:f]
				while "  " in title: title = title.replace ("  "," ")
			else: title = title + newFile.title
			title = title + '.txt'
			fileCommon = File (title)
			# comparer
			fileCommon.text = 'comparer\n' + self.path +'\n'+ newFile.path +'\n\n'
			message = self.tree.comparer (newFile.tree)
			message = message.replace (" .", " ")
			message = textFct.cleanBasic (message)
			message = message.replace ('\ncomparer', '\n\ncomparer')
			fileCommon.text = fileCommon.text + message
			fileCommon.write()

	def read (self):
		File.read (self)
		self.cleanText()
		self.treeFromText()

	def cleanText (self):
		self.text = self.text.replace ('\t', " ")
		self.text = self.text.replace ('\n', " ")
		self.text = self.text.replace ('\r', " ")
		self.text = textFct.cleanBasic (self.text)
		self.text = self.text.replace (" <", "<")
		self.text = self.text.replace ("> ", ">")
		self.text = self.text.replace (" >", ">")

	def treeFromText (self):
		self.text = self.text.replace (header, "")
		self.text = self.tree.treeFromText (self.text)
