#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium avec python
sources:
	https://pypi.org/project/selenium/
	https://www.selenium.dev/selenium/docs/api/py/
"""
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time

urlTest = 'https://forgeaxyus.local.axyus.com/plugins/docman/?group_id=171&action=show&id=6080'

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

assert 'forge' in driver.title
# assert 'ocumentation' in driver.title

fieldName = driver.find_element (By.NAME, 'form_loginname')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'form_pw')
fieldPwd.send_keys ('LmUFhiYhoub8!')
buttonSend = driver.find_element (By.NAME, 'login')
buttonSend.click()
# buttonSend.summit()

# assert 'ocumentation' in driver.title
print (driver)
