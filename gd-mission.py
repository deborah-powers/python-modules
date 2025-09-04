#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
from axe_selenium_python import Axe
import time
import warnings
warnings.filterwarnings("ignore")

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
prefs ={ 'profile.default_content_setting_values.clipboard': 1 }
options.add_experimental_option ('prefs', prefs)
driver = webdriver.Chrome (service=service, options=options)

""" ------------ les fonctions de base ------------ """

def remplirLoginFormCosmose():
	fieldName = driver.find_element (By.NAME, 'JCMS_login')
	if fieldName:
		fieldName.send_keys ('deborah.powers@cgi.com')
		fieldPwd = driver.find_element (By.NAME, 'JCMS_password')
		fieldPwd.send_keys ('Noisette-416')
	#	fieldRemember = driver.find_element (By.NAME, 'JCMS_persistentCookie')
	#	fieldRemember.click()
		buttonSend = driver.find_element (By.NAME, 'JCMS_opLogin')
		buttonSend.submit()

def fermerModalDialog():
	try:
		modalDialog = driver.find_element (By.CLASS_NAME, 'modal-dialog')
		modalDialog = modalDialog.find_element (By.CLASS_NAME, 'modal-footer')
		buttonClose = modalDialog.find_element (By.TAG_NAME, 'button')
		buttonClose.click()
		time.sleep(0.5)
	except exceptions.NoSuchElementException as modalAbsent:
		pass

def montrerProfilsCaches():
	try:
		seeMoreButton = driver.find_element (By.CLASS_NAME, 'see-more-wrapper')
		seeMoreButton = seeMoreButton.find_element (By.TAG_NAME, 'a')
		seeMoreButton.click()
		time.sleep (0.5)
	except exceptions.NoSuchElementException as buttonAbsent:
		pass

def obtenirLienDePartageCosmoseSeul (profile):
	urlPartage =""
	try:
		profile.click()
		time.sleep (0.5)
		shareButton = driver.find_element (By.CLASS_NAME, 'pub-action-share')
		shareButton.click()
		time.sleep (0.5)
		shareButton = driver.find_element (By.CLASS_NAME, 'jicons-users')
		shareButton.click()
		time.sleep (0.5)
		buttons = driver.find_element (By.CLASS_NAME, 'buttons').find_elements (By.TAG_NAME, 'button')
		buttons[1].click()	# copier le lien
		time.sleep (0.5)
		urlPartage = driver.execute_script ('return navigator.clipboard.readText()')
	except exceptions.JavascriptException as e:
		urlPartage =""
		print ("échec de la récupération du lien de partage, impossible de cliquer sur le profil.")
	except Exception as e:
		urlPartage =""
		print ("échec de la récupération du lien de partage", e)
	return urlPartage

def obtenirLienDePartageCosmoseListe (urlListPage):
	urlListText =""
	driver.get (urlListPage)
	time.sleep (0.5)
	container = driver.find_elements (By.CLASS_NAME, 'explorer-table-body')[1]
	profiles = container.find_elements (By.XPATH, './div')
	endRange = len (profiles)
	if 'oir plus' in container.text: endRange -=1
	profileRange = range (endRange)
	# aller sur la page des cv
	p=0
	for p in profileRange:
		print (p)
		urlPartage = obtenirLienDePartageCosmoseSeul (profiles[p])
		if urlPartage: urlListText = urlListText + urlPartage +'\n'
		driver.get (urlListPage)	# revenir à la liste des url
		time.sleep (0.5)
		fermerModalDialog()
		# restaurer la liste des boutons pour les dsci
		container = driver.find_elements (By.CLASS_NAME, 'explorer-table-body')[1]
		profiles = container.find_elements (By.XPATH, './div')

	if 'oir plus' in container.text:
		montrerProfilsCaches()
		container = driver.find_elements (By.CLASS_NAME, 'explorer-table-body')[1]
		profiles = container.find_elements (By.XPATH, './div')
		profileRange = range (p+1, len (profiles))
		for p in profileRange:
			print (p)
			urlPartage = obtenirLienDePartageCosmoseSeul (profiles[p])
			if urlPartage: urlListText = urlListText + urlPartage +'\n'
			driver.get (urlListPage)	# revenir à la liste des url
			time.sleep (0.5)
			fermerModalDialog()
			# restaurer la liste des boutons pour les dsci
			montrerProfilsCaches()
			container = driver.find_elements (By.CLASS_NAME, 'explorer-table-body')[1]
			profiles = container.find_elements (By.XPATH, './div')
	return urlListText

def creerBlockLienExcel (urlListText):
	urlListText = urlListText.strip()
	urlListText = urlListText.replace ('_DBFileDocument/fr/', '"&Q6&"')
	urlListText = urlListText.replace ('https://cosmose.developpement-durable.gouv.fr/jcms/', '=LIEN_HYPERTEXTE(P6&"')
	urlListText = urlListText.replace ('\n', '";"DSCI")\n')
	urlListText = urlListText + '";"DSCI")'
	return urlListText

""" ------------ les cv ------------ """

pageListCv = 'https://cosmose.developpement-durable.gouv.fr/jcms/c_2046138/fr/mtect-anct-synergie-infogerance?histstate=1&portlet=c_2046136&explorerCurrentCategory=c_2045218&explorerSort=udate&mids=&startDate=&endDate=&types=ALL&documentKinds=&pinnedCategoryIds='
driver.get (pageListCv)
time.sleep (0.5)
remplirLoginFormCosmose()
driver.get (pageListCv)
time.sleep (0.5)
urlCvText = obtenirLienDePartageCosmoseListe (pageListCv)
urlCvText = creerBlockLienExcel (urlCvText)
print ('cv\n', urlCvText)

""" ------------ les dsci ------------ ""

pageListDsci = 'https://cosmose.developpement-durable.gouv.fr/jcms/c_2046138/fr/mtect-anct-synergie-infogerance?portlet=c_2046136&explorerCurrentCategory=c_2045126&explorerSort=udate&mids=&startDate=&endDate=&types=ALL&documentKinds=&pinnedCategoryIds='

driver.get (pageListDsci)
time.sleep (0.5)
driver.get (pageListDsci)
time.sleep (0.5)
urlDsciText = obtenirLienDePartageCosmoseListe (pageListDsci)
urlDsciText = creerBlockLienExcel (urlDsciText)
print ('dsci\n\n' + urlDsciText)
"""