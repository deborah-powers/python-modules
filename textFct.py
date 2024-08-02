#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZaàâbcdeéêèëfghiîïjkmlmnoôpqrstuûvwxyz0123456789-\xe7\xc7'
uppercaseLetters = ('aA', 'àA', 'bB', 'cC', '\xe7\xc7', 'dD', 'eE', 'éE', 'èE', 'êE', 'ëE', 'fF', 'gG', 'hH', 'iI', 'îI', 'ïI', 'jJ', 'kK', 'lL', 'mM', 'nN', 'oO', '\xf4\xe4', 'pP', 'qQ', 'rR', 'sS', 'tT', 'uU', 'vV', 'wW', 'xX', 'yY', 'zZ')

# liste des points, des chaines de caracteres suivies par une majuscule
wordsBeginMaj = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'victo', 'tony', 'simplon', 'loïc', 'france', 'paris', 'rueil')
wordsBeginMin = ('Deborah.powers', 'Deborah.noisetier', 'Http', '\nPg_')
codeKeywords =(
	'set schema', 'declare', 'begin', 'do $$', 'update', 'select', 'from', 'inner join', 'outer join', 'left outer join', 'where',
	'having', 'group by', 'order by', 'insert into', 'if', 'elseif', 'end', 'loop', 'perform',
	'cd', 'psql', 'git', 'return', 'mvn', 'python', 'else',
	'def', 'class', 'console.log', 'var', 'function', 'private', 'protected', 'public',
	'log.debug', 'log.info'
)
urlWords =( (': /', ':/'), ('localhost: ', 'localhost:'), ('www. ', 'www.'), ('. jpg', '.jpg'), ('. png', '.png'), ('. css', '.css'), ('. js', '.js'), (': 80', ':80'), ('. com', '.com'), ('. org', '.org'), ('. net', '.net'), ('. fr', '.fr'), ('. ico', '.ico') )
weirdChars =(
	('« ', '"'), (' »', '"'), ('«', '"'), ('»', '"'), ('–', '-'), ('‘', "'"), ('’', "'"), ('“', '"'), ('”', '"'), ('"', '"'), ('&hellip;', '...'), ('&#8230;', '...'), ('…', '...'),
	('\n ', '\n'), ('\r', ''), (' \n', '\n'), ("\\'", "'"), ('\\n', '\n'), ('\\r', ''), ('\\t', '\t'),
	('\\u00c2', 'Â'), ('\\u00ca', 'Ê'), ('\\u00cb', 'Ë'), ('\\u00ce', 'Î'), ('\\u00cf', 'Ï'), ('\\u00d4', 'Ô'), ('\\u00d6', 'Ö'), ('\\u00db', 'Û'), ('\\u00e0', 'à'), ('\\u00e2', 'â'), ('\\u00e7', 'ç'), ('\\u00e8', 'è'), ('\\u00e9', 'é'), ('\\u00ea', 'ê'), ('\\u00eb', 'ë'), ('\\u00ee', 'î'), ('\\u00ef', 'ï'), ('\\u00f4', 'ô'), ('\\u00f6', 'ö'), ('\\u00fb', 'û'),
	('\\', '/'),
	('\x85', '.'), ('\x92', "'"), ('\x96', '"'), ('\x97', "'"), ('\x9c', ' '), ('\xa0', ' '),
	('&agrave;', 'à'), ('&acirc;', 'â'), ('&ccedil;', 'ç'), ('&eacute;', 'é'), ('&egrave;', 'è'), ('&ecirc;', 'ê'), ('&icirc;', 'î'), ('&iuml;', 'ï'), ('&ocirc;', 'ô'), ('&ugrave;', 'ù'), ('&ucirc;', 'û'), ('&apos;', "'"),
	('&mdash;', ' '), ('&nbsp;', ''), ('&oelig;', 'oe'), ('&quot;', ''), ('&lt;', '<'), ('&gt;', '>'), ('&lsquo;', '"'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&rsquo;', "'"), ('&laquo;', '"'), ('&raquo;', '"'), ('&#8220;', '"'), ('&#8221;', '"'), ('&#8211;', '-'),
	('&amp;', '&'), ('&#x27;', "'"), ('&#039', "'"), ('&#160;', ' '), ('&#39;', "'"), ('&#8217;', "'"), ('\n" ', '\n"')
)
tagHtml =(
	('\n<h1>', '\n====== '), ('</h1>\n', ' ======\n'), ('\n<h2>', '\n****** '), ('</h2>\n', ' ******\n'), ('\n<h3>', '\n------ '), ('</h3>\n', ' ------\n'), ('\n<h4>', '\n--- '), ('</h4>\n', ' ---\n'),
	('\n<hr>', '\n\n************************************************\n\n'), ("\n<img src='", '\nImg\t'), ('\n<figure>', '\nFig\n'), ('</figure>', '\n/fig\n'), ('\n<xmp>', '\ncode\n'), ('</xmp>', '\n/code\n'),
	('\n<li>', '\n\t')
)
# ________________________ ma mise en forme perso ________________________


def upperCaseIntern (text):
	text ='\n'+ text
	points =( '\n', '. ', '! ', '? ', ': ', '\n_ ', '\n* ', '\n- ', '\n\t', '###### ', '______ ', '______ ', '------ ', '****** ', '====== ')
	for i, j in uppercaseLetters:
		for p in points: text = text.replace (p+i, p+j)
	punctuation = '({[?!;.,:]})"\' \n\t'
	for word in wordsBeginMaj:
		for p in punctuation:
			text = text.replace (" "+ word +p, " "+ word.capitalize() +p)
			text = text.replace ("\t"+ word +p, "\t"+ word.capitalize() +p)
	"""
	for p in " "+ punctuation[-11:]:
		for q in " "+ punctuation[0:5]:
			for word in wordsBeginMaj:
				if word == 'powers': print (p,q)
				text = text.replace (q+ word +p, q+ word.capitalize() +p)
	"""
	for word in wordsBeginMin: text = text.replace (word, word.lower())
	# le code
	for artefact in codeKeywords:
		text = text.replace ('\n'+ artefact.capitalize() +' ', '\n'+ artefact +' ')
		text = text.replace ('\t'+ artefact.capitalize() +' ', '\t'+ artefact +' ')
		text = text.replace ('\n'+ artefact.capitalize() +'\n', '\n'+ artefact +'\n')
		text = text.replace ('\t'+ artefact.capitalize() +'\n', '\t'+ artefact +'\n')
	text = text.strip()
	return text

def upperCase (text, case=""):
	"""	rest: je supprime l'ancienne casse
		upper: je rajoute les majuscules
	log (type (text))
	"""
	if 'reset' in case: text = text.lower()
	if 'upper' in case:
		text = '\n'+ text +'\n'
		if '\n/code\n' in text:
			paragraphList = text.split ('\ncode\n')
			paragraphRange = range (1, len (paragraphList))
			for i in paragraphRange:
				d= paragraphList [i].find ('\n/code\n') +7
				paragraphList [i] = paragraphList [i][:d] + upperCaseIntern (paragraphList [i][d:])
			text = '\ncode\n'.join (paragraphList)
		else: text = upperCaseIntern (text)
	text = text.strip()
	return text

def findEndUrl (text, pos=0):
	charEndUrl = '\n\t \'",;!()[]{}'
	lenText = len (text) +1
	posEnd = lenText
	posTmp = lenText
	for char in charEndUrl:
		posTmp = text.find (char, pos)
		if posTmp >0 and posTmp < posEnd: posEnd = posTmp
	return posEnd

def cleanBasic (text):
	for i, j in weirdChars: text = text.replace (i, j)
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	text = text.replace ('\n ', '\n')
	text = text.replace (' \n', '\n')
	text = text.replace ('\t ', '\t')
	text = text.replace (' \t', '\t')
	while '\t\n' in text: text = text.replace ('\t\n', '\n')
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	return text

def cleanHtml (text):
	text = cleanBasic (text)
	text = text.replace ('\n', ' ')
	text = text.replace ('\t', ' ')
	for i, j in weirdChars: text = text.replace (i, j)
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	text = text.replace ('> ', '>')
	text = text.replace (' <', '<')
	text = text.replace (' >', '>')
	text = text.replace (' />', '/>')
	"""
	text = text.replace ('><', '>\n<')
	innerTagclosing =( 'a', 'p', 'span', 'i', 'strong', 'option', 'button', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4')
	for tag in innerTagclosing:
		text = text.replace ('\n</'+ tag +'>', '</'+ tag +'>')
		text = text.replace ('<'+ tag +'>\n', '<'+ tag +'>')
	text = text.replace ('</tr>\n<tr', '</tr><tr')
	"""
	return text

def cleanCss (text):
	text = cleanBasic (text)
	text = text.replace ('\n', ' ')
	text = text.replace ('\t', ' ')
	for i, j in weirdChars: text = text.replace (i, j)
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	tagCleanSpaces =( '{', '}', '/*', '*/', ':', ';' )
	for tag in tagCleanSpaces:
		text = text.replace (' '+ tag +' ', tag)
		text = text.replace (' '+ tag, tag)
		text = text.replace (tag +' ', tag)
		text = text.replace ('}', ';}')
		text = text.replace (';;', ';')
		text = text.replace ('};', '}')
	# nettoyer les commentaires
	commList = text.split ('/*')
	commRange = range (commList, 1)
	for c in commRange:
		f= commList[c].find ('*/')
		if '{' in commList[c][:f]: commList[c] = commList[c][f:]
	text = '/*'.join (commList)
	text = text.replace ('/**/', "")
	# optimiser les blocs
	commList = text.split ('{')
	commRange = range (commList, 1)
	for c in commRange:
		f= commList[c].find ('}')
		if f>0:
			innerComm = commList[c][:f].replace (' ', ';')
			if innerComm.count (';') >1:
				innerComm = innerComm.replace (';', ';\n\t')
				innerComm = '\n\t' + innerComm +'\n'
			elif innerComm.count (';') ==1: innerComm = ' '+ innerComm +' '
			commList[c] = innerComm + commList[c][f:]
		else: commList[c] = '\n\t' + commList[c]
	text = ' {'.join (commList)
	text = text.replace ('}', '}\n')
	text = text.replace ('/*', '\n/* ')
	text = text.replace ('*/', ' */\n')
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	return text

def cleanText (text):
	text = cleanBasic (text)
	# la ponctuation
	punctuation = '?!;.:,'
	for p in punctuation: text = text.replace (' '+p, p)
	while '....' in text: text = text.replace ('....', '...')
	for letter in letters:
		text = text.replace (letter +'!', letter +' !')
		text = text.replace (letter +';', letter +' ;')
		text = text.replace ('...' + letter, '... '+ letter)
	while '  ' in text: text = text.replace ('  ', ' ')
	# restaurer les url
	textList = text.split ('?')
	textRange = range (len (textList) -1)
	for t in textRange:
		if 'http' in textList[t]:
			d= textList[t].rfind ('http')
			if " " in textList[t][d:] or '\n' " " in textList[t][d:]: textList[t] = textList[t] +" "
		else: textList[t] = textList[t] +" "
	text = '?'.join (textList)
	# restaurer les heures
	textList = text.split (':')
	textRange = range (len (textList) -1)
	for t in textRange:
		if len (textList[t]) >1 and len (textList[t+1]) >1 and textList[t][-2] in '012345' and textList[t][-1] in '0123456789' and textList[t+1][0] in '012345' and textList[t+1][1] in '0123456789': continue
		else: textList[t+1] =" "+ textList[t+1]
	text = ':'.join (textList)
	while '  ' in text: text = text.replace ('  ', ' ')
	charEndUrl = '\n\t \'",;!()[]{}'
	for wordStart, wordEnd in urlWords[:8]: text = text.replace (wordStart, wordEnd)
	for wordStart, wordEnd in urlWords[8:]:
		for e in charEndUrl: text = text.replace (wordStart +e, wordEnd +e)
	return text

def cleanTextVa (text):
	text = cleanBasic (text)
	# la ponctuation
	punctuation = '?!;.:,'
	for p in punctuation: text = text.replace (' '+p, p)
	while '....' in text: text = text.replace ('....', '...')
	for letter in letters:
		text = text.replace (letter +'?', letter +' ?')
		text = text.replace (letter +'!', letter +' !')
		text = text.replace (letter +';', letter +' ;')
		text = text.replace ('...' + letter, '... '+ letter)
	text = text.replace (':', ': ')
	while '  ' in text: text = text.replace ('  ', ' ')
	# restaurer les heures
	liste = text.split (': ')
	rliste = range (1, len (liste))
	for l in rliste:
		if len (liste[l]) >1 and liste[l][0] in '012345' and liste[l][1] in '0123456789':
			if len (liste[l]) >2 and liste[l][2] != '.':
				d= findEndUrl (liste[l])
				if d!=2: liste[l] =' '+ liste[l]
		else: liste[l] =' '+ liste[l]
	text = ':'.join (liste)
	text = text.replace (' \n', '\n')
	text = text.replace (' \t', '\t')
	# restaurer les url
	charEndUrl = '\n\t \'",;!()[]{}'
	for wordStart, wordEnd in urlWords[:8]: text = text.replace (wordStart, wordEnd)
	for wordStart, wordEnd in urlWords[8:]:
		for e in charEndUrl: text = text.replace (wordStart +e, wordEnd +e)
	liste = text.split (' ?')
	rliste = range (1, len (liste))
	for l in rliste:
		d= findEndUrl (liste[l])
		if '=' not in liste[l][:d]: liste[l-1] = liste[l-1] +' '
	text = '?'.join (liste)
	return text

def shape (text, case=""):
	""" mettre le text en forme pour simplifier sa transformation
	j'utilise une mise en forme personnelle
	addCase
		rien: je ne rajoute pas les majuscules
		rest: je supprime l'ancienne casse
		upper: je rajoute les majuscules
	"""
	text = cleanText (text)
	text = '\n'+ text +'\n'
	for char in '*#=~-_':
		while 3* char in text: text = text.replace (3* char, 2* char)
		text = text.replace (' '+ 2* char +'\n', ' '+ 12* char +'\n\n')
		text = text.replace ('\n'+ 2* char +' ', '\n\n'+ 12* char +' ')
		text = text.replace ('\n'+ 2* char +'\n', '\n\n'+ 48* char +'\n\n')
	while '\n\n\n' in text: text = text.replace ('\n\n\n', '\n\n')
	if case: text = upperCase (text, case)
	return text

def toMarkdown (text):
	text = shape (text, 'upper')
	text = text.replace ('============', '=')
	text = text.replace ('************', '==')
	text = text.replace ('------------', "'''")
	text = text.replace ('\n\t', '\n- ')
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	text = text.replace ('\n', '\n\n')
	return text

	# ________________________ fonctions de bases ________________________

def fromModel (text, model):
	# remplacer scanf
	# préparer le modèle
	text = cleanBasic (text)
	model = cleanBasic (model)
	typeList = ['d', 'f', 's']
	model = model.replace ('%%', '$')
	modelTmp = model
	for t in typeList: modelTmp = modelTmp.replace ('%'+t, '%')
	# récupérer les données du message sous forme de string
	modelList = modelTmp.split ('%')
	results = []
	for line in modelList:
		d= find (text, line)
		results.append (text [:d])
		d+= len (line)
		text = text [d:]
	if len (text) >0: results.append (text)
	if not results[0]: trash = results.pop (0)
	d=0
	rangeRes = range (len (results))
	for r in rangeRes:
		d= model.find ('%', d) +1
		if d==0: continue
		if model [d] =='d': results [r] = int (results [r])
		elif model [d] =='f': results [r] = float (results [r])
	if (len (results) >2+ modelTmp.count ('%')): print ('erreur: %=', modelTmp.count ('%'), 'item =', len (results))
	return results

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
	return res

""" ________________________ conversion en html. ma mef est utilisée pour les textes simples ________________________ """

def toHtml (text):
	text = shape (text)
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
	text = text.replace ('\t', "")
	text = cleanText (text)
	# les <strong/>, mettre en gras le début d'une ligne
	if '\n* ' in text:
		paragraphList = text.split ('\n* ')
		lc= range (len (paragraphList))
		# rajouter les balises fermantes
		for l in lc:
			if ': ' in paragraphList[l][1:100]:
				paragraphList[l] = paragraphList[l].replace (': ',':</strong> ',1)
				paragraphList[l] = '<strong>' + paragraphList[l]
			text = '\n'.join (paragraphList)
	# rajouter les <p/>
	text = text.replace ('\n', '</p><p>')
	text = text.replace ('></p><p><', '><')
	text = text.replace ('></p><p>', '><p>')
	text = text.replace ('</p><p><', '</p><')
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
	text = cleanText (text)
	print ('clean\t', text)
	text = upperCase (text, 'upper')
	print ('upperCase\t', text)
	print ('find\t', find (text, "fk'", 20))
	print ('rfind\t', rfind (text, "fk'"))
	text = toHtml (text)
	print ('toHtml\t', text)
	text = fromHtml (text)
	print ('fromHtml\t', text)
	textList = fromModel (text, model)
	print (textList)

