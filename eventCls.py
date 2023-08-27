#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import loggerFct

help ="""
classe de gestion facile des dates
dépendences:
	datetime.datetime
source:
	https://www.guru99.com/date-time-and-datetime-classes-in-python.html
"""

types =( 'logement', 'boutique', 'nature', 'promenade')
typesStreet =( 'rue', 'avenue', 'passage', 'quai' )
templateUtz = '%Y-%m-%dT%H:%M:00.0Z'	# 2018-01-29T12:00:00+01:00.0Z

class Place():
	def __init__ (self):
		self.type =""
		self.name =""
		self.city =""
		self.postalCode =""
		self.street =""
		self.streetType =""
		self.number =""
		self.complement =""

monthDuration =( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
monthNames =( 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre' )

class DatePerso (datetime):
	# attriuts: year, month, day, our, minute, monthName
	def __init__ (self, year, month, day, hour=0, minute=0):
		datetime.__init__(self)
		self.monthName = monthNames[self.month -1]

	def difference (self, newDate):
		delta = None
		if self < newDate: delta = newDate - self
		else: delta = self - newDate
		return delta

	def today():
		dtDate = datetime.now()
		return DatePerso (dtDate.year, dtDate.month, dtDate.day, dtDate.hour, dtDate.minute)

	def fromUtz (dateStr):
		return DatePerso.fromStr (templateUtz, dateStr)

	def toUtz (self):
		return self.strftime (templateUtz)

	def fromGoogle (googleDate):
		if len (googleDate) ==10: return DatePerso.fromStr ('%Y-%m-%d', googleDate)
		else:
			googleDate = googleDate[:16]
			return DatePerso.fromStr ('%Y-%m-%dT%H:%M', googleDate)

	def fromStr_interne (self, model, source):
		dtDate = datetime.strptime (source, model)
		return DatePerso (dtDate.year, dtDate.month, dtDate.day, dtDate.hour, dtDate.minute)

	def fromStr (model, source):
		dtDate = datetime.strptime (source, model)
		return DatePerso (dtDate.year, dtDate.month, dtDate.day, dtDate.hour, dtDate.minute)

	def toStrDay (self):
		return self.strftime ('%Y/%m/%d')

	def toStrHour (self):
		return self.strftime ('%Y/%m/%d %H:%M')

	def __str__(self):
		return self.toStrHour()


DatePerso.today = staticmethod (DatePerso.today)
DatePerso.fromStr = staticmethod (DatePerso.fromStr)
DatePerso.fromUtz = staticmethod (DatePerso.fromUtz)
DatePerso.fromGoogle = staticmethod (DatePerso.fromGoogle)

data = DatePerso.fromGoogle ('2018-12-22T12:45')
dato = DatePerso.fromGoogle ('2018-12-14T12:26')
data.difference (dato)

"""
dt= DatePerso.today()
print (dt)
do= datetime (2022, 2, 25, 13, 45)
print (do)
print (do.year)
print (do.month)
print (do.day)
print (do.hour)
print (do.minute)
print (do.replace (day=28, hour=4))
"""

class Event():
	def __init__ (self):
		self.date		= DatePerso.today()
		self.duration	= 0	# en minutes
		self.location	=""
		self.category	=""
		self.title		=""
		self.infos		=""

	def equals (self, newEvt):
		if self.title == newEvt.title and self.infos == newEvt.infos: return True
		else: return False

	def __lt__ (self, newEvent):
		return self.date.__lt__ (newEvent.date)

	def __str__ (self):
		return self.toStrDay()

	def setDuration (self, datePerso):
		if datePerso < self.date: self.duration =0
		else:
			difference = self.date.difference (datePerso)
			if difference.days ==0 and difference.seconds >0: self.duration = difference.seconds /60

	def toStrHour (self):
		strEvt = self.date.toStrHour() +'\t'+ self.category +'\t'+ self.title +'\t'+ self.location +'\n\t'+ self.infos
		return strEvt

	def toStrDay (self):
		strEvt = self.date.toStrDay() +'\t'+ self.category +'\t'+ self.title +'\t'+ self.location +'\n\t'+ self.infos


