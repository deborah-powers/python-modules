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
	creds = None
	if exists ('token-' + appli + '.json'): creds = Credentials.from_authorized_user_file ('token-' + appli + '.json', scopes)
	if not creds and exists ('credentials-' + appli + '.json'):
		flow = InstalledAppFlow.from_client_secrets_file ('credentials-' + appli + '.json', scopes)
		creds = flow.run_local_server (port=0)
		with open ('token-' + appli + '.json', 'w') as token: token.write (creds.to_json())
	if creds and not creds.valid:
		try:
			creds.refresh (Request())
			with open ('token-' + appli + '.json', 'w') as token: token.write (creds.to_json())
		except RefreshError: print ('impossible de récupérer les authentifications')
	# récupérer le service
	service = build (appli, 'v3', credentials=creds)
	return service

