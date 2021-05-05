#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple import FileList

wordBegin =('drop', 'create', 'declare', 'begin', 'select', 'case when', 'when', 'else', 'end as', 'from', 'inner join', 'left join', 'left outer join', 'where', 'group by', 'order by', 'update', 'insert')

help ="""nettoyer les fichiers sql
utilisation
	python3 cleanSql.py fichier (tag)
"""
# ________________________ fonctions pour jpa ________________________

def cleanJoin (line):
	if ' join ' not in line: return line;
	d= line.find (' join ') +6
	newLine = line[:d]
	d= line.find (', ') +2
	table = line[d:]
	newLine = newLine + table +' on '+ table +'_pk = '+ table +'_fk'
	return newLine

def cleanWhere (line):
	if 'where ' != line[:6]: return line;
	line = line.replace ('), ', ' and ')
	return line

def getResult (line):
	if ' list ' not in line: return line, ""
	d= line.find (' list ')
	newLine = line[:d]
	line = line[d+6:]
	return newLine, line

class SqlFile (FileList):
	def __init__ (self, file =None):
		FileList.__init__ (self, file)
		self.extension = 'sql'

	def prepare (self):
		self.toText()
		self.text = self.text.lower()
		Text.clean (self)
		self.replace ('\t',' ')
		self.replace ('\n',' ')
		self.replace (',',', ')
		while self.contain ('\n\n'): self.replace ('\n\n','\n')
		while self.contain ('  '): self.replace ('  ',' ')

	def clean (self):
		self.replace (' --','\n--')
		self.replace ('; ',';\n')
		for word in wordBegin: self.replace (' '+ word, '\n'+ word)
		self.replace ('\ncase\nwhen','\n\tcase when')
		self.replace ('\nwhen','\n\twhen')
		while self.contain ('\n\n'): self.replace ('\n\n','\n')
		while self.contain ('  '): self.replace ('  ',' ')
		self.fromText()
		self.breakLine()

	def breakLine (self):
		sqlRange = self.range()
		for l in sqlRange:
			m= 160
			while m< len (self[l]):
				f= self[l][:m].rfind (' ')
				self[l] = self[l][:f] +'\n\t'+ self[l][f+1:]
				m+=160
		self.toText()
		self.text = self.text.lower()
		self.text = self.text.strip()

	def eraseComment (self):
		# supprimer les commentaires java, pour les requêtes jpa ou hibernate
		if self.contain ('\n// '):
			self.fromText()
			rangeLines = self.range()
			rangeLines.reverse()
			for l in rangeLines:
				if self[l][:3] =='// ': trash = self.pop(l)
			self.toText()

	# ________________________ fonctions pour hibernate ________________________

	def cleanHibernate (self):
		self.eraseComment()
		self.replace ('\nrequete')
		self.replace ('\n',' ')
		self.replace ('\t',' ')
		while self.contain ('  '): self.replace ('  ',' ')
		self.replace (');', ')')
		for word in toReplaceAppend: self.replaceAppend (word)
		self.replaceAppend ('virgule', ', ')
		self.replaceAppend ('equals', ' = ')
		self.replaceAppend ('" 1 "',"")
		self.replace ('.append(')
		self.replace (') = ', ' = ')
		self.replace ('), ', ', ')
		self.replace ('"\'', "'")
		self.replace ('\'"', "'")
		self.replace ('this.sumAs(', 'sum (')
		self.replace ('this.quote(', "'")
		self.replace ('.gettablename()')
		self.replace ('.getchamp()')
		self.replace (') ',' ')
		while self.contain ('  '): self.replace ('  ',' ')
		self.prepare()
		addUnderscoreBefore =( 'ac', 'montant', 'version', 'operation')
		addUnderscoreAfter =( 'beneficiaire', 'comptable', 'lien', 'montant', 'personne', 'recherche', 'vue')
		for name in addUnderscoreBefore: self.replace (name, '_'+ name)
		for name in addUnderscoreAfter:
			self.replace (' '+ name, ' '+ name +'_')
			self.replace ('.'+ name, '.'+ name +'_')
		tables =( ('vue_recherchecsf_ac', 'vue_recherche_csf_ac'), )
		for (nameWrong, nameGood) in tables: self.replace (nameWrong, nameGood)
		while self.contain ('__'): self.replace ('__','_')
		self.replace ('_ ',' ')
		self.replace (' _',' ')
		self.replace ('_.','.')
		self.replace ('._','.')
		self.clean()

	def replaceAppend (self, word, newWord=None):
		if not newWord:
			newWord = ' '+ word +' '
			if '_' in word: newWord = newWord.replace ('_',' ')
		self.replace ('.append(' + word +')', newWord)

	# ________________________ fonctions pour jpa ________________________

	def prepareJpa (self):
		self.prepare()
		self.eraseComment()
		artefacts =( ' q_', '(q_' )
		for a in artefacts: self.replace (a, a[0])
		artefacts =( ';', '_dpo' )
		for a in artefacts: self.replace (a)
		artefacts =('from', 'innerjoin', 'where', 'groupby', 'orderby', 'list')
		for w in artefacts: self.replace (').'+w+' (', ' '+w+' ')
		artefacts =('desc', 'asc')
		for w in artefacts: self.replace ('.'+w+' ()', ' '+w+' ')
		artefacts =(('eq', '='), ('ne', '!='))
		for v,w in artefacts: self.replace ('.'+v+' (', ' '+w+' ')
		artefacts =('inner join', 'group by', 'order by')
		for w in artefacts: self.replace (w.replace (' ',""), w)
		artefacts =( ('new jpaquery (this.entitymanager', 'select *'), ('.id', '_pk'), ('dpo_pk', '_pk'), (' list ', '\nlist '))
		for v,w in artefacts: self.replace (v,w)

	def cleanJpa (self):
		toSelect =""
		self.fromText()
		textRange = self.range()
		for l in textRange:
			textList[l] = cleanJoin (textList[l])
			textList[l] = cleanWhere (textList[l])
			if not toSelect:
				tmp = getResult (textList[l])
				textList[l] = tmp[0]
				toSelect = tmp[1]
		self.toText()
		if toSelect:
			if ', ' not in toSelect: toSelect = toSelect +'.*'
			self.replace ('select *', 'select '+ toSelect)
		self.replace (')')

	def main (self, tag):
	self.fromFile()
	if tag == 'jpa':
		self.prepareJpa()
		self.cleanJpa()
	elif tag == 'hib': self.cleanHibernate()
	else:
		self.prepare()
		self.clean()
	self.toFile()

nbArgs = len (argv)
if __name__ != '__main__': pass
elif nbArgs <2: print (help)
else:
	fileSql = fileSql (argv[1])
	tag = None
	if nbArgs >2: tag = argv[2]
	fileSql.main (tag)
