#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
from fileXml import FileXml

fileLegaName = 'C:\\Users\\deborah.powers\\Desktop\\sian-2026\\test ciphyto flux\\ciphyto utilisation operateur npsl 05-18 flux.xml'
fileNpslName = 'C:\\Users\\deborah.powers\\Desktop\\sian-2026\\test ciphyto flux\\ciphyto utilisation operateur npsl 05-26 flux.xml'

fileLega = FileXml (fileLegaName)
fileNpsl = FileXml (fileNpslName)

fileNpsl.read()
fileLega.read()
fileNpsl.comparer (fileLega)
