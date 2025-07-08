#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from invenspec import *

downloadFolder = downloadFolder + '-forge'
urlSpecForgeBase = 'https://forgeaxyus.local.axyus.com'
urlSpecForge = '/plugins/docman/?group_id=171&action=show&id=6080'
# https://forgeaxyus.local.axyus.com/plugins/docman/?group_id=171&action=show&id=6080

driver = createWebDriver (downloadFolder)
nameSpace = createFolderNameSpace (downloadFolder)

# me connecter à l'url. la première connection m'ammène sur la page de login
driver.get (urlSpecForgeBase + urlSpecForge)

# remplir et valider le formulaire de login
fieldName = driver.find_element (By.NAME, 'form_loginname')
fieldName.send_keys ('deborah.powers')
fieldPwd = driver.find_element (By.NAME, 'form_pw')
fieldPwd.send_keys ('LmUFhiYhoub8!')
buttonSend = driver.find_element (By.NAME, 'login')
buttonSend.submit()

# les fichiers
fileRes.title = fileRes.title +' forge'
fileRes.write()
fileError.title = fileError.title +' forge'
fileError.write()
fileRef = File ('b/fouille-spec\\invenspec forge 06-30.tsv')
fileRef.read()

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

def getFileData (fileElement, folderUrl, fileUrl, fileRes):
	# récupérer les infos du fichier lui-même
	fileElement.click()
	time.sleep (0.5)
	fileName = '.crdownload'
	countIter =0
	unwriten = True
	try:
		while '.crdownload' in fileName and countIter <8:
		#	log.log (fileName, countIter)
			fileName = os.listdir (downloadFolder)[0]
			countIter +=1
			time.sleep (15)
		if '.crdownload' in fileName:
			fileRes.text = fileRes.text % (fileName, '!! NON téléchargé !!')
			fileRes.write ('a')
			fileError.text = folderUrl[15:] + '\ttéléchargement raté de %s\t%s' % (fileName, fileUrl[15:])
			fileError.write ('a')
		#	log.message (fileError.text)
			unwriten = False
			emptyingFolder (downloadFolder)
		elif '.jar' == fileName[-4:] or '.zip' == fileName[-4:]:
			"""
			if unwriten:
				fileError.text = folderUrl[15:] + '\tfichier %s\t%s\t%s' % (fileName[-3:], fileName, fileUrl[15:])
				log.message (fileError.text)
				fileError.write ('a')
				unwriten = False
			"""
			emptyingFolder (downloadFolder)
		else:
			fileData = nameSpace.ParseName (fileName)
			fileSize = nameSpace.GetDetailsOf (fileData, 1)
			fileRes.text = fileRes.text % (fileName, fileSize.replace (' '," "))
			fileRes.write ('a')
		#	log.message (fileRes.text)
			emptyingFolder (downloadFolder)
	except Exception as e:
		if unwriten:
			fileRes.text = fileRes.text % (fileName, '!! NON téléchargé !!')
			fileRes.write ('a')
		#	log.message (fileRes.text)
		fileError.text = folderUrl[15:] + '\ttéléchargement raté de %s\t%s\n%s' % (fileName, fileUrl[15:], str(e))
		fileError.write ('a')
		emptyingFolder (downloadFolder)

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
		if len (linkList) <=1: return
		linkList = linkList[1].find_elements (By.TAG_NAME, 'a')
		linkRange = range (1, len (linkList), 3)	# linkList[l] = lien de l'élément, linkList[l+1] = lien vers ses métadonnées
		for l in linkRange:
			if l>= len (linkList): log.log ('index plus grand que la liste', len (linkList), l)
			childUrl = linkList[l].get_dom_attribute ('href')
			if not childUrl:
				fileError.text = url[15:] + '\tenfant sans lien\t' + linkList[l].text
				fileError.write ('a')
				continue
			elif childUrl in fileRef.text: continue
			elif '.jar' in linkList[l].text or '.zip' in linkList[l].text:
				"""
				fileError.text = url[15:] + '\tfichier zip ou jar\t%s\t%s' % (linkList[l].text, childUrl[15:])
				fileError.write ('a')
				"""
				continue
			nature = natureChild (childUrl, linkList[l+1])
			if 'dossier' == nature:
				links.append ((linkList[l].text, childUrl))
				continue
			elif not nature:
				fileError.text = url[15:] + '\tnature du lien enfant non précisable\t' + childUrl
				fileError.write ('a')
				continue
			else:
				fileRes.text = '%s\t%s\t%s\t%s\t%s\t%s' % ('%s', '%s', '%s', '%s', childUrl, filArianne)
				# récupérer les infos de la forge
				linkList[l+1].click()
				try:
					details = driver.find_element (By.CLASS_NAME, 'docman_item_menu')
					details.find_elements (By.TAG_NAME, 'a')[-1].click()
					time.sleep (0.5)
					details = driver.find_elements (By.TAG_NAME, 'table')[1]
					detailList = details.find_elements (By.TAG_NAME, 'tr')
					fileName = detailList[1].find_elements (By.TAG_NAME, 'td')[1].text
					# sauter certains types de fichiers
					if '.jar' == fileName[-4:] or '.zip' == fileName[-4:]:
						"""
						fileError.text = url[15:] + '\tfichier jar\t%s\t%s' % (fileName, childUrl[15:])
						fileError.write ('a')
						"""
						continue
					fileRes.text = fileRes.text % (fileName, '%s', detailList[5].find_elements (By.TAG_NAME, 'td')[1].text, '%s')
				except Exception as e:
					fileError.text = url[15:] + '\trécupération ratée de %s\t%s\n%s' % (fileName, childUrl[15:], str(e))
				#	log.message (fileError.text)
					fileError.write ('a')
				finally:
					driver.back()
					time.sleep(0.5)
					content = driver.find_element (By.CLASS_NAME, 'content')
					linkList = content.find_elements (By.TAG_NAME, 'ul')
					linkList = linkList[1].find_elements (By.TAG_NAME, 'a')
					getFileData (linkList[l], url, childUrl, fileRes)
		# traiter les liens enfants
		for name, url in links: getUrlData (url)

getUrlData (urlSpecForge)
