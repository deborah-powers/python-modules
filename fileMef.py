#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.text import Text, toUpperCase, majList
from debutils.file import File
from debutils.html import FileHtml

pointsShape =( '\n\t- ', '////// ', '====== ', '****** ', '------ ' )
balises =(
	('<h1>', '\n\n////// '), ('</h1>', ' //////\n\n'), ('<h2>', '\n\n====== '), ('</h2>', ' ======\n\n'), ('<h3>', '\n\n------ '), ('</h3>', ' ------\n\n'), ('<h4>', '\n\n--- '), ('</h4>', ' ---\n\n'),
	('<hr>', '\n\n______\n\n'), ("\n<img src='", '\nImg\t'),
	('<figure>', '\nFig\n'), ('</figure>', '\n/fig\n'), ('<xmp>', '\ncode\n'), ('</xmp>', '\n/code\n'), ('<li>' '\n\t'), ('<tr>', '\n'), ('<th>', '\t'), ('<td>', '\t')
)
balisesToText =( ('<hr/>', '\n______\n'), ('<br>', '\n'), ('<br/>', '\n'))
balisesToTextClosing =( 'li', 'tr', 'th', 'td')

def shapeText (self):
	# mettre le text en forme pour simplifier sa transformation
	self.clean()
	for char in '/=*-_':
		while self.contain (7* char): self.replace (7* char, 6* char)
		for i,j in majList: self.replace (6* char +' '+i, '\n\n'+ 6* char +' '+j)
		self.replace (' '+ 6* char, ' '+ 6* char +'\n\n')
		self.replace (6* char +' ', '\n\n'+ 6* char +' ')
	"""
	while self.contain ('///////'): self.replace ('///////', '//////')	# h1-h2
	while self.contain ('======='): self.replace ('=======', '======')	# h2
	while self.contain ('-------'): self.replace ('-------', '------')	# h3
	"""
	self.text = '\n'+ self.text +'\n'
	# rajouter les majuscules apres chaque point
	self.upperCaseMef()
	while self.contain ('\n\n\n'): self.replace ('\n\n\n', '\n\n')
	"""
	for p in pointsShape:
		for i,j in majList: self.replace (p+i, p+j)
	"""

def upperCaseMef (self):
	if self.contain ('\n/code\n'):
		paragraphList = self.split ('\ncode\n')
		paragraphRange = range (1, len (paragraphList))
		for i in paragraphRange:
			d= paragraphList [i].find ('\n/code\n') +7
			paragraphList [i] = paragraphList [i] [:d] + toUpperCase (paragraphList [i] [d:])
		self.text = '\ncode\n'.join (paragraphList)
	else: self.upperCase()

def shapeFile (self):
	self.fromFile()
	self.shape()
	self.toFile()

def toHtml (self):
	self.shape()
#	transformer la mise en page en balises
	for html, perso in balises:
		if perso in self.text: self.replace (perso, html)
#	ajustement pour les grands titres et les images
	paragraphList = self.text.split ('\n')
	paragraphRange = range (len (paragraphList))
	for i in paragraphRange:
		if '<img' in paragraphList [i]: paragraphList [i] = paragraphList [i] +"'/>"
	self.text = '\n'.join (paragraphList)
#	les figures
	if '<figure>' in self.text:
	#	mettre en forme le contenu des figures
		paragraphList = self.text.split ('figure>')
		lc= range (1, len (paragraphList), 2)
		for i in lc:
			# nettoyer le texte pour faciliter sa transformation
			paragraphList [i] = paragraphList [i].strip ('\n')
			paragraphList [i] = paragraphList [i].split ('\n')
			paragraphRange = range (len (paragraphList [i]) -1)
			for j in paragraphRange:
				# les images ont deja ete modifiees precedement
				if paragraphList [i] [j] [:4] != '<img':
					paragraphList [i] [j] = '<figcaption>' + paragraphList [i] [j] + '</figcaption>'
			paragraphList [i] = "".join (paragraphList [i])
		self.text = 'figure>'.join (paragraphList)
	# les bloc de code
	if '<xmp>' in self.text:
		paragraphList = self.text.split ('xmp>')
		paragraphRange = range (1, len (paragraphList), 2)
		for i in paragraphRange:
			paragraphList [i] = paragraphList [i].strip()
			paragraphList [i] = paragraphList [i].strip ('\n\t ')
			paragraphList [i] = paragraphList [i].replace ('\n', '\a')
			paragraphList [i] = paragraphList [i].replace ('\t', '\f')
		self.text = 'xmp>'.join (paragraphList)
		self.replace ('\a</xmp>', '</xmp>')
	# les listes
	if '<li>' in self.text:
		self.text = '\n'+ self.text +'\n'
		paragraphList = self.text.split ('\n')
		lc= range (len (paragraphList))
	#	rajouter les balises fermantes
		for l in lc:
			if '<li>' in paragraphList [l]: paragraphList [l] = paragraphList [l] +'</li>'
		lc= range (1, len (paragraphList) -1)
	#	rajouter les balises ouvrantes et fermantes delimitant la liste, <ul/>. reperer les listes imbriquees.
		for l in lc:
			if '<li>' in paragraphList [l]:
				# compter le niveau d'imbrication (n) de l'element paragraphList [l]
				n=0
				while '<li>'+n*'\t' in paragraphList [l]: n+=1
				n-=1
				if '<li>'+n*'\t' in paragraphList [l]:
					# debut de la liste (ou sous-liste), mettre le <ul>
					if '<li>'+n*'\t' not in paragraphList [l-1]: paragraphList [l] = '<ul>'+ paragraphList [l]
					# fin de la liste (ou sous-liste), mettre le </ul>
					if '<li>'+n*'\t' not in paragraphList [l+1]:
						while n >-1:
							if '<li>'+n*'\t' not in paragraphList [l+1]: paragraphList [l] = paragraphList [l] + '</ul>'
							n-=1
	#	mettre le texte au propre
		self.text = '\n'.join (paragraphList)
		self.text = self.text.strip ('\n')
		while '<li>t' in self.text: self.replace ('<li>t', '<li>')
		while '<ul>t' in self.text: self.replace ('<ul>t', '<ul>')
	# les tableaux
	if '\t' in self.text:
		paragraphList = self.text.split ('\n')
		len_chn = len (paragraphList)
		d=-1; c=-1; i=0
		while i< len_chn:
			# rechercher une table
			d=-1; c=-1
			if d==-1 and c==-1 and '\t' in paragraphList [i]:
				c= paragraphList [i].count ('\t')
				d=i; i+=1
			while i< len_chn and paragraphList [i].count ('\t') ==c: i+=1
			c=i-d
			# une table a ete trouve
			if c>1 and d>0:
				rtable = range (d, i)
				for j in rtable:
					# entre les cases
					paragraphList [j] = paragraphList [j].replace ('\t', '</td><td>')
					# bordure des cases
					paragraphList [j] = '<tr><td>' + paragraphList [j] +'</td></tr>'
				# les limites de la table
				paragraphList [d] = '<table>\n' + paragraphList [d]
				paragraphList [i-1] = paragraphList [i-1] +'\n</table>'
			i+=1
		self.text = '\n'.join (paragraphList)
		# les titres de colonnes ou de lignes
		if self.contain (':</td>'):
			paragraphList = self.split (':</td>')
			paragraphRange = range (len (paragraphList) -1)
			for p in paragraphRange:
				d= paragraphList [p].rfind ('<td>')
				paragraphList [p] = paragraphList [p] [:d] +'<th>'+ paragraphList [p] [d+4:]
			self.text = '</th>'.join (paragraphList)
	# transformer les p contenant un lien en a
	endingChars = '<;, !?\t\n'
	paragraphList = self.text.split ('http')
	paragraphRange = range (1, len (paragraphList))
	for p in paragraphRange:
		paragraphTmp = paragraphList [p]
		e=-1; f=-1; d=-1
		for char in endingChars:
			if char in paragraphTmp:
				f= paragraphTmp.find (char)
				paragraphTmp = paragraphTmp [:f]
		paragraphTmp = paragraphTmp.strip ('/')
		d= paragraphTmp.rfind ('/') +1
		e= len (paragraphTmp)
		if '.' in paragraphTmp: e= paragraphTmp.rfind ('.')
		paragraphList [p] = paragraphTmp +"'>"+ paragraphTmp [d:e] +'</a> '+ paragraphList [p] [f:]
	self.text = " <a href='http".join (paragraphList)
#	nettoyer le texte pour faciliter la suite des transformations
	self.replace ('\t')
	self.clean()
#	rajouter les <p/>
	self.replace ('\n', '</p><p>')
	self.replace ('></p><p><', '><')
	self.replace ('></p><p>', '><p>')
	self.replace ('</p><p><', '</p><')
#	rajouter d'eventuel <p/> s'il n'y a pas de balise en debut ou fin de self.text
	if '<' not in self.text [0:3]: self.text = '<p>'+ self.text
	if '>' not in self.text [-3:]: self.text = self.text +'</p>'
#	mettre en forme les balises pour clarifier le texte
	self.replace ('\n')
	self.replace ('\t')
	# pour les blocs de code
	self.replace ('\a', '\n')
	self.replace ('\f', '\t')
	self.clean()
	self.extension = 'html'
	self.fileFromData()
	self.toFile()

def fromHtml (self):
	fhtml = file (self.file)
	fhtml.fromFile()
	fhtml.clean()
	self.copyFile (fhtml)
	self.extension = 'txt'
	self.fileFromData()
	# les conteneurs
	container = [ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
	for tag in container:
		self.replace ('</'+ tag +'>')
		self.replace ('<'+ tag +'>')
	for html, perso in balises: self.replace (html, perso)
	for html, perso in balisesToText: self.replace (html, perso)
	for tag in balisesToTextClosing: self.replace ('</'+ tag +'>')
	# les lignes
	self.replace ('</p><p>', '\n')
	lines = [ 'p', 'caption', 'figcaption' ]
	for tag in lines:
		self.replace ('</'+ tag +'>', '\n')
		self.replace ('<'+ tag +'>', '\n')
	# les phrases
	inner = [ 'span', 'em', 'strong' ]
	for tag in inner:
		self.replace ('</'+ tag +'>', ' ')
		self.replace ('<'+ tag +'>', ' ')
	self.replace (' \n', '\n')
	self.replace ('\n ', '\n')
	# les liens
	ltext = self.split ('</a>')
	rtext = range (len (ltext) -1)
	for t in rtext:
		d= ltext [t].find ('href') +6
		f= ltext [t].find ("'", d)
		link = ltext [t] [d:f]
		f= ltext [t].find ('>', f) +1
		title = ltext [t] [f:]
		d= ltext [t].find ('<a ')
		ltext [t] = ltext [t] [:d] +' '+ title +': '+ link
	self.text = ' '.join (ltext)
	self.shape()
	self.toFile()

setattr (Text, 'upperCaseMef', upperCaseMef)
setattr (Text, 'shape', shapeText)
setattr (File, 'shapeFile', shapeFile)
setattr (File, 'toHtml', toHtml)
setattr (File, 'fromHtml', fromHtml)

if len (argv) <2: print ('il manque le nom du fichier')
else:
	tmpFile = File (argv[1])
	if argv[1][-4:] == 'html': tmpFile.fromHtml()
	elif argv[1][-3:] == 'txt':
		if len (argv) >2: tmpFile.shapeFile()
		else: tmpFile.toHtml()
	else: print ("le nom du fichier n'est pas correct. il doit être un html ou un txt.")
