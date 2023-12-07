#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import textFct
from htmlCls import Html


htmlTest = """<html>
<head><title>serveur python</title></head>
<body>
<p>serveur python pour ouvrir des fichiers</p>
</body></html>
"""
fileHtml = Html ('b/nouvel-article.html')

def cleanTitle (title):
	chars = "\t\n\\'.:;,_-/"
	for char in chars: title = title.replace (char,' ')
	title = title.strip()
	title = title.lower()
	while '  ' in title: title = title.replace ('  ',' ')
	return title

class BackEndCors (SimpleHTTPRequestHandler):
	def end_headers (self):
		self.send_header ('Access-Control-Allow-Origin', '*')
		self.send_header ('Access-Control-Allow-Methods', '*')
		self.send_header ('Access-Control-Allow-Headers', '*')
		SimpleHTTPRequestHandler.end_headers (self)

	def readBody (self):
		# rfile.read renvoie un texte en byte, il faut le transformer en string
		bodyLen = int (self.headers.get ('Content-Length'))
		bodyText =""
		if bodyLen >0: bodyText = self.rfile.read (bodyLen).decode('utf-8')
		return bodyText

	def writeBody (self, text):
		# wfile.write prend un texte en bytes comme argument, il faut parser les strings
		self.wfile.write (bytes (text, 'utf-8'))
	#	self.wfile.close()

	def do_GET (self):
		self.send_response (200)
		self.end_headers()
		self.writeBody (htmlTest)

	def do_POST (self):
		self.send_response (200)
		self.end_headers()
		postBody = json.loads (self.readBody())
		fileHtml.title = textFct.cleanHtml (postBody['title'])
		fileHtml.title = cleanTitle (fileHtml.title)
		fileHtml.text = textFct.cleanHtml (postBody['body'])
		fileHtml.link = postBody['link']
		fileHtml.write()
		self.writeBody ('ok')

if __name__ == '__main__':
	test (BackEndCors, HTTPServer, port=1407)

"""
url correspondant à index.html
http://localhost:1407/
si je rajoute une fonction do_GET à ma classe, le html du fichier est écrasé.
il faut générer du nouveau html dynamiquement grâce à self.wfile()

pour utiliser le script comme back-end dans un fichier js
const url = 'http://localhost:1407/server.py';
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function(){ if (this.readyState ==4) console.log (this.responseText); };
xhttp.open ('GET', url, true);
xhttp.send();
"""