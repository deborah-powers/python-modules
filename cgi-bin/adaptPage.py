#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import sys
import json
import cgi
import cgitb

sys.path.append ('/home/lenovo/Bureau/python/')
import htmlAtricle

cgitb.enable()
print ('Content-type: text/html; charset=utf-8')
print ('Access-Control-Allow-Origin: *')
print ('Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS')
print ('Access-Control-Allow-Headers: Content-Type')
print ("")

form = cgi.FieldStorage()
adress =""
if form.getvalue ('adress'): adress = form.getvalue ('adress')
adress = adress.replace (',','/')
article = htmlAtricle (adress)
article.formWeb()

responseDict ={
	'response': 'ok',
	'url': adress
}
responseJson = json.dumps (responseDict)
print (responseJson)
