#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc
from fileCls import File, Article
from eventCls import DatePerso
import loggerFct as log

# le fichier
fileSrc = 'C:\\Users\\LENOVO\\Desktop\\bus 2026-08 244 horaire.pdf'
filePdf = Article (fileSrc)
filePdf.fromPdf (False)
# les métadonnées
filePdf.subject = 'transport, bus'
filePdf.author = 'ratp'
today = DatePerso (2026, 5, 12)
today = today.today()
filePdf.meta['date'] = today.toStrDay()

# les données
filePdf.text = '\n'+ filePdf.text
filePdf.replace ('\n\n', '\n')
pages = filePdf.text.split ("\n== page ")
log.message (len (pages))
for page in pages:
	page = page[2:]
	page = page.strip()
	log.message (page)


# filePdf.write()