#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc


fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\rgaa-certif\\rgaa diaporama.html'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\rgaa présentation conv.pptx'
output = pypandoc.convert_file (fileSrc, 'pptx', outputfile=fileDst)

"""
fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\bdc.pdf'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\fichier.html'
output = pypandoc.convert_file (fileSrc, 'html', outputfile=fileDst)
fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\Portail Outils de gestion de projet avec ANCT.odt'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\gestion de projet.html'
output = pypandoc.convert_file (fileSrc, 'html', outputfile=fileDst)
"""