#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

sourceStr = '(abc((de)f))g(h(ij)k)l(mnopqrstu((vw)(xy)z))'
source = list (sourceStr)

def buildTree (source, strOuvre, strFerme):
	"""
	arguments: liste simple de str, sous-str ouvrante, sous-str fermante
	renvoi: un arbre de str sous forme de liste imbriquée
	"""
	if strOuvre not in source and strFerme not in source: return source
	elif source.count (strOuvre) != source.count (strFerme):
		print ('la source est malformée')
		return None
	# trouver les positions des parenthèses complémentaires
	sisA = source.index (strOuvre)
	sisB = source.index (strFerme, sisA)
	totA = source[sisA +1:sisB].count (strOuvre)
	totB = source[sisA +1:sisB].count (strFerme)
	while totA > totB:
		sisB = source.index (strFerme, sisB +1)
		totA = source[sisA +1:sisB].count (strOuvre)
		totB = source[sisA +1:sisB].count (strFerme)
	# créer la liste imbriquée finale
	tree =[]
	# le début de la liste
	rangeTmp = range (sisA)
	for t in rangeTmp: tree.append (source[t])
	# entre les parenthèses
	if strOuvre in source [sisA +1:sisB]:
		treeTmp = buildTree (source [sisA +1:sisB], strOuvre, strFerme)
		tree.append (treeTmp)
	else: tree.append (source [sisA +1:sisB])
	# la fin de la liste
	if strOuvre in source [sisB:]:
		treeTmp = buildTree (source [sisB +1:], strOuvre, strFerme)
		for item in treeTmp: tree.append (item)
	else:
		for item in source [sisB +1:]: tree.append (item)
	return tree

tree = buildTree (source, '(', ')')
print (tree[0][3])
