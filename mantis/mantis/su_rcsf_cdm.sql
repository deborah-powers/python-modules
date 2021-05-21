----------------------------------------------------------------------------------------------
-- rétrogradage du CSF1 de OP0000000
-- Source : cf. Mantis %numero%
-- Date : %date%
-- Auteur : CGI
----------------------------------------------------------------------------------------------

set schema 'cdm';

do $$ begin
	delete from suivi_integration_flux where suvi_inte_flx_typ_msg = 'FLUX_F3' and suvi_inte_flx_id_obj = 00000;
	update csf_versionne set
		motivation_ac = null, etat_precedent = null, date_decision_valnc = null, commentaire_decision_valnc = null,
		etat = 'EAVAC' where csf_versionne_pk = 00000;

	-- Mise à jour des flags de transfert vers l'agrégateur. quand je modifie une opération ou un objet qui en dépend
	update operation set statut_flux_agr = 1, statut_flux_agr_f3 = 1 where id_fonctionnel = 'OP0000000';
	-- tracer l'action
	insert into suivi_execution_script 
	values (nextval('suivi_execution_script_ses_pk_seq'), 'CDM', '%numero%', 'su_%numero%_retrogradage_csf', now(),
		'rétrogradage du CSF1 de OP0000000',
		'OP0000000-CSF1-V1: 00000' , false);
end $$
