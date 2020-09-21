#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import stdout
from fileClass import FilePerso

fileNameR = 'b/inversion-recet.txt'
fileNameL = 'b/inversion-local.txt'

def cleanFile (fileName):
	fileObj = FilePerso (fileName)
	fileObj.fromFile()
	fileObj.clean()
	fileObj.replace ('\n', ' ')
	fileObj.replace ('\t', '')
	fileObj.replace ('(', ' (')
	while '  ' in fileObj.text: fileObj.replace ('  ', ' ')
	fileObj.replace ('> ', '>')
	fileObj.replace (' <', '<')
	fileObj.replace ('( ', '(')
	fileObj.replace (' )', ')')
	fileObj.replace ('"', "'")
	fileObj.replace ('><', '>\n<')
	fileObj.replace ('$ ( ', '$(')
	"""
	fileObj.replace ('; ', ';\n')
	fileObj.title = fileObj.title + '-2'
	fileObj.fileFromData()
	print (fileObj)
	fileObj.toFile()
	"""
	return fileObj

fileR = cleanFile (fileNameR)
fileL = cleanFile (fileNameL)

"""
fileCommon = FilePerso ('b/comparison.txt')
fileCommon.dataFromFile()
fileCommon.text = fileL.comparLines (fileR, False, True)
fileCommon.toFile()
"""







