#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
lancer le serveur:
cd /var/www/
python -m http.server --cgi 1407
http://localhost:1407/cgi-bin/mon-folder/page.html
"""
import cgi, cgitb, json

# les cors
cgitb.enable()
print ('Content-type: text/html; charset=utf-8')
print ('Access-Control-Allow-Origin: *')
print ('Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS')
print ('Access-Control-Allow-Headers: Content-Type')
print ("")
# le formulaire
form = cgi.FieldStorage()

"""
if form.getvalue ('date'): print (form.getvalue ('date'))
dayJson = json.dumps (dayDict)
"""
