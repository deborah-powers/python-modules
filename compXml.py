#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileXml import FileXml

fileXmlTemplateNpsl = 'C:\\Users\\deborah.powers\\Desktop\\pcn flux 06-26\\pcn $infos npsl A-6-$numero flux.xml'
fileXmlTemplateLega = 'C:\\Users\\deborah.powers\\Desktop\\pcn flux 06-26\\pcn $infos lega A-6-$numero flux.xml'
"""
vit hongrie npsl A-6-W1SP4YVV	idem
vit hongrie lega A-6-ZZ89T233
né hongrie npsl A-6-9XFNEZ99	idem
né hongrie lega A-6-HGT91622
famille npsl A-6-3RB41GNN	idem
famille lega A-6-H6S0E8WW
fille mineure npsl A-6-CIOKP1EE	idem
fille mineure lega A-6-7RZL7TQQ
fils majeur protégé npsl A-6-80WY70QQ	idem
fils majeur protégé lega A-6-7GPGHUBB
qq d'autre, majeur npsl A-6-MQLSURSS	idem
qq d'autre, majeur lega A-6-EGDKCHGG
qq d'autre, famille npsl A-6-6CWHPHSS	idem
qq d'autre, famille lega A-6-VX01X2SS
qq d'autre, enfants npsl A-6-HXS6HGEE	idem
qq d'autre, enfants lega A-6-39NJ46VV
moi, 7 enfants mineurs npsl A-6-WZCAD4CC	.
moi, 7 enfants mineurs lega A-6-4CVNS077
qq d'autre, majeur, sas npsl A-6-BTAKJGBB	idem particulier
7 enfants mineurs lega A-6-R49JXXRR
tuteur entreprise lega A-6-JIT7H6XX
tuteur ?? Npsl A-6-EXUS60XX	.
tuteur particulier lega A-6-E85JGKEE
"""
fileNpslName = fileXmlTemplateNpsl.replace ('$infos', "").replace ('$numero', '')
fileLegaName = fileXmlTemplateLega.replace ('$infos', "").replace ('$numero', '')
fileNpsl = FileXml (fileNpslName)
fileLega = FileXml (fileLegaName)
fileNpsl.read()
fileLega.read()
fileNpsl.comparer (fileLega)
