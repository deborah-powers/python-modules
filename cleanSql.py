#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple.fileList import File
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
	newLine = newLine + table +' on '+ table +'_pk = '+ table +'_fk'
	return newLine

def cleanWhere (line):
	if 'where ' != line[:6]: return line;
	line = line.replace ('), ', ' and ')
	return line

def getResult (line):
	if line[:5] == 'list ':
		return line[5:]
	elif line[:13] == 'uniqueresult ':
		return line[13:]
		return newLine, line
	else: return ""

class SqlFile (File):
	def __init__ (self):
		File.__init__ (self, 'b/requete.txt')

	def prepare (self):
		self.fromFile()
		self.text = self.text.lower()
		self.clean()
		self.replace ('\t',' ')
		self.replace ('\n',' ')
		self.replace (',',', ')
		while self.contain ('  '): self.replace ('  ',' ')
		# self.replace (' (','(')
		self.replace (' .','.')

	def finish (self):
		self.replace (' --','\n--')
		self.replace ('; ',';\n')
		for word in wordBegin: self.replace (' '+ word, '\n'+ word)
		self.replace ('\ncase\nwhen','\n\tcase when')
		self.replace ('\nwhen','\n\twhen')
		while self.contain ('\n\n'): self.replace ('\n\n','\n')
		while self.contain ('  '): self.replace ('  ',' ')
	#	self.breakLine()

	def breakLine (self):
		sqlList = self.text.split ('\n')
		sqlRange = range (len (sqlList))
		for l in sqlRange:
			m= 160
			while m< len (sqlList[l]):
				f= sqlList[l][:m].rfind (' ')
				sqlList[l] = sqlList[l][:f] +'\n\t'+ sqlList[l][f+1:]
				m+=160
		self.text = '\n'.join (sqlList)
		self.text = self.text.lower()
		self.text = self.text.strip()

	def eraseComment (self):
		# supprimer les commentaires java, pour les requêtes jpa ou hibernate
		if self.contain ('\n// '):
			sqlList = self.text.split ('\n')
			sqlRange = range (len (sqlList) -1, 0, -1)
			for l in sqlRange:
				if sqlList[l][:3] =='// ': trash = self.pop(l)
			self.text = '\n'.join (sqlList)

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
		self.finish()

	def replaceAppend (self, word, newWord=None):
		if not newWord:
			newWord = ' '+ word +' '
			if '_' in word: newWord = newWord.replace ('_',' ')
		self.replace ('.append(' + word +')', newWord)

	# ________________________ fonctions pour jpa ________________________

	def prepareJpa (self):
		self.eraseComment()
		artefacts =( ' q_', '(q_' )
		for a in artefacts: self.replace (a, a[0])
		artefacts =( ';', '_dpo' )
		for a in artefacts: self.replace (a)
		artefacts =('from', 'innerjoin', 'leftjoin', 'where', 'groupby', 'orderby', 'list', 'uniqueresult')
		for w in artefacts:
			self.replace (').'+w+' (', ' '+w+' ')
			self.replace ('.'+w+' (', ' '+w+' ')
		artefacts =('desc', 'asc')
		for w in artefacts: self.replace ('.'+w+' ()', ' '+w+' ')
		artefacts =(('eq', '='), ('ne', '!='), ('istrue', 'is true'))
		for v,w in artefacts: self.replace ('.'+v+' (', ' '+w+' ')
		artefacts =('inner join', 'left join', 'group by', 'order by')
		for w in artefacts: self.replace (w.replace (' ',""), w)
		artefacts =( ('return ', ""), ('new jpaquery (', ""), ('this.entitymanager', 'select *'), ('.id', '_pk'), ('dpo_pk', '_pk'),
			(' list ', '\nlist '), (' uniqueresult ', '\nuniqueresult '))
		for v,w in artefacts: self.replace (v,w)

	def cleanJpa (self):
		toSelect =""
		self.finish()
		sqlList = self.text.split ('\n')
		sqlRange = range (len (sqlList))
		for l in sqlRange:
			sqlList[l] = cleanJoin (sqlList[l])
			sqlList[l] = cleanWhere (sqlList[l])
			if not toSelect:
				toSelect = getResult (sqlList[l])
				if toSelect: sqlList[l] =""
		self.text = '\n'.join (sqlList)
		if toSelect:
			if ', ' not in toSelect: toSelect = toSelect +'.*'
			self.replace ('select *', 'select '+ toSelect)
		self.replace (')')
		self.replace ('(')

	def main (self, tag):
		self.prepare()
		if tag == 'jpa':
			self.prepareJpa()
			self.cleanJpa()
		elif tag == 'hib': self.cleanHibernate()
		self.finish()
		self.title = self.title +' bis'
		self.fileFromData()
		self.toFile()

nbArgs = len (argv)
if __name__ != '__main__': pass
elif nbArgs >1:
	fileSql = SqlFile()
	tag = argv[1]
	fileSql.main (tag)
else: print (help)
