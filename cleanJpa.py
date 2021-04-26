#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileSimple import File

textOrigine ="""
new JPAQuery(this.entityManager).from(Q_AVIS_COMITE_OPERATION_DPO);
.innerJoin(Q_AVIS_COMITE_OPERATION_DPO.operationVersion, Q_OPERATION_VERSION_DPO)
                .innerJoin(Q_AVIS_COMITE_OPERATION_DPO.comite, Q_COMITE_DPO)
                .where(Q_OPERATION_VERSION_DPO.operationDpo.id.eq(idOperation),
                        Q_OPERATION_VERSION_DPO.id.ne(idOperationVersion))
                .orderBy(Q_OPERATION_VERSION_DPO.versionTechnique.desc(), Q_COMITE_DPO.type.asc())
                .list(Q_AVIS_COMITE_OPERATION_DPO);
"""

def cleanJoin (line):
	if ' join ' not in line: return line;
	d= line.find (' join ') +6
	newLine = line[:d]
	d= line.find (', ') +2
	table = line[d:]
	newLine = newLine + table +' on '+ table +'_pk = '+ table +'_fk'
	return newLine

def fromTextRequest (self, textOrigine):
	self.text = textOrigine
	self.text = self.text.lower()
	self.replace ('\n'," ")
	self.replace ('\t'," ")
	self.clean()
	artefacts =( ' q_', '(q_' )
	for a in artefacts: self.replace (a, a[0])
	artefacts =( ';', '_dpo' )
	for a in artefacts: self.replace (a)
	artefacts =('from', 'innerjoin', 'where', 'groupby', 'orderby')
	for w in artefacts: self.replace (').'+w+' (', ' '+w+' ')
	artefacts =('desc', 'asc')
	for w in artefacts: self.replace ('.'+w+' ()', ' '+w+' ')
	artefacts =(('eq', '='), ('ne', '!='))
	for v,w in artefacts: self.replace ('.'+v+' (', ' '+w+' ')
	artefacts =('inner join', 'group by', 'order by')
	for w in artefacts: self.replace (w.replace (' ',""), w)
	artefacts =( ('new jpaquery (this.entitymanager', 'select *'), ('.id', '_pk'), ('dpo_pk', '_pk'))
	for v,w in artefacts: self.replace (v,w)

setattr (File, 'fromText', fromTextRequest)

fileFin = File ('b/requete.txt')
fileFin.fromText (textOrigine)

while fileFin.contain ('  '): fileFin.replace ('  ',' ')
wordBegin =( 'select', 'case', 'when', 'else', 'end as', 'from', 'inner join', 'left join', 'where', 'group by', 'order by')
for w in wordBegin: fileFin.replace (' '+w+' ','\n'+w+' ')

textList = fileFin.text.split ('\n')
textRange = range (len (textList))
for l in textRange: textList[l] = cleanJoin (textList[l])
fileFin.text = '\n'.join (textList)

fileFin.fileFromData()
fileFin.toFile()
