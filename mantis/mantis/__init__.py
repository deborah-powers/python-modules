#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from fileSimple import File
from listFiles import ListFile
from fileHtml import FileHtml
import debutils.logger as log

types = ('ano', 'ddt', 'evo', 'ana', 'rcsf')
modules ={
	'cdm': ('cdm', 'gd', 'ac'),
	'sif': ('aec', 'sif', 'can'),
	'edi': ('edi', 'ord')
}
refPath = 'C:\\Users\\deborah.powers\\python\\mantis\\mantis\\'
refName = refPath + 'mantis-base.txt'
refFile = File (refName)
refSqlCdm = refPath + '01_CDM_DDT-00000_xxx.sql'
refSqlSif = refPath + '01_SIF_DDT-00000_xxx.sql'
refSqlCdmRcsf = refPath + '01_CDM_DDT-00000_reprise_csf.sql'
refSqlSifRcsf = refPath + '01_SIF_DDT-00000_suppression_csf.sql'

class Mantis():
	def __init__ (self, numext ='0', message ='?', module = '?', numint ='0', type ='ano'):
		self.message = message
		self.numext = numext
		self.module = module
		self.projet =""
		for pj in modules.keys():
			for md in modules[pj]:
				if md in module: self.projet = self.projet +', '+pj
		if self.projet: self.projet = self.projet[2:]
		else: self.projet = '?'
		self.numint = numint
		self.type = 'ano'
		if type in types: self.type = type
		elif 'ddt' in message.lower(): self.type = 'ddt'
		if module == 'rcsf':
			self.projet = 'cdm, sif'
			self.type = 'ddt'

	def __lt__ (self, newMantis):
		string = '%s %s'
		return string % (self.module, self.numext) < string % (newMantis.module, newMantis.numext)
	def __str__ (self):
		message = '%s - %s: %s\ttype: %s\tmodule: %s' % (self.numext, self.numint, self.message, self.type, self.module)
		return message

class MantisFile (Mantis, File):
	def __init__ (self, numext ='0', message ='?', module = '?', numint ='0', type ='ano'):
		Mantis.__init__ (self, numext, message, module, numint, type)
		File.__init__ (self, 'b/'+ self.type +' '+ numext + '.txt')

	def createFile (self):
		refFile.fromFile()
		strNum = str (self.numext)
		while len (strNum) <4: strNum = '0'+ strNum
		self.message = '000'+ strNum +': '+ self.message
		refFile.replace ('%message%', self.message)
		refFile.replace ('%numext%', self.numext)
		refFile.replace ('%numint%', self.numint)
		refFile.replace ('%projet%', self.projet)
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
		dateStr = '%02d/%02d' % (date.month, date.day)
		refFile.replace ('%date%', dateStr)
		refFile.file = self.file
		refFile.dataFromFile()
		refFile.replace (' ______\n', ' ______\n\n')
		refFile.toFile()
		if self.type == 'ddt':
			if 'cdm' in self.projet: self.createDdt (date, 'cdm')
			if 'sif' in self.projet: self.createDdt (date, 'sif')

	def createDdt (self, dtime, module='cdm'):
		sqlFile = File()
		if module == 'sif':
			if self.module == 'rcsf': sqlFile.file = refSqlSifRcsf
			else: sqlFile.file = refSqlSif
		elif module == 'cdm':
			if self.module == 'rcsf': sqlFile.file = refSqlCdmRcsf
			else: sqlFile.file = refSqlCdm
		sqlFile.dataFromFile()
		sqlFile.fromFile()
		sqlFile.replace ('%numero%', self.numext)
		dateStr = '%02d/%02d/%02d' % (dtime.day, dtime.month, dtime.year)
		sqlFile.replace ('%date%', dateStr)
		sqlFile.path = self.path
		sqlFile.title = sqlFile.title.replace ('00000', self.numext)
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

	def fromHtml (self, fhtml):
		# self.file est un fichier téléchargé de https://mantis2.axyus.com/view.php?id=3165
		self.file = fhtml
		File.fromFile (self)
		# le message
		d= self.index ('<title')
		d= self.index ('>',d) +1
		f= self.index ('</title>')
		self.message = self.text[d:f]
		d= self.message.find (': ')
		self.numext = self.message[:d]
		self.numext = self.numext.lstrip ('0')
		self.message = self.text[d+2:]
		# le module
		d= self.index ('<th>Sous-module</th>')
		d= self.index ('- ', d)+2
		f= self.index ('-', d)
		self.module = self.text[d:f].lower()
		# la livraison
		d= self.index ('<th>Version ciblée</th>')
		d= self.index ('<td>', d)+4
		f= self.index ('</td>', d)
		livraison = self.text[d:f]
		log.coucou()
		# les images
		images = self.text.split ('<img src=')
		trash = images.pop (0)
		trash = images.pop (-1)
		rangeImg = range (len (images))
		for i in rangeImg:
			f= images[i].find ('>') -1
			d= images[i][:f].rfind ('/') +1
			images[i] = images[i][d:f]
		textImg =""
		if images:
			textImg = '	'.join (images)
			textImg = 'images:	'+ textImg
		# créer le fichier
		self.createFile()
		if livraison: refFile.replace ('nom-liv', livraison)
		if textImg: refFile.replace ('====== infos ======', '====== infos ======\n\n' + textImg)
		if livraison or textImg: refFile.toFile()

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