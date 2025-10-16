#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
from textFct import *
from htmlFct import *
import loggerFct as log

def fromTable (text):
	text = text.replace ('</td>', "")
	text = text.replace ('</th>', ':')
	text = text.replace ('</tr>', "")
	text = text.replace ('<tr><td>', '\n')
	text = text.replace ('<tr><th>', '\n')
	text = text.replace ('<td>', '\t')
	text = text.replace ('<th>', '\t')
	return text

def fromImage (text):
	textList = text.split ('<img ')
	textRange = range (1, len (textList))
	for t in textRange:
		src =""
		alt =""
		f= textList[t].find ('>')
		if 'src=' in textList[t][:f]:
			d=5+ textList[t].find ('src=')
			e= textList[t].find (textList[t][d-1], d)
			src = textList[t][d:e]
		if 'alt=' in textList[t][:f]:
			d=5+ textList[t].find ('alt=')
			e= textList[t].find (textList[t][d-1], d)
			alt = textList[t][d:e]
		"""
		else:
			e= src.rfind ('.')
			d= src.rfind ('/')
			if '\\' in src: d= src.rfind ('\\')
			alt = src[d+1:f]
		textList[t] = alt +' ('+ src +') '+ textList[t][f+1:]
		"""
		if alt: src = src +' ('+ alt +')'	# inverse de la méthode de htmlFromText
		textList[t] = src +" "+ textList[t][f+1:]
	text = '\n'.join (textList)
	# text = '\nimg\t'.join (textList)
	return text

def fromLink (text):
	textList = text.split ('</a>')
	textRange = range (len (textList) -1)
	for t in textRange:
		title =""
		link =""
		f= textList[t].rfind ('>')
		if f>=0: title = textList[t][f+1:]
		if 'href=' in textList[t][:f]:
			textList[t] = textList[t][:f-1]
			d=6+ textList[t].rfind ('href=')
			f= textList[t].find (textList[t][d-1], d)
			link = textList[t][d:f]
		"""
		if not title:
			d= link.rfind ('/')
			if '\\' in src: d= link.rfind ('\\')
			title = link[d+1:]
			if '.' in title:
				f= title.rfind ('.')
				title = title[:f]
		"""
		f= textList[t].rfind ('<a')
		textList[t] = textList[t][:f] +" "+ link
		if title: textList[t] = textList[t] +' ('+ title +') '	# inverse de la méthode de htmlFromText
		"""
		textList[t] = textList[t][:f] +" "+ title +' ('+ link +') '
		textList[t] = textList[t][:f] +" "+ title +': '+ link
		"""
	text = " ".join (textList)
	return text

def fromHtml (text):
	# les conteneurs
	tagsBlank =( ('<hr/>', '\n**\n'), ('<hr>', '\n**\n'), ('<br>', '\n'), ('<br/>', '\n'))
	tagsClosing =( 'li', 'dd', 'tr', 'th', 'td', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
	for tag in listTagsContainer:
		text = text.replace ('</'+ tag +'>', "")
		text = text.replace ('<'+ tag +'>', "")
	text = fromTable (text)
	text = fromImage (text)
	# les tags
	for html, perso in tagHtml: text = text.replace (html.strip(), perso)
	for html, perso in tagsBlank: text = text.replace (html, perso)
	for tag in tagsClosing: text = text.replace ('</'+ tag +'>', "")
	# les lignes
	text = text.replace ('</p><p>', '\n')
	lines =( 'p', 'caption', 'figcaption' )
	for tag in lines:
		text = text.replace ('</'+ tag +'>', '\n')
		text = text.replace ('<'+ tag +'>', '\n')
	# les phrases
	for tag in listTagsIntern:
		text = text.replace ('</'+ tag +'>', " ")
		text = text.replace ('<'+ tag +'>', " ")
	text = text.replace (' \n', '\n')
	text = text.replace ('\n ', '\n')
	text = fromLink (text)
	text = shape (text)
	return text

