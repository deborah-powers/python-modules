#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

header = '<?xml version="1.0" encoding="utf-8"?>'

class NodeXml():
	def __init__ (self):
		self.name =""
		self.text =""
		self.children =[]
		self.attributes ={}

	def __eq__ (self, newNode):
		if self.name != newNode.name: return False
		if self.text !="" and self.text != newNode.text: return False
		result = True
		attributesSelf = self.attributes.keys()
		attributesNew = newNode.attributes.keys()
		for attr in attributesSelf:
			if attr not in attributesNew: result = False
		if result:
			for attr in attributesNew:
				if attr not in attributesSelf: result = False
				elif attributesSelf [attr] != attributesNew [attr]: result = False
		if result:
			childrenSelf = self.getChildrenNames()
			childrenNew = newNode.getChildrenNames()
			for child in childrenSelf:
				if child not in childrenNew: result = False
			if result:
				for child in childrenNew:
					if child not in childrenSelf: result = False
			if result:
				for child in childrenSelf:
					if child in childrenNew:
						cNew = newNode.findChildPosByName (child.name)
						resutlChild = child.__eq__ (newNode.children[cNew])
						if not resutlChild: result = False
		return result

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

class FileXml (File):
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.tree = NodeXml()

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
		print (self.tree.children[2])

fileName = 'C:\\Users\\deborah.powers\\Desktop\\ciphyto flux\\demarche ciphyto 05-11 17-06 lega flux.xml'
fileData = FileXml (fileName)
fileData.read()
