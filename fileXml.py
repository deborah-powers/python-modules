#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import textFct
from fileCls import File
from folderCls import Folder
import loggerFct as log

header = '<?xml version="1.0" encoding="utf-8"?>'
styleTag = "<?xml-stylesheet type='text/css' href='xml-style.css'?>"
desktopPath = 'C:\\Users\\deborah.powers\\Desktop\\'
folderPath = desktopPath + '$demarche flux\\'

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

	def findChildPosByName (self, childName, numOccurency=1):
		if childName == 'filiation': return -1
		nbChildren = len (self.children)
		c=0
		pos =-1
		while c< nbChildren and numOccurency >0:
			if self.children[c].name == childName:
				numOccurency -=1
				pos =c
			c+=1
		return pos

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
			rangeChild = range (len (self.children))
			for a in rangeChild:
				numOccurency =1+ self.children[a].countOccurencesNameInList (self.children[:a])
				o= newNode.findChildPosByName (self.children[a].name, numOccurency)
				if o>=0: messageChildren = messageChildren +'\n'+ self.children[a].comparer (newNode.children[o], longNameSelf, longNameNew)
		# nettoyer le message
		message = message.strip()
		while '\n\n' in message: message = message.replace ('\n\n', '\n')
		if message:
			if longNameSelf == longNameNew: message = 'comparer les noeuds '+ longNameSelf +'\n'+ message
			else: message = 'comparer les noeuds '+ longNameSelf +" et "+ longNameNew +'\n'+ message
		message = message + messageChildren
		# nettoyer le message
		message = message.strip()
		while '\n\n' in message: message = message.replace ('\n\n', '\n')
		return message

	def __eq__ (self, newNode):
		if self.name != newNode.name or self.text != newNode.text: return False
		isEquals = self.samesAttributes (newNode)
		if not isEquals: return False
		else: isEquals = self.samesChildren (newNode)
		if not isEquals: return False
		# comparer le contenu des noeuds enfants
		a=0
		nbChildren = len (self.children)
		while isEquals and a< nbChildren:
			numOccurency =1+ self.children[a].countOccurencesNameInList (self.children[:a])
			o= newNode.findChildPosByName (self.children[a].name, numOccurency)
			isEquals = self.children[a].__eq__ (newNode.children[o])
			a+=1
		return isEquals

	def __ne__ (self, newNode):
		return not self.__eq__ (newNode)

	def countOccurencesNameInList (self, liste):
		# liste est une liste de noeuds. utilisée dans les comparaisons
		isInList =0
		for node in liste:
			if node.name == self.name: isInList +=1
		return isInList

	def sameStructureTree (self, newNode):
		isSameStructure = self.sameStructureNode (newNode)
		if not isSameStructure: return False
		# la structure des noeuds enfants
		a=0
		nbChildren = len (self.children)
		while isSameStructure and a< nbChildren:
			numOccurency =1+ self.children[a].countOccurencesNameInList (self.children[:a])
			o= newNode.findChildPosByName (self.children[a].name, numOccurency)
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
		attributesSelf = list (self.attributes.keys())
		areSamesAttributes = True
		a=0
		nbAttributes = len (attributesSelf)
		while areSamesAttributes and a< nbAttributes:
			if self.attributes [attributesSelf[a]] != newNode.attributes [attributesSelf[a]]: areSamesAttributes = False
			a+=1
		return areSamesAttributes

	def sameAttributeStructure (self, newNodeAttributes):
		# les noms des attributs
		attributesSelf = list (self.attributes.keys())
		attributesNew = list (newNodeAttributes.keys())
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

	def comparer (self, newFile, pathDest=None):
		if not pathDest: pathDest = desktopPath
		self.toPath()
		newFile.toPath()
		if self.tree == newFile.tree: print ("les xml sont identiques:\n", self.path, '\n', newFile.path)
		else:
			# calculer le titre de la comparaison
			title = pathDest + 'comparer '+ self.title +" et "
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
		if '<?' in self.text:
			d= self.text.rfind ('<?')
			d=1+ self.find ('>',d)
			self.text = self.text[d:]
		self.text = self.tree.treeFromText (self.text)


def comparerTreeGroup (treeGroup, parentSelf=""):
	if 'filiation' in parentSelf or 'filiation' in treeGroup[0].name: return ""	# astuce pour éliminer des éléments parasites dans les flux de sian
	# noeuds identiques
	treeNb = len (treeGroup)
	rangeX = range (treeNb)
	tabCompar =[]
	# comparer les fichiers
	for i in rangeX:
		tabCompar.append ([])
		for d in rangeX: tabCompar[-1].append (9)
		"""
		fillExpress = False
		rangeY = range (i+1, treeNb)
		print (parentSelf, treeGroup[i].name)
		for d in rangeY:
			if treeGroup[i] == treeGroup[d]: tabCompar[-1][d] =0
		rangeY = range (i)
		for d in rangeY:
			if tabCompar[-1][d] ==0:
				rangeId = range (i+1, treeNb)
				for e in rangeId: tabCompar[i][e] = tabCompar[d][e]
				fillExpress = True
		if fillExpress: continue
		"""
		rangeY = range (i+1, treeNb)
		for d in rangeY:
			if treeGroup[i].name != treeGroup[d].name: tabCompar[-1][d] =6
			elif treeGroup[i] == treeGroup[d]: tabCompar[-1][d] =0
			elif not treeGroup[i].samesChildren (treeGroup[d]): tabCompar[-1][d] =5
			elif not treeGroup[i].sameAttributeStructure (treeGroup[d].attributes): tabCompar[-1][d] =3
			elif not treeGroup[i].samesAttributes (treeGroup[d]): tabCompar[-1][d] =2
			elif treeGroup[i].text != treeGroup[d].text: tabCompar[-1][d] =4
			elif treeGroup[i].text =="" or treeGroup[d].text =="": tabCompar[-1][d] =1
	scoreCompar =0
	intruCompar = False
	for i in rangeX:
		rangeY = range (i+1, treeNb)
		if 6 in tabCompar[i]: intruCompar = True
		for d in rangeY: scoreCompar += tabCompar[i][d]
	if scoreCompar ==0 or intruCompar: return ""
	# ajouter les messages
	message =""
	donesX =[]
	for i in rangeX:
		if i in donesX: continue
		donesX.append (i)
		prefix = str(i)
		rangeY = range (i+1, treeNb)
		donesY =[]
		for d in rangeY:
			if d in donesY: continue
			elif tabCompar[i][d] ==0:
				prefix = prefix +" "+ str(d)
				donesX.append (d)
		for d in rangeY:
			if d in donesY or d in donesX: continue
			donesY.append (d)
			suffix = str (d)
			if 0 in tabCompar[d]:
				rangeId = range (d+1, treeNb)
				for e in rangeId:
					if tabCompar[d][e] ==0:
						suffix = suffix +" "+ str(e)
						donesY.append (e)
			if tabCompar[i][d] ==5:
				message = message + '\nnoms des enfants différents %s - %s\n. ' % (prefix, suffix)
				children = treeGroup[d].getChildrenNames()
				for child in treeGroup[i].children:
					if child.name not in children: message = message + child.name +", "
				message = message +'\n. '
				children = treeGroup[i].getChildrenNames()
				for child in treeGroup[d].children:
					if child.name not in children: message = message + child.name +", "
			elif tabCompar[i][d] ==4:
				message = message + '\nles textes sont différents %s - %s' % (prefix, suffix)
				if treeGroup[i].text =="": message = message +'\n.'
				else: message = message +'\n'+ treeGroup[i].text
				if treeGroup[d].text =="": message = message +'\n.'
				else: message = message +'\n'+ treeGroup[d].text
			elif tabCompar[i][d] ==3: message = message + '\nles attributs ont des structures différentes %s - %s' % (prefix, suffix)
			elif tabCompar[i][d] ==2: message = message + '\nles attributs ont des valeurs différentes %s - %s' % (prefix, suffix)
	message = message +'\n'
	message = message.replace ('\n. \n', '\n.\n')
	message = message.replace ('\n. ', '\n')
	# les enfants
	messageChildren =""
	longNameSelf = parentSelf +'.'+ treeGroup[0].name
	donesX =[]
	# je considère que les listes d'enfants sont identiques
	childRange = range (len (treeGroup[0].children))
	for c in childRange:
		childGroup =[]
		for t in rangeX: childGroup.append (treeGroup[t].children[c])
		messageChildren = messageChildren +'\n'+ comparerTreeGroup (childGroup, longNameSelf)
	# nettoyer le message
	message = message.strip()
	while '\n\n' in message: message = message.replace ('\n\n', '\n')
	if message: message = 'comparer les noeuds '+ longNameSelf +'\n'+ message
	message = message + messageChildren
	# nettoyer le message
	message = message.strip()
	while '\n\n' in message: message = message.replace ('\n\n', '\n')
	return message

def comparerTreeGroup_fina (treeGroup, parentSelf=""):
	for i in rangeX:
		if i in donesX or 1 not in tabCompar[i]: continue
		rangeY = range (i+1, treeNb)
		rangeChild = range (len (treeGroup[i].children))
		for a in rangeChild:
			childGroup =[ treeGroup[i].children[a] ]
			for d in rangeY:
				if d in donesX or tabCompar[i][d] !=1: continue
				numOccurency =1+ treeGroup[i].children[a].countOccurencesNameInList (treeGroup[i].children[:a])
				o= treeGroup[d].findChildPosByName (treeGroup[i].children[a].name, numOccurency)
				childGroup.append (treeGroup[d].children[o])
			messageChildren = messageChildren +'\n'+ comparerTreeGroup (childGroup, longNameSelf)
		for d in rangeY:
			if tabCompar[i][d] ==1: donesX.append (d)

class FolderXml (Folder):
	# spécial pour les flux de sian
	def getTree (self, tagName=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			range_tag = range (len (subList) -1, -1, -1)
			for i in range_tag:
				if " flux.xml" not in subList[i]: trash = subList.pop(i)
			if tagName:
				range_tag = range (len (subList) -1, -1, -1)
				if sens:
					for i in range_tag:
						if tagName not in subList[i]: trash = subList.pop(i)
				else:
					for i in range_tag:
						if tagName in subList[i]: trash = subList.pop(i)
			if subList:
				for file in subList:
					fileTmp = FileXml (os.path.join (dirpath, file))
					fileTmp.fromPath()
					self.list.append (fileTmp)
		self.list.sort()
		self.fromPath()

	def get (self, tagName=None, sens=True):
		subList = os.listdir (self.path)
		range_tag = range (len (subList) -1, -1, -1)
		for i in range_tag:
			if " flux.xml" not in subList[i]: trash = subList.pop(i)
		if tagName:
			range_tag = range (len (subList) -1, -1, -1)
			if sens:
				for i in range_tag:
					if tagName not in subList[i]: trash = subList.pop(i)
			else:
				for i in range_tag:
					if tagName in subList[i]: trash = subList.pop(i)
		if subList:
			for file in subList:
				fileTmp = FileXml (self.path + file)
				fileTmp.fromPath()
				self.list.append (fileTmp)
		self.list.sort()
		self.fromPath()

	def findPairs (self):
		# trouver les paires de fichiers npsl - legacy afin de faire la comparaison
		filePairsTmp =[]
	#	fileSingles =[]
		nbFiles = len (self.list)
		rangeFiles = range (nbFiles)
		for f in rangeFiles:
			if f in filePairsTmp: continue
			g=f+1
			while g< nbFiles:
				if self.list[g].title[:-18] == self.list[f].title[:-18]:
					filePairsTmp.append (f)
					filePairsTmp.append (g)
					g= nbFiles
				g+=1
		filePairs =[]
		rangeFiles = range (0, len (filePairsTmp), 2)
		for f in rangeFiles: filePairs.append ((filePairsTmp[f], filePairsTmp[f+1]))
		return filePairs

	def findGroups (self):
		# trouver les groupes de fichiers npsl - legacy afin de faire la comparaison
		fileGroups =[]
		fileDones =[]
		nbFiles = len (self.list)
		rangeFiles = range (nbFiles)
		for f in rangeFiles:
			if f in fileDones: continue
			fileGroup =[f]
			fileDones.append (f)
			rangeTmp = range (f+1, nbFiles)
			for g in rangeTmp:
				if self.list[g].title[:-18] == self.list[f].title[:-18]:
					fileGroup.append (g)
					fileDones.append (g)
			if len (fileGroup) >1: fileGroups.append (fileGroup)
		return fileGroups

	def comparer (self):
		filePairs = self.findPairs()
		for (fa, fo) in filePairs:
			self.list[fa].path = self.path + self.list[fa].path
			self.list[fa].read()
			self.list[fo].path = self.path + self.list[fo].path
			self.list[fo].read()
			self.list[fa].comparer (self.list[fo], self.path)

	def comparerGroup (self, groupId, pathDest=None):
		if not pathDest: pathDest = desktopPath
		for f in groupId: self.list[f].toPath()
		lenId = len (groupId)
		rangeId = range (lenId)
		tabCompar =[]
		for i in rangeId:
			tabCompar.append ([])
			for d in rangeId: tabCompar[-1].append (10)
			rangeTmp = range (i+1, lenId)
			for d in rangeTmp:
				if self.list[i].tree == self.list[d].tree:
					print ("les xml sont identiques:\n", self.list[i].path, '\n', self.list[d].path)
					tabCompar[-1][d] =0
		scoreCompar =0
		for line in tabCompar: scoreCompar += sum (line)
		if scoreCompar ==0: print ('tous les xml sont identiques')
		else:
			# calculer le titre de la comparaison
			title = pathDest + 'comparer '+ self.list [groupId[0]].title[:-18] + '.txt'
			print (self.list [groupId[0]].title[:-18])
			fileCommon = File (title)
			# comparer
			fileCommon.text = 'comparer les fichiers'
			treeGroup =[]
			for f in groupId:
				fileCommon.text = fileCommon.text +'\n'+ self.list[f].path
				treeGroup.append (self.list[f].tree)
			fileCommon.text = fileCommon.text +'\n\n'
			message = comparerTreeGroup (treeGroup)
			message = message.replace (" .", " ")
			message = textFct.cleanBasic (message)
			message = message.replace ('\ncomparer', '\n\ncomparer')
			fileCommon.text = fileCommon.text + message
			fileCommon.write()

	def comparerGroups (self):
		fileGroups = self.findGroups()
		for group in fileGroups:
			for f in group:
				self.list[f].path = self.path + self.list[f].path
				self.list[f].read()
			self.comparerGroup (group)

if len (argv) ==2:
	folderPath = folderPath.replace ('$demarche', argv[1])
	folderComp = FolderXml (folderPath)
	folderComp.get()
#	folderComp.list.reverse()
	folderComp.comparerGroups()
else: print ("entrez l'abbréviation de la démarche")
