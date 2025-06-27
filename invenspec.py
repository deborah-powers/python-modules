#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
import os
import win32com.client as wclient
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time
from fileCls import File
import loggerFct as log

# les fichiers
dossierTelechargements = 'C:\\Users\\deborah.powers\\Desktop\\fouille-spec\\telechargements'
fileRes = File ('b/fouille-spec\\invenspec.tsv')
fileRes.text = "titre	nom	date de modification	taille	url	fil d'ariane"
fileError = File ('b/fouille-spec\\erreurs.tsv')
fileError.text = 'url	erreur	url enfant'

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
# options.add_argument ('download.default_directory=' + dossierTelechargements)
prefs ={ 'download.default_directory': dossierTelechargements }
options.add_experimental_option ('prefs', prefs)
driver = webdriver.Chrome (service=service, options=options)

# l'espace de nom, pour récupérer les métadonnées des fichiers
shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
nameSpace = shellApp.NameSpace (dossierTelechargements)

def viderTelechargements():
	fileNames = os.listdir (dossierTelechargements)
	for fileName in fileNames: os.remove (dossierTelechargements + os.sep + fileName)


