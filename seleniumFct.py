#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
# télécharger les fichiers dans un dossier spécifique
# options.add_argument ('download.default_directory=' + dossierTelechargements)
# prefs ={ 'download.default_directory': dossierTelechargements }
# options.add_experimental_option ('prefs', prefs)
driver = webdriver.Chrome (service=service, options=options)

# appeler: from seleniumFct import driver, time