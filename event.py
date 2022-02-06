#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from debutils.text import Text

help ="""
classe de gestion facile des dates
dépendences:
	datetime.datetime
	debutils.text
source:
	https://www.guru99.com/date-time-and-datetime-classes-in-python.html
"""

types =( 'logement', 'boutique', 'nature', 'promenade')
typesStreet =( 'rue', 'avenue', 'passage', 'quai' )

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

class DatePerso():

	def __init__ (self, day=1, hour=0, minute=0, month=1, year=2022):
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
		self.monthName = monthNames[month -1]

	def today (self):
		todayDatetime = datetime.now()
		self.year = todayDatetime.year
		self.month = todayDatetime.month
		self.day = todayDatetime.day
		self.hour = todayDatetime.hour
		self.minute = todayDatetime.minute

	# ________________________________________________ ajouter et supprimer ________________________________________________


	def addMonth (self, nb=1):
		self.month += nb
		if self.month >12:
			self.year +=1
			self.month -=12

	def delMonth (self, nb=1):
		self.month -= nb
		if self.month <1:
			self.year -=1
			self.month +=12


	def addDay (self, nb=1):
		self.day += nb
		if self.day > monthDuration[self.month -1]:
			if (self.month ==2 and self.isBissextile() and self.day <=29): pass
			self.day -= monthDuration[self.month -1]
			if (self.month ==2 and self.isBissextile()): self.day -=1
			self.addMonth (1)

	def delDay (self, nb=1):
		self.day -= nb
		if self.day <1:
			self.day += monthDuration[self.month -2]
			if (self.month ==3 and self.isBissextile()): self.day +=1
			self.delMonth (1)

	def addHour (self, nb=1):
		self.hour += nb
		if self.hour >23:
			self.hour -=24
			self.addDay (1)

	def delHour (self, nb=1):
		self.hour -= nb
		if self.hour <0:
			self.hour +=24
			self.delDay (1)

	def addMinute (self, nb=1):
		self.minute += nb
		if self.hour >59:
			self.hour -=60
			self.addHour (1)

	def delMinute (self, nb=1):
		self.minute -= nb
		if self.minute <0:
			self.minute +=60
			self.delHour (1)

	# ________________________________________________ lire et écrire ________________________________________________

	def __str__ (self):
		return self.toStrHour()

	def toStrFileName (self):
		return '%d-%d-%d-%d-%d' % (self.year, self.month, self.day, self.hour, self.minute)

	def toStrUtz (self):
		""" 2018-01-29T12:00:00+01:00 """
		return '%d-%d-%dT%d:%d:00' % (self.year, self.month, self.day, self.hour, self.minute)

	def toStrDay (self):
		return '%d/%d/%d' % (self.year, self.month, self.day)

	def toStrHour (self):
		return '%d/%d/%d %d:%d:00' % (self.year, self.month, self.day, self.hour, self.minute)

	def fromStrUtz (self, dateStr):
		""" dateStr ressemble à 2018-01-29T12:00:00+01:00 """
		dateStr = dateStr[:19]
		dateStr = dateStr.replace ('T', '/')
		return self.fromStr (dateStr)

	def fromStr (self, dateStr):
		dateStr = dateStr.replace ('-', '/')
		dateStr = dateStr.replace (' ', '/')
		dateStr = dateStr.replace (':', '/')
		dateList = dateStr.split ('/')
		self.year = int (dateList[0])
		self.month = int (dateList[1])
		self.day = int (dateList[2])
		if (len (dateList)) >4:
			self.hour = int (dateList[3])
			self.minute = int (dateList[4])

	# ________________________________________________ comparer ________________________________________________

	def difference (self, newDate):
		diff = self.compare (newDate)
		nbMinutesA =0
		nbMinutesB =0
		if diff >0:
			nbMinutesA = self.toMinutes()
			nbMinutesB = newDate.toMinutes()
		else:
			nbMinutesA = newDate.toMinutes()
			nbMinutesB = self.toMinutes()
		nbMinutesA -= nbMinutesB
		diffDate = DatePerso()
		diffDate.fromMinutes (nbMinutesA)
		return diffDate

	def __lt__ (self, newDate):
		return self.__str__() > newDate.__str__()

	def compare (self, newDate):
		diff =0
		if self.year		> newDate.year:	diff =5
		elif self.year		< newDate.year:	diff =-5
		elif self.month		> newDate.month:		diff =4
		elif self.month		< newDate.month:		diff =-4
		elif self.day		> newDate.day:		diff =3
		elif self.day		< newDate.day:		diff =-3
		elif self.hour		> newDate.hour:	diff =2
		elif self.hour		< newDate.hour:	diff =-2
		elif self.minute	> newDate.minute:	diff =1
		elif self.minute	< newDate.minute:	diff =-1
		return diff

	def isBissextile (self):
		bissextile = False
		if self.year %400 ==0: bissextile = True
		elif self.year %100 ==0: bissextile = False
		elif self.year %4 ==0: bissextile = True
		return bissextile

	def nbDaysYear (self):
		# number of days since year start
		numberDays = self.day
		rangeMois = range (self.month -1)
		for m in rangeMois: numberDays += monthDuration[m]
		if self.month >2 and self.isBissextile(): numberDays +=1
		return numberDays

	def toDays (self):
		# number of days since year 0
		numberDays = 365 * self.year
		nbYearsBissextiles = self.year //4 + self.year // 400 - self.year // 100
		numberDays += nbYearsBissextiles
		numberDays += self.nbDaysYear()

	def toMinutes (self):
		return self.minute + 60* self.hour + 1440 * self.toDays()

	def fromDays (self, nbDays):
		while (nbDays > 364):
			self.year +=1
			nbDays -= 365
			if self.isBissextile(): nbDays -=1
		m=0
		while nbDays > monthDuration[m]:
			nbDays -= monthDuration[m]
			m+=1
		if m<2 and self.isBissextile(): nbDays +=1
		self.month = m+1
		self.day = nbDays
		self.monthName = monthNames[month -1]

	def fromMinutes (self, nbMinutes):
		nbDays = nbMinutes // 1440
		self.fromDays (nbDays)
		nbMinutes = nbMinutes % 1440
		self.hour = nbMinutes // 60
		self.minute = nbMinutes % 60


class Event():
	def __init__ (self):
		self.date		= DatePerso()
		self.duration	= DatePerso()
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


