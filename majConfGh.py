#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileCls import File

newToken = 'mauvais token'
if len (argv) <2: print ('entrez le token')
else:
	newToken = argv[1]
	lenToken = len (argv[1])
	if newToken[:4] == 'ghp_' and lenToken !=40: newToken = 'mauvais token'
	elif newToken[:4] != 'ghp_':
		if lenToken ==36: newToken = 'ghp_' + newToken
		else: newToken = 'mauvais token'

fileNamePython = 'b/python'
fileNameWebext = 'b/webext'
fileNameHtml = 'C:\\wamp64\\www\\html'
fileNameSite = 'C:\\wamp64\\www\\site-dp'

class FileConfigGithub (File):
	def __init__ (self, path):
		File.__init__ (self, path + '\\.git\\config')
		self.remplaceToken (newToken)

	def remplaceToken (self, newToken):
		self.read()
		d= self.text.find ('ghp_')
		f= self.text.find ('@github.com')
		self.text = self.text[:d] + newToken + self.text[f:]
		self.write()

if newToken == 'mauvais token': print ('mauvais token')
else:
	fileWebext = FileConfigGithub (fileNameWebext)
	filePython = FileConfigGithub (fileNamePython)
	fileHtml = FileConfigGithub (fileNameHtml)
	fileSite = FileConfigGithub (fileNameSite)
