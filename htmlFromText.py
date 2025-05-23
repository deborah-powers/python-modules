#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
from os import sep
from PIL import Image
from io import BytesIO
import base64
from textFct import *
from htmlFct import *
from fileLocal import pathRoot
import loggerFct as log

protocols =( 'https://', 'http://', 'file:///' )

def toList (text):
	if '<li>' in text:
		text = '\n'+ text +'\n'
		textList = text.split ('\n')
		lc= range (len (textList))
		# rajouter les balises fermantes
		for l in lc:
			if '<li>' in textList[l]: textList[l] = textList[l] +'</li>'
		lc= range (1, len (textList) -1)
		# rajouter les balises ouvrantes et fermantes delimitant la liste, <ul/>. reperer les listes imbriquees.
		for l in lc:
			if '<li>' in textList[l]:
				# compter le niveau d'imbrication (n) de l'element textList[l]
				n=0
				while '<li>'+n*'\t' in textList[l]: n+=1
				n-=1
				if '<li>'+n*'\t' in textList[l]:
					# debut de la liste (ou sous-liste), mettre le <ul>
					if '<li>'+n*'\t' not in textList [l-1]: textList[l] = '<ul>'+ textList[l]
					# fin de la liste (ou sous-liste), mettre le </ul>
					if '<li>'+n*'\t' not in textList [l+1]:
						while n >-1:
							if '<li>'+n*'\t' not in textList [l+1]: textList[l] = textList[l] + '</ul>'
							n-=1
		# mettre le texte au propre
		text = '\n'.join (textList)
		text = text.strip ('\n')
		while '<li>\t' in text: text = text.replace ('<li>\t', '<li>')
		while '<ul>\t' in text: text = text.replace ('<ul>\t', '<ul>')
		# liste ordonnée
		while '<li># ' in text:
			d= text.find ('<li># ')
			d= text[:d].rfind ('<ul>')
			text = text[:d] + '<ol>' + text[d+4:]
			f= text.find ('</ul>', d)
			while text[d:f].count ('<ul>') != text[d:f].count ('</ul>'): f= text.find ('</ul>', f+4)
			text = text[:f] + '</ol>' + text[f+5:]
			text = text.replace ('<li># ', '<li>', 1)
	return text

def toDefList (text):
	if ": " not in text: return text
	textList = text.split ('\n')
	textListLen = len (textList)
	d=-1; t=0
	while t< textListLen:
		if ": " in textList[t] and textList[t].count (": ") ==1 and d==-1: d=t
		elif ": " not in textList[t] and d>=0:
			if t-d >1:
				listRange = range (d,t)
				for l in listRange: textList[l] = '<dt>' + textList[l].replace (": ", '</dt><dd>') + '</dd>'
				textList[d] = textList[d].replace ('<dt>', '<dl><dt>')
				textList[t-1] = textList[t-1].replace ('</dd>', '</dd></dl>')
			d=-1
		t+=1
	text = '\n'.join (textList)
	text = text.replace ('\n<dt>', '<dt>')
	text = text.replace ('</dd>\n', '<dd>')
	return text

def toTable (text):
	if '\t' not in text: return text
	# les cases vides sont représentées par un point. les doubles tabulations ont été rajoutées pour une meilleure lisibilité au format txt
	while '\t\t' in text: text = text.replace ('\t\t', '\t')
	textList = text.split ('\n')
	len_chn = len (textList)
	d=-1; c=-1; i=0
	while i< len_chn:
		# rechercher une table
		d=-1; c=-1
		if d==-1 and c==-1 and '\t' in textList[i]:
			c= textList[i].count ('\t')
			d=i; i+=1
		while i< len_chn and textList[i].count ('\t') ==c: i+=1
		c=i-d
		# une table a ete trouve
		if c>1 and d>0:
			rtable = range (d, i)
			for j in rtable:
				# entre les cases
				textList [j] = textList [j].replace ('\t', '</td><td>')
				# bordure des cases
				textList [j] = '<tr><td>' + textList [j] +'</td></tr>'
			# les limites de la table
			textList [d] = '<table>' + textList [d]
			textList [i-1] = textList [i-1] +'</table>'
		i+=1
	text = '\n'.join (textList)
	text = text.replace ('\n<tr>', '<tr>')
	# les titres de colonnes ou de lignes
	if ':</td></tr>' in text:
		textList = text.split (':</td></tr>')
		paragraphRange = range (len (textList) -1)
		for p in paragraphRange:
			d= textList[p].rfind ('<tr><td>')
			textList[p] = textList[p][:d] +'<tr><th>'+ textList[p][d+8:].replace ('td>', 'th>')
		text = '</th></tr>'.join (textList)
	if ':</td>' in text:
		textList = text.split (':</td>')
		paragraphRange = range (len (textList) -1)
		for p in paragraphRange:
			d= textList[p].rfind ('<td>')
			textList[p] = textList[p][:d] +'<th>'+ textList[p][d+4:]
		text = '</th>'.join (textList)
	text = text.replace ('\t', "")
	text = text.replace ('<td>.</td>', '<td></td>')
	return text

def toImageProtocolExtension (text, protocol, extension):
	extension = '.'+ extension
	if protocol not in text or extension not in text: return text
	endingChars = '<;, !\t\n';
	textList = text.split (extension);
	textRange = range (len (textList) -1)
	for i in textRange:
		if protocol not in textList[i]: continue
		d= textList[i].rfind (protocol)
		title = textList[i][d:]
		for char in endingChars:
			if char in title: d=-1
		if d==-1: continue
		textList[i] = textList[i][:d]
		title = title.replace ('http', 'ht/tp');
		title = title.replace ('file', 'fi/le');
		url = title + extension
		# trouver la description
		if textList[i+1][:2] == " (":
			d= textList[i+1].find (')')
			title = textList[i+1][2:d]
			textList[i+1] = textList[i+1][d+1:].strip()
		elif textList[i][-2:] == ": ":
			d=3+ textList[i].rfind ('<p>')
			title = textList[i][d:-2]
			if '>' in title or '<' in title: title = findTitleFromUrl (url)
			else: textList[i] = textList[i][:d]
		else: title = findTitleFromUrl (url)
		url = "<img src='" + url + "' alt='" + title +"' />"
		textList[i] = textList[i] + url
	text = extension.join (textList)
	text = text.replace ('/>' + extension, '/>')
	return text

def toImage (text):
	imgExtension =( 'jpg', 'jpeg', 'bmp', 'gif', 'png')
	text = text.replace ('C://', 'file:///C://')
	text = text.replace ('C:\\', 'file:///C:\\')
	for protocol in protocols:
		for extension in imgExtension: text = toImageProtocolExtension (text, protocol, extension)
	return text

def toImage_va (text):
	imgExtension =( 'jpg', 'jpeg', 'bmp', 'gif', 'png')
	imgCharStart = '>\n\t\'",;!()[]{}:'
	for ext in imgExtension:
		if '.'+ ext in text:
			textList = text.split ('.'+ ext)
			textRange = range (len (textList) -1)
			for i in textRange:
				d= textList[i].rfind (':')
				f= textList[i][:d].rfind (' ')
				for char in imgCharStart:
					e= textList[i][:d].rfind (char)
					if e>f: f=e
				f=f+1
				title = textList[i][f+1:].replace ('-'," ")
				if textList[i+1][:2] == ' (':
					e= textList[i+1].find (')')
					title = textList[i+1][2:e]
					textList[i+1] = textList[i+1][e+1:]
					title = title.replace ('-'," ")
				else: title = findTitleFromUrl (title)
				title = title.replace ('_'," ")
				title = title.replace ('.'," ")
				url = textList[i][f:].replace ('http', 'ht/tp')
				url = url.replace ('file', 'fi/le')
				textList[i] = textList[i][:f] + "<img src='" + url +"."+ ext +"' alt='" + title +"'/>"
			text = "".join (textList)
	return text

def toLinkProtocol (text, protocol):
	if protocol not in text: return text
	endingChars = '<;, !\t\n'
	textList = text.split (protocol)
	paragraphRange = range (1, len (textList))
	for p in paragraphRange:
		paragraphTmp = textList[p]
		e=-1; f=-1; d=-1
		for char in endingChars:
			if char in paragraphTmp:
				f= paragraphTmp.find (char)
				paragraphTmp = paragraphTmp [:f]
		paragraphTmp = paragraphTmp.strip ('/')
		d= paragraphTmp.rfind ('/') +1
		e= len (paragraphTmp)
		if '.' in paragraphTmp[d:]: e= paragraphTmp.rfind ('.')
		title =""
		if textList[p][f:f+2] == ' (':
			e= textList[p].find (')')
			title = textList[p][f+2:e]
			textList[p] = textList[p][e+1:]
		elif ': '== textList[p-1][-2:]:
			d=3+ textList[p-1].rfind ('<p>')
			title = textList[p-1][d:-2]
			if '>' in title or '<' in title: title = findTitleFromUrl (paragraphTmp)
			else: textList[p-1] = textList[p-1][:d]
			d= textList[p].find ('</p>')
			textList[p] = textList[p][d:]
		else:
			textList[p] = textList[p][f:]
			title = findTitleFromUrl (paragraphTmp)
		textList[p] = paragraphTmp +"'>"+ title +'</a> '+ textList[p]
	text = (" <a href='" + protocol).join (textList)
	text = text.replace ('> <a ', '><a ')
	return text

def toLink (text):
	text = text.replace ('c:/', 'file:///c:/')
	text = text.replace ('file:///file:///', 'file:///')
	for protocol in protocols: text = toLinkProtocol (text, protocol)
	return text

def toEmphasis (text):
	if '\n* ' in text:
		textList = text.split ('\n* ')
		lc= range (len (textList))
		# rajouter les balises fermantes
		for l in lc:
			if ': ' in textList[l][1:100]:
				textList[l] = textList[l].replace (': ',':</strong> ',1)
				textList[l] = '<strong>' + textList[l]
		text = '\n'.join (textList)
	return text

def toMath (text):
	if '\nM\t' in text:
		textList = text.split ('\n')
		paragraphRange = range (1, len (textList))
		for i in paragraphRange:
			if textList[i][:2] == 'M\t':
				if 'f/' in textList[i]:
					textList[i] = textList[i].replace (' f/ ', '<mfrac><mrow>')
					textList[i] = textList[i].replace ('\tf/ ', '<mfrac><mrow>')
					textList[i] = textList[i].replace (' /f', '</mrow></mfrac>')
					if '</mfrac>' not in textList[i]: textList[i] = textList[i] + '</mrow></mfrac>'
					textList[i] = textList[i].replace (' / ', '</mrow><mrow>')
				textList[i] = '<math>' + textList[i][2:] + '</math>'
		text = '\n'.join (textList)
	return text

def toFigure (text):
	if '<figure>' in text:
		# mettre en forme le contenu des figures
		textList = text.split ('<figure>')
		paragraphRange= range (1, len (textList))
		for i in paragraphRange:
			f= textList[i].find ('<p>/</p>')
			fin = '</figure>' + textList[i][f+8:]
			textList[i] = textList[i][:f].strip()
			textList[i] = textList[i].strip ('\n\t ')
			# nettoyer le texte
			textList[i] = textList[i].replace ('/></p>', '/>')
			textList[i] = textList[i].replace ('<p><img', '<img')
			textList[i] = textList[i].replace ('<p>', '<figcaption>', 1)
			textList[i] = textList[i].replace ('</p>', '</figcaption>', 1)
			textList[i] = textList[i] + fin
		text = '<figure>'.join (textList)
	return text

def toCode (text):
	if '<xmp>' not in text: return text
	elif '<xmp>:' in text:
		textList = text.split ('\n<xmp>:')
		paragraphRange = range (1, len (textList))
		for t in paragraphRange:
			textList[t] = textList[t].replace ('\n', '</xmp>', 1)
		text = '<xmp>'.join (textList)
	if '<xmp>!' in text:
		textList = text.split ('<xmp>!')
		paragraphRange = range (1, len (textList))
		for i in paragraphRange:
			f= textList[i].find ('\n/\n')
			fin = '</xmp>' + textList[i][f+3:]
			textList[i] = textList[i][:f].strip()
			textList[i] = textList[i].strip ('\n\t ')
			textList[i] = textList[i].replace ('\n', '\a')
			textList[i] = textList[i].replace ('\t', '\f')
			textList[i] = textList[i] + fin
		text = '<xmp>'.join (textList)
		text = text.replace ('\a</xmp>', '</xmp>')
	return text

def toHtml (text):
	text = shape (text)
	# transformer la mise en page en balises
	text = '\n'+ text +'\n'
	for html, perso in tagHtml:
		if perso in text: text = text.replace (perso, html)
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	# compléter les tîtres
	textList = text.split ('\n')
	textRange = range (len (textList))
	for l in textRange:
		if textList[l][:2] != '<h' or textList[l][3] != '>' or textList[l][2] not in '123456': continue
		textList[l] = textList[l] +'</h'+ textList[l][2] +'>'
	text = '\n'.join (textList)
	# autres modifications
	text = toMath (text)
	text = toCode (text)
	text = toList (text)
	text = toTable (text)
	text = toDefList (text)
	text = cleanText (text)
	text = toEmphasis (text)
	# rajouter les <p/>
	text = text.replace ('\n', '</p><p>')
	text = text.replace ('></p><p><', '><')
	text = text.replace ('></p><p>', '><p>')
	text = text.replace ('</p><p><', '</p><')
	# rajouter d'eventuel <p/> s'il n'y a pas de balise en debut ou fin de text
	if '<' not in text [0:3]: text = '<p>'+ text
	if '>' not in text [-3:]: text = text +'</p>'
	# autres modifications
	text = toImage (text)
	text = toLink (text)
	# restaurer le texte, remplacer mes placeholders
	text = text.replace ('ht/tp', 'http')
	text = text.replace ('fi/le', 'file')
	text = text.replace ('\a', '\n')
	text = text.replace ('\f', '\t')
	text = cleanBasic (text)
	text = text.replace (' </', '</')
	text = text.replace ('<p>.</p>', '<br/>')
	text = toFigure (text)
	text = text.replace ('<p>-->', "<p class='arrow'>")
	return text
