#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires

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

