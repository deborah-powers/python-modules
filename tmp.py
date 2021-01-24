#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from logger import Logger

log = Logger()
log.log ('a')
log.coucou()

class Test():
	def __init__ (self):
		self.a = 'a'
		log.log ('b')

	def printC (self):
		log.log ('c')

test = Test()
test.printC()