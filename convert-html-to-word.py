#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc

filePdf = 'https://magellanpartners.sharepoint.com/:b:/r/sites/MP-PRJ-ANCTSYNERGIECLOUD/Documents%20partages/General/04.%20UO01%20Pilotage%20-%20Suivi%20contractuel/02.%20Bons%20de%20commandes/BDC%20E2024000286%20AXYUS_MCO%20n%C2%B01%2030S.pdf?csf=1&web=1&e=8Pbv58'
fileHtml = 'C:\\Users\\deborah.powers\\Desktop\\fichier.html'
output = pypandoc.convert_file (filePdf, 'html', outputfile=fileHtml)

"""
fileWord = 'C:\\Users\\deborah.powers\\Desktop\\Portail Outils de gestion de projet avec ANCT.odt'
fileHtml = 'C:\\Users\\deborah.powers\\Desktop\\gestion de projet.html'
output = pypandoc.convert_file (fileWord, 'html', outputfile=fileHtml)
"""