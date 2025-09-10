#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
# récupérer les liens de mes photos google
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver import ActionChains	# clique droit
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager	# utiliser le navigateur chrome
import time

# lancer le navigateur, ici chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')

driver = webdriver.Chrome (service=service, options=options)
actionChains = ActionChains (driver)

def getImgData (first=False):
	time.sleep (0.5)
	# trouver le bouton pour afficher les infos
	buttonInfos = driver.find_elements (By.TAG_NAME, 'button')[4]
#	buttonInfos = driver.find_element (By.XPATH, './/button[@aria-label="Ouvrir les infos"]')
	buttonInfos.click()
	time.sleep (0.5)
	# récupérer le nom du fichier, qui contient des infos sur la photo
	imgAll = driver.find_elements (By.XPATH, './/dd/div[@aria-label]')
	imgLen = len (imgAll)
	imgData =""
	i=0
	while i< imgLen and imgData =="":
		imgTmp = imgAll[i].get_dom_attribute ('aria-label')
		if 'Nom du fichier' == imgTmp[:14]: imgData = imgAll[i].text[:-4]
		i+=1
	if imgData[-1] =='.': imgData = imgData[:-1]
	buttonInfos.click()
	time.sleep (0.5)
	# récupérer les images de la page
	imgAll = driver.find_elements (By.XPATH, './/img[contains(@src, "https://lh3.googleusercontent.com/pw/AP1Gcz")]')
	imgLen = len (imgAll)
	imgSrc =""
	if first: imgSrc = imgAll[0].get_dom_attribute ('src')[43:]
	else: imgSrc = imgAll[2].get_dom_attribute ('src')[43:]
	# aller à la page suivante
	print (imgData +"  "+ imgSrc)
	if imgLen ==6 or first:
		first = False
		buttonNext = driver.find_element (By.XPATH, './/div[@aria-label="Afficher la photo suivante"]')
		buttonNext.click()
		getImgData()

urlFirstPhoto = 'https://photos.google.com/share/AF1QipPao_azUraa3kWyoa7bgp67IGn60OYuyuVxnxrrOlO2Nfg1iY75owjIc1xDE7u2_A/photo/AF1QipMbNMMi93nR__ljAPKMR8PMICLgv-dZNphucGpc?key=Q1dlVDFqaVZlNTY4Q1puS3UwSmZsT21YUU1uWTJB'
urlFirstPhoto = 'https://photos.google.com/share/AF1QipPao_azUraa3kWyoa7bgp67IGn60OYuyuVxnxrrOlO2Nfg1iY75owjIc1xDE7u2_A/photo/AF1QipOYhq272IJ7i_MQIqHmYU3OewfNRUrVQkq9EWUd?key=Q1dlVDFqaVZlNTY4Q1puS3UwSmZsT21YUU1uWTJB'
driver.get (urlFirstPhoto)
getImgData (True)