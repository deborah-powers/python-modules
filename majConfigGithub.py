#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

newToken = 'ghp_rototo'

fileNamePython = 'b/python'
fileNameWebext = 'b/webext'
fileNameHtml = 'b/html'
fileNameSite = 'b/site-dp'

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

fileWebext = FileConfigGithub (fileNameWebext)
filePython = FileConfigGithub (fileNamePython)
fileHtml = FileConfigGithub (fileNameHtml)
fileSite = FileConfigGithub (fileNameSite)
