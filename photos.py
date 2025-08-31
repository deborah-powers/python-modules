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
# options.add_argument ('--ignore-ssl-errors')
# options.add_argument ('--log-level=3')

driver = webdriver.Chrome (service=service, options=options)
actionChains = ActionChains (driver)

urlAlbum = 'https://photos.google.com/share/AF1QipPao_azUraa3kWyoa7bgp67IGn60OYuyuVxnxrrOlO2Nfg1iY75owjIc1xDE7u2_A?key=Q1dlVDFqaVZlNTY4Q1puS3UwSmZsT21YUU1uWTJB'
driver.get (urlAlbum)

# récupérer les liens des images
linkAll = driver.find_elements (By.TAG_NAME, 'a')
linkImg =[]
for link in linkAll:
	if './share/' == link.get_dom_attribute ('href')[:8]: linkImg.append ('https://photos.google.com' + link.get_dom_attribute ('href')[1:])
#		linkImg.append (link)
# fouiller chaque page
linkImgSrc =""
for link in linkImg:
	driver.get (link)
	# retrouver le lien
	imgAll = driver.find_elements (By.TAG_NAME, 'img')
	imgNb = len (imgAll)
	i=0
	while i< imgNb and 'https://lh3.googleusercontent.com/pw/AP1Gcz' != imgAll[i].get_dom_attribute ('src')[:43]: i+=1
	if i< imgNb: linkImgSrc = linkImgSrc + imgAll[i].get_dom_attribute ('src')[43:-8] +'\n'
	driver.back()
print (linkImgSrc)
