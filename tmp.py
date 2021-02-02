#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from articleHtml import ArticleHtml
from fileHtml import FileHtml
from fileList import FileList
import urllib as ul
from urllib import request as urlRequest

flist = FileList()
flist.file = 'b/mantis 964 erreur.txt'
flist.fromFile()
flist.clean()
frange = flist.range()
frange.reverse()
for l in frange:
	if flist[l][0] == '\t' and 'fr.asp.synergie.' not in flist[l]: flist.pop (l)

flist.toFile()