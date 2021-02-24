#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
"""
champs intéressants de datetime
self.year, self.month, self.day, self.hour, self.minute, self.second
newDay = self.replace (day=4, month= self.month +3)
"""

class Date (datetime):

	def gapOld (self, newDate):
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

	def coucou (self):
		print ('coucou')

today = Date.now()
tomorow = today.replace (day=25)
tomorow.gap (today)


"""
print (tomorow)
	def __init__(self, year=0, month=1, day=1, hour=0, minute=20, second=0):
		datetime.__init__(self, year, month, day)
		# self = datetime.now()
"""
