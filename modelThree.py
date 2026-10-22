#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

sourceStr = '(abc((de)f))g(h(ij)k)l(mnopqrstu((vw)(xy)z))'
source = list (sourceStr)

def findComplementaryPos (source, strStart, strClose, posStart):
	posClose = source.index (strClose, posStart)
	totStart = source[posStart +1:posClose].count (strStart)
	totClose = source[posStart +1:posClose].count (strClose)
	while totStart > totClose:
		posClose = source.index (strClose, posClose +1)
		totStart = source[posStart +1:posClose].count (strStart)
		totClose = source[posStart +1:posClose].count (strClose)
	return posClose

def buildTree (source, strStart, strClose):
	"""
	arguments: liste simple de str, sous-str ouvrante, sous-str fermante
	renvoi: un arbre de str sous forme de liste imbriquée
	"""
	if strStart not in source and strClose not in source: return source
	elif source.count (strStart) != source.count (strClose):
		print ('la source est malformée')
		return None
	# trouver les positions des parenthèses complémentaires
	posStart = source.index (strStart)
	posClose = findComplementaryPos (source, strStart, strClose, posStart)
	# créer la liste imbriquée finale
	tree =[]
	# le début de la liste
	rangeTmp = range (posStart)
	for t in rangeTmp: tree.append (source[t])
	# entre les parenthèses
	if strStart in source [posStart +1:posClose]:
		treeTmp = buildTree (source [posStart +1:posClose], strStart, strClose)
		tree.append (treeTmp)
	else: tree.append (source [posStart +1:posClose])
	# la fin de la liste
	if strStart in source [posClose:]:
		treeTmp = buildTree (source [posClose +1:], strStart, strClose)
		for item in treeTmp: tree.append (item)
	else:
		for item in source [posClose +1:]: tree.append (item)
	return tree

"""
tree = buildTree (source, '(', ')')
print (tree[0][3])
"""

def findComplementaryBracket (source, pStart):
	# source est une string
	pClose = source.find ('}', pStart)
	nStart = source[pStart +1:pClose].count ('{')
	nClose = source[pStart +1:pClose].count ('}')
	while nStart > nClose:
		pClose = source.find ('}', pClose +1)
		nStart = source[pStart +1:pClose].count ('{')
		nClose = source[pStart +1:pClose].count ('}')
	return pClose
