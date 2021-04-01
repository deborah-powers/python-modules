#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from debutils.file import File

help ="""nettoyer les fichiers sql
utilisation
	python3 cleanSql.py fichier
"""

def cleanSql (self):
	self.shape()
	wordBegin =('drop', 'create', 'declare', 'begin', 'select', 'inner', 'left', 'outer', 'update', 'insert', )
	wordSql =( 'or', 'replace', 'function', 'returns', 'as', 'integer', 'from', 'join', 'on', 'where', 'is', 'not', 'null', 'then', 'set', 'delete', 'into', 'values', 'nextval', 'now', 'case', 'when', 'if', 'else', 'end', 'language')
	for word in wordBegin: self.replace (word.upper(), word)
	for word in wordSql: self.replace (word.upper(), word)
	self.replace ('\t',' ')
	self.replace ('\n',' ')
	self.replace (',',', ')
	self.replace (' --','\n--')
	self.replace ('; ',';\n')
	for word in wordBegin: self.replace (' '+ word, '\n'+ word)
	while self.contain ('\n\n'): self.replace ('\n\n','\n')
	while self.contain ('  '): self.replace ('  ',' ')
	"""
	self.replace ('\n ','\n')
	wordPct = ',()'
	for pct in wordPct: self.replace (pct +'\n', pct +' ')
	"""

setattr (File, 'cleanSql', cleanSql)

if len (argv) <2: print (help)
else:
	fileSql = File (argv[1])
	fileSql.fromFile()
	fileSql.cleanSql()
	fileSql.toFile()