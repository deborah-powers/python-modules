#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
pointsEnd = '\n\t .,;:)?!'	# liste des symboles suivant les mots spéciaux
pointsStart = '( \n\t'
majList = (('a', 'A'), ('à', 'A'), ('b', 'B'), ('c', 'C'), ('\xe7', '\xc7'), ('d', 'D'), ('e', 'E'), ('é', 'E'), ('è', 'E'), ('ê', 'E'), ('ë', 'E'), ('f', 'F'), ('g', 'G'), ('h', 'H'), ('i', 'I'), ('î', 'I'), ('ï', 'I'), ('j', 'J'), ('k', 'K'), ('l', 'L'), ('m', 'M'), ('\n', '\n'), ('o', 'O'), ('xf4', 'xe4'), ('p', 'P'), ('q', 'Q'), ('r', 'R'), ('s', 'S'), ('\t', '\t'), ('u', 'U'), ('v', 'V'), ('w', 'W'), ('x', 'X'), ('y', 'Y'), ('z', 'Z'))
# liste des points, des chaines de caracteres suivies par une majuscule
artefacts =( ('> ','>'), ('\n ','\n'), (' \n','\n'), ('\n\n\n', '\n\n'))
wordsBeginMaj = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'victo', 'tony', 'simplon', 'loïc', 'france', 'paris', 'rueil')
wordsBeginMin = ('Deborah.powers', 'Deborah.noisetier', 'Http',
	'\nUpdate ', '\nSelect ', '\nFrom ', '\nWhere ', '\nHaving ', '\nGroup by ', '\nOrder by ', 'Inner join ', 'Outer join ', 'Left outer join ', 'Insert into ', 'Set schema ',
	'\nCd ', '\nPsql ','\nPg_', '\nPython ', '\nGit ',
	'\nDef ', '\nClass ', '\nConsole.log', '\nVar ', '\nFunction ', '\tReturn ',
	'\nLog.', '\tLog.', 'Mvn ', '\tPrivate ', '\tProtected ', '\tPublic ', '\nPrivate ', '\nProtected ', '\nPublic ')
weirdChars =(
	('«', '"'), ('»', '"'), ('–', '-'), ('‘', "'"), ('’', "'"), ('“', '"'), ('”', '"'), ('"', '"'), ('&hellip;', '...'), ('…', '...'),
	('\n ', '\n'), ('\r', ''), (' \n', '\n'), ("\\'", "'"), ('\\n', '\n'), ('\\r', ''), ('\\t', '\t'),
	('\\u00c2', 'Â'), ('\\u00ca', 'Ê'), ('\\u00cb', 'Ë'), ('\\u00ce', 'Î'), ('\\u00cf', 'Ï'), ('\\u00d4', 'Ô'), ('\\u00d6', 'Ö'), ('\\u00db', 'Û'), ('\\u00e0', 'à'), ('\\u00e2', 'â'), ('\\u00e7', 'ç'), ('\\u00e8', 'è'), ('\\u00e9', 'é'), ('\\u00ea', 'ê'), ('\\u00eb', 'ë'), ('\\u00ee', 'î'), ('\\u00ef', 'ï'), ('\\u00f4', 'ô'), ('\\u00f6', 'ö'), ('\\u00fb', 'û'),
	('\\', ''),
	('\x85', '.'), ('\x92', "'"), ('\x96', '"'), ('\x97', "'"), ('\x9c', ' '), ('\xa0', ' '),
	('&agrave;', 'à'), ('&acirc;', 'â'), ('&ccedil;', 'ç'), ('&eacute;', 'é'), ('&egrave;', 'è'), ('&ecirc;', 'ê'), ('&icirc;', 'î'), ('&iuml;', 'ï'), ('&ocirc;', 'ô'), ('&ugrave;', 'ù'), ('&ucirc;', 'û'),
	('&mdash;', ' '), ('&nbsp;', ''), ('&quot;', ''), ('&lt;', '<'), ('&gt;', '>'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&rsquo;', "'"),
	('&amp;', '&'), ('&#x27;', "'"), ('&#039', "'"), ('&#160;', ' '), ('&#39;', "'"), ('&#8217;', "'"),
	(',', ', '), ('(', ' ('), (')', ') '), ('[', ' ['), (']', '] '), ('{', ' {'), ('}', '} ')
)
tagHtml =(
	('\n<h1>', '\n====== '), ('</h1>\n', ' ======\n'), ('\n<h2>', '\n****** '), ('</h2>\n', ' ******\n'), ('\n<h3>', '\n------ '), ('</h3>\n', ' ------\n'), ('\n<h4>', '\n--- '), ('</h4>\n', ' ---\n'),
	('\n<hr>', '\n______\n'), ("\n<img src='", '\nImg\t'), ('\n<figure>', '\nFig\n'), ('</figure>', '\n/fig\n'), ('\n<xmp>', '\ncode\n'), ('</xmp>', '\n/code\n'),
	('\n<li>', '\n\t')
)
# fonctions pour les textes simples

def clean (text):
	# remplacer les caractères bizzares
	for i, j in weirdChars: text = text.replace (i, j)
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	for p in pointsEnd: text = text.replace (' '+p, p)
	for p in pointsStart: text = text.replace (p+' ', p)
	while '\t\n' in text: text = text.replace ('\t\n', '\n')
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	# la ponctuation
	while '....' in text: text = text.replace ('....', '...')
	text = text.replace ('...', ' ... ')
	text = text.replace ('  ', ' ')
	points = '!?'
	for p in points: text = text.replace (p, ' '+p)
	points = '() !?.;,:'
	for p in points: text = text.replace (p+' "', p+'"')
	for p in points:
		for q in points:
			while p+' '+q in text: text = text.replace (p+' '+q, p+q)
	# les appostrophes
	lettreAppostrophe = ('c', 'd', 'j', 'l', 'm', 'n', 'qu', 'r', 's', 't')
	for l in lettreAppostrophe:
		text = text.replace (' '+l+"' ", ' '+l+"'")
		text = text.replace (' '+ l.upper() +"' ", ' '+ l.upper() +"'")
	text = text.replace ("Qu'","Qu'")
	text = text.strip()
	while '  ' in text: text = text.replace ('  ', ' ')
	text = text.replace ('< !', '<!')
	return text

def toUpperCase (text):
	text ='\n'+ text
	points =( '\n', '. ', '! ', '? ', ': ', '\n_ ', '\n\t')
	for i, j in majList:
		for p in points: text = text.replace (p+i, p+j)
		for html, perso in tagHtml: text = text.replace (perso +i, perso +j)
	for p in pointsEnd:
		for q in pointsStart:
			for word in wordsBeginMaj: text = text.replace (q+ word +p, q+ word.capitalize () +p)
	for i, j in artefacts: text = text.replace (i, j)
	for artefact in wordsBeginMin: text = text.replace (artefact, artefact.lower ())
	text = text.strip ()
	return text

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
	textTmp = text
	for line in modelList:
		d= textTmp.find (line)
		if d>0: results.append (textTmp [:d])
		d+= len (line)
		textTmp = textTmp [d:]
	if len (textTmp) >0: results.append (textTmp)
	d=0
	rangeRes = range (len (results))
	for r in rangeRes:
		d= model.find ('%', d) +1
		if model [d] =='d': results [r] = int (results [r])
		elif model [d] =='f': results [r] = float (results [r])
	if (len (results) >2+ modelTmp.count ('%')): print ('erreur: %=', modelTmp.count ('%'), 'item =', len (results))
	return results

class Text ():
	def __init__ (self, string=""):
		self.text = string
	# ________________________ fonctions de mise en forme ________________________

	def shape (self):
		""" mettre le text en forme pour simplifier sa transformation
		j'utilise une mise en forme personnelle
		"""
		Text.clean (self)
		for char in '=*-_':
			while self.contain (7* char): self.replace (7* char, 6* char)
			for i,j in majList: self.replace (6* char +' '+i, '\n\n'+ 6* char +' '+j)
			self.replace (' '+ 6* char, ' '+ 6* char +'\n\n')
			self.replace (6* char +' ', '\n\n'+ 12* char +' ')
			self.replace (' '+ 6* char, ' '+ 12* char +'\n\n')
		self.text = '\n'+ self.text +'\n'
		# rajouter les majuscules apres chaque point
		self.upperCase()
		while self.contain ('\n\n\n'): self.replace ('\n\n\n', '\n\n')

	def upperCase (self):
		if self.contain ('\n/code\n'):
			paragraphList = self.split ('\ncode\n')
			paragraphRange = range (1, len (paragraphList))
			for i in paragraphRange:
				d= paragraphList [i].find ('\n/code\n') +7
				paragraphList [i] = paragraphList [i][:d] + toUpperCase (paragraphList [i][d:])
			self.text = '\ncode\n'.join (paragraphList)
		else: self.text = toUpperCase (self.text)

	def clean (self):
		self.text = clean (self.text)

	def cleanEnglish (self):
		self.clean ()
		wordList = ('and', 'for', 'then', 'in', 'on', 'to')
		for word in wordList:
			self.replace (' '+ word +'\t', ' '+ word +' ')
			self.replace (' '+ word +'\n', ' '+ word +' ')

	def fromModel (self, model):
		return fromModel (self.text, model)

	def comparLines (self, otherText, keepCommon=True, toSort=False):
		self.clean ()
		otherText.clean ()
		self.text = self.text.lower ()
		otherText.text = otherText.text.lower ()
		if self.text == otherText.text:
			print ('les textes sont identiques')
			return 'pareil'
		listA = self.split ('\n')
		listB = otherText.split ('\n')
		if toSort:
			listA.sort ()
			listB.sort ()
		listF = []
		trash = None
		pos =0; nbAdd =0; nbDel =0; nbCom =0
		while listA:
			if listA [0] in listB:
				pos = listB.index (listA [0])
				if pos >0:
					rpos = range (pos)
					for p in rpos:
						listF.append ('<t'+ listB.pop (0))
					nbDel += pos
				if keepCommon: listF.append ('=t'+ listA.pop (0))
				else: trash = listA.pop (0)
				nbCom +=1
				trash = listB.pop (0)
			else:
				listF.append ('>t'+ listA.pop (0))
				nbAdd +=1
		while listB:
			listF.append ('<t'+ listB.pop (0))
			nbDel +=1
		if nbAdd ==0 and nbDel ==0:
			print ('les textes sont identiques')
			return 'pareil'
		elif nbCom ==0:
			print ("les textes n'ont rien de commun")
			return 'different'
		else:
			print ('il y a %d additions et %d délétions entre les textes' % (nbAdd, nbDel))
			return '\n'.join (listF)

	def domAccolade (self):
		blockList = []
		nbOuvrante = self.countWord (' {')
		if nbOuvrante != self.countWord ('} '):
			print ('le texte est mal écrit')
			return ""
		elif nbOuvrante ==0: return self.text
		posD = self.index (' {')
		posF = self.index ('} ') +1
		ecart = self.text [posD:posF].count (' {') - self.text [posD:posF].count ('} ')
		while ecart >0:
			posF = self.index ('} ', posF) +1
			ecart = self.text [posD:posF].count (' {') - self.text [posD:posF].count ('} ')
		blockList.append (self.text [:posD])
		newText = Text ()
		newText.text = self.text [posD +1:posF -1]
		blockList.append (newText.domAccolade ())
		self.text = self.text [posF:]
		blockList.append (self.domAccolade ())
		return blockList

	def domAccoladePlan (self):
		blockList = []
		nbOuvrante = self.countWord (' {')
		if nbOuvrante != self.countWord ('} '):
			print ('le texte est mal écrit')
			return ""
		elif nbOuvrante ==0: return self.text
		self.replace ('} ', ' {')
		self.replace (' {', ' {')
		return self.split (' {')

	# ________________________ fonctions de bases ________________________

	def length (self):
		return len (self.text)

	def __str__ (self):
		if self.text: return self.text
		else: return ""

	def split (self, word):
		return self.text.split (word)

	def replace (self, oldWord, newWord=''):
		self.text = self.text.replace (oldWord, newWord)

	def strip (self):
		self.text = self.text.strip ()

	def contain (self, word):
		if word in self.text: return True
		else: return False

	def countWord (self, word):
		nb=0
		if word in self.text: nb= self.text.count (word)
		return nb

	def index (self, word, pos=0):
		posFind =-1
		if pos <0: pos = len (self.text) -pos
		if self.contain (word): posFind = self.text.find (word, pos)
		return posFind

	def rindex (self, word):
		posFind =-1
		if self.contain (word): posFind = self.text.rfind (word)
		return posFind

	def sliceNb (self, posStart, posEnd):
		res =""
		lText = self.length ()
		if posStart <0: posStart += lText
		if posEnd <0: posEnd += lText
		if posStart < posEnd: res = self.text [posStart:posEnd]
		return res

	def slice (self, wordStart, wordEnd):
		res =""
		if self.contain (wordStart) and self.contain (wordEnd):
			d= self.index (wordStart) + len (wordStart)
			f= self.index (wordEnd, d)
			if f>0 and f>d: res = self.sliceNb (d, f)
		return res

	def __lt__ (self, otherText):
		""" nécessaire pour trier les listes """
		return self.text < otherText.text

	# ________________________ conversion en html. ma mef est utilisée pour les textes simples ________________________

	def toHtml (self):
		self.shape()
		for char in '=*-_': self.replace (12* char, 6* char)
		# transformer la mise en page en balises
		for html, perso in tagHtml:
			if perso in self.text: self.replace (perso, html)
		# ajustement pour les grands titres et les images
		paragraphList = self.text.split ('\n')
		paragraphRange = range (len (paragraphList))
		for i in paragraphRange:
			if '<img' in paragraphList [i]: paragraphList [i] = paragraphList [i] +"'/>"
		self.text = '\n'.join (paragraphList)
		# les formules
		if self.contain ('\nM\t'):
			paragraphList = self.text.split ('\n')
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
			self.text = '\n'.join (paragraphList)
		# les figures
		if '<figure>' in self.text:
			# mettre en forme le contenu des figures
			paragraphList = self.text.split ('figure>')
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
			self.text = '\n'.join (paragraphList)
			self.text = self.text.strip ('\n')
			while '<li>\t' in self.text: self.replace ('<li>\t', '<li>')
			while '<ul>\t' in self.text: self.replace ('<ul>\t', '<ul>')
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
					paragraphList [p] = paragraphList [p][:d] +'<th>'+ paragraphList [p][d+4:]
				self.text = '</th>'.join (paragraphList)
		# nettoyer le texte pour faciliter la suite des transformations
		self.replace ('\t')
		self.clean()
		# rajouter les <p/>
		self.replace ('\n', '</p><p>')
		self.replace ('></p><p><', '><')
		self.replace ('</p><p><', '</p><')
		self.replace ('></p><p>', '><p>')
		# rajouter d'eventuel <p/> s'il n'y a pas de balise en debut ou fin de self.text
		if '<' not in self.text [0:3]: self.text = '<p>'+ self.text
		if '>' not in self.text [-3:]: self.text = self.text +'</p>'
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
			if '.' in paragraphTmp[d:]: e= paragraphTmp.rfind ('.')
			title = paragraphTmp [d:e].replace ('-',' ')
			title = title.replace ('_',' ')
			paragraphList [p] = paragraphTmp +"'>"+ title +'</a> '+ paragraphList [p][f:]
		self.text = " <a href='http".join (paragraphList)
		self.replace ('> <a ', '><a ')
		# pour les blocs de code
		self.replace ('\a', '\n')
		self.replace ('\f', '\t')
		self.clean()
		self.replace (' </', '</')

	def fromHtml (self):
		# les conteneurs
		container = [ 'div', 'section', 'ol', 'ul', 'table', 'figure', 'math' ]
		tagsBlank =( ('<hr/>', '\n______\n'), ('<hr>', '\n______\n'), ('<br>', '\n'), ('<br/>', '\n'))
		tagsClosing =( 'li', 'tr', 'th', 'td')
		for tag in container:
			self.replace ('</'+ tag +'>')
			self.replace ('<'+ tag +'>')
		# les tableaux
		self.replace ('</td>')
		self.replace ('</th>', ':')
		self.replace ('</tr>')
		self.replace ('<tr><td>', '\n')
		self.replace ('<tr><th>', '\n')
		self.replace ('<td>', '\t')
		self.replace ('<th>', '\t')
		# les tags
		for html, perso in tagHtml: self.replace (html.strip(), perso)
		for html, perso in tagsBlank: self.replace (html, perso)
		for tag in tagsClosing: self.replace ('</'+ tag +'>')
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
			link = ltext [t][d:f]
			f= ltext [t].find ('>', f) +1
			title = ltext [t][f:]
			d= ltext [t].find ('<a ')
			ltext [t] = ltext [t][:d] +' '+ title +': '+ link
		self.text = ' '.join (ltext)
		self.shape()

def testText ():
	textAccolade = Text ('abdefghijkmlmnopqrstuvwxyz')
	textCoucou = Text ('coucou tu vas bien ?')
	print ('exemple:', textCoucou)
	print ('nb lettres:', textCoucou.length ())
	print ('nb o:', textCoucou.count ('o'))
	print ('pos c:', textCoucou.index ('c'), 'et', textCoucou.rindex ('c'))
	print ('tranche entre deux index:')
	print ('t2:', textCoucou.sliceNb (2))
	print ('t2, 5:', textCoucou.sliceNb (2, 5))
	print ('t2, -2:', textCoucou.sliceNb (2, -2))
	print ('t-5, -2:', textCoucou.sliceNb (-5, -2))
	print ('t-5:', textCoucou.sliceNb (-5))
	print ('tranche entre deux mots, tu et bien:', textCoucou.slice ('tu', 'bien'))
	textCoucou = textCoucou.replace ('o', 'a')
	print ('remplacer un caractère:', textCoucou)
	textAccolade = Text ('a {bde {fg {hij} km {lmn} o} pqrs {tuv} wx} yz')
	print ('exemple:', textAccolade)
	print ('domAccolade emboîté:')
	res = textAccolade.domAccolade ()
	for line in res: print ('\t', line)
	print ('domAccolade linéaire:')
	res = textAccolade.domAccoladePlan ()
	for line in res: print ('\t', line)
	print ('comparaisons ligne à ligne')
	textA = Text ('bnanencnrnuninp')
	textB = Text ('dnanonqntnynind')
	textC = Text ('dnfnonqntnynzno')
	res = textA.comparLines (textA)
	res = textA.comparLines (textC)
	res = textA.comparLines (textB)
	print (res)
	print ('comparaisons lettre à lettre')
	textA = Text ('baecruip')
	textB = Text ('daoqtyid')
	textC = Text ('dfoqtyzo')
	import textAlignment
	res = textA.comparScore (textA)
	res = textA.comparScore (textB)
	print (res)