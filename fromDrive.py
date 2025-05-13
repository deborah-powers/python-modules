#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError
from googleApi import setService
from fileCls import fromUrl, File
import loggerFct as log

# pour l'instant, ce script récupère la version de liens-data.js en ligne

scopes =[ 'https://www.googleapis.com/auth/drive.metadata.readonly' ]
service = setService ('drive', scopes)

"""
myFile = File ('b/from-drive.txt')
# for item in service.__dict__: myFile.text = myFile.text + item +':\t'+ log.objToStr (service.__dict__[item]) +'\n======\n'
for item in service.__dict__: myFile.text = myFile.text + item +':\t'+ str (service.__dict__[item]) +'\n'
myFile.write()
"""
if service:
	results = service.files().list (fields='nextPageToken, files(id, name, mimeType, webContentLink)', spaces='drive', q="name='liens-data.js'").execute()
	items = results.get ('files', [])
	if not items: print ('aucun fichiers trouvé')
	else:
		myFile = File ('b/from-drive.html')
		print ('fichiers trouvés', items[0])
	#	myFile.text = fromUrl (items[0]['webContentLink'])
		myFile.text = fromUrl ('https://www.googleapis.com/drive/v3/files/' + items[0]['id'])
		myFile.write()
