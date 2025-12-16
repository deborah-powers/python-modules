#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

templateTextMeta ="""==

sujet: %s
auteur: %s
lien: %s
%s"""

templateText = '%s\n\n' + templateTextMeta

templateHtml = """<!DOCTYPE html><html lang='fr-Fr'><head>
	<title>%s</title>
	<base target='_blank'/>
	<meta charset='utf-8'/>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta name='subject' content='%s'/>
	<meta name='author' content='%s'/>
	<meta name='link' content='%s'/>
%s
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/structure.css' />
	<link rel='stylesheet' type='text/css' href='file:///C:/wamp64/www/site-dp/library-css/perso.css' media='screen' />
</head><body>
%s
</body></html>"""

templateEreaderCss ="""
<style type='text/css' media='(max-width: 350px)'>
	* {
		box-sizing: border-box;
		padding: 0;
		margin: 0 0 1em 0;
		font-size: 1em;
		line-height: 1.5em;
		font-family: inherit;
		font-style: normal;
		font-weight: normal;
		text-decoration: none;
		background: none;
		color: black;
	}
	body { padding: 0 0.5em; }
	*:first-letter, title:first-letter { text-transform: uppercase; }
	h1 {
		font-size: 1.5em;
		background-color: #444;
		color: white;
		text-align: center;
	}
	dt {
		color: #444;
		float: left;
		clear: left;
		margin-right: 0.5em;
	}
	dt:after { content: ':'; }
	/*
	dl >* { display: block; }
	dt {
		color: #444;
		width: 90%%;
	}
	dt:after {
		content: ':';
		width: 5%%;
	}
	dd {
		margin-left: 0;
		width: 100%%;
	}
	*/
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
</style>"""
templateTheaterCssA ="""
<style type='text/css'>
	p.didascalie, span { font-style: italic; }
	span:before { content: '('; }
	span:after { content: ')'; }
	@media (min-width: 350px){
		dl { grid-template-columns: 6em 1fr; }
		p { color: var(--bord-color); }
		p.moi { color: var(--text-color); }
	}
</style>"""
templateTheaterCssB = '\n\tp { color: #444; }\n\tp.moi { color: black; }\n'
templateEreader = templateHtml % ('%s', '%s', '%s', '%s', templateEreaderCss, '%s')
templateEreader = templateEreader.replace (".css' />", ".css' media='(min-width: 350px)' />", 1)
templateEreader = templateEreader.replace ("media='screen' />", "media='screen and (min-width: 350px)' />", 1)
t= templateEreader.rfind ('</style>')
templateTheater = templateEreader[:t] + templateTheaterCssB + templateEreader[t:]
t= templateTheater.find ('<style ')
templateTheater = templateTheater[:t] + templateTheaterCssA + templateTheater[t:]

templateEreaderjs = """<script type='text/javascript'>
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
