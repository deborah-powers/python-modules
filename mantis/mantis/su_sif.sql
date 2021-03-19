----------------------------------------------------------------------------------------------
-- Script d'exemple
-- Source : cf. Mantis %numero%
-- Date : %date%
-- Auteur : CGI
----------------------------------------------------------------------------------------------
set schema 'sif';

do $$ begin

	-- tracer l'action
	insert into suivi_execution_script 
	values (nextval('suivi_execution_script_ses_pk_seq'), 'SIF', '%numero%',
		'su_%numero%_', now(),
		'Script d''exemple',
		'', '%numero%', '' , false);
end $$
