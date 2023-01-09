#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
from fileCls import File

html = """<html>
<head><title>Title goes here.</title></head>
<body>
<p>This is a test.</p>
</body></html>
"""

fileHtml = File ('b/test-be.html')

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
		self.writeBody (html)

	def do_POST (self):
		self.send_response (200)
		self.end_headers()
		postBody = self.readBody()
		pBody = postBody.find ('\n\n')
		fileHtml.title = postBody [:pBody]
		if not fileHtml.title or len (fileHtml.title) <3: fileHtml.title = 'tmp'
		fileHtml.text = postBody [pBody +2:]
		fileHtml.write()
		self.writeBody ('ok '+ fileHtml.title)



if __name__ == '__main__':
	test (BackEndCors, HTTPServer, port=1407)

"""
url correspondant à index.html
http://localhost:1407/
si je rajoute une fonction do_GET à ma classe, le html du fichier est écrasé.
il faut générer du nouveau html dynamiquement grâce à self.wfile()

pour utiliser le script comme back-end dans un fichier js
const url = 'http://localhost:1407/test.py';
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function(){ if (this.readyState ==4) console.log (this.responseText); };
xhttp.open ('GET', url, true);
xhttp.send();
"""