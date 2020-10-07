#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

help ="""convertir un fichier texte en fichier html
utilisation
	le script est appelable dans un fichier
"""

# balises
balises =( (' ______\n', '</h1>\n'), ('\n______\n______ ', '\n<h1>'), ('\n______ ', '\n<h2>'), ('\n------ ', '\n<h3>'), (' ------\n', '</h3>\n'), ('\n______\n', '\n<hr>\n'), ('\nImg\t', "\n<img src='") )
balises_internes = ('span', 'em', 'i', 'strong', 'b')
balises_externes = ('div', 'ul', 'table', 'math', 'figure')
balises_medianes = ('p', 'li', 'tr', 'figcaption', 'h1', 'h2', 'h3', 'h4', 'hr', 'img')

def creer_code (texte):
	"""
code
myfunc():
	mon code
x=y
/code
	"""
	texte = texte.replace ('\nCode\n', '\n<code>\n')
	texte = texte.replace ('\n/code\n', '\n</code>\n')
	list_chn = texte.split ('code>')
	lc= range (1, len (list_chn), 2)
	for i in lc:
#		nettoyer le texte pour faciliter sa transformation
		list_chn[i] = list_chn[i].strip ('\n')
		list_chn[i] = list_chn[i].split ('\n')
		ltexte = range (len (list_chn[i]) -1)
		k=0
		for j in ltexte:
			k=0
			while list_chn[i][j][k] == '\t': k+=1
			list_chn[i][j] = list_chn[i][j].strip ('\t')
			list_chn[i][j] = '>'+ list_chn[i][j] +'</p>'
			if k>0: list_chn[i][j] =(" class='indent-%d'" %j)+ list_chn[i][j]
			list_chn[i][j] = '<p'+ list_chn[i][j]
		list_chn[i] = "".join (list_chn[i])
	texte = 'code>'.join (list_chn)
	return texte

def creer_figure (texte):
	"""
fig
img	image.jpg
legende de l'image
/fig
	"""
#	transformer ma mise en page en balises html
	texte = texte.replace ('\nFig\n', '\n<figure>\n')
	texte = texte.replace ('\n/fig\n', '\n</figure>\n')
#	mettre en forme le contenu des figures
	list_chn = texte.split ('figure>')
	lc= range (1, len (list_chn), 2)
	for i in lc:
#		nettoyer le texte pour faciliter sa transformation
		list_chn[i] = list_chn[i].strip ('\n')
		list_chn[i] = list_chn[i].split ('\n')
		ltexte = range (len (list_chn[i]) -1)
		for j in ltexte:
#			les images ont deja ete modifiees precedement
			if list_chn[i][j][:4] != '<img':
				list_chn[i][j] = '<figcaption>' + list_chn[i][j] + '</figcaption>'
		list_chn[i] = "".join (list_chn[i])
	texte = 'figure>'.join (list_chn)
	return texte

def creer_liste (texte):
	"""
je vais faire mes courses:
	lait
	oeuf
	legumes
		haricots verts
		carottes
	yaourt
voila, j'ai tout trouve.
	"""
#	ajouter les balises ouvrantes des elements de la liste
	texte = '\n'+ texte +'\n'
	texte = texte.replace ('\n\t', '\n<li>')
#	separer les lignes pour permettre leurs transformation
	list_chn = texte.split ('\n')
	lc= range (len( list_chn))
#	rajouter les balises fermantes
	for l in lc:
		if '<li>' in list_chn[l]: list_chn[l] = list_chn[l] +'</li>'
	lc= range (1, len( list_chn) -1)
#	rajouter les balises ouvrantes et fermantes delimitant la liste, <ul/>. reperer les listes imbriquees.
	for l in lc:
		if '<li>' in list_chn[l]:
#			compter le niveau d'imbrication (n) de l'element list_chn[l]
			n=0
			while '<li>'+n*'\t' in list_chn[l]: n+=1
			n-=1
			if '<li>'+n*'\t' in list_chn[l]:
#				debut de la liste (ou sous-liste), mettre le <ul>
				if '<li>'+n*'\t' not in list_chn[l-1]: list_chn[l] = '<ul>'+ list_chn[l]
#				fin de la liste (ou sous-liste), mettre le </ul>
				if '<li>'+n*'\t' not in list_chn[l+1]:
					while n >-1:
						if '<li>'+n*'\t' not in list_chn[l+1]: list_chn[l] = list_chn[l] + '</ul>'
						n-=1
#	reunir les lignes
	texte ='\n'.join (list_chn)
#	mettre le texte au propre
	texte = texte.strip ('\n')
	while '<li>\t' in texte: texte = texte.replace ('<li>\t', '<li>')
	while '<ul>\t' in texte: texte = texte.replace ('<ul>\t', '<ul>')
	return texte

def creer_table (texte):
	"""
les cadeaux de Noel:
Huguette	un pull quitch
Sebastien	un stylo
Jean-Marc	un souvenir des dernieres vacances
	"""
#	separer les lignes pour permettre leurs transformation
	list_chn = texte.split ('\n')
	len_chn = len (list_chn)
	d=-1 ; c=-1 ; i=0
	while i< len_chn:
#		rechercher une table
		d=-1 ; c=-1
		if d==-1 and c==-1 and '\t' in list_chn[i]:
			c= list_chn[i].count ('\t')
			d=i ; i+=1
		while i< len_chn and list_chn[i].count ('\t') ==c: i+=1
		c=i-d
#		une table a ete trouve
		if c>1 and d>0:
			rtable = range (d,i)
			for j in rtable:
#				entre les cases
				list_chn[j] = list_chn[j].replace ('\t', '</td><td>')
#				bordure des cases
				list_chn[j] = '<tr><td>' + list_chn[j] +'</td></tr>'
#			les limites de la table
			list_chn[d] = '<table>\n' + list_chn[d]
			list_chn[i-1] = list_chn[i-1] +'\n</table>'
		i+=1
	texte ='\n'.join (list_chn)
	return texte

def createLink_oneType (type, texte):
	""" transformer les p contenant un lien en a """
	liste = texte.split ('<p>'+ type)
	range_liste = range (1, len (liste))
	for i in range_liste:
		# pour chaque lien, retrouver son extremite
		f1= liste[i].find (' ')
		if f1==-1: f1=1000
		f2= liste[i].find ('\t')
		if f2==-1: f2=1000
		f3= liste[i].find ('\n')
		if f3==-1: f3=1000
		f4= liste[i].find ('</p>')
		if f4==-1: f4=1000
		f= min (f1,f2,f3,f4)
		# pour chaque lien, le creer
		liste[i] = liste[i].replace ('</p>', '</a>', 1)
		link = "\n<a href='%s%s'>%s" %( type, liste[i][:f], liste[i][:f])
		liste[i] = link + liste[i][f:]
	texte = "".join (liste)
	return texte

def createLink (texte):
	texte = createLink_oneType ('http://', texte)
	texte = createLink_oneType ('https://', texte)
	texte = texte.replace ("'>www.", "'>")
	return texte

def textToHtml (texte):
#	ajouter les majuscules
	texte = '\n'+ texte +'\n'
	while '_______' in texte: texte = texte.replace ('_______', '______')
#	transformer la mise en page en balises
	for i,j in balises:
		if i in texte: texte = texte.replace (i,j)

#	ajustement pour les titres 2 et les images
	list_chn = texte.split ('\n')
	lc= range (len (list_chn))
	for i in lc:
		if '<h2>' in list_chn[i]: list_chn[i] = list_chn[i].replace ('</h1>', '</h2>')
		elif '<img' in list_chn[i]: list_chn[i] = list_chn[i] +"'/>"
	texte = '\n'.join (list_chn)
#	les tableaux et les listes
	if '\nFig' in texte: texte = creer_figure (texte)
	if '\nCode' in texte: texte = creer_code (texte)
	if '\n\t' in texte: texte = creer_liste (texte)
	if '\t' in texte: texte = creer_table (texte)

#	nettoyer le texte pour faciliter la suite des transformations
	texte = texte.strip()
	texte = texte.replace ('\t', "")
	while '\n\n' in texte: texte = texte.replace ('\n\n', '\n')
	while '  ' in texte: texte = texte.replace ('  ', ' ')

#	rajouter les <p/>
	texte = texte.replace ('\n', '</p><p>')
	texte = texte.replace ('></p><p><', '><')
	texte = texte.replace ('></p><p>', '><p>')
	texte = texte.replace ('</p><p><', '</p><')
	# transformer les p contenant un lien en a
	texte = createLink (texte)
#	rajouter d'eventuel <p/> s'il n'y a pas de balise en debut ou fin de texte
	if '<' not in texte[0:3]: texte = '<p>'+ texte
	if '>'not in texte[-3:]: texte = texte +'</p>'

#	mettre en forme les balises pour clarifier le texte
	texte = texte.replace ('\n', "")
	texte = texte.replace ('\t', "")
	texte = texte.replace ('<p', '\n\t<p')
	texte = texte.replace ('<h', '\n\t<h')
	texte = texte.replace ('<ul', '\n\t<ul')
	texte = texte.replace ('</ul', '\n\t</ul')
	texte = texte.replace ('<li', '\n\t\t<li')
	texte = texte.replace ('<table', '\n\t<table')
	texte = texte.replace ('</table', '\n\t</table')
	texte = texte.replace ('<caption', '\n\t\t<caption')
	texte = texte.replace ('<tr', '\n\t\t<tr')
	return texte

def htmlToText (textHtml):
	# nettoyage
	textHtml = textHtml.replace ('\n', "")
	textHtml = textHtml.replace ('\t', "")
	while '  ' in textHtml: textHtml = textHtml.replace ('  ', ' ')
	textHtml = textHtml.replace ('> ', '>')
	textHtml = textHtml.replace (' <', '<')
	# les titres
	textHtml = textHtml.replace ('<h1>', '\n______\n______ ')
	textHtml = textHtml.replace ('<h2>', '\n______ ')
	textHtml = textHtml.replace ('<h3>', '\n------ ')
	textHtml = textHtml.replace ('<h4>', '\n--- ')
	textHtml = textHtml.replace ('</h4>', ' ---\n')
	textHtml = textHtml.replace ('</h3>', ' ------\n')
	textHtml = textHtml.replace ('</h2>', ' ______\n')
	textHtml = textHtml.replace ('</h1>', ' ______\n')
	# les conteneurs
	container =[ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
	for tag in container:
		textHtml = textHtml.replace ('</'+ tag +'>', "")
		textHtml = textHtml.replace ('<'+ tag +'>', "")
	# les tableaux
	textHtml = textHtml.replace ('th>', 'td>')
	textHtml = textHtml.replace ('</td><td>', '\t')
	textHtml = textHtml.replace ('</td></tr><tr><td>', '\n')
	textHtml = textHtml.replace ('<tr>', '\n')
	textHtml = textHtml.replace ('</tr>', '\n')
	# les listes
	textHtml = textHtml.replace ('</li><li>', '\n\t')
	textHtml = textHtml.replace ('<li>', '\n\t')
	textHtml = textHtml.replace ('</li>', '\n')
	# les lignes
	textHtml = textHtml.replace ('</p><p>', '\n')
	lines =[ 'p', 'caption', 'figcaption' ]
	for tag in lines:
		textHtml = textHtml.replace ('</'+ tag +'>', '\n')
		textHtml = textHtml.replace ('<'+ tag +'>', '\n')
	# les phrases
	inner =[ 'span', 'em', 'strong' ]
	for tag in inner:
		textHtml = textHtml.replace ('</'+ tag +'>', ' ')
		textHtml = textHtml.replace ('<'+ tag +'>', ' ')
	textHtml = textHtml.replace (' \n', '\n')
	textHtml = textHtml.replace ('\n ', '\n')
	# autres
	textHtml = textHtml.replace ('<hr>', '\n________________________\n')
	textHtml = textHtml.replace ('<hr/>', '\n________________________\n')
	textHtml = textHtml.replace ('<br>', '\n')
	textHtml = textHtml.replace ('<br/>', '\n')
	while '\n\n' in textHtml: textHtml = textHtml.replace ('\n\n', '\n')
