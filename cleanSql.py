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
	self.shape()
	self.text = self.text.lower()
	wordBegin =('drop', 'create', 'declare', 'begin', 'select', 'case when', 'when', 'else', 'end as', 'from', 'inner join', 'left join', 'left outer join', 'where', 'group by', 'order by', 'update', 'insert')
	self.replace ('\t',' ')
	self.replace ('\n',' ')
	self.replace (',',', ')
	self.replace (' --','\n--')
	self.replace ('; ',';\n')
	for word in wordBegin: self.replace (' '+ word, '\n'+ word)
	self.replace ('\ncase\nwhen','\n\tcase when')
	self.replace ('\nwhen','\n\twhen')
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

if __name__ != '__main__': pass
elif len (argv) <2: print (help)
else:
	fileSql = File (argv[1])
	fileSql.fromFile()
	fileSql.cleanSql()
	fileSql.toFile()