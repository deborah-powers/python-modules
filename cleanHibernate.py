#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from cleanSql import *
from fileSimple import File

textOrigine ="""
        requete.append(SELECT);
        .from(Q_APPEL_FONDS_VERSION_DPO)
                .leftJoin(Q_APPEL_FONDS_VERSION_DPO.appelFonds, Q_APPEL_FONDS_DPO)
                .leftJoin(Q_APPEL_FONDS_DPO.lienFondsList, Q_LIEN_FONDS_APPEL_FONDS_DPO)
                .leftJoin(Q_APPEL_FONDS_DPO.programme, Q_PROGRAMME_DPO)
                .leftJoin(Q_PROGRAMME_DPO.codification, Q_CODIFICATION_DPO)
                .leftJoin(Q_CODIFICATION_DPO.lienOperationList, Q_LIEN_CODIFICATION_OPERATION_DPO)
                .leftJoin(Q_LIEN_CODIFICATION_OPERATION_DPO.operationVersion, Q_OPERATION_VERSION_DPO)
                .leftJoin(Q_CODIFICATION_DPO.lienFondsList, Q_LIEN_CODIFICATION_FONDS_DPO)
                .where(Q_APPEL_FONDS_VERSION_DPO.etat.eq(EtatFonctionnelAppelFondsEnum.AF_RENVOYE_CORRECTION),
                        Q_OPERATION_VERSION_DPO.id.eq(idOperation),
                        Q_LIEN_CODIFICATION_OPERATION_DPO.estPrincipale.isTrue(),
                        Q_LIEN_FONDS_APPEL_FONDS_DPO.fonds.id.eq(Q_LIEN_CODIFICATION_FONDS_DPO.fonds.id));
"""

def eraseComment (self):
	if self.contain ('\n// '):
		from debutils.list import List
		tmpLines = List()
		tmpLines.fromText ('\n', self.text)
		rangeLines = tmpLines.range()
		rangeLines.reverse()
		for l in rangeLines:
			if tmpLines[l][:3] =='// ': trash = tmpLines.pop(l)
		self.text = tmpLines.toText ('\n')

def fromTextRequest (self, textOrigine):
	self.text = textOrigine
	self.text = self.text.lower()
	while self.contain ('  '): self.replace ('  ',' ')
	self.replace ('\n ','\n')

def replaceAppend (self, word, newWord=None):
	if not newWord:
		newWord = ' '+ word +' '
		if '_' in word: newWord = newWord.replace ('_',' ')
	self.replace ('.append(' + word +')', newWord)

setattr (File, 'eraseComment', eraseComment)
setattr (File, 'fromText', fromTextRequest)
setattr (File, 'replaceAppend', replaceAppend)

toReplaceAppend =( 'select', 'as', 'case', 'when', 'then', 'else', 'inner_join', 'left_join', 'on', 'where', 'and', 'group_by')

fileFin = File ('b/requete.txt')
fileFin.fromText (textOrigine)
fileFin.eraseComment()
fileFin.replace ('\nrequete')
fileFin.replace ('\n',' ')
fileFin.replace ('\t',' ')
while fileFin.contain ('  '): fileFin.replace ('  ',' ')
fileFin.replace (');', ')')
for word in toReplaceAppend: fileFin.replaceAppend (word)
fileFin.replaceAppend ('virgule', ', ')
fileFin.replaceAppend ('equals', ' = ')
fileFin.replaceAppend ('" 1 "',"")
fileFin.replace ('.append(')
fileFin.replace (') = ', ' = ')
fileFin.replace ('), ', ', ')
fileFin.replace ('"\'', "'")
fileFin.replace ('\'"', "'")
fileFin.replace ('this.sumAs(', 'sum (')
fileFin.replace ('this.quote(', "'")
fileFin.replace ('.gettablename()')
fileFin.replace ('.getchamp()')
fileFin.replace (') ',' ')
while fileFin.contain ('  '): fileFin.replace ('  ',' ')
fileFin.cleanSql()
addUnderscoreBefore =( 'ac', 'montant', 'version', 'operation')
addUnderscoreAfter =( 'beneficiaire', 'comptable', 'lien', 'montant', 'personne', 'recherche', 'vue')
for name in addUnderscoreBefore: fileFin.replace (name, '_'+ name)
for name in addUnderscoreAfter:
	fileFin.replace (' '+ name, ' '+ name +'_')
	fileFin.replace ('.'+ name, '.'+ name +'_')
tables =( ('vue_recherchecsf_ac', 'vue_recherche_csf_ac'), )
for (nameWrong, nameGood) in tables: fileFin.replace (nameWrong, nameGood)
while fileFin.contain ('__'): fileFin.replace ('__','_')
fileFin.replace ('_ ',' ')
fileFin.replace (' _',' ')
fileFin.replace ('_.','.')
fileFin.replace ('._','.')
fileFin.fileFromData()
fileFin.toFile()

