#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
""" traiter les images
from os import sep
from PIL import Image
from io import BytesIO
import base64
from fileLocal import pathRoot
"""
from textFct import *
import loggerFct as log

listTagsContainer =( 'ul', 'ol', 'dl', 'table', 'nav', 'div', 'fieldset', 'form', 'figure', 'math', 'section', 'article', 'body', 'header', 'footer', 'main' )
listTagsIntern =( 'i', 'b', 'em', 'span', 'strong', 'thead', 'tbody' )
tagHtml =(
	('\n<h1>', '\n== '), ('\n<h2>', '\n** '), ('\n<h3>', '\n-- '), ('\n<h4>', '\n__ '), ('\n<h5>', '\n## '), ('\n<h6>', '\n++ '),
	("\n<hr class='h1'/>\n", '\n\n==\n\n'), ("\n<hr class='h2'/>\n", '\n\n**\n\n'), ("\n<hr class='h3'/>\n", '\n\n--\n\n'),
	("\n<hr>\n", '\n\n**\n\n'), ("\n<hr/>\n", '\n\n**\n\n'),
	('\n<figure>', '\nFig\n'), ('\n<xmp>!', '\nCode\n'), ('\n<xmp>: ', '\nCode: '), ('\n<li>', '\n\t')
)

def findTitleFromUrl (link):
	if link[-1] == '/' or link[-1] == '\\': link = link[:-1]
	pos =0
	if '/' in link: pos =1+ link.rfind ('/')
	elif '\\' in link: pos =1+ link.rfind ('\\')
	title = link[pos:]
	if '.' in title:
		pos = title.rfind ('.')
		if len (title) -pos <11: title = title[:pos]
	title = title.replace ('www.',"")
	urlWords =( '-', '_', '.', '?', '#', '%20' );
	for word in urlWords: title = title.replace (word, " ")
	while "  " in title: title = title.replace ("  "," ")
	return title

"""
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
"""

def cleanHtmlForWritting (text):
	if '</xmp>' in text: text = cleanBasic (text)
	else: text = cleanHtml (text)
	innerTags =( 'i', 'b', 'em', 'span', 'strong', 'a')
	for tag in listTagsIntern:
		text = text.replace ('<'+ tag +'>', ' <'+ tag +'>')
		text = text.replace ('</'+ tag +'>', '</'+ tag +'> ')
	text = text.replace ('</a>', '</a> ')
	text = text.replace ("<a ", " <a ")
	while "  " in text: text = text.replace ("  ", " ")
	text = text.replace ('> <', '><')
	points = '.,)'
	for p in points: text = text.replace (" "+p, p)
	text = text.replace ("( ", '(')
	for tag in innerTags:
		for tig in innerTags: text = text.replace ('</'+ tag + '><'+ tig +'>', '</'+ tag + '> <'+ tig +'>')
	return text
