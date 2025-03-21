#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
from os import sep
from PIL import Image, ImageOps
from io import BytesIO
import base64
from textFct import *
from htmlFct import *
from fileLocal import pathRoot
import loggerFct as log

def fromHtml (text):
	# les conteneurs
	tagsBlank =( ('<hr/>', '\n************\n'), ('<hr>', '\n************\n'), ('<br>', '\n'), ('<br/>', '\n'))
	tagsClosing =( 'li', 'dd', 'tr', 'th', 'td')
	for tag in listTagsContainer:
		text = text.replace ('</'+ tag +'>', "")
		text = text.replace ('<'+ tag +'>', "")
	# les tableaux
	text = text.replace ('</td>', "")
	text = text.replace ('</th>', ':')
	text = text.replace ('</tr>', "")
	text = text.replace ('<tr><td>', '\n')
	text = text.replace ('<tr><th>', '\n')
	text = text.replace ('<td>', '\t')
	text = text.replace ('<th>', '\t')
	# les images
	textList = text.split ('<img ')
	textRange = range (1, len (textList))
	for i in textRange:
		src =""
		alt =""
		f= textList[i].find ('>')
		if 'src=' in textList[i][:f]:
			d=5+ textList[i].find ('src=')
			e= textList[i].find (textList[i][d-1], d)
			src = textList[i][d:e]
		if 'alt=' in textList[i][:f]:
			d=5+ textList[i].find ('alt=')
			e= textList[i].find (textList[i][d-1], d)
			alt = textList[i][d:e]
		else:
			e= src.rfind ('.')
			d= src.rfind ('/')
			if '\\' in src: d= src.rfind ('\\')
			alt = src[d+1:f]
		textList[i] = alt +' ('+ src +') '+ textList[i][f+1:] +'\n'
	text = '\nimg\t'.join (textList)
	# les liens
	textList = text.split ('</a>')
	textRange = range (len (textList) -1)
	for i in textRange:
		linkText =""
		link =""
		f= textList[i].rfind ('>')
		if f>=0: linkText = textList[i][f+1:]
		if 'href=' in textList[i][:f]:
			textList[i] = textList[i][:f-1]
			d=6+ textList[i].rfind ('href=')
			f= textList[i].find (textList[i][d-1], d)
			link = textList[i][d:f]
		if not linkText:
			d= link.rfind ('/')
			if '\\' in src: d= link.rfind ('\\')
			linkText = link[d+1:]
			if '.' in linkText:
				f= linkText.rfind ('.')
				linkText = linkText[:f]
		f= textList[i].rfind ('<a')
		textList[i] = textList[i][:f] +" "+ linkText +' ('+ link +') '
	text = "".join (textList)
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
		text = text.replace ('</'+ tag +'>', ' ')
		text = text.replace ('<'+ tag +'>', ' ')
	text = text.replace (' \n', '\n')
	text = text.replace ('\n ', '\n')
	# les liens
	ltext = text.split ('</a>')
	rtext = range (len (ltext) -1)
	for t in rtext:
		d= ltext [t].find ('href') +6
		f= ltext [t].find ("'", d)
		link = ltext [t][d:f]
		f= ltext [t].find ('>', f) +1
		title = ltext [t][f:]
		d= ltext [t].find ('<a ')
		ltext [t] = ltext [t][:d] +' '+ title +': '+ link
	text = ' '.join (ltext)
	text = shape (text)
	return text

