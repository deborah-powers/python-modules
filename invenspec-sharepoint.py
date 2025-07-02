#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from invenspec import *

downloadFolder = downloadFolder + '-sharepoint'
urlSpecForgeBase = 'https://magellanpartners.sharepoint.com/sites/MP-PRJ-ANCTSYNERGIECLOUD/Documents%20partages/Forms/AllItems.aspx?'
urlSpecForge = 'id=%2Fsites%2FMP%2DPRJ%2DANCTSYNERGIECLOUD%2FDocuments%20partages%2FGeneral%2F08%2E%20Fonds%20documentaire%2FSp%C3%A9cifications%20Fonctionnelles&viewid=1e36e7b7%2D898c%2D45d2%2Db4de%2D1f26676d52a6&FolderCTID=0x012000CF7A84DB29E4C4498BE77545E32687D6'

# https://magellanpartners.sharepoint.com/sites/MP-PRJ-ANCTSYNERGIECLOUD/Documents%20partages/Forms/AllItems.aspx?id=%2Fsites%2FMP%2DPRJ%2DANCTSYNERGIECLOUD%2FDocuments%20partages%2FGeneral%2F08%2E%20Fonds%20documentaire%2FSp%C3%A9cifications%20Fonctionnelles&viewid=1e36e7b7%2D898c%2D45d2%2Db4de%2D1f26676d52a6&FolderCTID=0x012000CF7A84DB29E4C4498BE77545E32687D6

# les fichiers
fileRes.title = fileRes.title +' sharepoint'
# fileRes.write()
fileError.title = fileError.title +' sharepoint'
# fileError.write()

driver = createWebDriver (downloadFolder)
# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForgeBase + urlSpecForge)
time.sleep(1)

# remplir et valider le formulaire de login de la page https://login.microsoftonline.com/xxx
fieldName = driver.find_element (By.NAME, 'loginfmt')
fieldName.send_keys ('deborah.powers@cgi.com')
# bouton "suivant"
buttonConnect = driver.find_element (By.ID, 'idSIButton9')
buttonConnect.click()
"""
# bouton "se connecter"
buttonConnect = driver.find_element (By.ID, 'loginHeader')
print (buttonConnect)
buttonConnect.click()
"""
# me connecter manuellement
time.sleep(45)
# revenir sur ma vraie page
driver.get (urlSpecForgeBase + urlSpecForge)
time.sleep(1)

# récupérer les infos du dossier où je suis
content = driver.find_element (By.ID, 'appRoot')
# récupérer le fil d'arianne
listArianne = content.find_element (By.TAG_NAME, 'ol').find_elements (By.TAG_NAME, 'li')
filArianne =""
for crum in listArianne: filArianne = filArianne +" / "+ crum.text;
filArianne = filArianne[3:]
log.message (filArianne)
# récupérer les liens
content = driver.find_element (By.ID, 'html-list_2')
log.message (len (content.find_elements (By.CSS_SELECTOR, '*')))
log.message (len (content.find_elements (By.XPATH, './/*')))
log.message (len (content.find_elements (By.XPATH, '//*')))
driver.execute_script ("alert (document.getElementById ('html-list_2').children.length);")
res = driver.execute_script ("document.getElementById ('html-list_2').children.length;")
log.message (res)

content = content.find_element (By.CSS_SELECTOR, '*').find_elements (By.CSS_SELECTOR, '*')[7].find_elements (By.CSS_SELECTOR, '*')[1]
folders = content.find_elements (By.CSS_SELECTOR, '*')
log.message (len (folders))
"""
	content = document.getElementById ().children[0].children[0].children[0].children[0].children[0].children[7].children[1];
	document.body.style.overflow = 'scroll';
	var dataTab ="";	// titre	nom	date de modification	taille	url	fil d'ariane
	var folderList =[];
	for (var frame of content.children){
		if (frame.children[1].children[0].tagName === 'DIV' && frame.children[1].children[0].children[0].getAttribute ('aria-label').includes ('Dossier'))
			folderList.push (frame);
		else dataTab = dataTab + frame.extractFileData() +'\t'+ filArianne +'\n';
"""
