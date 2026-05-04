#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium et axe-core avec python
source: https://github.com/axe-selenium-python/axe-selenium-python
"""
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
from axe_selenium_python import Axe
import time
import warnings
warnings.filterwarnings("ignore")

urlTest = 'https://www.marseille.fr/'

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
driver = webdriver.Chrome (service=service, options=options)

# me connecter à l'url
driver.get (urlTest)
# faire une pause le temps de voir la page
time.sleep (1)

# reffuser les cookies
try:
	cookiesReffuser =  driver.find_element (By.ID, 'tarteaucitronAllDenied2')
	driver.execute_script ('arguments[0].click();', cookiesReffuser);
	time.sleep (1)
except exceptions.NoSuchElementException:
	print ('les cookies ont déjà été validés')

# lancer axe-core
axe = Axe (driver)
axe.inject()
results = axe.run()
axe.write_results (results, 'selenium-python-accessibilitie-rapport.json')
driver.close()

assert len (results['violations']) == 0, axe.report (results['violations'])
