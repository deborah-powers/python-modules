#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError
from googleApi import setService
from fileCls import fromUrl, File
import loggerFct as log

# pour l'instant, ce script récupère la version de liens-data.js en ligne

scopes =[ 'https://www.googleapis.com/auth/drive.metadata.readonly' ]
service = setService ('drive', scopes)
driveUrl = 'https://drive.google.com/drive/u/0/folders/10Yb98B6H2Wsf-Rg3uEtMtdOJyOCIDeXw'
driveUrl = 'https://drive.google.com/drive/folders/10Yb98B6H2Wsf-Rg3uEtMtdOJyOCIDeXw'

"""
myFile = File ('b/from-drive.txt')
# for item in service.__dict__: myFile.text = myFile.text + item +':\t'+ log.objToStr (service.__dict__[item]) +'\n======\n'
for item in service.__dict__: myFile.text = myFile.text + item +':\t'+ str (service.__dict__[item]) +'\n'
myFile.write()
"""

import os, io
from googleapiclient.http import MediaIoBaseDownload

def downloadFile (service, fileId, folderOutput, fileLog, totalPages):
	metadata = service.files().get (fileId=fileId).execute()
	fileName = metadata['name']
	try:
		print (metadata)
		if metadata['mimeType'] == 'applicaton/vnd.google-apps.document':
			request = service.files().export_media (fileId=fileId, mimeType='applicaton/pdf')
		elif metadata['mimeType'] == 'applicaton/vnd.google-apps.spreadsheet':
			request = service.files().export_media (fileId=fileId, mimeType='applicaton/vdn.openxmlformats-officedocument.spreadsheetml.sheet')
		elif metadata['mimeType'] == 'applicaton/vnd.google-apps.presentation':
			request = service.files().export_media (fileId=fileId, mimeType='applicaton/vdn.openxmlformats-officedocument.presentationml.presentation')
		else: request = service.files().get_media (fileId=fileId)
		filePath = os.path.join (folderOutput, fileName)
		os.makedirs (subFolderOutput, exist_ok=True)
		with io.FileIO (filePath, 'wb') as fh:
			downloader = MediaIoBaseDownload (fh, request)
			done = False
			while not done:
				status, done = downloader.next_chunk()
				print (status.progress())
		with open (fileLog, 'a') as log:
			log.write ('page no '+ totalPages +' fichier '+ filePath + ' téléchargé' if done else ' en cours de téléchargement')
		print ('le fichier est téléchargé '+ filePath)
	except Exception as e:
		print ('téléchargement impossible pour '+ filePath, e)
		with open (fileLog, 'a') as log: log.write ('erreur au téléchargement de '+ filePath)

def downloadFolder (service, folderId, folderOutput, fileLog):
	files, totalPages = list_files_in_folder (service, folderId)
	for file in files:
		# les sous-dossiers
		if file['mimeType'] == 'applicaton/vnd.google-apps.folder':
			subFolderId = file['id']
			subFolderName = file['name']
			subFolderOutput = os.path.join (folderOutput, subFolderName)
			os.makedirs (subFolderOutput, exist_ok=True)
			downloadFolder (service, subFolderId, subFolderOutput, fileLog)
		# les fichiers
		else: downloadFile (service, file['id'], folderOutput, fileLog, totalPages)

def listFolders (service, folderId):
	files =[]
	pageToken = None
	pageNb =1
	while True:
		request = service.files()
			.list (fields='nextPageToken, files(id, name, mimeType, webContentLink)', spaces='drive', pageToken= None if pageNb ==1 else pageToken, q=folderId +' in parents')
		response = request.execute()
	files.extends (response.get ('files', []))
	pageToken = response.get ('nextPageToken')
	if not pageToken: break
	pageNb +=1
	return files, pageNb

def downloadFolders (service, folderId, folderOutput):
	files, pageNb = listFolders (service, folderId)
	print ('télécharger le dossier', folderId, 'dans', folderOutput)
	fileLog = 'log.txt'
	for file in files:
		downloadFolder (service, file['id'], folderOutput, fileLog)




if service:
	results = service.files().list (fields='nextPageToken, files(id, name, mimeType, webContentLink)', spaces='drive', q="name='liens-data.js'").execute()
	items = results.get ('files', [])
	if not items: print ('aucun fichiers trouvé')
	else:
		myFile = File ('b/from-drive.html')
		print ('fichiers trouvés', items[0])
		myFile.text = fromUrl (items[0]['webContentLink'])
		print (myFile.text)
	#	myFile.text = fromUrl ('https://www.googleapis.com/drive/v3/files/' + items[0]['id'])
		myFile.write()
