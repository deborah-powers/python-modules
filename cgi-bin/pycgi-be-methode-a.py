#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
import sys
import json
import cgi
import cgitb

sys.path.append ('/home/lenovo/Bureau/python/')
import fileClass

cgitb.enable()
print ('Content-type: text/html; charset=utf-8')
print ('Access-Control-Allow-Origin: *')
print ('Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS')
print ('Access-Control-Allow-Headers: Content-Type')
print ("")

responseDict ={ 'response': 'pas de message' }
form = cgi.FieldStorage()
if form.getvalue ('message'): responseDict ['response'] = 'le message est '+ form.getvalue ('message')
responseJson = json.dumps (responseDict)
print (responseJson)

fileJson = fileClass.FilePerso ('b/cgi-bin/pycgi-result.json')
fileJson.dataFromFile()
fileJson.text = str (responseJson)
fileJson.toFile()

