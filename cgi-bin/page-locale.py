#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cgi, cgitb
cgitb.enable()

print ('Content-type: text/html; charset=utf-8')

html ="""
<!doctype html><html><head>
	<title>page locale</title>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<base target='_blank'>
<style type='text/css'>
	html { background-color: maroon; }
	body {
		color: maroon;
		background-color: pink;
		padding: 1em;
		padding-left: 3cm;
		width: 24cm;
	}
	* {
		color: inherit;
	}
</style></head><body>
	<h1>je suis la page locale</h1>
	<p>http://localhost:1407/cgi-bin/page-locale.py</p>
</body></html>"""

print (html)