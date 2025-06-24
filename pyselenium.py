#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium avec python
sources:
	https://pypi.org/project/selenium/
	https://www.selenium.dev/selenium/docs/api/py/
	https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
"""
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time

urlSpecForgeBase = 'https://forgeaxyus.local.axyus.com'
urlSpecForge = '/plugins/docman/?group_id=171&action=show&id=6080'

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
driver = webdriver.Chrome (service=service, options=options)

# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForgeBase + urlSpecForge)

"""
# faire une pause le temps de voir la page
time.sleep (1)
# reffuser les cookies
try:
	cookiesReffuser =  driver.find_element (By.ID, 'tarteaucitronAllDenied2')
	driver.execute_script ('arguments[0].click();', cookiesReffuser);
	time.sleep (1)
except exceptions.NoSuchElementException:
	print ('les cookies ont déjà été validés')
"""
# remplir et valider le formulaire de login
fieldName = driver.find_element (By.NAME, 'form_loginname')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'form_pw')
fieldPwd.send_keys ('LmUFhiYhoub8!')
buttonSend = driver.find_element (By.NAME, 'login')
buttonSend.submit()
# buttonSend.click()

def getUrlData (url, parentName):
	finalText = 'url: '+ urlSpecForge	# les informations
	linkList =[]	# les liens enfants
	try:
		# rediriger vers la page désirée pour de bon
		driver.get (urlSpecForgeBase + url)
		# fouiller le dom afin de trouver les données d'intérêt
		content = driver.find_element (By.CLASS_NAME, 'content')
		finalText = finalText + "\nfil d'ariane: "+ content.find_element (By.TAG_NAME, 'td').text[10:]
		content = content.find_elements (By.TAG_NAME, 'ul')[1]
		links = content.find_elements (By.TAG_NAME, 'a')
		for link in links:
			if link.text:
				href = link.get_dom_attribute ('href')
				print (link.text, href)
				# les fichiers
				if '/download/' in href or '.' in link.text:
					finalText = finalText +'\n'+ parentName +'\t'+ link.text +'\t'+ link.get_dom_attribute ('href')
				# les pages enfants
				else: linkList.append ((link.text, href))
	except Exception as e: print ('une érreur bloque le traitement de', url, e)
	else:
		# traiter les liens enfants
		for name, url in linkList: finalText = finalText +'\n\n'+ getUrlData (url, parentName +" - "+ name)
	return finalText

def getUrlData (url, parentName):
	finalText = 'url: '+ urlSpecForge	# les informations
	linkList =[]	# les liens enfants
	try:
		# rediriger vers la page désirée pour de bon
		driver.get (urlSpecForgeBase + url)
		# fouiller le dom afin de trouver les données d'intérêt
		content = driver.find_element (By.CLASS_NAME, 'content')
		finalText = finalText + "\nfil d'ariane: "+ content.find_element (By.TAG_NAME, 'td').text[10:]
		content = content.find_elements (By.TAG_NAME, 'ul')[1]
		links = content.find_elements (By.TAG_NAME, 'a')
		for link in links:
			if link.text:
				finalText = finalText +'\n'+ parentName +'\t'+ link.text +'\t'+ link.get_dom_attribute ('href')
				linkList.append ((link.text, link.get_dom_attribute ('href')))
	except Exception as e: print ('une érreur bloque le traitement de', url, e)
	else:
		# traiter les liens enfants
		for name, url in linkList:
			if '/download/' in url: print (name, url)
			else: finalText = finalText +'\n\n'+ getUrlData (url, parentName +" - "+ name)
	return finalText

finalText = getUrlData (urlSpecForge, '.')
print (finalText)
