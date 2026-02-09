#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime
from sys import argv
from googleapiclient.errors import HttpError
from googleApi import setService
import textFct
from eventCls import DatePerso, Event
from fileList import FileList
import loggerFct as log
"""
mise en place
https://developers.google.com/calendar/api/quickstart/python
projet calendrier deborah
"""
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

dateStart = DatePerso (2026, 1, 8)
dateEnd = DatePerso.today()
dateEndStr = dateEnd.toStrDay()
"""
calNameList = ('deborah.powers89@gmail.com', 'sante', 'anniversaires et appels', 'quotidien', 'journal', 'boulot')
	'anniversaires et appels':		'v6apvjh1jvlcf9m127b2d15ngg@group.calendar.google.com'
"""
calNameList = ('deborah.powers89@gmail.com', 'quotidien', 'journal')
calDict = {
	'deborah.powers89@gmail.com':	'deborah.powers89@gmail.com',
	'journal':						'33akjnknr3mp1oletdkm8tdjog@group.calendar.google.com',
	'quotidien':					'nb71ojvfs60b1lmm2re27kj8h4@group.calendar.google.com',
}
evtDict = {
	'repas':	('quotidien', '2'),
	'poids':	('quotidien', '2'),
	'regles':	('quotidien', '7'),
	'douleurs':	('quotidien', '2'),
	'depenses':	('quotidien', '2'),
	'journal':	('journal', '2'),
	'reves':	('journal', '7'),
}
def keyByValue (dico, value):
	keys = dico.keys()
	res = None
	for key in keys:
		if dico[key] == value or value in dico[key]: res = key
	return res

def getCalDict (service):
	calDict = {}
	calTmp = service.calendarList().list().execute()
	calList = calTmp.get ('items', [])
	for cal in calList:
		calName = cal.get ('summary')
		if calName in calNameList:
			calDict [calName] = cal.get ('id')
	return calDict

""" ____________________________________ classes personnelles simplifiant la manipulation des objets récupérés ____________________________________ """

class calendarGoogle():

	def __init__ (self):
		self.id =""
		self.title =""
		self.infos =""
		self.color =""

	def fromGoogleObj (self, tmpCal):
		self.id = tmpCal.get ('id')
		self.title = tmpCal.get ('summary')
		self.infos = tmpCal.get ('description')
		self.color = tmpCal.get ('colorId')

	def fromId (self, service, calId):
		tmpCal = service.calendarList().get (calendarId=calId).execute()
		self.fromGoogleObj (tmpCal)

	def fromName (self, service, calName):
		if calName in calDict.keys(): self.fromId (service, calDict [calName])

	def __str__ (self):
		strCal = "id: %s\tnom: %s\tcouleur: %s\tinfos: %s" % (self.id, self.title, self.color, self.infos)
		return strCal

class eventGoogle (calendarGoogle, Event):
	def __init__ (self):
		calendarGoogle.__init__ (self)
		Event.__init__ (self)
		self.idRec =""

	def fromGoogleObj (self, tmpEvt):
		calendarGoogle.fromGoogleObj (self, tmpEvt)
		self.location = tmpEvt.get ('location')
		dateKey = 'date'
		if 'dateTime' in tmpEvt.get ('start').keys(): dateKey = 'dateTime'
		self.date = DatePerso.fromGoogle (tmpEvt.get ('start').get (dateKey))
		if dateKey != 'date':
			newDate = DatePerso.fromGoogle (tmpEvt.get ('end').get (dateKey))
			self.setDuration (newDate)
		self.idRec = tmpEvt.get ('recurringEventId')

	def equals (self, newEvt):
		if Event.equals (self, newEvt) and self.idRec == newEvt.idRec: return True
		else: return False

	def __lt__ (self, newEvt):
		return self.__str__() < newEvt.__str__()

	def toLowercase (self):
		self.category = self.category.lower()
		self.title = self.title.lower()
		self.infos = self.infos.lower()
		self.location = self.location.lower()
		self.location = self.location.replace (', france', "")
		self.location = self.location.replace (' paris', "")
		self.location = self.location.replace ('-malmaison, 92500 rueil-malmaison', "")
		self.location = self.location.replace ('-les-moulineaux, 92130 issy-les-moulineaux', "")


	""" __________________ récupérer un type d'évenement __________________ """

	def getOneMeal (self):
		if self.color == evtDict ['repas'][1] and self.title == 'repas' and self.date <= dateEnd:
			dateMeal = self.date.toStrDay()
			if dateMeal > dateEndStr: return None
			if not self.infos: self.infos = 'non noté'
			else: self.infos = self.infos.replace ('\n', '\t')
			if self.date.hour >16: self.title = 'soir'
			elif self.date.hour >11: self.title = 'midi'
			else: self.title = 'matin'
			evtStr = '%s\t%s\t%s' % (dateMeal, self.title, self.infos)
			return evtStr
		else: return None

	def getOneWeight (self):
		# log (self.title +'\t'+ self.color +'\t'+ evtDict ['poids'][1])
		if self.color == evtDict ['poids'][1] and self.title.lower() == 'poids':
			dateStr = self.date.toStrDay()
			if dateStr > dateEndStr: return None
			else:
				self.infos = self.infos.replace ('\n', '\t')
				evtStr = '%s\t%s' % (dateStr, self.infos)
				return evtStr
		else: return None

	def getOnePeriod (self):
		if self.color == evtDict ['regles'][1] and self.title.lower() in ('règles', 'regles'):
			self.infos = self.infos.replace ('\n', '\t')
			evtStr = '%s\t%s' % (self.date.toStrDay(), self.infos)
			return evtStr
		else: return None

	def getOneWalk (self):
		if self.title == 'Balade':
			self.infos = self.infos.replace ('\r', "")
			evtStr = '%s\n%s' % (self.date.toStrDay(), self.infos)
			evtStr = evtStr.replace ('\n', '\n\t')
			evtStr = evtStr.replace ('\r',"")
			return evtStr
		else: return None

	def getOnePurchase (self):
		if self.color == evtDict ['depenses'][1] and self.infos and self.title.lower() not in 'regles règles poids douleurs repas balade':
			self.infos = self.infos.replace ('\r', "")
			self.infos = self.infos.replace ('\n', " ")
			details =""
			if " " in self.infos:
				d= self.infos.index (" ")
				details = self.infos [d+1:]
				self.infos = self.infos[:d]
			# tmpList = self.infos.split (" "); cost = tmpList.pop (-1)
			if self.infos =='0' or self.infos == '0.0': return None
			elif details: self.infos = self.infos +'\t'+ details
			evtStr = '%s\t%s\t%s\t%s' % (self.date.toStrDay(), self.location, self.title, self.infos)
			return evtStr
		else: return None

	def getOneDolor (self):
		if self.title == 'Douleur':
			strDate = self.date.toStrHour() +'\t'+ self.duration.toStrHour() +'\t'+ self.infos.replace ('. ', '\t')
			strDate = strDate.replace ('0/00/00 ',"")
			return strDate
		else: return None

	def getOneDiary (self):
		if self.color == evtDict ['journal'][1] and self.infos:
			self.infos = textFct.shape (self.infos, 'reset upper')
		#	evtStr = '======================== %s ========================\n\ndate: %s\nlieu: %s\ntags: o\npersonnes: o\n\n%s\n\n'
			evtStr = '== %s\n\ndate: %s\nlieu: %s\ntags: o\npersonnes: o\n\n%s\n\n'
			evtStr = evtStr %(self.title, self.date.toStrDay(), self.location, self.infos)
			evtStr = evtStr.replace ('None', "")
			return evtStr
		else: return None

	def getOneDream (self):
		if self.color == evtDict ['reves'][1]:
			self.infos = textFct.shape (self.infos, 'reset upper')
			evtStr = '== %s\n\ndate: %s\nlieu: %s\ntags: o\npersonnes: o\n\n%s\n\n'
			evtStr = evtStr %(self.title, self.date.toStrDay(), self.location, self.infos)
			evtStr = evtStr.replace ('None', "")
			return evtStr
		else: return None

class eventList (FileList):
	def __init__ (self):
		FileList.__init__ (self)
		self.path = 'b/calendrier.txt'
		self.fromPath()

	def fromCalendar (self, service, calendar, dateMin, duplicate='False'):
		evtListTmp = []
		dateStrMin = dateMin.toUtz()
		evtListTmp = service.events().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime', timeMin=dateStrMin).execute()
		"""
		if dateMax: ancien paramètre
			dateStrMax = dateMax.toUtz()
			evtListTmp = service.events().list (calendarId=calendar.id, singleEvents=duplicate, orderBy='startTime', timeMax=dateStrMax).execute()
		"""
		evtList = evtListTmp.get ('items', [])
		for evt in evtList:
			evtTmp = eventGoogle()
			evtTmp.fromGoogleObj (evt)
			if not evtTmp.color: evtTmp.color = calendar.color
			if (calendar.title, evtTmp.color) in evtDict.values(): evtTmp.category = keyByValue (evtDict, (calendar.title, evtTmp.color))
			else: evtTmp.category = 'divers'
			evtTmp.title = evtTmp.title.strip()
			evtTmp.title = evtTmp.title.lower()
			if evtTmp.infos:
				evtTmp.infos = evtTmp.infos.strip()
				evtTmp.infos = evtTmp.infos.lower()
			evtTmp.category = evtTmp.category.strip()
			evtTmp.category = evtTmp.category.lower()
			if evtTmp.location:
				evtTmp.location = evtTmp.location.strip()
				evtTmp.location = evtTmp.location.lower()
			self.append (evtTmp)

	def selectByCalendar (self, calId):
		newList = eventList()
		for evt in self.list:
			if evt.calId ==calId: newList.append (evt)
		return newList

	def selectByColor (self, colId):
		newList = eventList()
		for evt in self.list:
			if evt.color ==colId: newList.append (evt)
		return newList

	def select (self, calId, colId):
		tmpList = self.selectByCalendar (calId)
		newList = tmpList.selectByColor (colId)
		return newList

	def getAll (self):
		# récupérer tous les calendriers
		for calName in calDict.keys():
			loggerFct.log (calName)
			cal = calendarGoogle()
			cal.fromName (service, calName)
			# extraire tous leurs évênements
			tmpList = eventList()
		#	tmpList.fromCalendar (service, cal, dateMin=dateStart, dateMax=dateEnd)
			tmpList.fromCalendar (service, cal, dateStart)
			self.extend (tmpList.list)
		self.list.sort()
		self.list.reverse()
		evtList = FileList ('b/calendar.tsv', '\n')
		for evt in self.list: evtList.append (evt.date.__str__() +'\t'+ evt.category +'\t'+ evt.title)
		evtList.write()

	def getPastEvents (self, calName, func):
		cal = calendarGoogle()
		cal.fromName (service, calName)
		# extraire tous leurs évênemnts
		self.fromCalendar (service, cal, dateStart, True)
		evtList = FileList()
		evtList.path = 'b/calendar.tsv'
		evtList.fromPath()
		for evt in self.list:
			if not evt.infos: evt.infos =""
			if not evt.location: evt.location =""
			if not evt.category: evt.category =""
			evt.toLowercase()
			evtStr = func (evt)
			if evtStr: evtList.append (evtStr)
		evtList.reverse()
		evtList.write (True)

def showColors():
	colors = service.colors().get().execute()
	# Print available calendarListEntry colors.
	keys = colors['calendar'].keys()
	for key in keys: print (key, colors['calendar'][key]['background'])
	# Print available event colors.
	keys = colors['event'].keys()
	for key in keys: print (key, colors['event'][key]['background'], colors['event'][key]['foreground'])

# on appele ce script dans un autre script
evtList = eventList()

scopes =[ 'https://www.googleapis.com/auth/calendar.readonly' ]
service = setService ('calendar', scopes)

if __name__ != '__main__': pass
elif len (argv) <2: print (help)
elif argv[1] == 'journal':	evtList.getPastEvents (evtDict ['journal'] [0],	eventGoogle.getOneDiary)
elif argv[1] == 'reves':	evtList.getPastEvents (evtDict ['reves'] [0],		eventGoogle.getOneDream)
elif argv[1] == 'repas':	evtList.getPastEvents (evtDict ['repas'] [0],		eventGoogle.getOneMeal)
elif argv[1] == 'regles':	evtList.getPastEvents (evtDict ['regles'] [0],	eventGoogle.getOnePeriod)
elif argv[1] == 'poids':	evtList.getPastEvents (evtDict ['poids'] [0],		eventGoogle.getOneWeight)
elif argv[1] == 'depenses':	evtList.getPastEvents (evtDict ['depenses'] [0],	eventGoogle.getOnePurchase)
elif argv[1] == 'douleurs':	evtList.getPastEvents (evtDict ['douleurs'] [0],	eventGoogle.getOneDolor)
elif argv[1] == 'balade':	evtList.getPastEvents (evtDict ['balade'] [0],	eventGoogle.getOneWalk)
elif argv[1] == 'all':		evtList.getAll()
else: print (help)


