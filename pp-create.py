#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
from shutil import copyfile
from fileDeb.fileLocal import *
import fileDeb.fileClass as fc

pathPython = pathRoot + 'python' + os.sep
# les templates

templateInit ="""#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""

templateSetup ="""%s
from setuptools import setup, find_packages

author = 'deborah noisetier'
name = '%s'
description = "%s"
version = '0.1'

setup (
	name = name, version = version, description = description,
	author = author,
	packages = find_packages()
)
"""

folderName =""
name =""
description =""
nbArg = len (argv)

if nbArg <2: print ('entrez le nom du dossier, le nom et la description du package')
else:
	folderName = argv[1]
	if nbArg <3: name = argv[1]
	else:
		name = argv[2]
		if nbArg >3: description = argv[3]

	# créer les dossiers
	if folderName[-1] != os.sep: folderName = folderName + os.sep
	fc.createFolder (pathPython + folderName)
	fc.createFolder (pathPython + folderName + folderName)

	tmpFile = fc.FilePerso()
	# créer les fichiers
	tmpFile.path = pathPython + folderName + folderName
	tmpFile.title = '__init__'
	tmpFile.extension = 'py'
	tmpFile.fileFromData()
	tmpFile.text = templateInit
	tmpFile.toFile()

	tmpFile.path = pathPython + folderName
	tmpFile.title = 'setup'
	tmpFile.fileFromData()
	tmpFile.text = templateSetup %( templateInit, name, description)
	tmpFile.toFile()

	tmpFile.title = 'readme'
	tmpFile.extension = 'txt'
	tmpFile.fileFromData()
	tmpFile.text = '______ utilisation ______'
	tmpFile.toFile()

