#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from textFct import *


class Text (str):
	def __new__(cls, value):
		# explicitly only pass value to the str constructor
		return super (WcStr, cls).__new__ (cls, value)

	def clean (self):
		return cleanBasic (self)

	def cleanText (self):
		return cleanText (self)

	def coucou (self):
		print ('coucou '+ self)


myText = 'hello'
myText.coucou()
newText = myText.cleanText()

""" source: https://realpython.com/inherit-python-str/
https://eli.thegreenplace.net/2010/06/30/python-internals-adding-a-new-statement-to-python/
"""
