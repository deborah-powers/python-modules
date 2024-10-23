#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# attention, l'ordre des sous-fonctions est important
from textFct import *

tagHtml =(
	('\n<h1>', '\n====== '), ('</h1>\n', ' ======\n'), ('\n<h2>', '\n****** '), ('</h2>\n', ' ******\n'), ('\n<h3>', '\n------ '), ('</h3>\n', ' ------\n'), ('\n<h4>', '\n______ '), ('</h4>\n', ' ______\n'),
	('\n<hr>', '\n\n************************************************\n\n'), ("\n<img src='", '\nImg\t'), ('\n<figure>', '\nFig\n'), ('</figure>', '\n/fig\n'), ('\n<xmp>', '\ncode\n'), ('</xmp>', '\n/code\n'),
	('\n<li>', '\n\t')
)
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
			while '<li>#' in text:
				d= text.find ('<li># ')
				d= text[:d].rfind ('<ul>')
				text = text[:d] + '<ol>' + text[d+4:]
				f= text.find ('</ul>', d)
				while text[d:f].count ('<ul>') != text[d:f].count ('</ul>'): f= text.find ('</ul>', f+4)
				text = text[:f] + '</ol>' + text[f+5:]
				text = text.replace ('<li># ', '<li>', 1)
	return text

def toTable (text):
	if '\t' in text:
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
				textList [d] = '<table>\n' + textList [d]
				textList [i-1] = textList [i-1] +'\n</table>'
			i+=1
		text = '\n'.join (textList)
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

def toImage (text):
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
				else:
					if '/' in title:
						d=1+ title.rfind ('/')
						title = title[d:]
					if '\\' in title:
						d=1+ title.rfind ('\\')
						title = title[d:]
					if '.' in title:
						d=1+ title.rfind ('.')
						title = title[d:]
					title = cleanText (title)
				title = title.replace ('_'," ")
				title = title.replace ('.'," ")
				textList[i] = textList[i][:f] + "<img src='" + textList[i][f:].replace ('http', 'ht/tp') +"."+ ext +"' alt='" + title +"'/>"
			text = "".join (textList)
	return text

def toLink (text):
	endingChars = '<;, !\t\n'
	textList = text.split ('http')
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
		else:
			textList[p] = textList[p][f:]
			title = paragraphTmp [d:e].replace ('-',' ')
			title = title.replace ('_',' ')
			title = title.replace ('.'," ")
		textList[p] = paragraphTmp +"'>"+ title +'</a> '+ textList[p]
	text = " <a href='http".join (textList)
	text = text.replace ('> <a ', '><a ')
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
		textList = text.split ('figure>')
		paragraphRange= range (1, len (textList), 2)
		for i in paragraphRange:
			# nettoyer le texte pour faciliter sa transformation
			textList[i] = textList[i].strip ('\n')
			textList[i] = textList[i].split ('\n')
			paragraphRange = range (len (textList[i]) -1)
			for j in paragraphRange:
				# les images ont deja ete modifiees precedement
				if textList[i][j][:4] != '<img':
					textList[i][j] = '<figcaption>' + textList[i][j] + '</figcaption>'
			textList[i] = "".join (textList[i])
		text = 'figure>'.join (textList)
	return text

def toCode (text):
	if '<xmp>' in text:
		textList = text.split ('xmp>')
		paragraphRange = range (1, len (textList), 2)
		for i in paragraphRange:
			textList[i] = textList[i].strip()
			textList[i] = textList[i].strip ('\n\t ')
			textList[i] = textList[i].replace ('\n', '\a')
			textList[i] = textList[i].replace ('\t', '\f')
		text = 'xmp>'.join (textList)
		text = text.replace ('\a</xmp>', '</xmp>')
	return text

def toHtml (text):
	text = shape (text)
	for char in '=*-_': text = text.replace (12* char, 6* char)
	# transformer la mise en page en balises
	for html, perso in tagHtml:
		if perso in text: text = text.replace (perso, html)
	# autres modifications
	text = toMath (text)
	text = toFigure (text)
	text = toCode (text)
	text = toList (text)
	text = toTable (text)
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
	text = text.replace ('\a', '\n')
	text = text.replace ('\f', '\t')
	text = cleanHtml (text)
	text = text.replace (' </', '</')
	return text

def fromHtml (text):
	# les conteneurs
	container = [ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
	tagsBlank =( ('<hr/>', '\n************\n'), ('<hr>', '\n************\n'), ('<br>', '\n'), ('<br/>', '\n'))
	tagsClosing =( 'li', 'tr', 'th', 'td')
	for tag in container:
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
	# les tags
	for html, perso in tagHtml: text = text.replace (html.strip(), perso)
	for html, perso in tagsBlank: text = text.replace (html, perso)
	for tag in tagsClosing: text = text.replace ('</'+ tag +'>', "")
	# les lignes
	text = text.replace ('</p><p>', '\n')
	lines = [ 'p', 'caption', 'figcaption' ]
	for tag in lines:
		text = text.replace ('</'+ tag +'>', '\n')
		text = text.replace ('<'+ tag +'>', '\n')
	# les phrases
	inner = [ 'span', 'em', 'strong' ]
	for tag in inner:
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

def test():
	text = """nfznvvz
zef,z "ofk" v,sknvdzkl.fnz fk" g
à 50:30:60
adresse: http://www.fr
"""
	model = """fznvvz
%ssknvdzkl.fnz %s
"""
	text = toHtml (text)
	print ('toHtml\t', text)
	text = fromHtml (text)
	print ('fromHtml\t', text)
