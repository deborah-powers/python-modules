----------------------------------------------------------------------------------------------
-- Suppression du CSF1 de OP0000000
-- Source : cf. Mantis %numero%
-- Date : %date%
-- Auteur : CGI
----------------------------------------------------------------------------------------------
set schema 'sif';

do $$ begin
	delete from lien_csf_appel_fonds where lcaf_csf_id_fk = 00000;
	delete from montant_beneficiaire where mbe_csf_id_fk = 00000;
	delete from depense where dep_csf_id_fk = 00000;
	delete from csf where csf_id_pk = 00000;

	-- tracer l'action
	insert into suivi_execution_script 
	values (nextval('suivi_execution_script_ses_pk_seq'), 'SIF', '%numero%',
		'su_%numero%_suppression_csf', now(),
		'Suppression du CSF1 de OP0000000',
		'OP0000000-CSF1: 00000', '%numero%', '' , false);
end $$
