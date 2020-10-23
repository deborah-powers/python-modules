#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# mots speciaux devant debuter par une majuscule
wordsUpp = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'victo', 'tony', 'simplon', 'loïc', 'france', 'paris', 'rueil')
pointsEnd = '\n\t .,;:?!'	# liste des symboles suivant les mots spéciaux
# "dictionnaire" des majuscule prenant en compte les accents
accents =( ('a','A'), ('à','A'), ('b','B'), ('c','C'), ('\xe7','\xc7'), ('d','D'), ('e','E'), ('é','E'), ('è','E'), ('ê','E'), ('ë','E'), ('f','F'), ('g','G'), ('h','H'), ('i','I'), ('î','I'), ('ï','I'), ('j','J'), ('k','K'), ('l','L'), ('m','M'), ('n','N'), ('o','O'), ('\xf4', '\xe4'), ('p','P'), ('q','Q'), ('r','R'), ('s','S'), ('t','T'), ('u','U'), ('v','V'), ('w','W'), ('x','X'), ('y','Y'), ('z','Z') )
# liste des points, des chaines de caracteres suivies par une majuscule
points =( '\n', '. ', '! ', '? ', ': ', '\n_ ', '\n\t')
pointsShape =( '\n\t- ', '______ ', '\n------ ' )
artefacts =(
	('> ','>'), ('Deborah.powers', 'deborah.powers'), ('Http','http'), ('\n ','\n'), (' \n','\n'),
	(' ______\n', ' ______\n\n'), ('\n______ ', '\n\n______ '),
 	('\n______\n\n______ ', '\n\n______\n______ '),
	('------ ', '\n------ '), (' ------', ' ------\n'), ('\n\n\n', '\n\n')
)
# 	('\n______\n\n______ ', '\n\n________________________\n______ '),
# caractères à remplacer
weirdChars =(
	('«', '"'), ('»', '"'), ('–', '-'), ('‘', "'"), ('“', '"'), ('”', '"'), ('"', '"'), ('…', '...'),
	('\n ', '\n'), ('\r', ''), (' \n', '\n'), ('\\', ''), ("\\'", "'"), ('\\n', '\n'), ('\\r', ''), ('\\t', '\t'),
	('\\u00c2', 'Â'), ('\\u00ca', 'Ê'), ('\\u00cb', 'Ë'), ('\\u00ce', 'Î'), ('\\u00cf', 'Ï'), ('\\u00d4', 'Ô'), ('\\u00d6', 'Ö'), ('\\u00db', 'Û'), ('\\u00e0', 'à'), ('\\u00e2', 'â'), ('\\u00e7', 'ç'), ('\\u00e8', 'è'), ('\\u00e9', 'é'), ('\\u00ea', 'ê'), ('\\u00eb', 'ë'), ('\\u00ee', 'î'), ('\\u00ef', 'ï'), ('\\u00f4', 'ô'), ('\\u00f6', 'ö'), ('\\u00fb', 'û'),
	('\x85', '.'), ('\x92', "'"), ('\x96', '"'), ('\x97', "'"), ('\x9c', ' '), ('\xa0', ' '),
	('&agrave;', 'à'), ('&acirc;', 'â'), ('&ccedil;', 'ç'), ('&eacute;', 'é'), ('&egrave;', 'è'), ('&ecirc;', 'ê'), ('&icirc;', 'î'), ('&iuml;', 'ï'), ('&ocirc;', 'ô'), ('&ugrave;', 'ù'), ('&ucirc;', 'û'),
	('&mdash;', ' '), ('&nbsp;', ''), ('&quot;', ''), ('&lt;', '<'), ('&gt;', '>'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&rsquo;', "'"),
	('&amp;', '&'), ('&#039', "'"), ('&#160;', ' '), ('&#39;', "'"), ('&#8217;', "'")
)
# fonctions pour les textes simples
def clean (text):
	text = text.replace ('\r',"")
	# remplacer les caractères bizzares
	for i,j in weirdChars: text = text.replace (i,j)
	text = text.strip()
	while ('  ') in text: text = text.replace ('  ', ' ')
	text = text.replace (' \n', '\n')
	text = text.replace ('\n ', '\n')
	while ('\t\n') in text: text = text.replace ('\t\n', '\n')
	while ('\n\t') in text: text = text.replace ('\n\t', '\n')
	while ('\n\n') in text: text = text.replace ('\n\n', '\n')
	return text

def fromModel (text, model):
	# remplacer scanf
	# préparer le modèle
	typeList =['d','f','s']
	model = model.replace ('%%', '$')
	modelTmp = model
	for t in typeList: modelTmp = modelTmp.replace ('%'+t, '%')
	# récupérer les données du message sous forme de string
	modelList = modelTmp.split ('%')
	results =[]
	textTmp = text
	for line in modelList:
		d= textTmp.find (line)
		if d>0: results.append (textTmp[:d])
		d+= len (line)
		textTmp = textTmp[d:]
	if len (textTmp) >0: results.append (textTmp)
	d=0
	rangeRes = range (len (results))
	for r in rangeRes:
		d= model.find ('%',d) +1
		if model[d] =='d': results[r] = int (results[r])
		elif model[d] =='f': results[r] = float (results[r])
	if (len (results) >2+ modelTmp.count ('%')): print ('erreur: %=', modelTmp.count ('%'), 'item =', len (results))
	return results

class Text():
	def __init__(self, string=""):
		self.text = string

	# ________________________ fonctions de mise en forme ________________________

	def shape (self):
		self.clean()
		# mettre le text en forme pour simplifier sa transformation
		while self.contain ('_______'): self.replace ('_______', '______')
		while self.contain ('-------'): self.replace ('-------', '------')
		self.text = '\n'+ self.text +'\n'
		# rajouter les majuscules apres chaque point
		self.upperCase()
		for p in pointsShape:
			for i,j in accents: self.replace (p+i, p+j)
		for i,j in artefacts: self.replace (i,j)
		self.strip()

	def toMd (self):
		self.shape()
		self.text = '\n'+ self.text +'\n'
		tmpList = self.split ('______\n______ ')
		rangeList = range (1, len (tmpList))
		for l in rangeList:
			f= tmpList[l].find (' _')
			tmpList[l] = tmpList[l][:f].upper() + tmpList[l][f:]
		self.text = '============ '.join (tmpList)
		self.replace ('______ ', '============ ')
		self.replace (' ______', ' ============')
		self.replace ('------ ', '** ')
		self.replace (' ------', ' **')
		while self.contain ('\n\t\t'): self.replace ('\n\t\t', '\n\t')
		self.replace ('\n\t', '\n* ')
		self.replace ('\n', '\n\n')

	def upperCase (self):
	#	self.text = self.text.capitalize()
		for p in points:
			for i,j in accents: self.replace (p+i, p+j)
		for p in pointsEnd:
			for word in wordsUpp: self.replace (' '+ word +p, ' '+ word.capitalize() +p)

	def clean (self):
		self.text = clean (self.text)

	def cleanPunctuation (self):
		points = '.,;:?!'
		for p in points: self.replace (p, ' '+p+' ')
		while self.contain ('  '): self.replace ('  ', ' ')
		for p in points[:4]: self.replace (' '+p, p)
		while self.contain ('....'): self.replace ('....', '...')
		self.replace (': //', '://')
		self.replace ('. com', '.com')
		self.replace ('. fr', '.fr')
		self.replace ('. html', '.html')
		self.replace ('//www. ', '//www.')

	def fromModel (self, model):
		return fromModel (self.text, model)

	def comparLines (self, otherText, keepCommon=True, toSort=False):
		self.clean()
		otherText.clean()
		self.text = self.text.lower()
		otherText.text = otherText.text.lower()
		if self.text == otherText.text:
			print ('les textes sont identiques')
			return 'pareil'
		listA = self.split ('\n')
		listB = otherText.split ('\n')
		if toSort:
			listA.sort()
			listB.sort()
		listF =[]
		trash = None
		pos =0; nbAdd =0; nbDel =0; nbCom =0
		while listA:
			if listA[0] in listB:
				pos = listB.index (listA[0])
				if pos >0:
					rpos = range (pos)
					for p in rpos:
						listF.append ('<\t'+ listB.pop(0))
					nbDel += pos
				if keepCommon: listF.append ('=\t'+ listA.pop(0))
				else: trash = listA.pop(0)
				nbCom +=1
				trash = listB.pop(0)
			else:
				listF.append ('>\t'+ listA.pop(0))
				nbAdd +=1
		while listB:
			listF.append ('<\t'+ listB.pop(0))
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
		blockList =[]
		nbOuvrante = self.countWord ('{')
		if nbOuvrante != self.countWord ('}'):
			print ('le texte est mal écrit')
			return ""
		elif nbOuvrante ==0: return self.text
		posD = self.index ('{')
		posF = self.index ('}') +1
		ecart = self.text[posD:posF].count ('{') - self.text[posD:posF].count ('}')
		while ecart >0:
			print (ecart, posD, posF)
			posF = self.index ('}', posF) +1
			ecart = self.text[posD:posF].count ('{') - self.text[posD:posF].count ('}')
		blockList.append (self.text[:posD])
		newText = Text()
		newText.text = self.text[posD +1:posF -1]
		blockList.append (newText.domAccolade())
		self.text = self.text[posF:]
		blockList.append (self.domAccolade())
		return blockList

	def domAccoladePlan (self):
		blockList =[]
		nbOuvrante = self.countWord ('{')
		if nbOuvrante != self.countWord ('}'):
			print ('le texte est mal écrit')
			return ""
		elif nbOuvrante ==0: return self.text
		self.replace ('}', '{')
		self.replace (' {', '{')
		return self.split ('{')

	# ________________________ fonctions de bases ________________________

	def length (self):
		return len (self.text)

	def __str__(self):
		if self.text: return self.text
		else: return ""

	def split (self, word):
		return self.text.split (word)

	def replace (self, oldWord, newWord=''):
		self.text = self.text.replace (oldWord, newWord)

	def strip (self):
		self.text = self.text.strip()

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
		lText = self.length()
		if posStart <0: posStart += lText
		if posEnd <0: posEnd += lText
		if posStart < posEnd: res = self.text [posStart:posEnd]
		return res

	def slice (self, wordStart, wordEnd):
		res =""
		if self.contain (wordStart) and self.contain (wordEnd):
			d= self.index (wordStart) + len (wordStart)
			f= self.index (wordEnd, d)
			if f>0 and f>d: res = self.sliceNb (d,f)
		return res

	def __lt__ (self, otherText):
		""" nécessaire pour trier les listes """
		return self.text < otherText.text

def testText():
	textAccolade = Text ('abdefghijkmlmnopqrstuvwxyz')
	textCoucou = Text ('coucou tu vas bien ?')
	print ('exemple:', textCoucou)
	print ('nb lettres:', textCoucou.length())
	print ('nb o:', textCoucou.count ('o'))
	print ('pos c:', textCoucou.index ('c'), 'et', textCoucou.rindex ('c'))
	print ('tranche entre deux index:')
	print ('\t2:', textCoucou.sliceNb (2))
	print ('\t2,5:', textCoucou.sliceNb (2,5))
	print ('\t2,-2:', textCoucou.sliceNb (2,-2))
	print ('\t-5,-2:', textCoucou.sliceNb (-5,-2))
	print ('\t-5:', textCoucou.sliceNb (-5))
	print ('tranche entre deux mots, tu et bien:', textCoucou.slice ('tu', 'bien'))
	textCoucou = textCoucou.replace ('o', 'a')
	print ('remplacer un caractère:', textCoucou)
	
	textAccolade = Text ('a{bde{fg{hij}km{lmn}o}pqrs{tuv}wx}yz')
	print ('exemple:', textAccolade)
	print ('domAccolade emboîté:')
	res = textAccolade.domAccolade()
	for line in res: print ('\t', line)
	print ('domAccolade linéaire:')
	res = textAccolade.domAccoladePlan()
	for line in res: print ('\t', line)

	print ('comparaisons ligne à ligne')
	textA = Text ('b\na\ne\nc\nr\nu\ni\np')
	textB = Text ('d\na\no\nq\nt\ny\ni\nd')
	textC = Text ('d\nf\no\nq\nt\ny\nz\no')
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

if __name__ == '__main__': testText()
