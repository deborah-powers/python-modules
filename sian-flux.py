#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
from folderCls import Folder

folderFlux = Folder ('b/rnpp flux')
print (folderFlux.path)

def nettoyerFlux (self):
	self.replace ('\t', " ")
	self.replace ('\n', " ")
	while "  " in self.text: self.replace ("  "," ")
	self.replace (" <", '\n<')
	self.replace ('\n</', '</')
	self.replace ('></', '>\n</')

Setattr (File, 'nettoyerFlux', nettoyerFlux)

def renommerNvFlux():
	folderFlux.get ('flux_pass')
#	folderFlux.get ('recapPDF')
	folderFlux.read()
	for flux in folderFlux:
		flux.title = "rnpp o "+ flux.path[28:-9] +" flux"
		flux.path = folderFlux.path +'\t.xml'
		flux.nettoyerFlux()
	folderFlux.write()

def nettoyerFluxList():
	folderFlux.get ('flux.xml')
	folderFlux.read()
	for flux in folderFlux: flux.nettoyerFlux()
	folderFlux.write()

renommerNvFlux()