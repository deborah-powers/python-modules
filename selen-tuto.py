#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium avec python
source: https://datascientest.com/selenium-python-web-scraping
"""
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
# imports du tuto
from datetime import datetime, timedelta
import math
import time
import warnings
warnings.filterwarnings("ignore")
import loggerFct as log

# méthode pour utiliser une string template utilisant des paramètres nommés
urlRef = 'https://www.euronews.com/%(year)d/%(month)02d/%(day)02d'
urlFull = urlRef % { 'year': 2025, 'month': 1, 'day': 6, 'page': 2 }
log.logLst ('url à tester:', urlFull)

service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')

driver = webdriver.Chrome (service=service, options=options)

time.sleep (1)	# tuto. besoin d'un délai
driver.get(urlFull)
time.sleep (1)

# accepter automatiquement les cookies
# a. reprérer la boîte à cookies d'euronew par son id
accept_cookies =  driver.find_element (By.ID, 'didomi-notice-agree-button')
# b. cliquer dessus
driver.execute_script ('arguments[0].click();', accept_cookies);

# scroller
def scroll (value):
	for i in range (20): #nombre de micro-scroll à effectuer
		driver.execute_script ('window.scrollBy (0, %d)' % value)
		time.sleep (0.1) #Temps entre chaque scroll

scroll (300) #Scroll automatique vers le bas
scroll (-200) #Scroll automatique vers le haut

# récupérer les articles
nbArticles = driver.find_element (By.XPATH, '//p[@class="c-block-listing__results"]/strong[1]').text
log.logLst ('il y a', nbArticles, 'articles')
nbPages = int (nbArticles) /30	# 30 articles par pages
nbPages = math.ceil (nbPages) # arrondir à l'entier supérieur
rgPages = range (1, nbPages +1)
urlFull = urlFull + '?p=%d'
articleLinks =[]
for p in rgPages:
	driver.get (urlFull % p)
	articleTags = driver.find_elements (By.CLASS_NAME, 'm-object__title__link')
	for article in articleTags: articleLinks.append (article.get_attribute ('href'))

log.logLst ('les articles', articleLinks)

# fouiller les articles




""" options qui ne me servent pas
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
