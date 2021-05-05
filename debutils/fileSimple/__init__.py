#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import codecs
from debutils.text import Text
from fileSimple.fileLocal import *
extensions = 'txt log css html xml svg md tsv csv json js py sql jpeg jpg png bmp gif pdf mp3 mp4 wav vlc avi mpg srt mkv divx ass AVI torrent Divx flv wma m4a MP3 TMP tmp mht'

def createFolder (folder):
	if not os.path.exists (folder): os.mkdir (folder)

def encodingList():
	import encodings
	from tableClass import List
	encodList = List()
	encodList.extend (encodings.aliases.aliases.values())
	encodList.delDuplicates()
	return encodList

class File (Text):
	def __init__ (self, file =None):
		Text.__init__ (self)
		self.file = file
		self.title =""
		self.extension = 'txt'
		self.path = pathDesktop
		if file:
			self.shortcut()
			self.dataFromFile()

	def copyFile (self, newFile):
		self.file = newFile.file
		self.title = newFile.title
		self.text = newFile.text
		self.path = newFile.path
		self.extension = newFile.extension

	def __str__ (self):
		strShow = 'Titre: %s\tDossier: %s' % (self.title, self.path)
		if self.text: strShow += '\n\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		return self.title < newFile.title

	def shortcut (self):
		self.file = shortcut (self.file)
		self.path = shortcut (self.path)

	def fileFromData (self):
		self.file = self.path + self.title +'.'+ self.extension
		self.shortcut()

	def dataFromFile (self):
		self.file = shortcut (self.file)
		if os.sep not in self.file or '.' not in self.file:
			print ('fichier malformé:\n' + self.file)
			return
		elif self.file.rfind (os.sep) > self.file.rfind ('.'):
			print ('fichier malformé:\n' + self.file)
			return
		posS = self.file.rfind (os.sep) +1
		posE = self.file.rfind ('.')
		self.path = self.file [:posS]
		self.title = self.file [posS:posE]
		self.extension = self.file [posE+1:]
		if self.extension not in extensions:
			print ('entension inconnue', self.extension, '\t', self.file)

	""" ________________________ utiliser un fichier ________________________ """

	def fromFile (self):
		self.file = shortcut (self.file)
		if not os.path.exists (self.file): return
		self.dataFromFile()
		# ouvrir le file et recuperer le texte au format str
		"""
		textBrut = open (self.file, 'r')
		self.text = textBrut.read()
		"""
		textBrut = open (self.file, 'rb')
		tmpByte = textBrut.read()
		encodingList = ('utf-8', 'ascii', 'ISO-8859-1')
		for encoding in encodingList:
			try: self.text = codecs.decode (tmpByte, encoding=encoding)
			except UnicodeDecodeError: pass
			else: break
		"""
			else: print (encoding); break;
		self.text = codecs.decode (tmpByte, encoding='utf-8')
		"""
		textBrut.close()
	#	File.clean (self)

	def toFile (self, mode='w'):
		# pas de texte
		if not self.text:
			print ('rien a ecrire pour:', self.title)
			return
		self.fileFromData()
		chars = '/\\\t\n'; c=0
		while chars != 'error' and c<4:
			if chars [c] in self.title:
				print ('le fichier est mal formé:', self.title [:100])
				print (c, chars[c])
				chars = 'error'
			c+=1
		if chars != 'error':
			if mode == 'a' and os.path.isfile (self.file): self.text ='\n'+ self.text
			# ouvrir le fichier et ecrire le texte
			textBrut = open (self.file, mode +'b')
			textBrut.write (self.text.encode ('utf-8'))
			textBrut.close()

	""" ________________________ comparer deux fichiers ________________________ """

	def compareGroom (self):
		self.fromFile()
		self.text = self.text.lower()
		self.clean()

	def compareGroomSql (self):
		self.replace ('\t')
		self.clean()
		self.replace (', ', ', n')
		self.replace (', ', ', n')
		self.replace (' from', 'nfrom')
		self.replace (' where', 'nwhere')
		self.replace (' select', 'nselect')
		self.replace (' union', 'nunion')
		self.replace (' group by', 'ngroup by')
		self.replace (' order by', 'norder by')
		self.replace ('-- ', '\n')
		while self.contain ('\n\n'): self.replace ('\n\n', '\n')

	def compare (self, otherFile, method='lines'):
		self.compareGroom()
		otherFile.compareGroom()
		if self.extension == 'sql':
			self.compareGroomSql()
			otherFile.compareGroomSql()
		textFinal =""
		if method == 'lsort': textFinal = Text.comparLines (self, otherFile, False, True)
		elif method == 'lsortKeep': textFinal = Text.comparLines (self, otherFile, True, True)
		elif method == 'linesKeep': textFinal = Text.comparLines (self, otherFile, True, False)
	#	elif method == 'score': textFinal = Text.comparScore (self, otherFile)
		else: textFinal = Text.comparLines (self, otherFile, False, False)
		if textFinal != 'pareil' and textFinal != 'different':
			titleFinal = 'compare '
			if self.title == otherFile.title: titleFinal = titleFinal + self.title
			else:
				lenA = len (self.title)
				lenB = len (otherFile.title)
				t=0
				while t< lenA and t< lenB:
					if self.title [t] == otherFile [t]: titleFinal = titleFinal + self.title [t]
					else: t= lenA +10
					t+=1
				if len (titleFinal) <12: titleFinal = 'compare '+ self.title +' - '+ otherFile.title
			fileFinal = File ('b/'+ titleFinal +'.txt')
			fileFinal.dataFromFile()
			print ('voir', fileFinal.title)
			fileFinal.text = textFinal
			fileFinal.toFile()

	def test (self):
		self.title = 'tester File'
		self.fileFromData()
		self.text = '________________________________________________________________________\nje suis un message test\nsur plusieurs lignes.\nune liste:\nta, ntb, ntc.'
		print (self)
		print (self.text)
		print ('écrire le fichier')
		self.toFile()
		print ('récupérer le fichier')
		self.fromFile()
		print ('modifier le fichier')
		self.clean()
		print (self.text)
		print ('écrire le fichier')
		self.text = 'je suis une ligne rajoutée.'
		self.toFile ('a')
		self.fromFile()
		print (self.text)


modelText ="""Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""
class Article (File):
	# classe pour les fichiers txt
	def __init__ (self, file =None):
		File.__init__ (self, file)
		self.author =""
		self.subject =""
		self.link =""
		self.autlink =""

	def copyFile (self, newFile):
		File.copyFile (self, newFile)
		self.author = newFile.author
		self.subject = newFile.subject
		self.link = newFile.link
		self.autlink = newFile.autlink

	def fromFile (self):
		File.fromFile (self)
		metadata = self.fromModel (modelText)
		self.subject = metadata [0]
		self.author = metadata [1]
		self.link = metadata [2]
		self.autlink = metadata [3]
		self.text = metadata [4]

	def toFile (self, mode='w'):
		# self.replace ('\n', '\n\n')
		text = modelText % (self.subject, self.author, self.link, self.autlink, self.text)
		self.text = text
		File.toFile (self, mode)

	def __str__ (self):
		strShow = 'Titre: %s\tDossier: %s\nSujet: %s\tAuteur: %s' % (self.title, self.path, self.subject, self.author)
		if self.text: strShow += '\n\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		struct = '%st%st%s'
		return struct % (self.subject, self.author, self.title) < struct % (newFile.subject, newFile.author, newFile.title)

	def test (self):
		self.title = 'tester Article'
		self.author = 'deborah powers'
		self.subject = 'test'
		self.link = 'http://deborah-powers.fr/doudou'
		self.autlink = 'http://deborah-powers.fr/'
		self.fileFromData()
		self.text = '________________________________________________________________________nje suis un message testnsur plusieurs lignes.nune liste:nta, ntb, ntc.'
		self.toFile()
		self.fromFile()
		print (self)

	def tmp (self):
		self.file = 'b/tmp.txt'
		self.dataFromFile()
		self.shortcut()
		self.fromFile()
		self.clean()
		self.replace ('\n')
		self.replace ('\t')
		self.replace ('> <', '><')
		self.replace ('><', '>\n<')
		self.replace ('>\n</p>', '></p>')
		self.replace ('$ ', '\n')
		self.toFile()