#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
import os
import win32com.client as wclient
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time
from functools import cmp_to_key
from fileCls import File
from fileList import FileTable
import loggerFct as log

# les fichiers
downloadFolder = 'C:\\Users\\deborah.powers\\Desktop\\fouille-spec\\telechargements'
fileRes = File ('b/fouille-spec\\invenspec.tsv')
fileRes.text = "titre	nom	date de modification	taille	url	fil d'ariane"
# fileRes.text = "titre	date de modification	url	fil d'ariane"
fileError = File ('b/fouille-spec\\erreurs.tsv')
fileError.text = 'url	erreur	url enfant'

# lancer le navigateur, ici chrome
def createWebDriver (downloadFolder):
	service = Service()
	options = webdriver.ChromeOptions()
	options.add_argument ('--enable-unsafe-swiftshader')
	options.add_argument ('--ignore-certificate-errors')
	options.add_argument ('--ignore-ssl-errors')
	options.add_argument ('--log-level=3')
	# options.add_argument ('download.default_directory=' + downloadFolder)
	prefs ={ 'download.default_directory': downloadFolder }
	options.add_experimental_option ('prefs', prefs)
	driver = webdriver.Chrome (service=service, options=options)
	return driver

def createFolderNameSpace (downloadFolder):
	# l'espace de nom, pour récupérer les métadonnées des fichiers
	shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
	nameSpace = shellApp.NameSpace (downloadFolder)
	return nameSpace

def emptyingFolder (downloadFolder):
	fileNames = os.listdir (downloadFolder)
	for fileName in fileNames: os.remove (downloadFolder + os.sep + fileName)

def sortIsLines (fileA, fileO):
	if fileA[5] > fileO[5]: return True
	elif fileA[5] < fileO[5]: return False
	elif fileA[4] > fileO[4]: return True
	elif fileA[4] < fileO[4]: return False
	elif fileA[0] > fileO[0]: return True
	elif fileA[0] < fileO[0]: return False
	elif fileA[2] > fileO[2]: return True
	elif fileA[2] < fileO[2]: return False
	elif fileA[1] > fileO[1]: return True
	elif fileA[1] < fileO[1]: return False
	elif fileA[3] > fileO[3]: return True
	elif fileA[3] < fileO[3]: return False
	else: return True

def sortInvenspec (invenspecFile):
#	invenspecFile = FileTable (invenspecFile)
	invenspecFile = FileTable ('b/fouille-spec\\invenspec '+ invenspecFile + '.tsv')
	invenspecFile.read()
	log.message (len (invenspecFile.list))
	header = invenspecFile.list.pop (0)
	invenspecFile.list.sort()
	invenspecRange = invenspecFile.range()
	invenspecRange.reverse()
	nonTelecharges =[]
	for i in invenspecRange:
		if '!! NON téléchargé !!' in invenspecFile.list[i][3]: nonTelecharges.append (invenspecFile.list.pop (i))
	invenspecFile.list.sort (key=cmp_to_key (sortIsLines))
	nonTelecharges.sort (key=cmp_to_key (sortIsLines))
	invenspecFile.list.insert (0, header)
	invenspecFile.list.extend (nonTelecharges)
	invenspecFile.title = invenspecFile.title +' bis'
	invenspecFile.write()
