#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from debutils.file import File

textOrigine ="""
	requete.append(SELECT);
	// Opération
	requete.append(VueRechercheCsfAc.ID_FONCTIONNEL_OPERATION).append(VIRGULE);
	requete.append(VueRechercheCsfAc.ETAT_TECHNIQUE_OPERATION).append(VIRGULE);
	// CSF
	requete.append(VueRechercheCsfAc.ID_FONCTIONNEL_CSF).append(VIRGULE);
	requete.append(Csf.NUMERO_ORDRE).append(VIRGULE);
	requete.append(Csf.RESPONSABLE_CSF).append(VIRGULE);
	// CSF version
	requete.append(VueRechercheCsfAc.VERSION_TECHNIQUE).append(VIRGULE);
	requete.append(VueRechercheCsfAc.DATE_VALIDATION_AC).append(VIRGULE);
	requete.append(VueRechercheCsfAc.MOTIVATION_AC).append(VIRGULE);
	requete.append(CASE)
		// Commentaire décision COMAC
		.append(WHEN).append(CsfVersionne.ETAT).append(EQUALS)
		.append(this.quote(CsfVersionne.ETAT_COMTABILISE_AC)).append(THEN)
		.append(CsfVersionne.COMMENTAIRE_DECISION_COMAC)
		// Commentaire décision VALNC
		.append(WHEN).append(CsfVersionne.ETAT).append(EQUALS)
		.append(this.quote(CsfVersionne.ETAT_VALIDE_NON_COMPTABILISE)).append(THEN)
		.append(CsfVersionne.COMMENTAIRE_DECISION_VALNC)
		// Commentaire décision ENCAC
		.append(WHEN).append(CsfVersionne.ETAT).append(EQUALS)
		.append(this.quote(CsfVersionne.ETAT_EN_CERTIFICATION_AC)).append(THEN)
		.append(CsfVersionne.COMMENTAIRE_DECISION_ENCAC)
		// Commentaire décision autre
		.append(ELSE).append(CsfVersionne.COMMENTAIRE_DECISION_AC).append(END);
	requete.append(AS).append(CsfVersionne.COMMENTAIRE_DECISION_AC.getChamp()).append(VIRGULE);
	requete.append(CsfVersionne.DATE_DECISION_COMAC).append(VIRGULE);
	requete.append(CsfVersionne.COMMENTAIRE_DECISION_COMAC).append(VIRGULE);
	requete.append(CsfVersionne.EST_COVID19).append(VIRGULE);
	requete.append(VueRechercheCsfAc.ETAT).append(VIRGULE);
	// csf versionne montant
	requete.append(CsfVersionneMontant.MONTANT_DEPENSE_RETENU_CSF_TOTAL).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_TOTAL_ECRETEMENT).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_TOTAL_RETENU_PUBLIC).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_PART_PUB_ECRETE_UE).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_PART_PUB_ECRETE_NAT).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_PART_ECRETE_AUTOFINANCE).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_PART_PUB_RETENU_NAT).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_PART_PUB_RETENU_UE).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_TOTAL_SURREALISEE_PUBLIC).append(VIRGULE);
	requete.append(CsfVersionneMontant.MONTANT_TOTAL_SURREALISEE_PRIVEE).append(VIRGULE);
	// Personne Morale
	requete.append(PersonneMorale.TYPE_DE_DROIT).append(VIRGULE);
	// Exercice comptable.
	requete.append(ExerciceComptable.LIBELLE_COURT).append(VIRGULE);
	// Appel de fonds notification.
	requete.append(VueRechercheCsfAc.ID_FONCTIONNEL_AFN);

	// FROM
	requete.append(FROM);
	requete.append(VueRechercheCsfAc.getTableName());

	// INNER JOIN
	requete.append(INNER_JOIN);
	requete.append(Csf.getTableName());
	requete.append(ON).append(Csf.CSF_PK).append(EQUALS).append(VueRechercheCsfAc.CSF_PK);
	requete.append(INNER_JOIN);
	requete.append(CsfVersionne.getTableName());
	requete.append(ON).append(CsfVersionne.CSF_VERSIONNE_PK).append(EQUALS)
		.append(VueRechercheCsfAc.CSF_VERSIONNE_PK);
	requete.append(INNER_JOIN);
	requete.append(OperationVersion.getTableName());
	requete.append(ON).append(OperationVersion.OPERATION_VERSION_PK).append(EQUALS)
		.append(Csf.OPERATION_VERSION_FK);
	// LEFT JOIN
	requete.append(LEFT_JOIN);
	requete.append(LienBeneficiaireOperation.getTableName());
	requete.append(ON).append(LienBeneficiaireOperation.OPERATION_VERSION_FK).append(EQUALS)
		.append(OperationVersion.OPERATION_VERSION_PK);
	requete.append(AND).append(LienBeneficiaireOperation.EST_CHEF_DE_FILE);
	requete.append(LEFT_JOIN);
	requete.append(BeneficiaireVersion.getTableName());
	requete.append(ON).append(LienBeneficiaireOperation.BENEFICIAIRE_VERSION_FK).append(EQUALS)
		.append(BeneficiaireVersion.BENEFICIAIRE_VERSION_PK);
	requete.append(LEFT_JOIN);
	requete.append(PersonneMorale.getTableName());
	requete.append(ON).append(PersonneMorale.PERSONNE_MORALE_PK).append(EQUALS)
		.append(BeneficiaireVersion.PERSONNE_MORALE_FK);
	requete.append(LEFT_JOIN);
	requete.append(CsfVersionneMontant.getTableName());
	requete.append(ON).append(CsfVersionneMontant.CSF_VERSIONNE_FK).append(EQUALS)
		.append(VueRechercheCsfAc.CSF_VERSIONNE_PK);
	requete.append(LEFT_JOIN);
	requete.append(ExerciceComptable.getTableName());
	requete.append(ON).append(VueRechercheCsfAc.ID_EXERCICE_COMPTABLE).append(EQUALS)
		.append(ExerciceComptable.EXCERCICE_COMPTABLE_PK);
	// WHERE
	requete.append(WHERE);
	requete.append(Csf.CSF_PK).append(" IN ( ").append(StringUtils.join(listIdCsf, ",")).append(" ) ");
	// FIXME Impact irrégularités : on ne remonte que les CSF car la vue remonte aussi les CORFIN
	// A évoluer
	requete.append(AND).append(VueRechercheCsfAc.TYPE_DONNEE_FIN).append(EQUALS).append("'CSF'");
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

fileFin = File ('b/requete.txt')
fileFin.fromText()
fileFin.eraseComment()
fileFin.replace ('\nrequete')
fileFin.replace ('\n',' ')
fileFin.replace ('\t',' ')
while fileFin.contain ('  '): fileFin.replace ('  ',' ')
fileFin.replace (');', ')')
fileFin.replaceAppend ('select')
fileFin.replaceAppend ('as')
fileFin.replaceAppend ('virgule', ', ')
fileFin.replaceAppend ('case')
fileFin.replaceAppend ('when')
fileFin.replaceAppend ('then')
fileFin.replaceAppend ('else')
fileFin.replaceAppend ('inner_join')
fileFin.replaceAppend ('left_join')
fileFin.replaceAppend ('on')
fileFin.replaceAppend ('equals', ' = ')
fileFin.replaceAppend ('where')
fileFin.replaceAppend ('and')
fileFin.replaceAppend ('group_by')
fileFin.replaceAppend ('" 1 "',"")

"""
fileFin.replace ('.append(select)', ' select ')
fileFin.replace ('.append(as)', ' as ')
fileFin.replace ('.append(virgule)', ', ')
fileFin.replace ('.append(case)', ' case ')
fileFin.replace ('.append(when)', ' when ')
fileFin.replace ('.append(then)', ' then ')
fileFin.replace ('.append(else)', ' else ')
fileFin.replace ('.append(from)', ' from ')
fileFin.replace ('.append(inner_join)', ' inner join ')
fileFin.replace ('.append(left_join)', ' left join ')
fileFin.replace ('.append(on)', ' on ')
fileFin.replace ('.append(equals)', ' = ')
fileFin.replace ('.append(where)', ' where ')
fileFin.replace ('.append(and)', ' and ')
fileFin.replace ('.append(group_by)', ' group by ')
fileFin.replace ('.append(" 1 ")')
"""
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
wordBegin =( 'select', 'case', 'when', 'else', 'end as', 'from', 'inner join', 'left join', 'where', 'group by')
for w in wordBegin: fileFin.replace (' '+w+' ','\n'+w+' ')
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


