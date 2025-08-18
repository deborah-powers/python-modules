#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

templateTextMeta ="""==

sujet: %s
auteur: %s
lien: %s
%s"""

templateText = '%s\n\n' + templateTextMeta

templateHtml = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_blank'/>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
%s
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/perso.css' media='screen'/>
</head><body>
%s
</body></html>"""

templateHtmlEreader = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_self'>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
	%s
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/perso.css' media='screen'/>
<!-- style type='text/css' media='(width: 295px) and (height: 380px)' -->
<style type='text/css' media='(max-width: 600px)'>
	* {
		box-sizing: border-box;
		padding: 0;
		margin-bottom: 1em;
		font-size: 1em;
		font-family: inherit;
		font-style: normal;
		font-weight: normal;
		text-decoration: none;
		line-height: 1.5em;
		color: inherit;
		background: none;
	}
	*:first-letter, title:first-letter { text-transform: uppercase; }
	h1 {
		font-size: 1.2em;
		text-align: center;
		font-weight: bold;
		border-top: double 6px grey;
		border-bottom: solid 2px grey;
	}
	h2 {
		font-size: 1.2em;
		text-align: center;
		color: white;
		background-color: grey;
	}
	h3 {
		font-weight: bold;
		text-align: center;
	}
	h4 { font-style: italic; }
	ul { margin-left: 2em; }
	img { max-width: 100%%; }
	dl { width: 100%%; }
	dl >* { display: inline-block; }
	dt {
		min-width: 6em;
		max-width: 30%%;
	}
	dd {
		min-width: 10em;
		max-width: 70%%;
	}
/*	dt {
		float: left;
		clear: left;
		min-width: 6em;
		display: inline-block;
	}
	dd {
		float: right;
		clear: right;
		min-width: 10em;
		display: inline-block;
	}*/
	dt:after { content: ' :'; }
</style></head><body>
%s
</body></html>"""

templateHtmlEreaderjs = """<script type='text/javascript'>
	var titles = document.getElementsByTagName ('h1');
	var sommaire = "<section id='sommaire'>";
	// que des titres h1
	for (var h=0; h< titles.length; h++){
		titles[h].id = 'title-' +h;
		sommaire = sommaire + "<a href='#title-" +h+ "'>" + titles[h].innerHTML + '</a>';
	}
	sommaire = sommaire + '</section>';
	document.body.innerHTML = sommaire + document.body.innerHTML;
</script>"""

templateXhtml ="""<?xml version='1.0' encoding='utf-8'?>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='fr'>
<head>
	<title>%s</title>
	<meta name='viewport' content='width=device-width,initial-scale=1'/>
	<meta charset='utf-8'/>
	<link rel='stylesheet' type='text/css' href='/var/www/html/site-dp/library-css/structure.css'/>
	<link rel='stylesheet' type='text/css' href='/var/www/html/site-dp/library-css/perso.css' media='screen'/>
	<link rel='stylesheet' type='text/css' href='../liseuse.css'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
%s
</head><body>
%s
</body></html>"""
