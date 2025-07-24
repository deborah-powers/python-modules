#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileTable
import loggerFct as log
invenspecPath = 'b/fouille-spec\\invenspec cosmose %s.tsv'

class Categorie():
	def __init__(self, symbol, message):
		self.message = message
		self.symbol = symbol
		self.nbFiles =0
		self.files =[]

	def append (self, symbol, fileC):
		if symbol == self.symbol:
			self.files.append (fileC)
			self.nbFiles +=1

	def print (self):
		if self.nbFiles:
			print (self.nbFiles, self.message)
			for nameC in self.files[:40]: print (nameC)

# les fichiers cosmose - forge et cosmose - sharepoint
def compareDates (plateForme):
	categories = [
		Categorie ('=', 'fichiers ont été modifiés en même temps sur cosmose et '+ plateForme),
		Categorie ('~', 'fichiers ont été modifiés le même jour sur cosmose et '+ plateForme),
		Categorie ('<', 'fichiers ont été modifiés sur cosmose avant '+ plateForme),
		Categorie ('>', 'fichiers ont été modifiés sur cosmose après '+ plateForme)
	]
	invenspecFile = FileTable (invenspecPath % plateForme)
	invenspecFile.read()
	invenspecFile.pop (0)
	for nameC, compDate in invenspecFile.list:
		for category in categories: category.append (compDate, nameC)
	for category in categories: category.print()

compareDates ('forge')
compareDates ('sharepoint')

# les fichiers cosmose - forge - sharepoint
categories = [
	Categorie ('~=', 'fichiers ont été modifiés le même jour sur la forge et en même temps sur le sharepoint'),
	Categorie ('>=', 'fichiers ont été modifiés avant sur la forge et en même temps sur le sharepoint'),
	Categorie ('<=', 'fichiers ont été modifiés avant sur la forge et en même temps sur le sharepoint'),
	Categorie ('~~', 'fichiers ont été modifiés le même jour sur les trois plate-formes'),
	Categorie ('<~', 'fichiers ont été modifiés avant sur la forge et le même jour sur le sharepoint'),
	Categorie ('>~', 'fichiers ont été modifiés avant sur la forge et le même jour sur le sharepoint'),
	Categorie ('~>', 'fichiers ont été modifiés le même jour sur la forge et avant sur le sharepoint'),
	Categorie ('<>', 'fichiers ont été modifiés après sur la forge et avant sur le sharepoint'),
	Categorie ('>>', 'fichiers ont été modifiés avant cosmose sur la forge et le sharepoint'),
	Categorie ('~<', 'fichiers ont été modifiés le même jour sur la forge et après sur le sharepoint'),
	Categorie ('<<', 'fichiers ont été modifiés après cosmose sur la forge et le sharepoint'),
	Categorie ('><', 'fichiers ont été modifiés avant sur la forge et après sur le sharepoint')
]
invenspecFile = FileTable (invenspecPath % 'forge sharepoint')
invenspecFile.read()
invenspecFile.pop (0)

for nameC, compDateF, compDateS in invenspecFile.list:
	for category in categories: category.append (compDateF + compDateS, nameC)
for category in categories: category.print()
