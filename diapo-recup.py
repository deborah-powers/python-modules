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

class PhotoGoogle():
	def __init__ (self):
		self.date =""
		self.city =""
		self.place =""
		self.themes =""
		self.title =""
		self.url =""

	def extractCityFromLocation (self):
		pass

	def __str__(self):
		photoStr = self.date +'\t'+ self.city +'\t'+ self.title +'\t'+ self.themes +'\t'+ self.place +'\t'+ self.url
		return photoStr

	def __eq__(self, photo):
		# également ne !=, gt >, lt <, ge >=, le <=
		if photo.__class__ != self.__class__: return False
		elif self.city == photo.city and self.place == photo.place and self.date == photo.date and self.themes == photo.themes and self.title == photo.title and self.url == photo.url:
			return True
		else: return False

	def __ne__(self, photo):
		if photo.__class__ != self.__class__: return False
		else: return not self.__eq__(photo)

	def __gt__(self, photo):
		if photo.__class__ != self.__class__: return False
		elif self.city > photo.city: return True
		elif self.city < photo.city: return False
		elif self.place > photo.place: return True
		elif self.place < photo.place: return False
		elif self.date > photo.date: return True
		elif self.date < photo.date: return False
		elif self.themes > photo.themes: return True
		elif self.themes < photo.themes: return False
		elif self.title > photo.title: return True
		elif self.title < photo.title: return False
		elif self.url > photo.url: return True
		else: return False

	def __lt__(self, photo):
		if photo.__class__ != self.__class__: return False
		else: return not self.__gt__(photo)

	def __ge__(self, photo):
		if photo.__class__ != self.__class__: return False
		elif self.__eq__(photo): return True
		else: return self.__gt__(photo)

	def __le__(self, photo):
		if photo.__class__ != self.__class__: return False
		elif self.__eq__(photo): return True
		else: return self.__lt__(photo)

	def comparByDate (self, photo):
		if self.date > photo.date: return 1
		elif self.date < photo.date: return -1
		elif self.city > photo.city: return 1
		elif self.city < photo.city: return -1
		elif self.place > photo.place: return 1
		elif self.place < photo.place: return -1
		elif self.themes > photo.themes: return 1
		elif self.themes < photo.themes: return -1
		elif self.title > photo.title: return 1
		elif self.title < photo.title: return -1
		else: return 0

	def comparByCity (self, photo):
		if self.city > photo.city: return 1
		elif self.city < photo.city: return -1
		elif self.place > photo.place: return 1
		elif self.place < photo.place: return -1
		elif self.date > photo.date: return 1
		elif self.date < photo.date: return -1
		elif self.themes > photo.themes: return 1
		elif self.themes < photo.themes: return -1
		elif self.title > photo.title: return 1
		elif self.title < photo.title: return -1
		else: return 0

class PhotoGoogleList (FileList):
	def __str__(self):
		photoStr =""
		for photo in self.list: photoStr = photoStr + photo.__str__() + self.sep
		return photoStr

	def write (self):
		pass


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