#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError
from googleApi import setService
from fileCls import fromUrl
import loggerFct as log

# pour l'instant, ce script récupère la version de liens-data.js en ligne

scopes =[ 'https://www.googleapis.com/auth/drive.metadata.readonly' ]
service = setService ('drive', scopes)

results = service.files().list (fields='nextPageToken, files(id, name, mimeType, webContentLink)', spaces='drive', q="name='liens-data.js'").execute()
items = results.get ('files', [])
if not items: print ('aucun fichiers trouvé')
else:
	print ('fichiers trouvés')
	text = fromUrl (items[0]['webContentLink'])
	print (text)
