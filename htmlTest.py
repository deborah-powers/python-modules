#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from sys import argv
from html.parser import HTMLParser
from fileCls import File

fileName = 'b/test-py.html'
file = File (fileName)
file.read ()

class MyHTMLParser (HTMLParser):
	def handle_starttag (self, tag, attrs):
		print ("Encountered a start tag:", tag)

	def handle_endtag (self, tag):
		print ("Encountered an end tag :", tag)

	def handle_data (self, data):
		print ("Encountered some data :", data)

parser = MyHTMLParser ()
parser.feed ('<html><head><title>Test</title></head><body><h1>Parse me!</h1><div>a<div>b</div></div></body></html>')
