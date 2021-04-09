#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from debutils.file import File
from debutils.listFile import ListFile
import debutils.logger as log

types = ('ano', 'ddt', 'evo')
refName = 'C:\\Users\\deborah.powers\\python\\mantis\\mantis\\mantis-base.txt'
refFile = File (refName)
sqlName = 'C:\\Users\\deborah.powers\\python\\mantis\\mantis\\su_cdm.sql'
sqlFile = File (sqlName)

class Mantis():
	def __init__ (self, numext ='0', message ='?', module = '?', numint ='0', type ='?'):
		self.message = message
		self.numext = numext
		self.module = module
		self.numint = numint
		self.type = '?'
		if type in types: self.type = type
		else:
			self.types = 'ano'
			if 'ddt' in message.lower(): self.type = 'ddt'

	def __lt__ (self, newMantis):
		string = '%s %s'
		return string % (self.module, self.numext) < string % (newMantis.module, newMantis.numext)
	def __str__ (self):
		message = '%s - %s: %s\ttype: %s\tmodule: %s' % (self.numext, self.numint, self.message, self.type, self.module)
		return message

class MantisFile (Mantis, File):
	def __init__ (self, numext ='0', message =' ?', module = ' ?', numint ='0', type =' ?'):
		Mantis.__init__ (self, numext, message, module, numint, type)
		File.__init__ (self, 'b/mantis ' + numext + '.txt')

	def createFile (self):
		refFile.fromFile()
		strNum = str (self.numext)
		while len (strNum) <4: strNum = '0'+ strNum
		self.message = '000'+ strNum +': '+ self.message
		refFile.replace ('%message%', self.message)
		refFile.replace ('%numext%', self.numext)
		refFile.replace ('%numint%', self.numint)
		refFile.replace ('%module%', self.module)
		refFile.replace ('%type%', self.type)
		commandesStr = 'log.debug ("________________________ requete ________________________");\nlog.debug (obj.getA() +"\t"+ obj.getB());'
		solutionStr = 'commit sur %s,\nbranche mantis-%s\nreprise de donnée nécessaire: ?' % (self.module, self.numext)
		if self.type == 'ddt':
			solutionStr = 'su_%s_' % self.numext
			commandesStr =""
		refFile.replace ('%commandes%', commandesStr)
		refFile.replace ('%solution%', solutionStr)
		schema = 'cdm'
		if self.module in 'aec can sif': schema = 'sif'
		refFile.replace ('%schema%', schema)
		date = datetime.now()
		dateStr = '%02d/%02d/%02d' % (date.year, date.month, date.day)
		refFile.replace ('%date%', dateStr)
		refFile.file = self.file
		refFile.dataFromFile()
		refFile.replace (' ______\n', ' ______\n\n')
		refFile.toFile()
		if self.type == 'ddt': self.createDdt (dateStr)

	def createDdt (self, dateStr):
		if self.module in 'aec can sif':
			sqlFile.file = sqlFile.file.replace ('_cdm', '_sif');
			sqlFile.dataFromFile()
		sqlFile.fromFile()
		sqlFile.replace ('%numero%', self.numext)
		sqlFile.replace ('%date%', dateStr)
		sqlFile.path = self.path
		sqlFile.title = sqlFile.title.replace ('su_', 'su_'+ self.numext +'_')
		sqlFile.fileFromData()
		sqlFile.toFile()

	def fromFile (self):
		File.fromFile (self)
		self.clean()
		while self.contain ('\n\n'): self.replace ('\n\n', '\n')
		refFile.fromFile()
		refFile.clean()
		while refFile.contain ('\n\n'): refFile.replace ('\n\n', '\n')
		refFile.replace ('%message%', '%s')
		refFile.replace ('%numext%', '%s')
		refFile.replace ('%numint%', '%s')
		refFile.replace ('%module%', '%s')
		refFile.replace ('%type%', '%s')
		d= refFile.index ('\ntype')
		d= refFile.index ('\n_____', d)
		data = self.fromModel (refFile.text [:d])
		self.message = data [1]
		self.numext = data [2]
		self.numint = data [3]
		self.module = data [4]
		self.type = data [5]

	def toHtml (self):
		from debutils.html import FileHtml
		fhtml = FileHtml()
		fhtml.fromFileName (self.file)

class MantisList (ListFile):
	def __init__ (self):
		ListFile.__init__ (self, 'm/')
	def get (self, TagNomfile=None, sens=True):
		for dirpath, SousListDossiers, subList in os.walk (self.path):
			if not subList: continue
			if TagNomfile and sens:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if TagNomfile not in subList [i] or '.txt' not in subList [i]: trash = subList.pop (i)
			elif TagNomfile:
				range_tag = range (len (subList) -1, -1, -1)
				for i in range_tag:
					if TagNomfile in subList [i] and '.txt' in subList [i]: trash = subList.pop (i)
			if subList:
				for file in subList:
					fileTmp = File (os.path.join (dirpath, file))
					fileTmp.dataFromFile()
					self.append (fileTmp)
		self.sort()
		rangeFile = self.range()
		for f in rangeFile: self [f].fromFile()

	def getByNumext (self, numext):
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