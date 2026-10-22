#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileList import FileList
import loggerFct as log

filePhoto = FileList ('s/portfolio\\diaporama\\photos-data.tsv')
filePhoto.read()
# filePhoto.sort()
photoRange = range (len (filePhoto.list))
for p in photoRange: filePhoto.list[p] = str(p+1) +';'+ filePhoto.list[p]
filePhoto.title = filePhoto.title +" ids"
filePhoto.write()