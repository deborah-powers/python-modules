#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from dateClass import DatePerso
from fileList import FileList
from fileClass import FilePerso

help ="""
créer une fiche mantis perso.
python mantis.py cdm 29700 message (type / numint)
type vaut evo, ddt, ano
si un numéro de mantis interne est précisé à la place, le type est automatiquement fixé à ano.
"""
templateJson ="""{
"head": {
	"message": "%s",
	"numExt": %s,
	"numInt": %s,
	"modules": ["%s"],
	"date": "%s",
	"type": "%s"
},
"infos": [],
"solution": ""
}"""

templateSmall = """message		%s
num ext		%s
num int		%s
module		%s
type		%s
debut		%s
"""

template ="""
__________________________
______ présentation ______

message		%s
num ext		%s
num int		%s
module		%s
type		%s
debut		%s


______________________
______ solution ______


commit		?
branche		%s mantis-%s


___________________
______ infos ______

/10.202.202.254/marcheNTIC/Projet PILOT_CF/Production/01 -STD/
select * from deb_autorite where operation like 'AL000%%';


______________________________
______ %s aprem ______

______________________________
______ %s matin ______
"""

types =( 'ano', 'ddt', 'evo')

class Mantis (FilePerso):
	def __init__(self, numero ='0', message ='?', module = '?', numint ='0', type ='?'):
		FilePerso.__init__ (self)
		self.message = message
		self.numero = numero
		self.module = module
		self.type = type
		self.numint = numint
		self.date = DatePerso()
		self.date.today()

	def fromFile (self):
		FilePerso.fromFile (self)
		self.clean()
		while self.contain ('\n\n'): self.replace ('\n\n', '\n')
		data = self.fromModel (templateSmall)
		self.message = data[1]
		self.numero = data[2]
		self.numint = data[3]
		self.module = data[4]
		self.type = data[5]
		self.date.fromStr (data[6])
		print (self)

	def createFileOld (self):
		self.createFileText()

	def createFile (self):
		self.file = 'b/mantis '+ self.numero + '.txt'
		self.dataFromFile()
		self.text = template %( self.message, self.numero, self.numint, self.module, self.type, self.date.toStrDay(), self.module, self.numero, self.date.toStrDay(), self.date.toStrDay())
		if self.type != 'ddt': self.text = self.text + """
log.debug ("________________________ requete ________________________");
log.debug (obj.getA() +"\t"+ obj.getB);"""
		self.toFile()

	def createFileJson (self):
		self.file = 'b/mantis '+ self.numero + '.json'
		self.dataFromFile()
		self.text = templateJson %( self.message, self.numero, self.numint, self.module.replace (' ', '", "'), self.date.toStrDay(), self.type)
		self.toFile()

	def __lt__(self, newMantis):
		string = '%s %s'
		return string %( self.date.toStrDay(), self.numero) < string %( newMantis.date.toStrDay(), newMantis.numero)

	def __str__ (self):
		message = '%s - %s: %s\t\t\ttype: %s\tmodule: %s\tdébut: %s' %( self.numero, self.numint, self.message, self.type, self.module, self.date)
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

	def getByNumero (self, numero):
		self.get (numero)

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
	numero = argv[2]
	message = argv[3]
	numint ='0'
	type = '?'
	if len (argv) >4:
		type = argv[4]
		if type not in types:
			type = 'ano'
			numint = argv[4]
	fileMantis = Mantis (numero, message, module, numint, type)
	fileMantis.createFile()
# il manque des données
else: print (help)
