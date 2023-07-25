#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import json
from fileCls import File
from list import ListText, List, TableText, TableBdd

tsvName = 'b/html/gens.tsv'
tsvFile = ListText (tsvName)
tsvFile.fromFile ()
tsvRange = tsvFile.range ()
for t in tsvRange:
	tsvFile.list [t] = tsvFile.list [t].lower ()
tsvFile.list.sort ()
tsvFile.title = tsvFile.title +'-2'
tsvFile.toFile ()
