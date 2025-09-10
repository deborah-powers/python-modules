#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium avec python
sources:
	https://datascientest.com/selenium-python-web-scraping
	https://pypi.org/project/selenium/
	https://www.selenium.dev/selenium/docs/api/py/
	https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
"""
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time

myurl = 'http://www.my-url.com'

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
# télécharger les fichiers dans un dossier spécifique
# options.add_argument ('download.default_directory=' + dossierTelechargements)
prefs ={ 'download.default_directory': dossierTelechargements, 'profile.default_content_setting_values.clipboard': 1 }
options.add_experimental_option ('prefs', prefs)
driver = webdriver.Chrome (service=service, options=options)

# charger ma page dans le navigateur
driver.get (myurl)

# remplir et valider le formulaire de login. le get me redirige automatiquement vers une page de login
fieldName = driver.find_element (By.NAME, 'login-name')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'login-pwd')
fieldPwd.send_keys ('noisette416')
buttonSend = driver.find_element (By.NAME, 'login-button')
buttonSend.submit()	# input type='button', type='submit'
buttonSend.click()	# button, anchor
# après la validation, rediriger vers ma page. elle est affichée
driver.get (myurl)
# laisser une seconde pour que ma page se charge
time.sleep (1)

# reffuser les cookies
try:
	cookiesReffuser = driver.find_element (By.ID, 'cookies-reffuser')
	cookiesReffuser.click()	# méthode 1
	driver.execute_script ('arguments[0].click();', cookiesReffuser)	# méthode 2
	time.sleep (1)
except exceptions.NoSuchElementException: print ('les cookies ont déjà été validés')

# recupérer des éléments
gotById = driver.find_element (By.ID, 'valeur')
gotByClass = driver.find_element (By.CLASS_NAME, 'valeur')
gotByTag = driver.find_element (By.TAG_NAME, 'valeur')
gotByInputName = driver.find_element (By.NAME, 'valeur')
gotByXpath = driver.find_element (By.XPATH, '//p[@class="valeur"]/strong[1]')
gotFromElement = gotById.find_element (By.CLASS_NAME, 'valeur')
gotList = driver.find_elements (By.CLASS_NAME, 'valeur')
directChildren = gotById.find_elements (By.XPATH, './*')
allDescents = gotById.find_elements (By.XPATH, './/*')
someDescents = gotById.find_elements (By.XPATH, './/img[".jpg"=substring(@src, string-length(@src) -4)]')

# récupérer les propriétés des éléments
innerText = gotById.text
domAttribute = anchorElement.get_dom_attribute ('href')
customAttribute = gotById.get_attribute ('perso')

# scroller
def scroll (value):
	rangeMicroScroll =( 0,1,2,3,4,5,6,7,8,9 )	# nombre de micro-scroll à effectuer
	for i in rangeMicroScroll:
		driver.execute_script ('window.scrollBy (0, %d)' % value)
		time.sleep (0.1)	# Temps entre chaque scroll

scroll (300)	# scroll automatique vers le bas
scroll (-200)	# scroll automatique vers le haut

# revenir en arrière
driver.get (myurl)
content = driver.find_element (By.CLASS_NAME, 'toto')
# actions
# l'élément content est perdu
driver.get (myurlBis)
# actions
# la page est rechargée. récupérer l'élément content
driver.back()
driver.execute_script ('window.history.go(-1)')
content = driver.find_element (By.CLASS_NAME, 'toto')

""" options du navigateur chrome qui ne me servent pas
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--log-level=3')
options.add_argument ('--accept_insecure_certs')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-certificate-errors-spki-list')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--disable-gpu')
options.add_argument ('--mute-audio')
options.add_argument ('--disable-infobars')
options.add_argument ('--no-sandbox')
options.add_argument ('--no-zygote')
options.add_argument ('--allow-running-insecure-content')
options.add_argument ('--disable-web-security')
options.add_argument ('--disable-features=VizDisplayCompositor')
options.add_argument ('--disable-breakpad')
"""
