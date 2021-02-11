#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileDeb.textClass import Text
from fileDeb.fileClass import FilePerso, Article, help

# on appele ce script dans un autre script
if __name__ != '__main__': pass
elif len (argv) <2: print (help)
elif argv[1] =='tmp':
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
	elif argv[1] =='lis': filePerso.toLiseuse()
	elif argv[1] =='md': filePerso.toMd()
	filePerso.toFile()
elif argv[1] == 'testFile':
	filePerso = FilePerso()
	filePerso.test()
elif argv[1] == 'testArtic':
	filePerso = Article()
	filePerso.test()
# le nom du fichier n'a pas ete donne
else: print (help)