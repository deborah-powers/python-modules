#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import funcList
import funcText
from classFile import File
import funcLogger

sql = File ('b/requete.txt')
sql.read()
# nettoyer le texte
sql.text = sql.text.replace ('\n', "")
sql.text = sql.text.replace ('\t', ' ')
sql.text = funcText.clean (sql.text)
sql.text = funcText.upperCase (sql.text, 'reset')

wordSql = ('where')
wordSqlSpace = ('inner join', 'left join')

sql.text = sql.text.replace (';', "")
sql.text = sql.text.replace ('_dpo', "")
sql.text = sql.text.replace ('(q_', '(')
sql.text = sql.text.replace (') . where (', '\nwhere ')
sql.text = sql.text.replace (') . where (', '\nwhere ')

funcLogger.log (sql.text)

d= sql.text.find ('(q_')
sql.text = sql.text[d:]



