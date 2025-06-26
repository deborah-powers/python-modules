#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
""" tuto pour utiliser selenium avec python
sources:
	https://pypi.org/project/selenium/
	https://www.selenium.dev/selenium/docs/api/py/
	https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
"""
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

dossierTelechargements = 'C:\\Users\\deborah.powers\\Desktop\\fouille-spec\\telechargements'
urlSpecForgeBase = 'https://forgeaxyus.local.axyus.com'
urlSpecForge = '/plugins/docman/?group_id=171&action=show&id=6080'

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

# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForgeBase + urlSpecForge)

# l'espace de nom, pour récupérer les métadonnées des fichiers
shellApp = wclient.gencache.EnsureDispatch ('Shell.Application',0)
nameSpace = shellApp.NameSpace (dossierTelechargements)

# remplir et valider le formulaire de login
fieldName = driver.find_element (By.NAME, 'form_loginname')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'form_pw')
fieldPwd.send_keys ('LmUFhiYhoub8!')
buttonSend = driver.find_element (By.NAME, 'login')
buttonSend.submit()
# buttonSend.click()

fileRes = File ('b/fouille-spec\\inventaire.tsv')
fileRes.text = "titre	nom	date de modification	taille	url	fil d'ariane"
fileRes.write()
fileError = File ('b/fouille-spec\\erreurs.tsv')
fileError.text = 'url	erreur	url enfant'
fileError.write()
fileRef = File ('b/fouille-spec\\inventaire 06-25.tsv')
fileRef.read()

def viderTelechargements():
	fileNames = os.listdir (dossierTelechargements)
	for fileName in fileNames: os.remove (dossierTelechargements + os.sep + fileName)

def natureChild (childUrl, childLink):
	nature =""
	if '/plugins/docman/?group_id=' in childUrl: nature = 'dossier'
	elif '/download/' in childUrl: nature = 'fichier'
	else:
		try:
			childLink.click()
			frameDetail = driver.find_element (By.CLASS_NAME, 'docman_item_menu')
			if 'ouveau dossier' in frameDetail.text: nature = 'dossier'
			else: nature = 'fichier'
			frameDetail.find_element (By.TAG_NAME, 'a').click()
		except Exception as e:
			fileError.text = childUrl + '\ttest de la nature du lien\t.'
			fileError.write ('a')
		finally: return nature
	return nature

def getUrlData (url):
	links =[]	# les liens enfants
	linkList =[]
	textRes =""
	try:
		# rediriger vers la page désirée pour de bon
		driver.get (urlSpecForgeBase + url)
		time.sleep (0.5)	# donner le temps au dom de bien se charger
		# fouiller le dom afin de trouver les données d'intérêt
		content = driver.find_element (By.CLASS_NAME, 'content')
		time.sleep (0.5)
		filArianne = content.find_element (By.TAG_NAME, 'td').text[10:]
		linkList = content.find_elements (By.TAG_NAME, 'ul')
	except Exception as e:
		fileError.text = url + '\tdébut du traitement\t.'
		fileError.write ('a')
	else:
		if len (linkList) >1:
			linkList = linkList[1].find_elements (By.TAG_NAME, 'a')
			linkRange = range (1, len (linkList), 3)	# linkList[l] = lien de l'élément, linkList[l+1] = lien vers ses métadonnées
			for l in linkRange:
				childUrl = linkList[l].get_dom_attribute ('href')
				if not childUrl:
					fileError.text = url[15:] + '\tenfant sans lien\t' + linkList[l].text
					fileError.write ('a')
					continue
				nature = natureChild (childUrl, linkList[l+1])
				if 'dossier' == nature: links.append ((linkList[l].text, childUrl))
				elif 'fichier' == nature and childUrl in fileRef.text: continue
				elif not nature:
					fileError.text = url[15:] + '\tnature du lien enfant non précisable\t' + childUrl
					fileError.write ('a')
				else:
					# fil d'ariane, titre de la forge, vrai nom du fichier, url, date de modification de la forge, taille réelle
					fileRes.text = '%s\t%s\t%s\t%s\t%s\t%s' % ('%s', '%s', '%s', '%s', childUrl, filArianne)
					# récupérer les infos du fichier lui-même
					linkList[l].click()
					time.sleep (0.5)
					fileName = '.crdownload'
					countIter =0
					try:
						while '.crdownload' in fileName and countIter <12:
							fileName = os.listdir (dossierTelechargements)[0]
							countIter +=1
							time.sleep (3)
						if '.crdownload' in fileName:
							fileRes.text = fileRes.text % ('%s', fileName, '%s', '!! NON récupérée !!')
							fileError.text = url[15:] + '\ttéléchargement raté de %s\t%s' % (fileName, childUrl[15:])
							fileError.write ('a')
						else:
							fileData = nameSpace.ParseName (fileName)
							fileSize = nameSpace.GetDetailsOf (fileData, 1)
							fileRes.text = fileRes.text % ('%s', fileName, '%s', fileSize.replace (' '," "))
						# récupérer les infos de la forge
							linkList[l+1].click()
							content = driver.find_element (By.CLASS_NAME, 'docman_item_menu')
							content.find_elements (By.TAG_NAME, 'a')[-1].click()
							time.sleep (0.5)
							content = driver.find_elements (By.TAG_NAME, 'table')[1]
							linkList = content.find_elements (By.TAG_NAME, 'tr')
							fileRes.text = fileRes.text % (linkList[1].find_elements (By.TAG_NAME, 'td')[1].text, linkList[5].find_elements (By.TAG_NAME, 'td')[1].text)
						fileRes.write ('a')
						os.remove (dossierTelechargements + os.sep + fileName)
						driver.back()
						content = driver.find_element (By.CLASS_NAME, 'content')
						linkList = content.find_elements (By.TAG_NAME, 'ul')
						linkList = linkList[1].find_elements (By.TAG_NAME, 'a')
					except Exception as e:
						fileError.text = url[15:] + '\trécupération ratée de %s\t%s\t%s' % (fileName, childUrl[15:], str(e))
						fileError.write ('a')
						viderTelechargements()
			# traiter les liens enfants
			for name, url in links: getUrlData (url)

textRes = getUrlData (urlSpecForge)
fileRes.text = fileRes.text + textRes
fileRes.write ('a')

