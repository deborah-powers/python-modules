#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from sys import argv
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from debutils.date import DatePerso, EventPerso
from debutils.list import dictGetKeyByValue
from debutils.fileList import FileList, FileTable
from debutils.text import Text
help =""" récupérer des évenements
utilisation
	python3 %s tag
les valeurs de tag
	regles: récupérer les dates de mes dernières règles
	reves:		"	la liste de mes rêves
	journal:	"	mon journal
	poids:		"	"	poids
	depenses:	"	"	dépenses
	repas:		"	"	repas
""" % __file__
dateStart = DatePerso ()
dateStart.today ()
dateStart.year =2020
dateStart.month =10
dateStart.day =6
dateEnd = DatePerso ()
dateEnd.today ()
dateEnd.addDays ()
calNameList = ('deborah.powers89@gmail.com', 'sante', 'anniversaires et appels', 'quotidien', 'journal', 'boulot')
calDict = {
	'sante':						'nb9aoslkd7jcfuudfr2pgp676k@group.calendar.google.com',
	'journal':						'33akjnknr3mp1oletdkm8tdjog@group.calendar.google.com',
	'deborah.powers89@gmail.com':	'deborah.powers89@gmail.com',
	'boulot':						'gtbloq5ifee0j3iv08ue8u399g@group.calendar.google.com',
	'quotidien':					'nb71ojvfs60b1lmm2re27kj8h4@group.calendar.google.com',
	'anniversaires et appels':		'v6apvjh1jvlcf9m127b2d15ngg@group.calendar.google.com'
}
evtDict = {
	'repas':	('quotidien', '1'),
	'poids':	('sante', '7'),
	'regles':	('sante', '7'),
	'douleurs':	('sante', '7'),
	'depenses':	('quotidien', '7'),
	'journal':	('journal', '2'),
	'reves':	('journal', '7'),
	'balade':	('journal', '7')
}
def setService ():
	# fonction de google
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
	creds = None
	if os.path.exists ('token.pickle'):
		with open ('token.pickle', 'rb') as token:
			creds = pickle.load (token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh (Request ())
		else:
			flow = InstalledAppFlow.from_client_secrets_file (
				'credentials.json', SCOPES)
			creds = flow.run_local_server ()
		# Save the credentials for the next run
		with open ('token.pickle', 'wb') as token:
			pickle.dump (creds, token)
	service = build ('calendar', 'v3', credentials=creds)
	return service
def getCalDict (service):
	calDict = {}
	calTmp = service.calendarList ().list ().execute ()
	calList = calTmp.get ('items', [])
	for cal in calList:
		calName = cal.get ('summary')
		if calName in calNameList:
			calDict [calName] = cal.get ('id')
	return calDict
""" ____________________________________ classes personnelles simplifiant la manipulation des objets récupérés ____________________________________ """
class calendarGoogle ():
	def __init__ (self):
		self.id =""
		self.title =""
		self.infos = Text ()
		self.color =""
	def fromGoogleObj (self, tmpCal):
		self.id = tmpCal.get ('id')
		self.title = tmpCal.get ('summary')
		self.infos.text = tmpCal.get ('description')
		self.color = tmpCal.get ('colorId')
	def fromId (self, service, calId):
		tmpCal = service.calendarList ().get (calendarId=calId).execute ()
		self.fromGoogleObj (tmpCal)
	def fromName (self, service, calName):
		if calName in calDict.keys (): self.fromId (service, calDict [calName])
	def __str__ (self):
		strCal = "nom: %stcouleur: %stinfos: %s" % (self.title, self.color, self.infos.text)
		return strCal
class eventGoogle (calendarGoogle, EventPerso):
	def __init__ (self):
		calendarGoogle.__init__ (self)
		EventPerso.__init__ (self)
		self.idRec =""
	def fromGoogleObj (self, tmpEvt):
		calendarGoogle.fromGoogleObj (self, tmpEvt)
		self.location = tmpEvt.get ('location')
		dateKey = 'date'
		if 'dateTime' in tmpEvt.get ('start').keys (): dateKey = 'dateTime'
		self.date.fromStrUtz (tmpEvt.get ('start').get (dateKey))
		if dateKey == 'date': self.duration.day =1
		else:
			self.duration.fromStrUtz (tmpEvt.get ('end').get (dateKey))
			self.duration = self.date.gapDates (self.duration)
		self.idRec = tmpEvt.get ('recurringEventId')
	def equals (self, newEvt):
		if EventPerso.equals (self, newEvt) and self.idRec == newEvt.idRec: return True
		else: return False
	def __lt__ (self, newEvt):
		return self.__str__ () < newEvt.__str__ ()
	def toLowercase (self):
		self.category = self.category.lower ()
		self.title = self.title.lower ()
		self.location = self.location.lower ()
		self.infos.text = self.infos.text.lower ()
	""" __________________ récupérer un type d'évenement __________________ """
	def getOneMeal (self):
		if self.color == evtDict ['repas'] [1]:
			if not self.infos.text: self.infos.text = 'non noté'
			else: self.infos.replace ('\n', '\t')
			evtStr = '%st%st%s' % (self.date.toStrDay (), self.title, self.infos.text)
			return evtStr
		else: return None
	def getOneWeight (self):
		if self.color == evtDict ['poids'] [1] and self.title.lower () == 'poids':
			self.infos.replace ('\n', '\t')
			evtStr = '%st%s' % (self.date.toStrDay (), self.infos.text)
			return evtStr
		else: return None
	def getOnePeriod (self):
		if self.color == evtDict ['regles'] [1] and self.title.lower () in ('règles', 'regles'):
			self.infos.replace ('\n', '\t')
			evtStr = '%st%s' % (self.date.toStrDay (), self.infos.text)
			return evtStr
		else: return None
	def getOneWalk (self):
		if self.title == 'Balade':
			self.infos.replace ('\r')
			evtStr = '%sn%s' % (self.date.toStrDay (), self.infos.text)
			evtStr = evtStr.replace ('\n', '\n\t')
			evtStr = evtStr.replace ('\r',"")
			return evtStr
		else: return None
	def getOnePurchase (self):
		if self.color == evtDict ['depenses'] [1] and self.infos.text:
			self.infos.replace ('\r')
			details =""
			if self.infos.contain ('\n'):
				d= self.infos.index ('\n')
				details = self.infos.text [d+1:]
				self.infos.text = self.infos.text [:d]
			tmpList = self.infos.split (' ')
			cost = tmpList.pop (-1)
			if cost =='0' or cost == '0.0': return None
			self.infos.text = ' '.join (tmpList) +'\t' + cost
			if details: self.infos.text = self.infos.text +'\t'+ details
			self.toLowercase ()
			evtStr = '%st%st%st%s' % (self.date.toStrDay (), self.location, self.title, self.infos.text)
			return evtStr
		else: return None
	def getOneDolor (self):
		if self.title == 'Douleur':
			strDate = self.date.toStrHour () +'\t'+ self.duration.toStrHour () +'\t'+ self.infos.text.replace ('. ', '\t')
			strDate = strDate.replace ('0/00/00 ',"")
			return strDate
		else: return None
	def getOneDiary (self):
		if self.color == evtDict ['journal'] [1]:
			if self.infos.text:
				self.infos.shape ()
				self.infos.replace ('"', '"')
				self.infos.replace ('\n', '", \n\t\t"')
			else: self.infos.text =""
			evtStr =""" {
	"date":"%s",
	"place":"%s",
	"title":"%s",
	"tags": [],
	"peoples": [],
	"content": [
		"%s"\n\t] \n},""" % (self.date.toStrDay (), self.location, self.title, self.infos.text)
			return evtStr
		else: return None
	def getOneDream (self):
		if self.color == evtDict ['reves'] [1] and self.title != 'Balade':
			self.infos.shape ()
			self.infos.replace ('"', '"')
			self.infos.replace ('\n', '", \n\t\t"')
			evtStr =""" {
	"date":"%s",
	"place":"%s",
	"title":"%s",
	"tags": [],
	"peoples": [],
	"content": [
		"%s"\n\t] \n},""" % (self.date.toStrDay (), self.location, self.title, self.infos.text)
			evtStr = evtStr.replace ('"None"', '""')
			return evtStr
		else: return None
class eventList (FileList):
	def __init__ (self):
		FileList.__init__ (self)
		self.file = 'b/calendar.txt'
		self.dataFromFile ()
	def fromCalendar (self, service, calendar, duplicate='False', dateMin=None, dateMax=None):
		evtListTmp = []
		if not duplicate: duplicate = 'False'
		if dateMin:
			dateStrMin = dateMin.toStrUtz () +'Z'
			if dateMax:
				dateStrMax = dateMax.toStrUtz () +'Z'
				evtListTmp = service.events ().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime', timeMin=dateStrMin, timeMax=dateStrMax).execute ()
			else: evtListTmp = service.events ().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime', timeMin=dateStrMin).execute ()
		elif dateMax:
			dateStrMax = dateMax.toStrUtz () +'Z'
			evtListTmp = service.events ().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime', timeMax=dateStrMax).execute ()
		else: evtListTmp = service.events ().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime').execute ()
		evtList = evtListTmp.get ('items', [])
		for evt in evtList:
			evtTmp = eventGoogle ()
			evtTmp.fromGoogleObj (evt)
			if not evtTmp.color: evtTmp.color = calendar.color
			if (calendar.title, evtTmp.color) in evtDict.values (): evtTmp.category = dictGetKeyByValue (evtDict, (calendar.title, evtTmp.color))
			else: evtTmp.category = 'divers'
			self.add (evtTmp)
	def selectByCalendar (self, calId):
		newList = eventList ()
		for evt in self.list:
			if evt.calId ==calId: newList.add (evt)
		return newList
	def selectByColor (self, colId):
		newList = eventList ()
		for evt in self.list:
			if evt.color ==colId: newList.append (evt)
		return newList
	def select (self, calId, colId):
		tmpList = self.selectByCalendar (calId)
		newList = tmpList.selectByColor (colId)
		return newList
	def toFile (self):
		newList = FileTable ()
		newList.title = 'calendar'
		newList.extension = 'tsv'
		newList.fileFromData ()
		for evt in self.list:
			newList.addLine ([ evt.date.__str__ (), evt.category, evt.title, evt.infos.__str__ ().replace ('\n', '\t') ])
		newList.sort ()
		newList.toFile ()
	def getAll (self):
		# récupérer tous les calendriers
	#	service = setService ()
	#	calDict = getCalDict (service)
		for calName in calDict.keys ():
			cal = calendarGoogle ()
			cal.fromName (service, calName)
			# extraire tous leurs évênements
			tmpList = eventList ()
			tmpList.fromCalendar (service, cal, dateMin=dateStart, dateMax=dateEnd)
			self.addList (tmpList.list)
		self.list.sort ()
		self.list.reverse ()
		self.toFile ()
	def getPastEvents (self, calName, func):
	#	service = setService ()
		cal = calendarGoogle ()
		cal.fromName (service, calName)
		# extraire tous leurs évênemnts
		self.fromCalendar (service, cal, True, dateMin=dateStart, dateMax=dateEnd)
		evtList = FileList ()
		evtList.file = 'b/calendar.tsv'
		evtList.dataFromFile ()
		for evt in self.list:
			if not evt.infos.text: evt.infos.text =""
			if not evt.location: evt.location =""
			if not evt.category: evt.category =""
			evtStr = func (evt)
			if evtStr: evtList.add (evtStr)
		evtList.reverse ()
		evtList.toFile ()
# on appele ce script dans un autre script
evtList = eventList ()
service = setService ()
if __name__ != '__main__': pass
elif len (argv) <2: print (help)
elif argv [1] == 'journal':	evtList.getPastEvents (evtDict ['journal'] [0],	eventGoogle.getOneDiary)
elif argv [1] == 'reves':	evtList.getPastEvents (evtDict ['reves'] [0],		eventGoogle.getOneDream)
elif argv [1] == 'repas':	evtList.getPastEvents (evtDict ['repas'] [0],		eventGoogle.getOneMeal)
elif argv [1] == 'regles':	evtList.getPastEvents (evtDict ['regles'] [0],	eventGoogle.getOnePeriod)
elif argv [1] == 'poids':	evtList.getPastEvents (evtDict ['poids'] [0],		eventGoogle.getOneWeight)
elif argv [1] == 'depenses':	evtList.getPastEvents (evtDict ['depenses'] [0],	eventGoogle.getOnePurchase)
elif argv [1] == 'douleurs':	evtList.getPastEvents (evtDict ['douleurs'] [0],	eventGoogle.getOneDolor)
elif argv [1] == 'balade':	evtList.getPastEvents (evtDict ['balade'] [0],	eventGoogle.getOneWalk)
elif argv [1] == 'all':		evtList.getAll ()
else: print (help)