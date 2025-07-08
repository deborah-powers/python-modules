#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from invenspec import *

downloadFolder = downloadFolder + '-sharepoint'
urlSpecForge = 'https://magellanpartners.sharepoint.com/sites/MP-PRJ-ANCTSYNERGIECLOUD/Documents%20partages/Forms/AllItems.aspx?id=%2Fsites%2FMP%2DPRJ%2DANCTSYNERGIECLOUD%2FDocuments%20partages%2FGeneral%2F08%2E%20Fonds%20documentaire%2FSp%C3%A9cifications%20Fonctionnelles&viewid=1e36e7b7%2D898c%2D45d2%2Db4de%2D1f26676d52a6&FolderCTID=0x012000CF7A84DB29E4C4498BE77545E32687D6'

# https://magellanpartners.sharepoint.com/sites/MP-PRJ-ANCTSYNERGIECLOUD/Documents%20partages/Forms/AllItems.aspx?id=%2Fsites%2FMP%2DPRJ%2DANCTSYNERGIECLOUD%2FDocuments%20partages%2FGeneral%2F08%2E%20Fonds%20documentaire%2FSp%C3%A9cifications%20Fonctionnelles&viewid=1e36e7b7%2D898c%2D45d2%2Db4de%2D1f26676d52a6&FolderCTID=0x012000CF7A84DB29E4C4498BE77545E32687D6

# les fichiers
fileRes.title = fileRes.title +' sharepoint'
fileRes.text = "titre	date de modification	taille	url	fil d'ariane"
fileRes.write()
fileError.title = fileError.title +' sharepoint'
# fileError.write()

driver = createWebDriver (downloadFolder)
# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForge)
time.sleep(1)

body = driver.find_element (By.TAG_NAME, 'body').get_attribute ('innerHTML')
# remplir et valider le formulaire de login de la page https://login.microsoftonline.com/xxx
if 'loginfmt' in body:
	fieldName = driver.find_element (By.NAME, 'loginfmt')
	fieldName.send_keys ('deborah.powers@cgi.com')
	# bouton "suivant"
	buttonConnect = driver.find_element (By.ID, 'idSIButton9')
	buttonConnect.click()
# else: print (body)
time.sleep(5)
body = driver.find_element (By.TAG_NAME, 'body').get_attribute ('innerHTML')
# remplir et valider le formulaire de login de la page https://login.microsoftonline.com/xxx
if 'kmsiArea' in body:
#	fieldName = driver.find_element (By.NAME, 'UserName')
#	fieldName.send_keys ('deborah.powers@cgi.com')
	fieldPwd = driver.find_element (By.NAME, 'Password')
	fieldPwd.send_keys ('gLace420')
#	fieldMaintainSession = driver.find_element (By.NAME, 'Kmsi')
#	fieldMaintainSession.send_keys ('true')
	# bouton "suivant"
	buttonConnect = driver.find_element (By.ID, 'submitButton')
	buttonConnect.click()

# me connecter manuellement
time.sleep(45)
# revenir sur ma vraie page
driver.get (urlSpecForge)

def getFileData():
	time.sleep(3)
	log.log (driver.title, driver.current_url[112:])
	# récupérer les infos du dossier où je suis
	content = driver.find_element (By.ID, 'appRoot')
	# récupérer le fil d'arianne
	listArianne = content.find_element (By.TAG_NAME, 'ol').find_elements (By.TAG_NAME, 'li')
	filArianne =""
	for crum in listArianne: filArianne = filArianne +" / "+ crum.text;
	filArianne = filArianne[3:]
	log.message (filArianne)
	# récupérer les liens
	# content = driver.execute_script ("return document.getElementById ('html-list_2').children[0].children[7].children[1];")
	content = driver.find_element (By.ID, 'html-list_2').find_element (By.XPATH, './*')
	content = content.find_elements (By.XPATH, './*')[7].find_elements (By.XPATH, './*')[1]
	children = content.find_elements (By.XPATH, './*')
	tabHeader = children.pop (0)
	# titre	date de modification	taille	url	fil d'ariane
	for child in children:
		button = child.find_elements (By.TAG_NAME, 'span')[1]	# bouton où cliquer pour entrer dans un dossier
		if 'aria-label="Dossier' in child.get_attribute ('innerHTML'):
			try:
				currentUrl = driver.current_url
				log.message (driver.current_url[112:])
				button.click()
				getFileData()
				driver.back()
				time.sleep(0.5)
				log.message (currentUrl[112:])
				log.message (driver.current_url[112:])
			except exceptions.StaleElementReferenceException as staleException:
				log.log ('élément manquant', filArianne, driver.current_url[112:])
		else:
			fileRes.text = 'fichier\t%s\t%s\n' % (driver.current_url[112:], filArianne)
			fileRes.write()
getFileData()