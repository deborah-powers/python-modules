#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple.fileList import FileList
from debutils.text import Text
from debutils.logger import log, coucou, message

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
	log (str(d) +' '+ table)
	newLine = newLine + table +' on '+ table +'_pk = '+ table +'_fk'
	return newLine

def cleanWhere (line):
	if 'where ' != line[:6]: return line;
	line = line.replace ('), ', ' and ')
	return line

def getResult (line):
	if ' list ' in line:
		d= line.find (' list ')
		newLine = line[:d]
		line = line[d+6:]
		return newLine, line
	elif ' uniqueresult ' in line:
		d= line.find (' uniqueresult ')
		newLine = line[:d]
		line = line[d+6:]
		return newLine, line
	else: return line, ""

class SqlFile (FileList):
	def __init__ (self, file=None):
		FileList.__init__ (self, '\n', file)

	def prepare (self):
		self.toText()
		self.text = self.text.lower()
		Text.clean (self)
		Text.replace (self, '\t',' ')
		Text.replace (self, '\n',' ')
		Text.replace (self, ',',', ')
		while self.contain ('\n\n'): Text.replace (self, '\n\n','\n')
		while self.contain ('  '): Text.replace (self, '  ',' ')

	def clean (self):
		self.toText()
		Text.replace (self, ' --','\n--')
		Text.replace (self, '; ',';\n')
		for word in wordBegin: Text.replace (self, ' '+ word, '\n'+ word)
		Text.replace (self, '\ncase\nwhen','\n\tcase when')
		Text.replace (self, '\nwhen','\n\twhen')
		while self.contain ('\n\n'): Text.replace (self, '\n\n','\n')
		while self.contain ('  '): Text.replace (self, '  ',' ')
		self.fromText()
		self.breakLine()

	def breakLine (self):
		sqlRange = self.range()
		for l in sqlRange:
			m= 160
			while m< len (self.list[l]):
				f= self.list[l][:m].rfind (' ')
				self.list[l] = self.list[l][:f] +'\n\t'+ self.list[l][f+1:]
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
				if self.list[l][:3] =='// ': trash = self.pop(l)
			self.toText()

	# ________________________ fonctions pour hibernate ________________________

	def cleanHibernate (self):
		self.eraseComment()
		Text.replace (self, '\nrequete')
		Text.replace (self, '\n',' ')
		Text.replace (self, '\t',' ')
		while self.contain ('  '): Text.replace (self, '  ',' ')
		Text.replace (self, ');', ')')
		for word in toReplaceAppend: self.replaceAppend (word)
		self.replaceAppend ('virgule', ', ')
		self.replaceAppend ('equals', ' = ')
		self.replaceAppend ('" 1 "',"")
		Text.replace (self, '.append(')
		Text.replace (self, ') = ', ' = ')
		Text.replace (self, '), ', ', ')
		Text.replace (self, '"\'', "'")
		Text.replace (self, '\'"', "'")
		Text.replace (self, 'this.sumAs(', 'sum (')
		Text.replace (self, 'this.quote(', "'")
		Text.replace (self, '.gettablename()')
		Text.replace (self, '.getchamp()')
		Text.replace (self, ') ',' ')
		while self.contain ('  '): Text.replace (self, '  ',' ')
		self.prepare()
		addUnderscoreBefore =( 'ac', 'montant', 'version', 'operation')
		addUnderscoreAfter =( 'beneficiaire', 'comptable', 'lien', 'montant', 'personne', 'recherche', 'vue')
		for name in addUnderscoreBefore: Text.replace (self, name, '_'+ name)
		for name in addUnderscoreAfter:
			Text.replace (self, ' '+ name, ' '+ name +'_')
			Text.replace (self, '.'+ name, '.'+ name +'_')
		tables =( ('vue_recherchecsf_ac', 'vue_recherche_csf_ac'), )
		for (nameWrong, nameGood) in tables: Text.replace (self, nameWrong, nameGood)
		while self.contain ('__'): Text.replace (self, '__','_')
		Text.replace (self, '_ ',' ')
		Text.replace (self, ' _',' ')
		Text.replace (self, '_.','.')
		Text.replace (self, '._','.')
		self.clean()

	def replaceAppend (self, word, newWord=None):
		if not newWord:
			newWord = ' '+ word +' '
			if '_' in word: newWord = newWord.replace ('_',' ')
		Text.replace (self, '.append(' + word +')', newWord)

	# ________________________ fonctions pour jpa ________________________

	def prepareJpa (self):
		self.prepare()
		self.fromText()
		self.eraseComment()
		artefacts =( ' q_', '(q_' )
		for a in artefacts: Text.replace (self, a, a[0])
		artefacts =( ';', '_dpo' )
		for a in artefacts: Text.replace (self, a)
		artefacts =('from', 'innerjoin', 'leftjoin', 'where', 'groupby', 'orderby', 'list', 'uniqueresult')
		for w in artefacts:
			Text.replace (self, ').'+w+' (', ' '+w+' ')
			Text.replace (self, '.'+w+' (', ' '+w+' ')
		artefacts =('desc', 'asc')
		for w in artefacts: Text.replace (self, '.'+w+' ()', ' '+w+' ')
		artefacts =(('eq', '='), ('ne', '!='))
		for v,w in artefacts: Text.replace (self, '.'+v+' (', ' '+w+' ')
		artefacts =('inner join', 'left join', 'group by', 'order by')
		for w in artefacts: Text.replace (self, w.replace (' ',""), w)
		artefacts =( ('new jpaquery (this.entitymanager', 'select *'), ('.id', '_pk'), ('dpo_pk', '_pk'), (' list ', '\nlist '), (' uniqueresult ', '\nuniqueresult '))
		for v,w in artefacts: Text.replace (self, v,w)

	def cleanJpa (self):
		toSelect =""
		# self.fromText()
		textRange = self.range()
		message ('l', len (textRange))
		for l in textRange:
			self.list[l] = cleanJoin (self.list[l])
			self.list[l] = cleanWhere (self.list[l])
			if not toSelect:
				tmp = getResult (self.list[l])
				self.list[l] = tmp[0]
				toSelect = tmp[1]
		self.toText()
		if toSelect:
			if ', ' not in toSelect: toSelect = toSelect +'.*'
			Text.replace (self, 'select *', 'select '+ toSelect)
		Text.replace (self, ')')

	def main (self, tag):
		self.fromFile()
		if tag == 'jpa':
			self.prepareJpa()
			self.cleanJpa()
		elif tag == 'hib': self.cleanHibernate()
		else:
			self.prepare()
			self.clean()
		self.fromText()
		self.toFile()

nbArgs = len (argv)
if __name__ != '__main__': pass
elif nbArgs <2: print (help)
else:
	fileSql = SqlFile (argv[1])
	tag = None
	if nbArgs >2: tag = argv[2]
	fileSql.main (tag)
