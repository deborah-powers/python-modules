#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

help ="""convertir un fichier self.text en fichier html
utilisation
	le script est appelable dans un fichier
"""




def fromText (self):


def findEndLink (text):
	endingChar = '< \t\n.;:,!?/\\'
	for char in endingChar:
		if char in text: text = text[:f]
	return text




def createLink_oneType (type, self.text):
	""" transformer les p contenant un lien en a """
	liste = self.text.split ('<p>'+ type)
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
	self.text = "".join (liste)

def htmlToText (textHtml):
	# nettoyage
	textHtml.replace ('\n')
	textHtml.replace ('\t')
	while '  ' in textHtml: textHtml.replace ('  ', ' ')
	textHtml.replace ('> ', '>')
	textHtml.replace (' <', '<')
	# les titres
	textHtml.replace ('<h1>', '\n______\n______ ')
	textHtml.replace ('<h2>', '\n______ ')
	textHtml.replace ('<h3>', '\n------ ')
	textHtml.replace ('<h4>', '\n--- ')
	textHtml.replace ('</h4>', ' ---\n')
	textHtml.replace ('</h3>', ' ------\n')
	textHtml.replace ('</h2>', ' ______\n')
	textHtml.replace ('</h1>', ' ______\n')
	# les conteneurs
	container =[ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
	for tag in container:
		textHtml.replace ('</'+ tag +'>')
		textHtml.replace ('<'+ tag +'>')
	# les tableaux
	textHtml.replace ('th>', 'td>')
	textHtml.replace ('</td><td>', '\t')
	textHtml.replace ('</td></tr><tr><td>', '\n')
	textHtml.replace ('<tr>', '\n')
	textHtml.replace ('</tr>', '\n')
	# les listes
	textHtml.replace ('</li><li>', '\n\t')
	textHtml.replace ('<li>', '\n\t')
	textHtml.replace ('</li>', '\n')
	# les lignes
	textHtml.replace ('</p><p>', '\n')
	lines =[ 'p', 'caption', 'figcaption' ]
	for tag in lines:
		textHtml.replace ('</'+ tag +'>', '\n')
		textHtml.replace ('<'+ tag +'>', '\n')
	# les phrases
	inner =[ 'span', 'em', 'strong' ]
	for tag in inner:
		textHtml.replace ('</'+ tag +'>', ' ')
		textHtml.replace ('<'+ tag +'>', ' ')
	textHtml.replace (' \n', '\n')
	textHtml.replace ('\n ', '\n')
	# autres
	textHtml.replace ('<hr>', '\n________________________\n')
	textHtml.replace ('<hr/>', '\n________________________\n')
	textHtml.replace ('<br>', '\n')
	textHtml.replace ('<br/>', '\n')
	while '\n\n' in textHtml: textHtml.replace ('\n\n', '\n')
