#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


templateText ="""%s

================================================

Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""

templateTextOld ="""Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""

templateHtml = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_blank'/>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
	<meta name='autlink' content='%s'/>
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
	<meta name='autlink' content='%s'/>
	%s
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/perso.css' media='screen'/>
<style type='text/css'>
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

templateHtmlIndependant = """<!DOCTYPE html><html><head>
	<title>%s</title>
	<base target='_self'>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
	<meta name='autlink' content='%s'/>
<style type='text/css'>
	body {
		margin: auto;
		padding: 0.5em;
		background-color: ivory;
		color: #606;
		font-family: serif;
		font-size: 1.4em;
	}
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
		font-size: 1.5em;
		text-align: center;
		color: ivory;
		background-color: teal;
	}
	h2 {
		font-size: 1.2em;
		text-align: center;
		border-bottom: solid 2px teal;
	}
	section#sommaire { column-count: 2; }
	section#sommaire > a { display: block; }
	section#sommaire > a.h1 { font-weight: bold; }
</style></head><body>
%s
</body><script type='text/javascript'>
	var titles = document.getElementsByTagName ('h1');
	const titleH2 = document.getElementsByTagName ('h2')[0];
	var sommaire = "<section id='sommaire'>";
	// que des titres h1
	if (titleH2 === undefined && titles.length >0) for (var h=0; h< titles.length; h++){
		titles[h].id = 'title-' +h;
		sommaire = sommaire + "<a href='#title-" +h+ "'>" + titles[h].innerHTML + '</a>';
	}
	// titres h1 et h2
	else if (titleH2 !== undefined && titles.length >0){
		titles = document.querySelectorAll ('h1,h2');
		var h1nb =0;
		var h2nb =0;
		for (var h=0; h< titles.length; h++){
			if (titles[h].tagName === 'H1'){
				h1nb +=1;
				h2nb =0;
				titles[h].id = 'title-' + h1nb;
				sommaire = sommaire + "<a href='#title-" + h1nb + "' class='h1'>" + titles[h].innerHTML + '</a>';
			}
			else{
				h2nb +=1;
				titles[h].id = 'title-' + h1nb +'-'+ h2nb;
				sommaire = sommaire + "<a href='#title-" + h1nb +'-'+ h2nb + "'>" + titles[h].innerHTML + '</a>';
			}
		}
	}
	sommaire = sommaire + '</section>';
	document.body.innerHTML = sommaire + document.body.innerHTML;
</script></html>"""

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
	<meta name='autlink' content='%s'/>
%s
</head><body>
%s
</body></html>"""
