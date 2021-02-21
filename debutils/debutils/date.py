#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from debutils.text import Text
help ="""
classe de gestion facile des dates
dépendences:
	datetime.datetime
source:
	https://www.guru99.com/date-time-and-datetime-classes-in-python.html
"""
class Event():
	def __init__ (self):
		self.date		= Date()
		self.duration	= Date()
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

monthsName	= [ 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre' ]
daysWeek	= [ 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche' ]
daysWork	= [ 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi' ]

class Date():
	def __init__ (self):
		self.monthsDuration	= [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.year			=0
		self.month			=0
		self.day			=0
		self.hour			=0
		self.min			=0
		self.dayName		=""
	def setMonth (self, monthNb =0):
		if monthNb >0: self.month = monthNb
		self.isBissextile()
	def today (self):
		today = datetime.now()
		self.FromDate (today)
	def gapDates (self, newDate):
		diff = self.compareMins (newDate)
		if diff <0: return newDate.gapDates (self)
		else:
			thirdDate = Date()
			thirdDate.monthsDuration = self.monthsDuration
			thirdDate.min = self.min
			thirdDate.hour = self.hour
			thirdDate.day = self.day
			thirdDate.month = self.month
			thirdDate.year = self.year
			thirdDate.remMinutes (newDate.min)
			thirdDate.remHours (newDate.hour)
			thirdDate.remDays (newDate.day)
			thirdDate.remMonth (newDate.month)
			thirdDate.year -= newDate.year
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
		if diff >0:		diff +=2
		elif diff <0:	diff -=2
		elif self.hour	> newDate.hour:	diff =2
		elif self.hour	< newDate.hour:	diff =-2
		elif self.min	> newDate.min:	diff =1
		elif self.min	< newDate.min:	diff =-1
		return diff
	def remMonth (self, nb=1):
		self.month -=nb
		if self.month <0: self.year -=1; self.month +=12
	def remDays (self, nb=1):
		self.day -=nb
		self.isBissextile()
		if self.day <0:
			self.day += self.monthsDuration [self.month -2]
			self.remMonth (1)
	def remHours (self, nb=1):
		self.hour -=nb
		if self.hour <0: self.remDays (1); self.hour +=24
	def remMinutes (self, nb=1):
		self.min -=nb
		if self.min <0: self.remHours (1); self.min +=60
	def addMonths (self, nb=1):
		self.month +=nb
		if self.month >12: self.year +=1; self.month -=12
	def addDays (self, nb=1):
		self.day +=nb
		self.isBissextile()
		if self.day > self.monthsDuration [self.month -1]:
			self.day -= self.monthsDuration [self.month -1]
			self.addMonths (1)
	def addHours (self, nb=1):
		self.hour +=nb
		if self.hour >23: self.addDays (1); self.hour -=24
	def addMinutes (self, nb=1):
		self.min +=nb
		if self.min >59: self.addHours (1); self.min -=60
	# ________________________________________________ utiles ________________________________________________
	def __lt__ (self, newDate):
		string = '%d/%d/%d/%d/%d'
		return string % (self.year, self.month, self.day, self.hour, self.min) < string % (newDate.year, newDate.month, newDate.day, newDate.hour, newDate.min)
	def isBissextile (self):
		bissextile = False
		if self.year %400 ==0: bissextile = True
		elif self.year %100 !=0 and self.year %4 ==0: bissextile = True
		if bissextile: self.monthsDuration [1] =29
		else: self.monthsDuration [1] =28
	def nbDays (self):
		""" nombres approximatif de jours écoulés depuis l'an 0, pour comparer deux dates. je considère que les années écoulées font toutes 365j """
		nbDays = self.day
		rangeMonth = range (1, self.month)
		for m in rangeMonth: nbDays += self.monthsDuration [m-1]
		return nbDays
	def nbMins (self):
		""" nb de minutes écoulées depuis le début de la journée """
		nbMin = self.min
		nbMin += 60* self.hour
		return nbMin
	# ________________________________________________ lire et écrire ________________________________________________
	def __str__ (self):
		return self.toStrHour()
	def toStrFileName (self):
		strDate = '%d-%02d-%02d-%02d-%02d' % (self.year, self.month, self.day, self.hour, self.min)
		return strDate
	def toStrUtz (self):
		""" 2018-01-29T12:00:00+01:00 """
		if self.day ==0: self.day =1
		if self.month ==0: self.month =1
		strDate = '%d-%02d-%02dT%02d:%02d:00' % (self.year, self.month, self.day, self.hour, self.min)
		return strDate
	def toStrDay (self):
		strDate = '%d/%02d/%02d' % (self.year, self.month, self.day)
		return strDate
	def toStrHour (self):
		strDate = '%s %02d:%02d' % (self.toStrDay(), self.hour, self.min)
		return strDate
	def toPhrase (self):
		strDate = '%s %02d %s %d' % (self.self.dayName, self.day, monthsName [self.month -1], self.year)
		return strDate
	def fromStrUtz (self, dateStr):
		""" dateStr ressemble à 2018-01-29T12:00:00+01:00 """
		dateList = dateStr.split ('T')
		dateListTmp = dateList [0].split ('-')
		self.year = int (dateListTmp [0])
		self.month = int (dateListTmp [1])
		self.day = int (dateListTmp [2])
		self.isBissextile()
		if len (dateList) ==1: return
		dateListTmp = dateList [1].split (':')
		self.hour = int (dateListTmp [0])
		self.min = int (dateListTmp [1])
	def fromStr (self, dateStr):
		dateStr = dateStr.replace ('-', '/')
		dateStr = dateStr.replace (' ', '/')
		dateStr = dateStr.replace (':', '/')
		dateList = dateStr.split ('/')
		self.year = int (dateList [0])
		self.month = int (dateList [1])
		self.day = int (dateList [2])
		if len (dateList) ==5:
			self.hour = int (dateList [3])
			self.min = int (dateList [3])
		self.isBissextile()
	def FromDate (self, newDate):
		""" newDate est un objet datetime """
		self.year		= newDate.year
		self.month		= newDate.month
		self.day		= newDate.day
		self.hour		= newDate.hour
		self.min		= newDate.minute
		self.dayName	= daysWeek [newDate.weekday()]
		self.isBissextile()
	def toDate (self):
		pass
	def test (self):
		self.fromStrUtz ('2018-02-25T12:30:00+01:00')
		print (self)
		self.addDays (10)
		print (self)
		self.fromStr ('2016/02/25 12:30')
		self.addDays (10)
		print (self)