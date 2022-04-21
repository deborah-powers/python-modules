#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import logger

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmlmnopqrstuvwxyz0123456789'
punctuation = '({[\n\t.,;:]})?!'
uppercase = ('aA', 'àA', 'bB', 'cC', '\xe7\xc7', 'dD', 'eE', 'éE', 'èE', 'êE', 'ëE', 'fF', 'gG', 'hH', 'iI', 'îI', 'ïI', 'jJ', 'kK', 'lL', 'mM', 'nN', 'oO', '\xf4\xe4', 'pP', 'qQ', 'rR', 'sS', 'tT', 'uU', 'vV', 'wW', 'xX', 'yY', 'zZ')

# liste des points, des chaines de caracteres suivies par une majuscule
wordsBeginMaj = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'victo', 'tony', 'simplon', 'loïc', 'france', 'paris', 'rueil')
wordsBeginMin = ('Deborah.powers', 'Deborah.noisetier', 'Http',
	'\nUpdate ', '\nSelect ', '\nFrom ', '\nWhere ', '\nHaving ', '\nGroup by ', '\nOrder by ', 'Inner join ', 'Outer join ', 'Left outer join ', 'Insert into ', 'Set schema ',
	'\nCd ', '\nPsql ','\nPg_', '\nPython ', '\nGit ',
	'\nDef ', '\nClass ', '\nConsole.log', '\nVar ', '\nFunction ', '\tReturn ',
	'\nLog.', '\tLog.', 'Mvn ', '\tPrivate ', '\tProtected ', '\tPublic ', '\nPrivate ', '\nProtected ', '\nPublic ')

wordUrl =( ('. com', '.com'), ('. org', '.org'), ('. fr/', '.fr/'), ('www. ', 'www.'), ('. jpg', '.jpg'), ('. png', '.png') )
weirdChars =(
	('«', '"'), ('»', '"'), ('–', '-'), ('‘', "'"), ('’', "'"), ('“', '"'), ('”', '"'), ('"', '"'), ('&hellip;', '...'), ('…', '...'),
	('\n ', '\n'), ('\r', ''), (' \n', '\n'), ("\\'", "'"), ('\\n', '\n'), ('\\r', ''), ('\\t', '\t'),
	('\\u00c2', 'Â'), ('\\u00ca', 'Ê'), ('\\u00cb', 'Ë'), ('\\u00ce', 'Î'), ('\\u00cf', 'Ï'), ('\\u00d4', 'Ô'), ('\\u00d6', 'Ö'), ('\\u00db', 'Û'), ('\\u00e0', 'à'), ('\\u00e2', 'â'), ('\\u00e7', 'ç'), ('\\u00e8', 'è'), ('\\u00e9', 'é'), ('\\u00ea', 'ê'), ('\\u00eb', 'ë'), ('\\u00ee', 'î'), ('\\u00ef', 'ï'), ('\\u00f4', 'ô'), ('\\u00f6', 'ö'), ('\\u00fb', 'û'),
	('\\', ''),
	('\x85', '.'), ('\x92', "'"), ('\x96', '"'), ('\x97', "'"), ('\x9c', ' '), ('\xa0', ' '),
	('&agrave;', 'à'), ('&acirc;', 'â'), ('&ccedil;', 'ç'), ('&eacute;', 'é'), ('&egrave;', 'è'), ('&ecirc;', 'ê'), ('&icirc;', 'î'), ('&iuml;', 'ï'), ('&ocirc;', 'ô'), ('&ugrave;', 'ù'), ('&ucirc;', 'û'), ('&apos;', "'"),
	('&mdash;', ' '), ('&nbsp;', ''), ('&oelig;', 'oe'), ('&quot;', ''), ('&lt;', '<'), ('&gt;', '>'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&rsquo;', "'"),
	('&amp;', '&'), ('&#x27;', "'"), ('&#039', "'"), ('&#160;', ' '), ('&#39;', "'"), ('&#8217;', "'"), ('\n" ', '\n"')
)
tagHtml =(
	('\n<h1>', '\n====== '), ('</h1>\n', ' ======\n'), ('\n<h2>', '\n****** '), ('</h2>\n', ' ******\n'), ('\n<h3>', '\n------ '), ('</h3>\n', ' ------\n'), ('\n<h4>', '\n--- '), ('</h4>\n', ' ---\n'),
	('\n<hr>', '\n\n************************************************\n\n'), ("\n<img src='", '\nImg\t'), ('\n<figure>', '\nFig\n'), ('</figure>', '\n/fig\n'), ('\n<xmp>', '\ncode\n'), ('</xmp>', '\n/code\n'),
	('\n<li>', '\n\t')
)


def findEnd (text, pos=0):
	end =[]
	if '\n' in text: end.append (text.find ('\n', pos))
	if '\t' in text: end.append (text.find ('\t', pos))
	if ' ' in text: end.append (text.find (' ', pos))
	return min (end)

	# ________________________ ma mise en forme perso ________________________

def upperCaseIntern (text):
	text ='\n'+ text
	points =( '\n', '. ', '! ', '? ', ': ', '\n_ ', '\n\t', '______ ', '------ ', '****** ', '====== ')
	for i, j in uppercase:
		for p in points: text = text.replace (p+i, p+j)
	for p in " "+ punctuation[-11:]:
		for q in " "+ punctuation[0:5]:
			for word in wordsBeginMaj: text = text.replace (q+ word +p, q+ word.capitalize() +p)
	for artefact in wordsBeginMin: text = text.replace (artefact, artefact.lower())
	text = text.strip()
	return Text (text)

def upperCase (text, case=""):
	"""	rest: je supprime l'ancienne casse
		upper: je rajoute les majuscules
	log (type (text))
	"""
	text = text
	if 'reset' in case: text = text.lower()
	if 'upper' in case:
		text = Text ('\n'+ text +'\n')
		if '\n/code\n' in text:
			paragraphList = text.split ('\ncode\n')
			paragraphRange = range (1, len (paragraphList))
			for i in paragraphRange:
				d= paragraphList [i].find ('\n/code\n') +7
				paragraphList [i] = paragraphList [i][:d] + toUpperCase (paragraphList [i][d:])
			text = '\ncode\n'.join (paragraphList)
		else: text = text.upperCaseIntern()
	text = text.strip()
	return text

def protectHour (text):
	if ':' not in text: return text
	nbChar = len (text) -3
	text = text
	#logger.log (nbChar)
	d=0
	while d< nbChar and d>=0:
		d= text.find (':', d)
		if d<0: continue
		if text[d+3] == ':':
			f= findEnd (text, d)
			dateProtected = text[d:f].replace (':', '§§§')
			dateProtected = dateProtected.replace (',', '£££')
			text = text.replace (text[d:f], dateProtected)
		d=d+4
	return Text (text)

def protectUrl (text, s=False):
	word = '\nhttp://'
	if s: word = '\nhttps://'
	textList = text.split (word)
	textRange = range (1, len (textList))
	for l in textRange:
		f= findEnd (textList[l])
		urlProtected = textList[l][:f].replace ('.', '***')
		urlProtected = urlProtected.replace ('?', '$$$')
		urlProtected = urlProtected.replace (':', '§§§')
		textList[l] = textList[l].replace (textList[l][:f], urlProtected)
	text = word.join (textList)
	return Text (text)

def cleanUrl (text, s=False):
	word = '\nhttp://'
	if s: word = '\nhttps://'
	textList = text.split (word)
	textRange = range (1, len (textList))
	for l in textRange:
		a= textList[l].find ('\n')
		url = textList[l][:a]
		textList[l] = textList[l][a:]
		url = url.lower()
		url = url.replace (' ',"")
		textList[l] = url + textList[l]
	text = word.join (textList)
	return Text (text)

def clean (text):
	text = text
	for i, j in weirdChars: text = text.replace (i, j)
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	text = text.replace ('\n ', '\n')
	text = text.replace (' \n', '\n')
	while '\t\n' in text: text = text.replace ('\t\n', '\n')
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	text = text.protectUrl (True)
	text = text.protectUrl (False)
	text = text.protectHour()
	for p in punctuation:
		text = text.replace (' '+p, p)
		text = text.replace (p+' ', p)
	while '....' in text: text = text.replace ('....', '...')
	for l in letters:
		for p in punctuation[0:3]: text = text.replace (l+p, l+' '+p)
		for p in punctuation[-2:]: text = text.replace (l+p, l+' '+p)
		for p in punctuation[-9:]: text = text.replace (p+l, p+' '+l)
	for l in letters[:26]:
		text = text.replace ('."'+l, '. "'+l)
		text = text.replace ('," '+l, '", '+l)
	# les appostrophes
	points = 'cdjlmnrst'
	for p in points:
		text = text.replace (' '+p+"' ", ' '+p+"'")
		text = text.replace (' '+ p.upper() +"' ", ' '+ p.upper() +"'")
	text = text.replace ("Qu' ","Qu'")
	text = text.replace ("qu' ","qu'")
	"""
	text = text.cleanUrl (True)
	text = text.cleanUrl (False)
	"""
	# nettoyer les urls et les dates
	text = text.replace ('***', '.')
	text = text.replace ('$$$', '?')
	text = text.replace ('§§§', ':')
	text = text.replace ('£££', ',')
	for wOld, wNew in wordUrl: text = text.replace (wOld, wNew)
	return text

def shape (text, case=""):
	""" mettre le text en forme pour simplifier sa transformation
	j'utilise une mise en forme personnelle
	addCase
		rien: je ne rajoute pas les majuscules
		rest: je supprime l'ancienne casse
		upper: je rajoute les majuscules
	"""
	text = text.clean()
	for char in '=*-_':
		while 7* char in text: text = text.replace (7* char, 6* char)
		text = text.replace (' '+ 6* char, ' '+ 6* char +'\n\n')
		text = text.replace (6* char +' ', '\n\n'+ 12* char +' ')
		text = text.replace (' '+ 6* char, ' '+ 12* char +'\n\n')
	while '\n\n\n' in text: text = text.replace ('\n\n\n', '\n\n')
	if case: text = text.upperCase (case)
	return text

	# ________________________ fonctions de bases ________________________

def fromModel (text, model):
	# remplacer scanf
	# préparer le modèle
	typeList = ['d', 'f', 's']
	model = model.replace ('%%', '$')
	modelTmp = model
	for t in typeList: modelTmp = modelTmp.replace ('%'+t, '%')
	# récupérer les données du message sous forme de string
	modelList = modelTmp.split ('%')
	results = []
	text = text
	for line in modelList:
		d= text.find (line)
		if d>0: results.append (text [:d])
		d+= len (line)
		text = text [d:]
	if len (text) >0: results.append (text)
	d=0
	rangeRes = range (len (results))
	for r in rangeRes:
		d= model.find ('%', d) +1
		if model [d] =='d': results [r] = int (results [r])
		elif model [d] =='f': results [r] = float (results [r])
	if (len (results) >2+ modelTmp.count ('%')): print ('erreur: %=', modelTmp.count ('%'), 'item =', len (results))
	return results

def replace (text, oldWord, newWord=''):
	return Text (str.replace (text, oldWord, newWord))

def strip (text, chars=""):
	if chars: return Text (str.strip (text, chars))
	else: return Text (str.strip (text))

def find (text, word, pos=0):
	posFind =-1
	if pos <0: pos = len (text) -pos
	if word in text: posFind = str.find (text, word, pos)
	elif '"' in word:
		word = word.replace ('"', "'")
		posFind = str.find (text, word, pos)
	elif "'" in word:
		word = word.replace ("'", '"')
		posFind = str.find (text, word, pos)
	return posFind

def rfind (text, word):
	posFind =-1
	if word in text: posFind = str.rfind (text, word)
	elif '"' in word:
		word = word.replace ('"', "'")
		posFind = str.rfind (text, word)
	elif "'" in word:
		word = word.replace ("'", '"')
		posFind = str.rfind (text, word)
	return posFind


def sliceWord (text, wordStart, wordEnd):
	res =""
	if wordStart in text and wordEnd in text:
		d= text.find (wordStart) + len (wordStart)
		f= text.find (wordEnd, d)
		if f>0 and f>d: res = text[d:f]
	return Text (res)

	# ________________________ conversion en html. ma mef est utilisée pour les textes simples ________________________

def toHtml (text):
	text = text.shape()
	for char in '=*-_': text = text.replace (12* char, 6* char)
	# transformer la mise en page en balises
	for html, perso in tagHtml:
		if perso in text: text = text.replace (perso, html)
	# ajustement pour les grands titres et les images
	paragraphList = text.split ('\n')
	paragraphRange = range (len (paragraphList))
	for i in paragraphRange:
		if '<img' in paragraphList [i]: paragraphList [i] = paragraphList [i] +"'/>"
	text = '\n'.join (paragraphList)
	# les formules
	if '\nM\t' in text:
		paragraphList = text.split ('\n')
		paragraphRange = range (1, len (paragraphList))
		for i in paragraphRange:
			if paragraphList[i][:2] == 'M\t':
				if 'f/' in paragraphList[i]:
					paragraphList[i] = paragraphList[i].replace (' f/ ', '<mfrac><mrow>')
					paragraphList[i] = paragraphList[i].replace ('\tf/ ', '<mfrac><mrow>')
					paragraphList[i] = paragraphList[i].replace (' /f', '</mrow></mfrac>')
					if '</mfrac>' not in paragraphList[i]: paragraphList[i] = paragraphList[i] + '</mrow></mfrac>'
					paragraphList[i] = paragraphList[i].replace (' / ', '</mrow><mrow>')
				paragraphList[i] = '<math>' + paragraphList[i][2:] + '</math>'
		text = '\n'.join (paragraphList)
	# les figures
	if '<figure>' in text:
		# mettre en forme le contenu des figures
		paragraphList = text.split ('figure>')
		paragraphRange= range (1, len (paragraphList), 2)
		for i in paragraphRange:
			# nettoyer le texte pour faciliter sa transformation
			paragraphList [i] = paragraphList [i].strip ('\n')
			paragraphList [i] = paragraphList [i].split ('\n')
			paragraphRange = range (len (paragraphList [i]) -1)
			for j in paragraphRange:
				# les images ont deja ete modifiees precedement
				if paragraphList [i][j][:4] != '<img':
					paragraphList [i][j] = '<figcaption>' + paragraphList [i][j] + '</figcaption>'
			paragraphList [i] = "".join (paragraphList [i])
		text = 'figure>'.join (paragraphList)
	# les bloc de code
	if '<xmp>' in text:
		paragraphList = text.split ('xmp>')
		paragraphRange = range (1, len (paragraphList), 2)
		for i in paragraphRange:
			paragraphList [i] = paragraphList [i].strip()
			paragraphList [i] = paragraphList [i].strip ('\n\t ')
			paragraphList [i] = paragraphList [i].replace ('\n', '\a')
			paragraphList [i] = paragraphList [i].replace ('\t', '\f')
		text = 'xmp>'.join (paragraphList)
		text = text.replace ('\a</xmp>', '</xmp>')
	# les listes
	if '<li>' in text:
		text = '\n'+ text +'\n'
		paragraphList = text.split ('\n')
		lc= range (len (paragraphList))
		# rajouter les balises fermantes
		for l in lc:
			if '<li>' in paragraphList [l]: paragraphList [l] = paragraphList [l] +'</li>'
		lc= range (1, len (paragraphList) -1)
		# rajouter les balises ouvrantes et fermantes delimitant la liste, <ul/>. reperer les listes imbriquees.
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
		# mettre le texte au propre
		text = '\n'.join (paragraphList)
		text = text.strip ('\n')
		while '<li>\t' in text: text = text.replace ('<li>\t', '<li>')
		while '<ul>\t' in text: text = text.replace ('<ul>\t', '<ul>')
	# les tableaux
	if '\t' in text:
		paragraphList = text.split ('\n')
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
		text = '\n'.join (paragraphList)
		# les titres de colonnes ou de lignes
		if ':</td>' in text:
			paragraphList = text.split (':</td>')
			paragraphRange = range (len (paragraphList) -1)
			for p in paragraphRange:
				d= paragraphList [p].rfind ('<td>')
				paragraphList [p] = paragraphList [p][:d] +'<th>'+ paragraphList [p][d+4:]
			text = '</th>'.join (paragraphList)
	# nettoyer le texte pour faciliter la suite des transformations
	text = text.replace ('\t')
	text = text.clean()
	# rajouter les <p/>
	text = text.replace ('\n', '</p><p>')
	text = text.replace ('></p><p><', '><')
	text = text.replace ('</p><p><', '</p><')
	text = text.replace ('></p><p>', '><p>')
	# rajouter d'eventuel <p/> s'il n'y a pas de balise en debut ou fin de text
	if '<' not in text [0:3]: text = '<p>'+ text
	if '>' not in text [-3:]: text = text +'</p>'
	# transformer les p contenant un lien en a
	endingChars = '<;, !?\t\n'
	paragraphList = text.split ('http')
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
		if '.' in paragraphTmp[d:]: e= paragraphTmp.rfind ('.')
		title = paragraphTmp [d:e].replace ('-',' ')
		title = title.replace ('_',' ')
		paragraphList [p] = paragraphTmp +"'>"+ title +'</a> '+ paragraphList [p][f:]
	text = " <a href='http".join (paragraphList)
	text = text.replace ('> <a ', '><a ')
	# pour les blocs de code
	text = text.replace ('\a', '\n')
	text = text.replace ('\f', '\t')
	text = text.clean()
	text = text.replace (' </', '</')
	return text

def fromHtml (text):
	# les conteneurs
	container = [ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
	tagsBlank =( ('<hr/>', '\n************\n'), ('<hr>', '\n************\n'), ('<br>', '\n'), ('<br/>', '\n'))
	tagsClosing =( 'li', 'tr', 'th', 'td')
	text = text
	for tag in container:
		text = text.replace ('</'+ tag +'>')
		text = text.replace ('<'+ tag +'>')
	# les tableaux
	text = text.replace ('</td>')
	text = text.replace ('</th>', ':')
	text = text.replace ('</tr>')
	text = text.replace ('<tr><td>', '\n')
	text = text.replace ('<tr><th>', '\n')
	text = text.replace ('<td>', '\t')
	text = text.replace ('<th>', '\t')
	# les tags
	for html, perso in tagHtml: text = text.replace (html.strip(), perso)
	for html, perso in tagsBlank: text = text.replace (html, perso)
	for tag in tagsClosing: text = text.replace ('</'+ tag +'>')
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
	text = Text (' '.join (ltext))
	text = text.shape()
	return text