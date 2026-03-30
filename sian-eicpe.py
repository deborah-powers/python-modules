#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from sianTest import *

myurl = 'https://psl-int-cgi-pslexec.pic-snau.service-public.fr/mademarche/demarcheGenerique/?codeDemarche=EICPE'

# charger ma page dans le navigateur
driver.get (myurl)
time.sleep (1)
print ('page 1')
goNextPage()
# refuser les cookies
try:
	buttonCookies = driver.find_element (By.CLASS_NAME, 'orejime-Button--decline')
	buttonCookies.click()
	time.sleep (1)
except NoSuchElementException: print ('les cookies ont déjà été validés')
# naviguer de page en page

def doPage1():
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


doPage2()

# python test-sian.py