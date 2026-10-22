#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import folderCls as fd
from textFct import fromModel, shape

ficOld = fd.Folder ('a/')
ficNew = fd.Folder ('b/ficnew')

templateFinal ="""%s
======
Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
"""

templateTab ="""Sujet:	%s
Auteur:	%s
Lien:	%s
Laut:	%s
%s"""

templateSpace ="""Sujet: %s
Auteur: %s
Lien: %s
Laut: %s
%s"""

ficOld.get ('.txt')
ficOld.read()

for file in ficOld.list:
	if 'Auteur:\t' in file.text:
		if '\ndate:\t' in file.text:
			file.text = file.text.replace ('\ndate:\t', '\nDate:\t')
			if '\ntitre:\t' in file.text: file.text = file.text.replace ('\ntitre:\t', '\nTitre:\t')
			file.text = file.text.strip()
			ficNew.append (file)
		elif '\ntitre:\t' in file.text:
			file.text = file.text.replace ('\ntitre:\t', '\nTitre:\t')
			file.text = file.text.strip()
			ficNew.append (file)
"""
		data = fromModel (file.text, templateTab)
		if len (data) <5:
			print ('il manque des données dans', file.title)
			continue
		elif ':\t' in " ".join (data[:4]):
			print ('mauvais entête dans', file.title)
			continue
		file.text = templateFinal %( data[4], data[0], data[1], data[2], data[3])
		file.text = shape (file.text, 'ru')
		file.title = file.title
		ficNew.append (file)
	elif 'Auteur: ' in file.text:
		print ('space', file.title)
		data = fromModel (file.text, templateSpace)
		if len (data) <5:
			print ('il manque des données dans', file.title)
			continue
		elif ': ' in "\t".join (data[:4]):
			print ('mauvais entête dans', file.title)
			continue
		file.text = templateFinal %( data[4], data[0], data[1], data[2], data[3])
		file.text = shape (file.text, 'ru')
		file.title = file.title +' space'
		ficNew.append (file)
	else: print ('pas de metadonnées dans', file.title)
"""
ficNew.write()
