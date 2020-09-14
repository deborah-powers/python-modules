#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import codecs
from textClass import Text

help ="""traiter des fichiers
utilisation
	le script est appelable dans un fichier
	python3 fileClass.py tag fichier (fichierB)
les valeurs de tag
	maj: rajouter les majuscules dans un texte
	mef: mettre en forme un texte utilisant ma mise en forme spécifique
	cpr: comparer deux fichiers ligne à ligne
"""

""" ____________________________________ quelques raccourci ____________________________________

faciliter l'ecriture des noms de files lorsque l'on utilise l'un des scripts dependant de celui-ci
vous pouvez rajouter vos propres racourcis
"""
extensions = 'txt html xml svg tsv csv json js py jpeg jpg png bmp gif pdf mp3 mp4 waw vlc'
pathDesktop = 'C:\\Users\\deborah.powers\\Desktop\\'
pathProject = 'C:\\dev\\synergie\\GIT\\'

dictShortcut ={
	'b/': pathDesktop,
	'a/': pathDesktop + 'articles\\',
	'h/': pathDesktop + 'html\\',
	'm/': pathDesktop + 'mantis\\',
	'd/': pathDesktop + 'dtt local\\',
	'u/': pathDesktop + 'bdd-dump\\',
	'p/': pathProject
}
def encodingList():
	import encodings
	from tableClass import ListPerso
	encodList = ListPerso()
	encodList.extend (encodings.aliases.aliases.values())
	encodList.delDuplicates()
	return encodList

def shortcut (path):
	if pathDesktop in path or pathProject in path: return path
	elif path[:2] in dictShortcut.keys():
		path = path.replace (path[:2], dictShortcut [path[:2]])
	else: print ('chemin inconnu:', path)
	return path

class FilePerso (Text):
	def __init__(self, file =None):
		Text.__init__(self)
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

	def __str__ (self):
		strShow = 'Titre: %s\tDossier: %s' %( self.title, self.path)
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
		self.shortcut()
		if os.sep not in self.file or '.' not in self.file:
			print ('fichier malformé:\n' + self.file)
			return
		posS = self.file.rfind (os.sep) +1
		posE = self.file.rfind ('.')
		self.path = self.file[:posS]
		self.title = self.file[posS:posE]
		self.extension = self.file[posE+1:]
		if self.extension not in extensions:
			print ('entension inconnue', self.extension, '\t', self.file)
			return

	""" ________________________ utiliser un fichier ________________________ """

	def fromFile (self):
		self.shortcut()
		if not os.path.exists (self.file): return
		self.dataFromFile()
		# ouvrir le file et recuperer le texte au format str
		"""
		textBrut = open (self.file, 'r')
		self.text = textBrut.read()
		"""
		textBrut = open (self.file, 'rb')
		tmpByte = textBrut.read()
		encodingList =('utf-8', 'ISO-8859-1', 'ascii')
		for encoding in encodingList:
			try: self.text = codecs.decode (tmpByte, encoding=encoding)
			except UnicodeDecodeError: pass
			else: break
		"""
			else: print (encoding); break;
		self.text = codecs.decode (tmpByte, encoding='utf-8')
		"""
		textBrut.close()
		FilePerso.clean (self)

	def toFile (self, mode='w'):
		self.fileFromData()
		# pas de texte
		if not self.text:
			print ('rien a ecrire pour:', self.title)
			return
		chars = '/\\\t\n'; c=0
		while chars != 'error' and c<4:
			if chars[c] in self.title:
				print ('le fichier est mal formé:', self.title)
				chars = 'error'
			c+=1
		if chars != 'error':
			if mode == 'a' and os.path.isfile (self.file): self.text ='\n'+ self.text
			# ouvrir le fichier et ecrire le texte
			textBrut = open (self.file, mode)
			textBrut.write (self.text)
			textBrut.close()

	def compare (self, otherFile, method='lines'):
		self.fromFile()
		otherFile.fromFile()
		textFinal =""
		if method == 'lsort': textFinal = Text.comparLines (self, otherFile, True)
	#	elif method == 'score': textFinal = Text.comparScore (self, otherFile)
		else: textFinal = Text.comparLines (self, otherFile)
		if textFinal != 'pareil' and textFinal != 'different':
			fileFinal = FilePerso ('b/compare %s - %s.txt' % (self.title, otherFile.title))
			fileFinal.dataFromFile()
			print ('voir', fileFinal.title)
			fileFinal.text = textFinal
			fileFinal.toFile()

	def test (self):
		self.title = 'tester FilePerso'
		self.fileFromData()
		self.text = '________________________________________________________________________\nje suis un message test\nsur plusieurs lignes.\nune liste:\n\ta,\n\tb,\n\tc.'
		print (self)
		print (self.text)
		print ('écrire le fichier')
		self.toFile()
		print ('récupérer le fichier')
		self.fromFile()
		print ('modifier le fichier')
		self.shape()
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

class Article (FilePerso):
	# classe pour les fichiers txt
	def __init__(self, file =None):
		FilePerso.__init__(self, file)
		self.author =""
		self.subject =""
		self.link =""
		self.autlink =""

	def copyFile (self, newFile):
		FilePerso.copyFile (self, newFile)
		self.author = newFile.author
		self.subject = newFile.subject
		self.link = newFile.link
		self.autlink = newFile.autlink

	def fromFile (self):
		FilePerso.fromFile (self)
		metadata = self.fromModel (modelText)
		self.subject = metadata[0]
		self.author = metadata[1]
		self.link = metadata[2]
		self.autlink = metadata[3]
		self.text = metadata[4]

	def toFile (self, mode='w'):
		text = modelText %( self.subject, self.author, self.link, self.autlink, self.text)
		self.text = text
		FilePerso.toFile (self, mode)

	def __str__ (self):
		strShow = 'Titre: %s\tDossier: %s\nSujet: %s\tAuteur: %s' %( self.title, self.path, self.subject, self.author)
		if self.text: strShow += '\n\t%d caractères' % len (self.text)
		return strShow

	def __lt__ (self, newFile):
		""" nécessaire pour trier les listes """
		struct = '%s\t%s\t%s'
		return struct %( self.subject, self.author, self.title) < struct %( newFile.subject, newFile.author, newFile.title)

	def test (self):
		self.title = 'tester Article'
		self.author = 'deborah powers'
		self.subject = 'test'
		self.link = 'http://deborah-powers.fr/doudou'
		self.autlink = 'http://deborah-powers.fr/'
		self.fileFromData()
		self.text = '________________________________________________________________________\nje suis un message test\nsur plusieurs lignes.\nune liste:\n\ta,\n\tb,\n\tc.'
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
		self.replace ('$ ','\n')
		self.toFile()

# on appele ce script dans un autre script
if __name__ != '__main__': pass
elif len (argv) >=2 and argv[1] =='tmp':
	fileTxt = Article()
	fileTxt.tmp()
elif len (argv) ==4 and argv[1][:3] == 'cpr':
	fpA = FilePerso (argv[2])
	fpB = FilePerso (argv[3])
	if argv[1] == 'cprs': fpA.compare (fpB, 'lsort')
	else: fpA.compare (fpB)
elif len (argv) ==3:
	filePerso = FilePerso (argv[2])
	filePerso.fromFile()
	if argv[1] =='maj': filePerso.clean()
	elif argv[1] =='mef': filePerso.shape()
	filePerso.toFile()
elif argv[1] == 'testFile':
	filePerso = FilePerso()
	filePerso.test()
elif argv[1] == 'testArtic':
	filePerso = Article()
	filePerso.test()
# le nom du fichier n'a pas ete donne
else: print (help)



