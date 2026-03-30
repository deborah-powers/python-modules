#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver	# contrôle le navigateur
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By	# accède aux élements de la page web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

service = Service()
# les options
options = Options()
options.add_argument ('--enable-unsafe-swiftshader')
options.add_argument ('--ignore-certificate-errors')
options.add_argument ('--ignore-ssl-errors')
options.add_argument ('--log-level=3')
# lancer le navigateur, ici firefox
driver = webdriver.Firefox (service=service, options=options)

def goNextPage():
	try:
		buttonNext = driver.find_element (By.ID, 'btn-next')
		buttonNext.click()
		time.sleep (1)
	except NoSuchElementException: print ('le bouton suivant a disparu')

def fillInputText (inputId, message):
	inputToFill = driver.find_element (By.ID, inputId)
	inputToFill.send_keys (message)
	inputToFill.send_keys (Keys.ENTER)

def checkInput (inputId):
	# pour les boutons radio et les checkbox
	inputToCheck = driver.find_element (By.ID, inputId)
	# inputToCheck.click()	échoue si l'élément est recouvert par un autre
	driver.execute_script ('arguments[0].click();', inputToCheck)

def checkSelect (selectId, value):
	selectToCheck = Select (driver.find_element (By.ID, selectId))
	selectToCheck.select_by_value (value)
	# selectToCheck.select_by_visible_text (message)