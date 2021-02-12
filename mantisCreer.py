#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.date import DatePerso
from debutils.fileList import FileList
from debutils.file import FilePerso

help ="""
créer une fiche mantis perso.
python mantis.py cdm 29700 message (type / numint)
type vaut evo, ddt, ano
si un numéro de mantis interne est précisé à la place, le type est automatiquement fixé à ano.
"""
templateSmall = """message		%s
num ext		%s
num int		%s
module		%s
type		%s
"""

template ="""
__________________________
______ présentation ______

message		%s
num ext		%s
num int		%s
module		%s
type		%s


______________________
______ solution ______

%s

___________________
______ infos ______

select * from deb_autorite where operation = 'AL0000012';

______ données ______


______ marche à suivre ______


______________________________
______ %s aprem ______

______________________________
______ %s matin ______
"""

types =( 'ano', 'ddt', 'evo')

class Mantis (FilePerso):
	def __init__(self, numext ='0', message ='?', module = '?', numint ='0', type ='?'):
		FilePerso.__init__ (self)
		self.message = message
		self.numext = numext
		self.module = module
		self.type = type
		self.numint = numint
		if (not type or type == '?') and 'ddt' in message.lower(): self.type = 'ddt'

	def fromFile (self):
		FilePerso.fromFile (self)
		self.clean()
		while self.contain ('\n\n'): self.replace ('\n\n', '\n')
		data = self.fromModel (templateSmall)
		self.message = data[1]
		self.numext = data[2]
		self.numint = data[3]
		self.module = data[4]
		self.type = data[5]

	def createFile (self):
		self.file = 'b/mantis '+ self.numext + '.txt'
		self.dataFromFile()
		solutionStr = 'branche: %s mantis-%s\nreprise de donnée nécessaire: ?' %( self.module, self.numext)
		if self.type == 'ddt': solutionStr = 'su_%s_' % self.numext
		date = DatePerso()
		date.today()
		self.text = template %( self.message, self.numext, self.numint, self.module, self.type, solutionStr, date.toStrDay(), date.toStrDay())
		if self.type != 'ddt': self.text = self.text + """
log.debug ("________________________ requete ________________________");
log.debug (obj.getA() +"\t"+ obj.getB);"""
		if 'aec' in self.module or 'sif' in self.module: self.replace ('deb_autorite', 'deb_autorite_ope')
		self.toFile()

	def __lt__(self, newMantis):
		string = '%s %s'
		return string %( self.module, self.numext) < string %( newMantis.module, newMantis.numext)

	def __str__ (self):
		message = '%s - %s: %s\t\t\ttype: %s\tmodule: %s' %( self.numext, self.numint, self.message, self.type, self.module)
		return message

class MantisList (FileList):
	def __init__(self):
		FileList.__init__(self, 'm/')

	def get (self, TagNomfile=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			if TagNomfile and sens:
				range_tag = range (len (subList) -1,-1,-1)
				for i in range_tag:
					if TagNomfile not in subList[i] or '.txt' not in subList[i]: trash = subList.pop (i)
			elif TagNomfile:
				range_tag = range (len (subList) -1,-1,-1)
				for i in range_tag:
					if TagNomfile in subList[i] and '.txt' in subList[i]: trash = subList.pop (i)
			if subList:
				for file in subList:
					fileTmp = fc.FilePerso (os.path.join (dirpath, file))
					fileTmp.dataFromFile()
					self.append (fileTmp)
		self.sort()
		rangeFile = self.range()
		for f in rangeFile: self[f].fromFile()

	def getBynumext (self, numext):
		self.get (numext)

	def getByType (self, type):
		newList = MantisList()
		for file in self.list:
			if file.type == type: newList.add (file)
		return newList

	def getByModule (self, module):
		newList = MantisList()
		for file in self.list:
			if file.module == module: newList.add (file)
		return newList

# on appele ce script dans un autre script
if __name__ != '__main__': pass
# créer une fiche
elif len (argv) >3:
	module = argv[1]
	numext = argv[2]
	message = argv[3]
	numint ='0'
	type = '?'
	if len (argv) >4:
		type = argv[4]
		if type not in types:
			type = 'ano'
			numint = argv[4]
	fileMantis = Mantis (numext, message, module, numint, type)
	fileMantis.createFile()
# il manque des données
else: print (help)
