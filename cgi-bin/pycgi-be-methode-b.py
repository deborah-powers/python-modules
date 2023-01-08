#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cgi, cgitb
cgitb.enable()
# cgitb.enable (display=0, logdir='/home/lenovo/Bureau/logs')

print ('Content-type: text/html; charset=utf-8')
form = cgi.FieldStorage()

htmlHead ="""
<!doctype html>
<html>
<head>
	<title>test de cgi avec python, méthode du formulaire</title>
	<meta name='Content-type' content='text/html'/>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<base target='_blank'>
	<style type='text/css'>
		* { color: maroon; }
	</style>
</head>
<body>
	<h1>test de cgi avec python, méthode du formulaire</h1>
	<p>je suis la page de réponse</p>
	"""
htmlFoot = """
</body></html>"""

print (htmlHead)
if form.getvalue ('message'): print ('<p>le message est '+ form.getvalue ('message') +'</p>')
else: print ('<p>pas de message</p>')
print (htmlFoot)