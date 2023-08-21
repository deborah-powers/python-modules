#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

sourceStr = '(abc((de)f))g(h(ij)k)l(mnopqrstu((vw)(xy)z))'
source = list (sourceStr)

def buildTree (source, strA, strB):
	"""
	arguments: liste simple de str, sous-str ouvrante, sous-str fermante
	renvoi: un arbre de str sous forme de liste imbriquée
	"""
	if strA not in source and strB not in source: return source
	elif source.count (strA) != source.count (strB):
		print ('la source est malformée')
		return None
	# trouver les positions des parenthèses complémentaires
	sisA = source.index (strA)
	sisB = source.index (strB, sisA)
	totA = source[sisA +1:sisB].count (strA)
	totB = source[sisA +1:sisB].count (strB)
	while totA > totB:
		sisB = source.index (strB, sisB +1)
		totA = source[sisA +1:sisB].count (strA)
		totB = source[sisA +1:sisB].count (strB)
	# créer la liste imbriquée finale
	tree =[]
	# le début de la liste
	rangeTmp = range (sisA)
	for t in rangeTmp: tree.append (source[t])
	# entre les parenthèses
	if strA in source [sisA +1:sisB]:
		treeTmp = buildTree (source [sisA +1:sisB], strA, strB)
		tree.append (treeTmp)
	else: tree.append (source [sisA +1:sisB])
	# la fin de la liste
	if strA in source [sisB:]:
		treeTmp = buildTree (source [sisB +1:], strA, strB)
		for item in treeTmp: tree.append (item)
	else:
		for item in source [sisB +1:]: tree.append (item)
	return tree

tree = buildTree (source, '(', ')')
print (tree[0][3])
