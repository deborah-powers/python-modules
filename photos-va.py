#!/usr/bin/python3.10
from __future__ import print_function
from datetime import datetime
import os.path
from sys import argv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

def setService():
	# récupérer les authorisations
	# If modifying these scopes, delete the file token.json.
	scopes =[ 'https://photospicker.googleapis.com', 'https://photospicker.googleapis.com/v1/sessions', 'https://www.googleapis.com/auth/photospicker.mediaitems.readonly' ]
	creds = None
	# récupérer les accrédiations
	# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
	if os.path.exists ('token-photos.json'): creds = Credentials.from_authorized_user_file ('token-photos.json', scopes)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			try: creds.refresh (Request())
			except RefreshError:
				flow = InstalledAppFlow.from_client_secrets_file ('credentials-photos.json', scopes)
				creds = flow.run_local_server (port=0)
				# Save the credentials for the next run
				with open ('token-photos.json', 'w') as token: token.write (creds.to_json())
		else:
			flow = InstalledAppFlow.from_client_secrets_file ('credentials-photos.json', scopes)
			creds = flow.run_local_server (port=0)
		# Save the credentials for the next run
		with open ('token-photos.json', 'w') as token: token.write (creds.to_json())
	# récupérer le service
	service = build ('photospicker', 'v1', credentials=creds, static_discovery=False)
	return service

service = setService()
print (service.__dir__())
print (service.sessions())
