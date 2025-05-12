#!/usr/bin/python3.10
import os
from sys import argv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from fileCls import fromUrl
import loggerFct as log

# pour l'instant, ce script récupère la version de liens-data.js en ligne

def setService():
	# récupérer les authorisations
	# If modifying these scopes, delete the file token.json.
	scopes =[ 'https://www.googleapis.com/auth/drive.metadata.readonly' ]
	creds = None
	# récupérer les accrédiations
	# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
	if os.path.exists ('token-drive.json'): creds = Credentials.from_authorized_user_file ('token-drive.json', scopes)
	if not creds and os.path.exists ('credentials-drive.json'):
		flow = InstalledAppFlow.from_client_secrets_file ('credentials-drive.json', scopes)
		creds = flow.run_local_server (port=0)
		with open ('token-drive.json', 'w') as token: token.write (creds.to_json())
	if creds and not creds.valid:
		try:
			creds.refresh (Request())
			with open ('token-drive.json', 'w') as token: token.write (creds.to_json())
		except RefreshError: print ('impossible de récupérer les authentifications')
	# récupérer le service
	service = build ('drive', 'v3', credentials=creds)
	return service

service = setService()
results = service.files().list (fields='nextPageToken, files(id, name, mimeType, webContentLink)', spaces='drive', q="name='liens-data.js'").execute()
items = results.get ('files', [])
if not items: print ('aucun fichiers trouvé')
else:
	print ('fichiers trouvés')
	fromUrl (items[0]['webContentLink'])
