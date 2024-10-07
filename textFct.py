#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZaàâbcdeéêèëfghiîïjkmlmnoôpqrstuûvwxyz0123456789-\xe7\xc7'
uppercaseLetters = ('aA', 'àA', 'bB', 'cC', '\xe7\xc7', 'dD', 'eE', 'éE', 'èE', 'êE', 'ëE', 'fF', 'gG', 'hH', 'iI', 'îI', 'ïI', 'jJ', 'kK', 'lL', 'mM', 'nN', 'oO', '\xf4\xe4', 'pP', 'qQ', 'rR', 'sS', 'tT', 'uU', 'vV', 'wW', 'xX', 'yY', 'zZ')

# liste des points, des chaines de caracteres suivies par une majuscule
wordsBeginMaj = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'papi', 'victo', 'tony', 'robert', 'simplon', 'loïc', 'jared', 'leto', 'ville valo', 'valo', 'shelby', 'magritte', 'france', 'paris', 'rueil', 'malmaison', 'avon', 'fontainebleau', 'ivry', 'chateaudun', 'châteaudun' )
wordsBeginMin = ('Deborah.powers', 'Deborah.noisetier', 'Http', '\nPg_')
codeKeywords =(
	'set schema', 'declare', 'begin', 'do $$', 'update', 'select', 'from', 'inner join', 'outer join', 'left outer join', 'where',
	'having', 'group by', 'order by', 'insert into', 'if', 'elseif', 'end', 'loop', 'perform', 'drop ',
	'cd', 'psql', 'git', 'return', 'mvn', 'python', 'else',
	'def', 'class', 'console.log', 'var', 'function', 'private', 'protected', 'public',
	'log.debug', 'log.info'
)
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
urlWords =( (': /', ':/'), ('localhost: ', 'localhost:'), ('www. ', 'www.'), ('. jpg', '.jpg'), ('. png', '.png'), ('. css', '.css'), ('. js', '.js'), (': 80', ':80'), ('. com', '.com'), ('. org', '.org'), ('. net', '.net'), ('. fr', '.fr'), ('. ico', '.ico') )

# ________________________ ma mise en forme perso ________________________

def upperCaseIntern (text):
	text ='\n'+ text
	points =( '\n', '. ', '! ', '? ', ': ', ':\t', '\n_ ', '\n* ', '\n- ', '\n\t', '###### ', '______ ', '______ ', '------ ', '****** ', '====== ')
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
				d= paragraphList[i].find ('\n/code\n') +7
				paragraphList[i] = paragraphList[i][:d] + upperCaseIntern (paragraphList[i][d:])
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
		text = text.replace (letter +'?', letter +' ?')
		text = text.replace (letter +';', letter +' ;')
		text = text.replace ('...' + letter, '... '+ letter)
	while '  ' in text: text = text.replace ('  ', ' ')
	# restaurer les url
	if 'http' in text:
		"""
		textList = text.split ('http')
		textRange = range (1, len (textList))
		for t in textRange:
			print ('t',t)
			f= textList[t].find ('\n')
			if '\t' in textList[t][:f]: f= textList[t].find ('\t')
			if " ?" in textList[t][:f]: print (textList[t][:f])
		"""
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
	text = text.replace (' \n', '\n')
	text = text.replace (' \t', '\t')
	text = text.replace ('\t ', '\t')
	text = text.replace ('\n ', '\n')
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
		while 4* char in text: text = text.replace (4* char, 3* char)
		text = text.replace (' '+ 3* char +'\n', ' '+ 12* char +'\n\n')
		text = text.replace ('\n'+ 3* char +' ', '\n\n'+ 12* char +' ')
		text = text.replace ('\n'+ 3* char +'\n', '\n\n'+ 48* char +'\n\n')
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
	text = text.lower()
	model = cleanBasic (model)
	model = model.lower()
	typeList = ['d', 'f', 's']
	model = model.replace ('%%', '$')
	modelTmp = model
	for t in typeList: modelTmp = modelTmp.replace ('%'+t, '%')
	# récupérer les données du message sous forme de string
	modelList = modelTmp.split ('%')
	if not modelList[-1]: trash = modelList.pop (-1)
	if not modelList[0]: trash = modelList.pop (0)
	results = []
	for line in modelList:
		d= text.find (line)
		if d>0: results.append (text[:d])
		d+= len (line)
		text = text[d:]
	if len (text) >0: results.append (text)
	if not results[0]: trash = results.pop (0)
	d=0
	rangeRes = range (len (results))
	for r in rangeRes:
		d= model.find ('%', d) +1
		if d==0: continue
		if model[d] =='d': results[r] = int (results[r])
		elif model[d] =='f': results[r] = float (results[r])
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
	textList = fromModel (text, model)
	print (textList)

