#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
""" ouvrir des fichiers via un navigateur
dépendences js:
	text.js
	fileBackend.js
"""
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
fileArticle = 'b/	.html'

def findPath (postBody):
	path =""
	if 'path' in postBody.keys(): path = postBody['path']
	else: path = fileArticle.replace ('\t', postBody['title'])
	return path

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

	def readArticle (self, postBody):
		fileToRead = fileCls.Article (postBody['file'])
		fileToRead.read()
		if fileToRead.path[-5:] == '.html': fileToRead.text = textFct.cleanHtml (fileToRead.text)
		else: fileToRead.text = textFct.cleanText (fileToRead.text)
		sendBody ={
			'title': fileToRead.title,
			'text': fileToRead.text,
			'path': fileToRead.path,
			'author': fileToRead.author,
			'link': fileToRead.link,
			'authLink': fileToRead.authLink,
			'subject': fileToRead.subject
		}
		return sendBody

	def readFile (self, postBody):
		fileToRead = fileCls.File (postBody['file'])
		fileToRead.read()
		if fileToRead.path[-5:] == '.html': fileToRead.text = textFct.cleanHtml (fileToRead.text)
		elif fileToRead.path[-4:] == '.css': fileToRead.text = textFct.cleanCss (fileToRead.text)
		else: fileToRead.text = textFct.cleanText (fileToRead.text)
		sendBody ={
			'title': fileToRead.title,
			'text': fileToRead.text,
			'path': fileToRead.path
		}
		return sendBody

	def writeFile (self, postBody):
		path = findPath (postBody)
		fileToRead = fileCls.Article (path)
		fileToRead.link = postBody['link']
		fileToRead.text = postBody['text']
		fileToRead.author ='o'
		fileToRead.authLink ='o'
		fileToRead.subject ='o'
		fileToRead.write()

	def writeArticle (self, postBody):
		path = findPath (postBody)
		fileToRead = fileCls.Article (path)
		fileToRead.link = postBody['link']
		fileToRead.text = postBody['text']
		fileToRead.author = postBody['author']
		fileToRead.authLink = postBody['authLink']
		fileToRead.subject = postBody['subject']
		fileToRead.write()

	"""
	def do_GET (self):
		self.send_response (200)
		self.end_headers()
		self.writeBody (htmlTest)
	"""

	def do_POST (self):
		""" lire un fichier
		postBody = { text: 'mon long texte à écrire', path: 'path/to/myfile.html' }
		"""
		self.send_response (200)
		self.end_headers()
		bodyTmp = self.readBody()
		postBody = json.loads (bodyTmp)
		sendBody ={}
		if 'text' in postBody.keys():
			if 'author' in postBody.keys(): self.writeArticle (postBody)
			else: self.writeFile (postBody)
			sendBody['reponse'] = 'fichier écrit'
		elif 'type' in postBody.keys() and postBody['type'] == 'text': sendBody = self.readFile (postBody)
		else: sendBody = self.readArticle (postBody)
		sendJson = json.dumps (sendBody)
		self.writeBody (sendJson)

if __name__ == '__main__':
	test (BackEndCors, HTTPServer, port=1407)

"""
url correspondant à index.html
http://localhost:1407/
si je rajoute une fonction do_GET à ma classe, le html du fichier est écrasé.
il faut générer du nouveau html dynamiquement grâce à self.wfile()
"""