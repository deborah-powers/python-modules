----------------------------------------------------------------------------------------------
-- Script d'exemple
-- Source : cf. Mantis %numero%
-- Date : %date%
-- Auteur : CGI
----------------------------------------------------------------------------------------------

set schema 'cdm';

do $$ begin

	-- Mise à jour des flags de transfert vers l'agrégateur. quand je modifie une opération ou un objet qui en dépend
	update operation set statut_flux_agr = 1, statut_flux_agr_f3 = 1 where id_fonctionnel = 'MP0002386';
	-- tracer l'action
	insert into suivi_execution_script 
	values (nextval('suivi_execution_script_ses_pk_seq'), 'CDM', '%numero%', 'su_%numero%_', now(), 'Script d''exemple', '' , false);
end $$
