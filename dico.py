#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_1750_mots_fran%C3%A7ais_les_plus_courants
from sys import argv
from debutils.text import wordsEnd
from fileSimple import File
from debutils.list import List
from fileSimple.fileList import FileList, FileTable
# import debutils.logger as logger

suffix =( 'ionnelles', 'ionnelle', 'ionnels', 'ateurs', 'ations', 'ennant', 'ennent', 'ionnel', 'itions', 'trices', 'ables', 'aires', 'amant', 'ament', 'ances', 'aient', 'ation', 'asmes', 'ateur', 'âtres', 'elles', 'ement', 'ences', 'èques', 'esses', 'ettes', 'euses', 'ibles', 'ières', 'iques', 'ismes', 'ition', 'oires', 'teurs', 'tions', 'trice', 'able', 'ages', 'aire', 'ance', 'asme', 'âmes', 'âtre', 'bles', 'eaux', 'elle', 'ence', 'esse', 'èque', 'ères', 'ette', 'eurs', 'euse', 'ible', 'ière', 'iers', 'ions', 'ique', 'isme', 'ités', 'îmes', 'mant', 'ment', 'oire', 'ques', 'sses', 'teur', 'tion', 'age', 'ais', 'ait', 'ant', 'aux', 'ble', 'eau', 'els', 'ent', 'ère', 'eur', 'ées', 'ier', 'ion', 'ité', 'nes', 'ont', 'ons', 'que', 'sse', 'ai', 'al', 'au', 'el', 'er', 'es', 'et', 'ez', 'ée', 'ne', 'a', 'e', 'é', 's', 't', 'x')
prefix = ('dés', 'imm', 'inn', 'mal', 'més', 'pré', 'dé', 'im', 'in', 'mé', 're', 'ré', 'sur')
newPoints = "-'() /_\"\n\t<> [](){}|%#$@=+*°&0123456789"


class FileRef (FileTable):
	def __init__ (self):
		FileTable.__init__ (self, '\n', ' ', 'b/dico.txt')
		self.fromFile()
		while self.length() <3: self.addLine (List())

	def sort (self):
		tmpRange = self.range()
		for l in tmpRange: self[l].sort()

ref = FileRef()

class ListSrc (List):
	def __init__ (self, text):
		List.__init__ (self)
		List.fromText (self, ' ', text)
		self.sort()
		self.rg = self.range()
		self.rg.reverse()

	def delDouble (self):
		for t in self.rg:
			d= self.count (self.list[t])
			if d>1: trash = self.pop (t)
		self.rg = self.range()
		self.rg.reverse()

	def delKnown (self):
		refText = ref.toText (ref.sepLin, ref.sepCol)
		for t in self.rg:
			if self.list[t] in refText: trash = self.pop (t)

class FileSrc (File):
	def __init__ (self, fileName=None):
		File.__init__ (self, fileName)
		if fileName: self.fromFile()

	def clean (self):
		self.text = self.text.lower()
		for p in newPoints: self.replace (p, ' ')
		for p in wordsEnd: self.replace (p, ' ')
		File.clean (self)
		self.text =' '+ self.text +' '
		for ext in suffix: self.replace (ext +' ',' ')
		for ext in prefix: self.replace (' '+ ext,' ')


srcf = FileSrc ('a/romans/quand la terre hurla.txt')
srcf.clean()
srcl = ListSrc (srcf.text)
srcl.delDouble()
srcl.delKnown()
for word in srcl.list: ref.list[2].add (word)
ref.sort()
ref.toFile()



