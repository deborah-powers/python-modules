#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileHtml import FileHtml
from fileClass import FilePerso

if len (argv) <2: print ('indiquez le numéro de la fiche à convertir au format html')
else:
	numero = argv[1]
	fileName = 'm/mantis %s.txt' % numero
	fhtml = FileHtml()
	fhtml.fromFilePersoName (fileName)
	fsimple = FilePerso (fhtml.file)
	fsimple.fromFile()
	fsimple.clean()
	oldStyle = "\t<link rel='stylesheet' type='text/css' href='C:Usersdeborah.powersDesktophtmlutilsstructure.css'/>\n\t<link rel='stylesheet' type='text/css' href='C:Usersdeborah.powersDesktophtmlutilsperso.css'/>"
	newStyle = "<style type='text/css'>\n\t* {\n\t\tfont-size: 1em;\n\t\tfont-weight: normal;\n\t\ttext-decoration: none;\n\t\tcolor: black;\n\t}\n\th1 {\n\t\tfont-size: 2em;\n\t\tborder-top: double 6px green;\n\t}\n\th2 {\n\t\tfont-size: 1.5em;\n\t\ttext-align: center;\n\t\tcolor: green;\n\t\tborder-top: solid 2px green;\n\t}\n\th1, h2 { margin-top: 2em; }\n</style>"
	fsimple.replace (oldStyle, newStyle)
	fsimple.toFile()