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
		d=6+ textList[t].rfind ('href=')
		f= textList[t].find (textList[t][d-1], d+1)
		link = textList[t][d:f]
		f=1+ textList[t].find ('>', f)
		title = textList[t][f:]
		d= textList[t].rfind ('<a ')
		textList[t] = textList[t][:d]
		textList[t] = textList[t] + link +' ('+ title +')'	# inverse de la méthode de htmlFromText
	text = " ".join (textList)
	text = text.replace (' <','<')
	text = text.replace ('> ','>')
	return text

def fromHtml (text):
	text = cleanHtml (text)
	text = text.replace ('</dt><dd>', ': ')
	text = fromLink (text)
	# les conteneurs
	tagsBlank =( ('<hr/>', '\n**\n'), ('<hr>', '\n**\n'), ('<br>', '\n'), ('<br/>', '\n'), ('<dt>', '\n'), ('<xmp>', '\nCode\n'), ('</xmp>', '\n/\n'), ('<figure>', '\nFigure\n'), ('</figure>', '\n/\n'))
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
	text = shape (text)
	return text

