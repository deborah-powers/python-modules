#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc

fileWord = 'C:\\Users\\deborah.powers\\Desktop\\Portail Outils de gestion de projet avec ANCT.odt'
fileHtml = 'C:\\Users\\deborah.powers\\Desktop\\gestion de projet.html'
output = pypandoc.convert_file (fileWord, 'html', outputfile=fileHtml)