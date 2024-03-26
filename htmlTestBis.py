#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from sys import argv
from html.parser import HTMLParser
from fileCls import File

"""
https://docs.python.org/3/library/html.parser.html
https://stackoverflow.com/questions/16773583/python-extracting-specific-data-with-html-parser
"""
fileName = 'b/test-py.html'
file = File (fileName)
file.read ()

def attributeExists (attributes, attrName):
	attrValue = None
	for name, value in attributes:
		if name == attrName:

class MyHTMLParser (HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.text =""

	def handle_starttag (self, tag, attrs):
		if tag == 'body': self.text = 'ok'

	def handle_data (self, data):
		if self.text == 'ok': self.text = data

parser = MyHTMLParser ()
parser.feed ("<html><head><title>Test</title></head><body><h1 id='parse'>Parse me!</h1><div backgroundColor='red'>a<div>b</div></div></body></html>")