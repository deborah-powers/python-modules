#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from folderCls import Folder

folderFlux = Folder ('b/rnpp flux')
print (folderFlux.path)

folderFlux.get ('flux_pass')
folderFlux.read()
for flux in folderFlux:
	flux.title = "rnpp o "+ flux.path[28:-9] +" flux"
	flux.path = folderFlux.path +'\t.xml'
folderFlux.write()

"""
folderFlux.get ('flux_pass')
folderFlux.get ('recapPDF')
"""