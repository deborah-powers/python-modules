#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import funcList
import funcText
from classFile import File
import funcLogger

sql = File ('b/requete.txt')
sql.read()
# nettoyer le texte
sql.replace ('\n', ' ')
sql.replace ('\t', ' ')
sql.text = funcText.clean (sql.text)
sql.text = funcText.upperCase (sql.text, 'reset')
sql.replace ('. ', '.')

wordsSql = ('from', 'where')
wordsSqlSpace = ('inner join', 'left join', 'group by')
wordsSqlInner = (('eq', '='), ('in', 'in'))

d= sql.text.find ('(q_')
sql.text = sql.text[d:]

sql.replace (';')
sql.replace ('_dpo')
sql.replace ('(q_', '(')
sql.replace (' q_', ' ')
for word in wordsSqlSpace: sql.replace (').'+ word.replace (" ","") +'(', '\n'+ word +' ')
for word, char in wordsSqlInner: sql.replace ('.'+ word +'(', ' '+ char +' ')
for word in wordsSql: sql.replace (').'+ word +'(', '\n'+ word +' ')
sql.text = sql.text.strip ('()')

# les jointures
sqlList = sql.text.split ('\n')
sqlRange = funcList.range (sqlList)
for s in sqlRange:
	if ' join ' in sqlList[s]:
		d= sqlList[s].find (' join ') +6
		e= sqlList[s].find ('.')
		f= sqlList[s].find (', ')
		sqlList[s] = sqlList[s][:d] + sqlList[s][f+2:] +' on '+ sqlList[s][f+2:] + '_pk = '+ sqlList[s][d:e] + '_pk'
sql.text = '\n'.join (sqlList)

sql.text = 'select *\nfrom '+ sql.text
print (sql.text)



