#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
from os import sep
from PIL import Image, ImageOps
from io import BytesIO
import base64
from textFct import *
from fileLocal import pathRoot
import loggerFct as log

listTagsContainer = ( 'ul', 'ol', 'dl', 'table', 'nav', 'div', 'fieldset', 'form', 'figure', 'math', 'section', 'article', 'body', 'header', 'footer', 'main' )
listTagsIntern =( 'i', 'b', 'em', 'span', 'strong', 'thead', 'tbody' )

def getTitleFromLink (link):
	d= link.rfind ('/')
	if '\\' in link: d= link.rfind ('\\')
	title = link[d+1:]
	if '.' in title:
		d= title.rfind ('.')
		if len (title -d) <11: title = title[:d]
	title = title.replace ('-'," ")
	title = title.replace ('_'," ")
	title = title.replace ('.'," ")
	while "  " in title: title = title.replace ("  "," ")
	return title

def imageFromBase64One (imgStr):
	buff = BytesIO (base64.b64decode (imgStr))
	return Image.open (buff)

def imgToB64One (imageName):
	imageOriginal = Image.open (imageName)
	imageOriginal = imageOriginal.convert ('RGB')
	buff = BytesIO()
	if imageName[-3:] == 'jpg': imageOriginal.save (buff, format='jpeg')
	else: imageOriginal.save (buff, format=imageName[-3:])
	imgStr = base64.b64encode (buff.getvalue())
	imgStr = 'data:image/' + imageName[-3:] + ';base64,' + str (imgStr)[2:-1]
	return imgStr

def imgToB64 (text):
	if 'src=' in text:
		text = text.replace ("src='http", "scr='http")
		text = text.replace ('src="http', 'scr="http')
		if 'src=' in text:
			textList = text.split ('src=')
			textRange = range (1, len (textList))
			for t in textRange:
			#	if textList[t][1:5] == 'http': continue
				f= textList[t].find (textList[t][0], 2)
				if textList[t][f-4:f] not in '.bmp .png .gif .jpg': continue
				imageName = textList[t][1:f].replace ('/', sep)
				if pathRoot not in imageName: continue
				imgStr = imgToB64One (imageName)
				textList[t] = textList[t][0] + imgStr + textList[t][f:]
			text = 'src='.join (textList)
		text = text.replace ('scr=', 'src=')
	return text
