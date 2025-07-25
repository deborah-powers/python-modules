#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
from fileList import FileTable
import loggerFct as log
invenspecPath = 'b/fouille-spec\\invenspec %s.tsv'


# fichiers contenant les données originelles
invenspecForge = FileTable (invenspecPath % 'forge tout')
invenspecSharepoint = FileTable (invenspecPath % 'sharepoint tout')
invenspecForge.read()
invenspecForge.pop (0)
invenspecSharepoint.read()
invenspecSharepoint.pop(0)

# fichiers contenant les données triées
invenspecCFS = File (invenspecPath % 'cosmose forge sharepoint')
invenspecCFS.read()
invenspecCF = File (invenspecPath % 'cosmose forge')
invenspecCF.read()
invenspecCS = File (invenspecPath % 'cosmose sharepoint')
invenspecCS.read()

invenspecFonly = File (invenspecPath % 'forge uniquement')
invenspecSonly = File (invenspecPath % 'sharepoint uniquement')

"""
for title, nom, modif, fariane in invenspecForge.list:
	if nom not in invenspecCF.text and nom not in invenspecCFS.text and nom not in invenspecFonly.text and title not in invenspecCF.text and title not in invenspecCFS.text and title not in invenspecFonly.text:
			invenspecFonly.text = invenspecFonly.text +'\n'+ title
invenspecFonly.write()
"""
for title, modif, typeElm, chemin in invenspecSharepoint.list:
	if title not in invenspecCS.text and title not in invenspecCFS.text and title not in invenspecSonly.text and typeElm in ('document', 'élément'): invenspecSonly.text = invenspecSonly.text +'\n'+ title
invenspecSonly.write()