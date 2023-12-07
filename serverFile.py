#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import textFct
import fileCls

htmlTest = """<html>
<head><title>serveur python</title></head>
<body>
<p>serveur python pour ouvrir des fichiers</p>
</body></html>
"""
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

	def readFile (self, postBody):
		fileToRead = fileCls.File (postBody['file'])
		fileToRead.read()
		if fileToRead.path[-5:] == '.html': fileToRead.text = textFct.cleanHtml (fileToRead.text)
		elif fileToRead.path[-4:] == '.css': fileToRead.text = textFct.cleanCss (fileToRead.text)
		else: fileToRead.text = textFct.cleanText (fileToRead.text)
		sendBody ={
			'title': fileToRead.title,
			'text': fileToRead.text
		}
		sendJson = json.dumps (sendBody)
		return sendJson

	def readArticle (self, postBody):
		fileToRead = fileCls.Article (postBody['file'])
		fileToRead.read()
		if fileToRead.path[-5:] == '.html': fileToRead.text = textFct.cleanHtml (fileToRead.text)
		else: fileToRead.text = textFct.cleanText (fileToRead.text)
		sendBody ={
			'title': fileToRead.title,
			'text': fileToRead.text,
			'author': "",
			'authLink': "",
			'link': "",
			'subject': ""
		}
		sendBody['author'] = fileToRead.author
		sendBody['authLink'] = fileToRead.authLink
		sendBody['link'] = fileToRead.link
		sendBody['subject'] = fileToRead.subject
		sendJson = json.dumps (sendBody)
		return sendJson

	def writeFile (self, postBody):
		fileToRead = fileCls.File (postBody['file'])
		fileToRead.text = postBody['text']
		fileToRead.write()

	def writeArticle (self, postBody):
		fileToRead = fileCls.Article (postBody['file'])
		fileToRead.author = postBody['author']
		fileToRead.authLink = postBody['authLink']
		fileToRead.link = postBody['link']
		fileToRead.subject = postBody['subject']
		fileToRead.text = postBody['text']
		fileToRead.write()

	"""
	def do_GET (self):
		self.send_response (200)
		self.end_headers()
		self.writeBody (htmlTest)
	"""

	def do_POST (self):
		""" lire un fichier
		postBody = { type: 'article', file: 'path/to/myfile.html', action: 'read' }
		"""
		self.send_response (200)
		self.end_headers()
		bodyTmp = self.readBody()
		postBody = json.loads (bodyTmp)
		sendBody ={ 'title': 'action inconnue', 'text': 'action inconnue '+ postBody['action'] }
		if postBody['action'] == 'read':
			if postBody['type'] == 'article': sendBody = self.readArticle (postBody)
			else: sendBody = self.readFile (postBody)
		elif postBody['action'] == 'write':
			if postBody['type'] == 'article': self.writeArticle (postBody)
			else: self.writeFile (postBody)
			sendBody['title'] = 'fichier écrit'
			sendBody['text'] = postBody['file']
		self.writeBody (sendBody)

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