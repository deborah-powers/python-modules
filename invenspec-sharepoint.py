#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from invenspec import *

urlSpecForgeBase = 'https://forgeaxyus.local.axyus.com'
urlSpecForge = '/plugins/docman/?group_id=171&action=show&id=6080'

# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForgeBase + urlSpecForge)

# remplir et valider le formulaire de login
fieldName = driver.find_element (By.NAME, 'form_loginname')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'form_pw')
fieldPwd.send_keys ('')
buttonSend = driver.find_element (By.NAME, 'login')
buttonSend.submit()

# les fichiers
fileRes.title = fileRes.title +' sharepoint'
fileRes.write()
fileError.title = fileError.title +' sharepoint'
fileError.write()

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
			fileError.text = childUrl + '\ttest de la nature du lien\n' + str(e)
			print (fileError.text)
			fileError.write ('a')
		finally: return nature
	return nature

def getUrlData (url):
	links =[]	# les liens enfants
	linkList =[]
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
		fileError.text = url + '\tdébut du traitement\n' + str(e)
		print (fileError.text)
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
				elif childUrl in fileRef.text: continue
				nature = natureChild (childUrl, linkList[l+1])
				if 'dossier' == nature: links.append ((linkList[l].text, childUrl))
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
						while '.crdownload' in fileName and countIter <100:
							fileName = os.listdir (dossierTelechargements)[0]
							countIter +=1
							time.sleep (3)
						if '.crdownload' in fileName:
							fileRes.text = fileRes.text % ('%s', fileName, '%s', '!! NON téléchargé !!')
							fileError.text = url[15:] + '\ttéléchargement raté de %s\t%s' % (fileName, childUrl[15:])
							print (fileError.text)
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
						fileError.text = url[15:] + '\trécupération ratée de %s\t%s\n%s' % (fileName, childUrl[15:], str(e))
						print (fileError.text)
						fileError.write ('a')
						viderTelechargements()
			# traiter les liens enfants
			for name, url in links: getUrlData (url)

getUrlData (urlSpecForge)

