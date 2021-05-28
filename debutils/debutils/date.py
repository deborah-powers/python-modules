#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from debutils.text import Text
from debutils.logger import log
"""
champs intéressants de datetime
self.year, self.month, self.day, self.hour, self.minute, self.second
newDay = self.replace (day=4, month= self.month +3)
%Y-%m-%d-%H-%M%S
"""
help ="""
classe de gestion facile des dates
dépendences:
	datetime.datetime
source:
	https://www.guru99.com/date-time-and-datetime-classes-in-python.html
"""

class Event():
	def __init__ (self):
		self.date		= Date.now()
		self.duration	= Date.now()
		self.location	=""
		self.category	=""
		self.title		=""
		self.infos		= Text()

	def equals (self, newEvt):
		if self.title == newEvt.title and self.infos == newEvt.infos: return True
		else: return False

	def __lt__ (self, newEvent):
		return self.date.__lt__ (newEvent.date)

	def __str__ (self):
		return self.toStrDay()

	def toStrHour (self):
		strEvt = self.date.toStrHour() +'\t'+ self.category +'\t'+ self.title +'\t'+ self.location +'\n\t'+ self.infos.text
		return strEvt

	def toStrDay (self):
		strEvt = self.date.toStrDay() +'\t'+ self.category +'\t'+ self.title +'\t'+ self.location +'\n\t'+ self.infos.text
		return strEvt

class DateVb():
	def __init__ (self):
		self.date = datetime

class Date (datetime):
	def gap (self, newDate):
		# renvoi un timedelta
		thirdDate = self - newDate
		return thirdDate

	def compareDays (self, newDate):
		diff =0
		if self.year	> newDate.year:		diff =3
		elif self.year	< newDate.year:		diff =-3
		elif self.month	> newDate.month:	diff =2
		elif self.month	< newDate.month:	diff =-2
		elif self.day	> newDate.day:		diff =1
		elif self.day	< newDate.day:		diff =-1
		return diff

	def compareMins (self, newDate):
		diff = self.compareDays (newDate)
		if diff >0:		diff +=3
		elif diff <0:	diff -=3
		elif self.hour		> newDate.hour:		diff =3
		elif self.hour		< newDate.hour:		diff =-3
		elif self.minute	> newDate.minute:	diff =2
		elif self.minute	< newDate.minute:	diff =-2
		elif self.second	> newDate.second:	diff =1
		elif self.second	< newDate.second:	diff =-1
		return diff
	# ________________________________________________ lire et écrire ________________________________________________

	def __str__ (self):
		return self.toStrHour()

	def toStrFileName (self):
		strDate = self.strftime ('%Y-%m-%d-%H-%M')
		return strDate

	def toStrUtz (self):
		""" 2018-01-29T12:00:00+01:00 """
		strDate = self.strftime ('%Y-%m-%dT%H:%M:%S')
		return strDate

	def toStrDay (self):
		strDate = self.strftime ('%Y/%m/%d')
		return strDate

	def toStrHour (self):
		strDate = self.strftime ('%Y/%m/%d %H:%M:%S')
		return strDate

	def fromStrUtz (self, dateStr):
		""" dateStr ressemble à 2018-01-29T12:00:00+01:00 """
		dateStr = dateStr[:19]
		dateStr = dateStr.replace ('T', '/')
		return self.fromStr (dateStr)

	def fromStr (self, dateStr):
		dateStr = dateStr.replace ('-', '/')
		dateStr = dateStr.replace (' ', '/')
		dateStr = dateStr.replace (':', '/')
		dateTmp = None
		if dateStr.count ('/') ==5: dateTmp = datetime.strptime (dateStr, '%Y/%m/%d/%H/%M/%S')
		elif dateStr.count ('/') ==2: dateTmp = datetime.strptime (dateStr, '%Y/%m/%d')
		dateNew = Date (dateTmp.year, dateTmp.month, dateTmp.day)
		dateNew = dateNew.replace (hour=dateTmp.hour, minute=dateTmp.minute)
		return dateNew
