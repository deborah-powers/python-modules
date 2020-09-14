#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from tableClass import ListText
import fileClass

fileClass.extensions = fileClass.extensions +' java jsp properties'

""" raccourcis possibles
cdm/web/xxx
cdm/service/xxx
cdm/repository/xxx
cdm/jsp/xxx
cdm/action/xxx
cdm/pom
cdm/config
cdm/lfj
"""

class TypeEnum():
	def __init__(self, name, shortcut, longcut):
		self.name = name
		self.shortcut = shortcut
		self.longcut = longcut
		self.place =""
		self.getPlace()

	def getPlace (self):
		if self.shortcut[-1] =='/' and self.shortcut[0] =='/': self.place = 'middle'
		elif self.shortcut[-1] =='/': self.place = 'start'
		else: self.place = 'end'

	def __str__(self):
		return self.name +'\t'+ self.shortcut +'\t'+ self.longcut

class TypeList():
	def __init__(self):
		self.list =[]

	def get (self, code):
		result = None
		i=0
		while i< len (self.list):
			if self.list[i].name == code:
				result = self.list[i]
				i= len (self.list) +2
			i+=1
		return result

	def getByShortcut (self, shortcut):
		result = None
		i=0
		while i< len (self.list):
			if self.list[i].shortcut == shortcut:
				result = self.list[i]
				i= len (self.list) +2
			i+=1
		return result

	def append (self, element):
		self.list.append (element)

	def create (self, name, shortcut, longcut):
		self.append (TypeEnum (name, shortcut, longcut))

	def contain (self, name):
		inside = False
		for enum in self.list:
			if enum.name == name: inside = True
		return inside

	def containShortcut (self, shortcut):
		inside = False
		for enum in self.list:
			if enum.shortcut == shortcut: inside = True
		return inside

	def addAll (self):
		self.create ('cdm', 'cdm/', fileClass.pathProject + 'app-cdm\\')
		self.create ('ac', 'aco/', fileClass.pathProject + 'app-ac\\')
		self.create ('cdm-batch', 'cbt/', fileClass.pathProject + 'app-cdm-batch\\')
		self.create ('sif', 'sif/', fileClass.pathProject + 'app-sif\\')
		self.create ('aec', 'aec/', fileClass.pathProject + 'app-aec\\')
		self.create ('sif-batch', 'sbt/', fileClass.pathProject + 'app-sif-batch\\')
		self.create ('pom', '/pom', 'pom.xml')
		self.create ('web', '/web/', 'app-%s-web\\src\\main\\')
		self.create ('serice', '/ser/', 'app-%s-service\\src\\main\\')
		self.create ('repository', '/rep/', 'app-%s-repository\\src\\main\\')
		self.create ('jsp', '/jsp/', 'app-%s-web\\src\\main\\webapp\\jsp\\')
		self.create ('ressource', '/res/', 'app-%s-web\\src\\main\\resources\\')
		self.create ('java', '/jav/', 'java\\fr\\asp\\synergie\\app\\%s\\')
		self.create ('action', '/act/', 'app-%s-web\\src\\main\\java\\fr\\asp\\synergie\\app\\%s\\action\\')
		self.create ('log4j', '/lfj', 'app-%s-web\\src\\main\\resources\\log4j.properties')
		self.create ('config', '/cfg', 'app-%s-web\\src\\main\\resources\\config.properties')

	def getModules (self):
		moduList = TypeList()
		for enum in self.list:
			if enum.place == 'start': moduList.append (enum)
		return moduList

	def getSubModules (self):
		moduList = TypeList()
		moduList.append (self.get ('web'))
		moduList.append (self.get ('serice'))
		moduList.append (self.get ('repository'))
		return moduList

	def getNames (self):
		nameList =""
		for enum in self.list: nameList +=' '+ enum.name
		return nameList

	def getShortcut (self):
		nameList =""
		for enum in self.list: nameList +=' '+ enum.shortcut
		return nameList

	def __str__(self):
		message =""
		for enum in self.list: message += '\n'+ str (enum)
		return message[1:]

typeList = TypeList()
typeList.addAll()
moduList = typeList.getModules()
subModuList = typeList.getSubModules()

class FileProjet (fileClass.FilePerso):
	def __init__(self, file =None):
		fileClass.FilePerso.__init__(self, file)
		self.type = 'all'
		self.module = 'cdm'

	def shortcut (self):
		if self.file.find (fileClass.pathProject) ==0: return
		if not moduList.containShortcut (self.file[:4]):
			print ('module inconnu: %s. choisir une valeur dans %s' %( self.file[:3], moduList.getShortcut() ))
			return
		enumTmp = moduList.getByShortcut (self.file[:4])
		self.module = enumTmp.name
		path = enumTmp.longcut
		self.file = self.file[3:]
		enumTmp = typeList.getByShortcut (self.file[:5])
		path = path + enumTmp.longcut
		# continuer l'opération si le fichier n'est pas le pom
		if enumTmp.name == 'pom':
			self.file = path
			self.dataFromFile()
			return
		paramNb = path.count ('%s')
		if paramNb ==1: path = path % self.module
		elif paramNb ==2: path = path % (self.module, self.module)
		self.file = self.file[4:]
		if self.file[:5] == '/jav/':
			enumTmp = typeList.get ('java')
			path += enumTmp.longcut
			path = path % self.module
			self.file = self.file[4:]
		if self.file[0] =='/': self.file = self.file[1:]
		self.file = path + self.file
		self.dataFromFile()

	def fromFile (self):
		self.shortcut()
		fileClass.FilePerso.fromFile (self);
		# nettoyer le fichier
		self.replace ('    ')
		self.replace ('\t')
		self.clean()
		while self.contain ('\n\n'): self.replace ('\n\n', '\n')
		self.replace ('\n{', ' {')
		self.replace ('\n(', ' (')
		self.replace ('\n[', ' [')
		while self.contain ('  '): self.replace ('  ', ' ')
		# nettoyer la jsp
		if self.type == 'jsp' or self.extension == 'xml':
			self.replace ('\n', ' ')
			self.replace ('  ', ' ')
			self.replace ('> ', '>\n')
			self.replace (' <', '\n<')


def printList (myList):
	for line in myList: print ('-->', line)
fileNameA = 'cdm/rep/jav/entities\\entity\\beneficiaire\\recherche\\PorteurDpo.java'
fileObjA = FileProjet (fileNameA)
fileNameB = 'cdm/rep/jav/entities\\entity\\instruction\\comite\\OperationComiteDpo.java'
fileObjB = FileProjet (fileNameB)
fileObjA.compar (fileObjB, 'lsort')
"""
domRes = fileObjA.domAccoladePlan()
printList (domRes)
"""





