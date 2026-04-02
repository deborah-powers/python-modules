#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from sianTest import *

myurl = 'https://psl-int-cgi-pslexec.pic-snau.service-public.fr/mademarche/demarcheGenerique/?codeDemarche=EICPE'

def getElementByTagAndClass (tagName, className):
	elements = driver.find_elements (By.TAG_NAME, tagName)
	element = None
	rangeElement = range (len (elements))
	for e in rangeElement:
		if className in elements[e].get_dom_attribute ('class'):
			element = elements[e]
	return element

# charger ma page dans le navigateur
driver.get (myurl)
time.sleep (1)
# refuser les cookies
try:
	buttonCookies = driver.find_element (By.CLASS_NAME, 'orejime-Button--decline')
	buttonCookies.click()
	time.sleep (1)
except NoSuchElementException: print ('les cookies ont déjà été validés')

# naviguer de page en page

def doPage1():
	if 'tape 1 sur 9' not in driver.find_element (By.TAG_NAME, 'body').text: goNextPage()
	checkInput ('radio2-1')
	checkInput ('radio3-0')
	time.sleep (1)
	checkInput ('radio9-1')
	checkInput ('idSaisie4')
	checkInput ('idSaisie5')
	checkInput ('idSaisie6')
	checkInput ('idSaisie7')

def doPage2():
	doPage1()
	goNextPage()
	checkInput ('radio11-0')
	time.sleep (1)
	checkInput ('radio14-1')
	time.sleep (1)
	checkInput ('radio15-0')
	checkInput ('radio18-0')
	fillInputText ('idSaisie19', '1985-02-14')
	print ('naissance entrée')
	fillInputText ('idSaisie21', '13000918600011')
#	buttonUseSiret = driver.find_elements (By.XPATH, './button[class="fr-mb-4v"]')[0]
#	buttonUseSiret = driver.find_element (By.XPATH, '//button[@class="fr-mb-4v"]')
	buttonUseSiret = getElementByTagAndClass ('button', 'fr-mb-4v')
	buttonUseSiret.click()
	time.sleep (1)
	buttonUseSiret.click()
	time.sleep (1)
	fillInputText ('idSaisie22', 'noisetier')
	fillInputText ('idSaisie23', 'noisette')
	time.sleep (1)
	fillInputText ('idSaisie34', '0612345689')
	fillInputText ('idSaisie33', '0112345689')
	time.sleep (1)
	fillInputText ('idSaisie38', 'noisette@gmail.com')
	time.sleep (1)
	checkInput ('radio40-0')



def doPage3():
	doPage2()
	goNextPage()
	fillInputText ('idSaisie42', "test d'intégration")

doPage2()

# python sian-eicpe.py