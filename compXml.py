#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileXml import FileXml

fileXmlTemplateNpsl = 'C:\\Users\\deborah.powers\\Desktop\\pcn flux 06-26\\pcn $infos npsl A-6-$numero flux.xml'
fileXmlTemplateLega = 'C:\\Users\\deborah.powers\\Desktop\\pcn flux 06-26\\pcn $infos lega A-6-$numero flux.xml'
"""
A-6-EXUS60XX	.	inté	npsl	30	10:14	ok	tuteur
A-6-E85JGKEE	.	inté	lega	30	11:51	ok	tuteur particulier
"""
fileNpslName = fileXmlTemplateNpsl.replace ('$infos', "tuteur enfants").replace ('$numero', 'EXUS60XX')
fileLegaName = fileXmlTemplateLega.replace ('$infos', "tuteur sas enfants").replace ('$numero', 'JIT7H6XX')
fileNpsl = FileXml (fileNpslName)
fileLega = FileXml (fileLegaName)
fileNpsl.read()
fileLega.read()
fileNpsl.comparer (fileLega)
