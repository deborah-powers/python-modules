#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileXml import FileXml

# fileXmlTemplate = 'C:\\Users\\deborah.powers\\Desktop\\sian-2026\\test ciphyto flux\\ciphyto $ flux.xml'
fileXmlTemplate = 'C:\\Users\\deborah.powers\\Desktop\\$acte 06-09 $appli flux.xml'
"""
fileLegaName = fileXmlTemplate.replace ('$', 'utilisation operateur rn npsl 05-27')
fileNpslName = fileXmlTemplate.replace ('$', 'utilisation operateur pd npsl 05-26')
"""
fileLegaName = fileXmlTemplate.replace ('$acte', 'mariage').replace ('$appli', 'npsl')
fileNpslName = fileXmlTemplate.replace ('$acte', 'deces').replace ('$appli', 'npsl')

fileLega = FileXml (fileLegaName)
fileNpsl = FileXml (fileNpslName)

fileNpsl.read()
fileLega.read()
fileNpsl.comparer (fileLega)
