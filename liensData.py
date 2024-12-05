#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# comparer la version sur mon ordi du fichier liens-data.js et la nouvelle version téléchargée
import json
from fileCls import File
from fileLocal import pathLienData

jsonTitleB = 'r/Downloads\\liens-data.js'
jsonTitleC = 'b/liens-data.js'

jsonFileA = File (pathLienData)
jsonDataA = jsonFileA.readJson()
jsonFileB = File (jsonTitleB)
jsonDataB = jsonFileB.readJson()

modif = False
for b in jsonDataB.keys():
	if b not in jsonDataA.keys():
		print ('nouvelle catégorie', b)
		jsonDataA[b] = jsonDataB[b]
		modif = True
	elif jsonDataB[b] != jsonDataA[b]:
		for c in jsonDataB[b]:
			if c not in jsonDataA[b]:
				modif = True
				nouveau = True
				for a in jsonDataA[b]:
					if a['name'] == c['name']: nouveau = False
				if nouveau:
					print ('nouvelle entrée dans', b, c['name'])
					jsonDataA[b].append (c)
				else:
					print ('entrée modifiée dans', b, c['name'])
					c['name'] = c['name'] +' double'
					jsonDataA[b].append (c)
			jsonDataA[b] = sorted (jsonDataA[b], key=lambda d: d['name'])

if modif:
	jsonFileC = File (pathLienData)
	jsonFileC.text = json.dumps (jsonDataA)
	jsonFileC.replace ('}, {', ' },\n\t{ ')
	jsonFileC.replace ('}], "', ' }\n],\n"')
	jsonFileC.replace ('": [{"', '": [\n\t{ "')
	jsonFileC.text = 'var linkList ={\n' + jsonFileC.text[1:]
	jsonFileC.replace ('}]}', ' }\n]};')
	jsonFileC.write()
#	jsonFileA.remove()
else: print ("les fichiers sont identiques")
jsonFileB.remove()
