#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires
from fileClass import FilePerso
from textClass import Text
from listFile import ListFile

def tmp (file):
	file.clean()
	file.shape()

flist = ListFile ('a/romans/')
flist.get ('.txt')
flist.modify (Text.clean)
for file in flist: print (file.title)



def launchApp():
	# lancer mon lecteur vidéo, totem
	import os
	pathFile = 'papi.wav'
	pathTotem = '/usr/bin/totem'
	cmdTotem = '%s --play %s' %( pathTotem, pathFile)
	pathVlc = '/snap/bin/vlc'
	cmdVlc = '%s %s' %( pathVlc, pathFile)
	os.system (cmdVlc)

dirA = 'C:\\Users\\deborah.powers\\Desktop\\html\\'
dirB = 'C:\\Users\\deborah.powers\\Desktop\\html vb\\'

def changeCss():
	fllst = FileList ('b/localhost/site-dp/')
	fllst.get ('.html')
	fllst.replace ('library-js/debby-play/debbyPlay.css', 'library-css/debbyPlay.css')
	fllst.replace ('library-js/debby-play/debbyPlay.js', 'library-js/debbyPlay.js')

