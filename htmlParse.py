#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from html.parser import HTMLParser

"""
https://docs.python.org/3/library/html.parser.html
"""

htmlText = """
<!DOCTYPE html><html><head>
	<title>page de test</title>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<link rel='icon' type='image/svg+xml' href='../../site-dp/data/nounours-perso.svg'/>
	<link rel='stylesheet' type='text/css' href='../../site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='../../site-dp/library-css/perso.css' media='screen'/>
<style type='text/css'>
	h1 { text-align: center; }
</style></head><body>
	<h1>bonjour !</h1>
	<p>je suis Deborah</p>
	<p class='coco' color='green'>je suis Deborah</p>
</body></html>
"""

class MyHTMLParser (HTMLParser):
    def handle_starttag (self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)

    def handle_endtag (self, tag):
        print("Encountered an end tag :", tag)

    def handle_data (self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed (htmlText)