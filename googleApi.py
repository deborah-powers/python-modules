#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
from os.path import exists
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

def setService (appli, scopes):
	""" appli = drive ou calendar
	scopes est une liste d'url de googleapis
	"""
	fileToken = 'token-' + appli + '.json'
	fileCreds = 'credentials-' + appli + '.json'
	creds = None
	if not exists (fileCreds) and not exists (fileToken):
		print ("impossible de récupérer les authentifications, aucun fichier d'authentification n'existe")
		return None
	elif exists (fileToken): creds = Credentials.from_authorized_user_file (fileToken, scopes)
	if not creds and exists (fileCreds):
		flow = InstalledAppFlow.from_client_secrets_file (fileCreds, scopes)
		creds = flow.run_local_server (port=0)
		with open (fileToken, 'w') as token: token.write (creds.to_json())
	if creds and not creds.valid:
		try:
			creds.refresh (Request())
			with open (fileToken, 'w') as token: token.write (creds.to_json())
		except RefreshError: print ('impossible de récupérer les authentifications')
	# récupérer le service
	service = build (appli, 'v3', credentials=creds, client_options={ 'quota_project_id': appli + '-deborah' })
	return service

