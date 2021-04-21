#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileSimple import File
from debutils.list import List

help ="""nettoyer les fichiers sql
utilisation
	python3 cleanSql.py fichier
"""

def cleanSql (self):
	self.text = self.text.lower()
	self.shape()
	wordBegin =('drop', 'create', 'declare', 'begin', 'select', 'case when', 'from', 'inner', 'left', 'outer', 'where', 'group by', 'order by', 'update', 'insert')
	"""
	wordSql =( 'or', 'replace', 'function', 'returns', 'as', 'integer', 'from', 'join', 'on', 'where', 'is', 'not', 'null', 'then', 'set', 'delete', 'into', 'values', 'nextval', 'now', 'case', 'when', 'if', 'else', 'end', 'language')
	for word in wordBegin: self.replace (word.upper(), word)
	for word in wordSql: self.replace (word.upper(), word)
	"""
	self.replace ('\t',' ')
	self.replace ('\n',' ')
	self.replace (',',', ')
	self.replace (' --','\n--')
	self.replace ('; ',';\n')
	for word in wordBegin: self.replace (' '+ word, '\n'+ word)
	self.replace ('\ncase when','\n\tcase when')
	while self.contain ('\n\n'): self.replace ('\n\n','\n')
	while self.contain ('  '): self.replace ('  ',' ')
	sqlList = List()
	self.text = sqlList.breakLine (self.text)

def breakLine (self, text):
	self.fromText ('\n', text)
	sqlRange = self.range()
	for l in sqlRange:
		m= 160
		while m< len (self[l]):
			f= self[l][:m].rfind (' ')
			self[l] = self[l][:f] +'\n\t'+ self[l][f+1:]
			m+=160
	text = self.toText ('\n')
	text = text.lower()
	text = text.strip()
	return text

setattr (List, 'breakLine', breakLine)
setattr (File, 'cleanSql', cleanSql)

if len (argv) <2: print (help)
else:
	fileSql = File (argv[1])
	fileSql.fromFile()
	fileSql.cleanSql()
	fileSql.toFile()