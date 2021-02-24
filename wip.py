#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
"""
champs intéressants de datetime
self.year, self.month, self.day, self.hour, self.minute, self.second
newDay = self.replace (day=4, month= self.month +3)
"""
today = datetime.now()
print (today, today.__class__)

class Date (datetime):
	def __init__(self):
		self.now()

	def coucou (self):
		print ('coucou')

tomorow = Date()
print (tomorow)


"""
"""
