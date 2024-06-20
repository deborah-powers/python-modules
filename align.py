#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import random

scoreGap =1
scoreAli =10
scoreChoice =[-1,1]
scoreMatrix = { 'ab': 4, 'ac': 4, 'ad': 4, 'ae': 4, 'af': 4, 'ag': 4, 'ah': 4, 'ai': 4, 'aj': 4, 'ak': 4, 'al': 4, 'am': 4, 'an': 4, 'ao': 4, 'ap': 4, 'aq': 4, 'ar': 4, 'as': 4, 'at': 4, 'au': 4, 'av': 4, 'aw': 4, 'ax': 4, 'ay': 4, 'az': 4, 'ba': 4, 'bc': 4, 'bd': 4, 'be': 4, 'bf': 4, 'bg': 4, 'bh': 4, 'bi': 4, 'bj': 4, 'bk': 4, 'bl': 4, 'bm': 4, 'bn': 4, 'bo': 4, 'bp': 4, 'bq': 4, 'br': 4, 'bs': 4, 'bt': 4, 'bu': 4, 'bv': 4, 'bw': 4, 'bx': 4, 'by': 4, 'bz': 4, 'ca': 4, 'cb': 4, 'cd': 4, 'ce': 4, 'cf': 4, 'cg': 4, 'ch': 4, 'ci': 4, 'cj': 4, 'ck': 4, 'cl': 4, 'cm': 4, 'cn': 4, 'co': 4, 'cp': 4, 'cq': 4, 'cr': 4, 'cs': 4, 'ct': 4, 'cu': 4, 'cv': 4, 'cw': 4, 'cx': 4, 'cy': 4, 'cz': 4, 'da': 4, 'db': 4, 'dc': 4, 'de': 4, 'df': 4, 'dg': 4, 'dh': 4, 'di': 4, 'dj': 4, 'dk': 4, 'dl': 4, 'dm': 4, 'dn': 4, 'do': 4, 'dp': 4, 'dq': 4, 'dr': 4, 'ds': 4, 'dt': 4, 'du': 4, 'dv': 4, 'dw': 4, 'dx': 4, 'dy': 4, 'dz': 4, 'ea': 4, 'eb': 4, 'ec': 4, 'ed': 4, 'ef': 4, 'eg': 4, 'eh': 4, 'ei': 4, 'ej': 4, 'ek': 4, 'el': 4, 'em': 4, 'en': 4, 'eo': 4, 'ep': 4, 'eq': 4, 'er': 4, 'es': 4, 'et': 4, 'eu': 4, 'ev': 4, 'ew': 4, 'ex': 4, 'ey': 4, 'ez': 4, 'fa': 4, 'fb': 4, 'fc': 4, 'fd': 4, 'fe': 4, 'fg': 4, 'fh': 4, 'fi': 4, 'fj': 4, 'fk': 4, 'fl': 4, 'fm': 4, 'fn': 4, 'fo': 4, 'fp': 4, 'fq': 4, 'fr': 4, 'fs': 4, 'ft': 4, 'fu': 4, 'fv': 4, 'fw': 4, 'fx': 4, 'fy': 4, 'fz': 4, 'ga': 4, 'gb': 4, 'gc': 4, 'gd': 4, 'ge': 4, 'gf': 4, 'gh': 4, 'gi': 4, 'gj': 4, 'gk': 4, 'gl': 4, 'gm': 4, 'gn': 4, 'go': 4, 'gp': 4, 'gq': 4, 'gr': 4, 'gs': 4, 'gt': 4, 'gu': 4, 'gv': 4, 'gw': 4, 'gx': 4, 'gy': 4, 'gz': 4, 'ha': 4, 'hb': 4, 'hc': 4, 'hd': 4, 'he': 4, 'hf': 4, 'hg': 4, 'hi': 4, 'hj': 4, 'hk': 4, 'hl': 4, 'hm': 4, 'hn': 4, 'ho': 4, 'hp': 4, 'hq': 4, 'hr': 4, 'hs': 4, 'ht': 4, 'hu': 4, 'hv': 4, 'hw': 4, 'hx': 4, 'hy': 4, 'hz': 4, 'ia': 4, 'ib': 4, 'ic': 4, 'id': 4, 'ie': 4, 'if': 4, 'ig': 4, 'ih': 4, 'ij': 4, 'ik': 4, 'il': 4, 'im': 4, 'in': 4, 'io': 4, 'ip': 4, 'iq': 4, 'ir': 4, 'is': 4, 'it': 4, 'iu': 4, 'iv': 4, 'iw': 4, 'ix': 4, 'iy': 4, 'iz': 4, 'ja': 4, 'jb': 4, 'jc': 4, 'jd': 4, 'je': 4, 'jf': 4, 'jg': 4, 'jh': 4, 'ji': 4, 'jk': 4, 'jl': 4, 'jm': 4, 'jn': 4, 'jo': 4, 'jp': 4, 'jq': 4, 'jr': 4, 'js': 4, 'jt': 4, 'ju': 4, 'jv': 4, 'jw': 4, 'jx': 4, 'jy': 4, 'jz': 4, 'ka': 4, 'kb': 4, 'kc': 4, 'kd': 4, 'ke': 4, 'kf': 4, 'kg': 4, 'kh': 4, 'ki': 4, 'kj': 4, 'kl': 4, 'km': 4, 'kn': 4, 'ko': 4, 'kp': 4, 'kq': 4, 'kr': 4, 'ks': 4, 'kt': 4, 'ku': 4, 'kv': 4, 'kw': 4, 'kx': 4, 'ky': 4, 'kz': 4, 'la': 4, 'lb': 4, 'lc': 4, 'ld': 4, 'le': 4, 'lf': 4, 'lg': 4, 'lh': 4, 'li': 4, 'lj': 4, 'lk': 4, 'lm': 4, 'ln': 4, 'lo': 4, 'lp': 4, 'lq': 4, 'lr': 4, 'ls': 4, 'lt': 4, 'lu': 4, 'lv': 4, 'lw': 4, 'lx': 4, 'ly': 4, 'lz': 4, 'ma': 4, 'mb': 4, 'mc': 4, 'md': 4, 'me': 4, 'mf': 4, 'mg': 4, 'mh': 4, 'mi': 4, 'mj': 4, 'mk': 4, 'ml': 4, 'mn': 4, 'mo': 4, 'mp': 4, 'mq': 4, 'mr': 4, 'ms': 4, 'mt': 4, 'mu': 4, 'mv': 4, 'mw': 4, 'mx': 4, 'my': 4, 'mz': 4, 'na': 4, 'nb': 4, 'nc': 4, 'nd': 4, 'ne': 4, 'nf': 4, 'ng': 4, 'nh': 4, 'ni': 4, 'nj': 4, 'nk': 4, 'nl': 4, 'nm': 4, 'no': 4, 'np': 4, 'nq': 4, 'nr': 4, 'ns': 4, 'nt': 4, 'nu': 4, 'nv': 4, 'nw': 4, 'nx': 4, 'ny': 4, 'nz': 4, 'oa': 4, 'ob': 4, 'oc': 4, 'od': 4, 'oe': 4, 'of': 4, 'og': 4, 'oh': 4, 'oi': 4, 'oj': 4, 'ok': 4, 'ol': 4, 'om': 4, 'on': 4, 'op': 4, 'oq': 4, 'or': 4, 'os': 4, 'ot': 4, 'ou': 4, 'ov': 4, 'ow': 4, 'ox': 4, 'oy': 4, 'oz': 4, 'pa': 4, 'pb': 4, 'pc': 4, 'pd': 4, 'pe': 4, 'pf': 4, 'pg': 4, 'ph': 4, 'pi': 4, 'pj': 4, 'pk': 4, 'pl': 4, 'pm': 4, 'pn': 4, 'po': 4, 'pq': 4, 'pr': 4, 'ps': 4, 'pt': 4, 'pu': 4, 'pv': 4, 'pw': 4, 'px': 4, 'py': 4, 'pz': 4, 'qa': 4, 'qb': 4, 'qc': 4, 'qd': 4, 'qe': 4, 'qf': 4, 'qg': 4, 'qh': 4, 'qi': 4, 'qj': 4, 'qk': 4, 'ql': 4, 'qm': 4, 'qn': 4, 'qo': 4, 'qp': 4, 'qr': 4, 'qs': 4, 'qt': 4, 'qu': 4, 'qv': 4, 'qw': 4, 'qx': 4, 'qy': 4, 'qz': 4, 'ra': 4, 'rb': 4, 'rc': 4, 'rd': 4, 're': 4, 'rf': 4, 'rg': 4, 'rh': 4, 'ri': 4, 'rj': 4, 'rk': 4, 'rl': 4, 'rm': 4, 'rn': 4, 'ro': 4, 'rp': 4, 'rq': 4, 'rs': 4, 'rt': 4, 'ru': 4, 'rv': 4, 'rw': 4, 'rx': 4, 'ry': 4, 'rz': 4, 'sa': 4, 'sb': 4, 'sc': 4, 'sd': 4, 'se': 4, 'sf': 4, 'sg': 4, 'sh': 4, 'si': 4, 'sj': 4, 'sk': 4, 'sl': 4, 'sm': 4, 'sn': 4, 'so': 4, 'sp': 4, 'sq': 4, 'sr': 4, 'st': 4, 'su': 4, 'sv': 4, 'sw': 4, 'sx': 4, 'sy': 4, 'sz': 4, 'ta': 4, 'tb': 4, 'tc': 4, 'td': 4, 'te': 4, 'tf': 4, 'tg': 4, 'th': 4, 'ti': 4, 'tj': 4, 'tk': 4, 'tl': 4, 'tm': 4, 'tn': 4, 'to': 4, 'tp': 4, 'tq': 4, 'tr': 4, 'ts': 4, 'tu': 4, 'tv': 4, 'tw': 4, 'tx': 4, 'ty': 4, 'tz': 4, 'ua': 4, 'ub': 4, 'uc': 4, 'ud': 4, 'ue': 4, 'uf': 4, 'ug': 4, 'uh': 4, 'ui': 4, 'uj': 4, 'uk': 4, 'ul': 4, 'um': 4, 'un': 4, 'uo': 4, 'up': 4, 'uq': 4, 'ur': 4, 'us': 4, 'ut': 4, 'uv': 4, 'uw': 4, 'ux': 4, 'uy': 4, 'uz': 4, 'va': 4, 'vb': 4, 'vc': 4, 'vd': 4, 've': 4, 'vf': 4, 'vg': 4, 'vh': 4, 'vi': 4, 'vj': 4, 'vk': 4, 'vl': 4, 'vm': 4, 'vn': 4, 'vo': 4, 'vp': 4, 'vq': 4, 'vr': 4, 'vs': 4, 'vt': 4, 'vu': 4, 'vw': 4, 'vx': 4, 'vy': 4, 'vz': 4, 'wa': 4, 'wb': 4, 'wc': 4, 'wd': 4, 'we': 4, 'wf': 4, 'wg': 4, 'wh': 4, 'wi': 4, 'wj': 4, 'wk': 4, 'wl': 4, 'wm': 4, 'wn': 4, 'wo': 4, 'wp': 4, 'wq': 4, 'wr': 4, 'ws': 4, 'wt': 4, 'wu': 4, 'wv': 4, 'wx': 4, 'wy': 4, 'wz': 4, 'xa': 4, 'xb': 4, 'xc': 4, 'xd': 4, 'xe': 4, 'xf': 4, 'xg': 4, 'xh': 4, 'xi': 4, 'xj': 4, 'xk': 4, 'xl': 4, 'xm': 4, 'xn': 4, 'xo': 4, 'xp': 4, 'xq': 4, 'xr': 4, 'xs': 4, 'xt': 4, 'xu': 4, 'xv': 4, 'xw': 4, 'xy': 4, 'xz': 4, 'ya': 4, 'yb': 4, 'yc': 4, 'yd': 4, 'ye': 4, 'yf': 4, 'yg': 4, 'yh': 4, 'yi': 4, 'yj': 4, 'yk': 4, 'yl': 4, 'ym': 4, 'yn': 4, 'yo': 4, 'yp': 4, 'yq': 4, 'yr': 4, 'ys': 4, 'yt': 4, 'yu': 4, 'yv': 4, 'yw': 4, 'yx': 4, 'yz': 4, 'za': 4, 'zb': 4, 'zc': 4, 'zd': 4, 'ze': 4, 'zf': 4, 'zg': 4, 'zh': 4, 'zi': 4, 'zj': 4, 'zk': 4, 'zl': 4, 'zm': 4, 'zn': 4, 'zo': 4, 'zp': 4, 'zq': 4, 'zr': 4, 'zs': 4, 'zt': 4, 'zu': 4, 'zv': 4, 'zw': 4, 'zx': 4, 'zy': 4, ' _': 2, ' -': 2, ' .': 4, ' ?': 4, ' !': 4, ' :': 4, ' ;': 4, ' ,': 4, ' {': 2, ' }': 2, ' (': 2, ' )': 2, ' [': 2, ' ]': 2, '01': 4, '02': 4, '03': 4, '04': 4, '05': 4, '06': 4, '07': 4, '08': 4, '09': 4, '10': 4, '12': 4, '13': 4, '14': 4, '15': 4, '16': 4, '17': 4, '18': 4, '19': 4, '20': 4, '21': 4, '23': 4, '24': 4, '25': 4, '26': 4, '27': 4, '28': 4, '29': 4, '30': 4, '31': 4, '32': 4, '34': 4, '35': 4, '36': 4, '37': 4, '38': 4, '39': 4, '40': 4, '41': 4, '42': 4, '43': 4, '45': 4, '46': 4, '47': 4, '48': 4, '49': 4, '50': 4, '51': 4, '52': 4, '53': 4, '54': 4, '56': 4, '57': 4, '58': 4, '59': 4, '60': 4, '61': 4, '62': 4, '63': 4, '64': 4, '65': 4, '67': 4, '68': 4, '69': 4, '70': 4, '71': 4, '72': 4, '73': 4, '74': 4, '75': 4, '76': 4, '78': 4, '79': 4, '80': 4, '81': 4, '82': 4, '83': 4, '84': 4, '85': 4, '86': 4, '87': 4, '89': 4, '90': 4, '91': 4, '92': 4, '93': 4, '94': 4, '95': 4, '96': 4, '97': 4, '98': 4, '"\'': 4, '\'"': 4, '/\\': 4, '\\/': 4, '_ ': 2, '_-': 4, '_.': 2, '_?': 2, '_!': 2, '_:': 2, '_;': 2, '_,': 2, '_{': 2, '_}': 2, '_(': 2, '_)': 2, '_[': 2, '_]': 2, '- ': 2, '-_': 4, '-.': 2, '-?': 2, '-!': 2, '-:': 2, '-;': 2, '-,': 2, '-{': 2, '-}': 2, '-(': 2, '-)': 2, '-[': 2, '-]': 2, '. ': 4, '._': 2, '.-': 2, '.?': 4, '.!': 4, '.:': 4, '.;': 4, '.,': 4, '.{': 2, '.}': 2, '.(': 2, '.)': 2, '.[': 2, '.]': 2, '? ': 4, '?_': 2, '?-': 2, '?.': 4, '?!': 4, '?:': 4, '?;': 4, '?,': 4, '?{': 2, '?}': 2, '?(': 2, '?)': 2, '?[': 2, '?]': 2, '! ': 4, '!_': 2, '!-': 2, '!.': 4, '!?': 4, '!:': 4, '!;': 4, '!,': 4, '!{': 2, '!}': 2, '!(': 2, '!)': 2, '![': 2, '!]': 2, ': ': 4, ':_': 2, ':-': 2, ':.': 4, ':?': 4, ':!': 4, ':;': 4, ':,': 4, ':{': 2, ':}': 2, ':(': 2, ':)': 2, ':[': 2, ':]': 2, '; ': 4, ';_': 2, ';-': 2, ';.': 4, ';?': 4, ';!': 4, ';:': 4, ';,': 4, ';{': 2, ';}': 2, ';(': 2, ';)': 2, ';[': 2, ';]': 2, ', ': 4, ',_': 2, ',-': 2, ',.': 4, ',?': 4, ',!': 4, ',:': 4, ',;': 4, ',{': 2, ',}': 2, ',(': 2, ',)': 2, ',[': 2, ',]': 2, '{ ': 2, '{_': 2, '{-': 2, '{.': 2, '{?': 2, '{!': 2, '{:': 2, '{;': 2, '{,': 2, '{}': 4, '{(': 4, '{)': 4, '{[': 4, '{]': 4, '} ': 2, '}_': 2, '}-': 2, '}.': 2, '}?': 2, '}!': 2, '}:': 2, '};': 2, '},': 2, '}{': 4, '}(': 4, '})': 4, '}[': 4, '}]': 4, '( ': 2, '(_': 2, '(-': 2, '(.': 2, '(?': 2, '(!': 2, '(:': 2, '(;': 2, '(,': 2, '({': 4, '(}': 4, '()': 4, '([': 4, '(]': 4, ') ': 2, ')_': 2, ')-': 2, ').': 2, ')?': 2, ')!': 2, '):': 2, ');': 2, '),': 2, '){': 4, ')}': 4, ')(': 4, ')[': 4, ')]': 4, '[ ': 2, '[_': 2, '[-': 2, '[.': 2, '[?': 2, '[!': 2, '[:': 2, '[;': 2, '[,': 2, '[{': 4, '[}': 4, '[(': 4, '[)': 4, '[]': 4, '] ': 2, ']_': 2, ']-': 2, '].': 2, ']?': 2, ']!': 2, ']:': 2, '];': 2, '],': 2, ']{': 4, ']}': 4, '](': 4, '])': 4, '][': 4}

def printMatrix (matrix):
	for line in matrix: print (line)

def prependText (text, item):
	return item + text

def newText():
	return ""

def compareText (itemA, itemB, aliMatrix, a, b):
	aliScore =0
	if itemA == itemB: aliScore = scoreAli
	elif itemA + itemB in scoreMatrix.keys (): aliScore = scoreMatrix [itemA + itemB ]
	elif itemB + itemA in scoreMatrix.keys (): aliScore = scoreMatrix [itemB + itemA ]
	scoreTmp =[
		aliMatrix [a-1][b] + scoreGap,
		aliMatrix [a-1][b-1] + aliScore,
		aliMatrix [a][b-1] + scoreGap
	]
	aliScore = max (scoreTmp)
	return aliScore, scoreTmp.index (aliScore) -1

def prependList (liste, item):
	listeNew =[ item ]
	for old in liste: listeNew.append (old)
	return listeNew

def newList():
	return []

def compareList (itemA, itemB, aliMatrix, a, b):
	if itemA == itemB: return scoreAli, 0
	else: return 0, random.choice (scoreChoice)

def align (anyA, anyB, funcPrepend, funcCompare, funcNew):
	# préparer les éléments
	anyA = funcPrepend (anyA, '_')
	anyB = funcPrepend (anyB, '_')
	# construire les matrices
	aliMatrix =[]
	aliPath =[]
	rangeA = range (1, len (anyA))
	rangeB = range (1, len (anyB))
	aliMatrix.append ([0])
	aliPath.append ([0])
	for b in rangeB:
		aliMatrix[0].append (scoreGap *b)
		aliPath[0].append (1)
	for a in rangeA:
		aliMatrix.append ([ scoreGap *a ])
		aliPath.append ([-1])
		for b in rangeB:
			aliMatrix[-1].append (0)
			aliPath[-1].append (0)
	# phase aller
	for a in rangeA:
		for b in rangeB: aliMatrix[a][b], aliPath[a][b] = funcCompare (anyA[a], anyB[b], aliMatrix, a, b)
	# phase retour
	anyAnew = funcNew()
	anyBnew = funcNew()
	lenA = len (anyA) -1
	lenB = len (anyB) -1
	while lenA >0 or lenB >0:
		if aliPath [lenA][lenB] ==0:
			anyAnew = funcPrepend (anyAnew, anyA [lenA])
			anyBnew = funcPrepend (anyBnew, anyB [lenB])
			lenA -=1
			lenB -=1
		elif aliPath [lenA][lenB] ==1:
			anyAnew = funcPrepend (anyAnew, '_')
			anyBnew = funcPrepend (anyBnew, anyB [lenB])
			lenB -=1
		else:
			anyAnew = funcPrepend (anyAnew, anyA [lenA])
			anyBnew = funcPrepend (anyBnew, '_')
			lenA -=1
	aliScore = aliMatrix[-1][-1] / len (anyAnew)
	return aliScore, anyAnew, anyBnew

def alignText (textA, textB):
	return align (textA, textB, prependText, compareText, newText)

def alignList (listA, listB):
	return align (listA, listB, prependList, compareList, newList)


def test():
	textA = 'abcd'
	textB = '5555'
	listA =[ 'a', 'b', 'c', 'd']
	listB =[ '5', '5', '5', '5']

	print ('textes identiques\n', alignText (textA, textA))
	print ('textes différents\n', alignText (textA, textB))
	print ('listes identiques\n', alignList (listA, listA))
	print ('listes différentes\n', alignList (listA, listB))

test()

def createScoreMatrix():
	allLetters = 'abcdefghijklmnopqrstuvwxyz tn0123456789"\'/\\*°_-.?!:;,%$@&# {}()[]'
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	voyels = 'aeiouy';
	consomns = 'bcdfghjklmnpqrstvwxz'
	numbers = '0123456789'
	spaces = ' \t\n';
	quotes = '"\'';
	brackets = '{}()[]';
	slashs = '/\\';
	tirets = '_-';
	points = '. ?!:;, '
	scoreMatrix = {}
	for la in allLetters:
		for lb in allLetters:
		#	if la==lb: scoreMatrix [la+la] =6
			if la==lb: continue
			elif (la in consomns and lb in consomns) or (la in voyels and lb in voyels) or (la in points and lb in points) or (la in tirets and lb in tirets) or (la in slashs and lb in slashs) or (la in brackets and lb in brackets) or (la in quotes and lb in quotes) or (la in spaces and lb in spaces) or (la in numbers and lb in numbers) or (la in numbers and lb in numbers) or (la in alphabet and lb in alphabet):
				scoreMatrix [la+lb] =4
			#	scoreMatrix [lb+la] =4
			elif (la in voyels and lb in consomns) or (la in consomns and lb in voyels) or (la in points and lb in tirets) or (la in tirets and lb in points) or (la in points and lb in brackets) or (la in brackets and lb in points) or (la in tirets and lb in brackets) or (la in brackets and lb in tirets):
				scoreMatrix [la+lb] =2
		"""	else:
				scoreMatrix [la+lb] =0
				scoreMatrix [lb+la] =0
		"""
	print (scoreMatrix)