#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileCls import File

help ="""
nettoyer les fichiers de web catalogue

utilisation:
python cleanBnf.py type chemin/et/nom/du/fichier

les valeurs de type: jsp, js, css, action, java
"""

pathRoot = '/home/ent6904919/git/catalogue/WebCatalogueGeneralWeb/src/main/'
pathJsp = pathRoot + 'webapp/jsp/'
pathCss = pathRoot + 'webapp/styles/'
pathJs = pathRoot + 'webapp/js/'
pathJava = pathRoot + 'java/fr/bnf/catalogue/'
pathAction = pathJava + 'cca/web/action/'

def cleanCode (self):
	self.text = self.text.strip()
	self.text = self.text.replace ('\r', "")
	while '  ' in self.text: self.text = self.text.replace ('  ', ' ')
	self.text = self.text.replace ('\n ', '\n')
	self.text = self.text.replace (' \n', '\n')
	self.text = self.text.replace ('\t ', '\t')
	self.text = self.text.replace (' \t', '\t')
	if self.path[-4:] == '.jsp':
		while '\t\t' in self.text: self.text = self.text.replace ('\t\t', '\t')
		self.text = self.text.replace ('\t\n', '\n')
	while '\t\n' in self.text: self.text = self.text.replace ('\t\n', '\n')
	while '\n\n' in self.text: self.text = self.text.replace ('\n\n', '\n')
	if self.path[-4:] == '.jsp':
		self.text = self.text.replace ('>\n<', '><')
		self.text = self.text.replace ('%><', '%>\n<')
		self.text = self.text.replace ('><%', '>\n<%')
		self.text = self.text.replace ('><!--', '>\n<!--')
		self.text = self.text.replace ('--><', '-->\n<')

setattr (File, 'cleanBnf', cleanCode)

if len (argv) <3: print (help)
else:
	fileName =""
	if argv[1] == 'jsp': fileName = pathJsp + argv[2] + '.jsp'
	elif argv[1] == 'js': fileName = pathJs + argv[2] + '.js'
	elif argv[1] == 'css': fileName = pathCss + argv[2] + '.css'
	elif argv[1] == 'action': fileName = pathAction + argv[2] + '.java'
	elif argv[1] == 'java': fileName = pathJava + argv[2] + '.java'
	else: fileName = pathRoot + argv[2]
	fileCode = File (fileName)
	fileCode.read()
	fileCode.cleanBnf()
	fileCode.write()


