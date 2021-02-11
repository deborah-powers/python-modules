#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from textClass import Text
from listClass import ListPerso

scoreGap =1
scoreMatrix = {'ab': 2, 'ba': 2, 'ac': 2, 'ca': 2, 'ad': 2, 'da': 2, 'ae': 4, 'ea': 4, 'af': 2, 'fa': 2, 'ag': 2, 'ga': 2, 'ah': 2, 'ha': 2, 'ai': 4, 'ia': 4, 'aj': 2, 'ja': 2, 'ak': 2, 'ka': 2, 'al': 2, 'la': 2, 'am': 2, 'ma': 2, 'an': 2, 'na': 2, 'ao': 4, 'oa': 4, 'ap': 2, 'pa': 2, 'aq': 2, 'qa': 2, 'ar': 2, 'ra': 2, 'as': 2, 'sa': 2, 'at': 2, 'ta': 2, 'au': 4, 'ua': 4, 'av': 2, 'va': 2, 'aw': 2, 'wa': 2, 'ax': 2, 'xa': 2, 'ay': 4, 'ya': 4, 'az': 2, 'za': 2, 'bc': 4, 'cb': 4, 'bd': 4, 'db': 4, 'be': 2, 'eb': 2, 'bf': 4, 'fb': 4, 'bg': 4, 'gb': 4, 'bh': 4, 'hb': 4, 'bi': 2, 'ib': 2, 'bj': 4, 'jb': 4, 'bk': 4, 'kb': 4, 'bl': 4, 'lb': 4, 'bm': 4, 'mb': 4, 'bn': 4, 'nb': 4, 'bo': 2, 'ob': 2, 'bp': 4, 'pb': 4, 'bq': 4, 'qb': 4, 'br': 4, 'rb': 4, 'bs': 4, 'sb': 4, 'bt': 4, 'tb': 4, 'bu': 2, 'ub': 2, 'bv': 4, 'vb': 4, 'bw': 4, 'wb': 4, 'bx': 4, 'xb': 4, 'by': 2, 'yb': 2, 'bz': 4, 'zb': 4, 'cd': 4, 'dc': 4, 'ce': 2, 'ec': 2, 'cf': 4, 'fc': 4, 'cg': 4, 'gc': 4, 'ch': 4, 'hc': 4, 'ci': 2, 'ic': 2, 'cj': 4, 'jc': 4, 'ck': 4, 'kc': 4, 'cl': 4, 'lc': 4, 'cm': 4, 'mc': 4, 'cn': 4, 'nc': 4, 'co': 2, 'oc': 2, 'cp': 4, 'pc': 4, 'cq': 4, 'qc': 4, 'cr': 4, 'rc': 4, 'cs': 4, 'sc': 4, 'ct': 4, 'tc': 4, 'cu': 2, 'uc': 2, 'cv': 4, 'vc': 4, 'cw': 4, 'wc': 4, 'cx': 4, 'xc': 4, 'cy': 2, 'yc': 2, 'cz': 4, 'zc': 4, 'de': 2, 'ed': 2, 'df': 4, 'fd': 4, 'dg': 4, 'gd': 4, 'dh': 4, 'hd': 4, 'di': 2, 'id': 2, 'dj': 4, 'jd': 4, 'dk': 4, 'kd': 4, 'dl': 4, 'ld': 4, 'dm': 4, 'md': 4, 'dn': 4, 'nd': 4, 'do': 2, 'od': 2, 'dp': 4, 'pd': 4, 'dq': 4, 'qd': 4, 'dr': 4, 'rd': 4, 'ds': 4, 'sd': 4, 'dt': 4, 'td': 4, 'du': 2, 'ud': 2, 'dv': 4, 'vd': 4, 'dw': 4, 'wd': 4, 'dx': 4, 'xd': 4, 'dy': 2, 'yd': 2, 'dz': 4, 'zd': 4, 'ef': 2, 'fe': 2, 'eg': 2, 'ge': 2, 'eh': 2, 'he': 2, 'ei': 4, 'ie': 4, 'ej': 2, 'je': 2, 'ek': 2, 'ke': 2, 'el': 2, 'le': 2, 'em': 2, 'me': 2, 'en': 2, 'ne': 2, 'eo': 4, 'oe': 4, 'ep': 2, 'pe': 2, 'eq': 2, 'qe': 2, 'er': 2, 're': 2, 'es': 2, 'se': 2, 'et': 2, 'te': 2, 'eu': 4, 'ue': 4, 'ev': 2, 've': 2, 'ew': 2, 'we': 2, 'ex': 2, 'xe': 2, 'ey': 4, 'ye': 4, 'ez': 2, 'ze': 2, 'fg': 4, 'gf': 4, 'fh': 4, 'hf': 4, 'fi': 2, 'if': 2, 'fj': 4, 'jf': 4, 'fk': 4, 'kf': 4, 'fl': 4, 'lf': 4, 'fm': 4, 'mf': 4, 'fn': 4, 'nf': 4, 'fo': 2, 'of': 2, 'fp': 4, 'pf': 4, 'fq': 4, 'qf': 4, 'fr': 4, 'rf': 4, 'fs': 4, 'sf': 4, 'ft': 4, 'tf': 4, 'fu': 2, 'uf': 2, 'fv': 4, 'vf': 4, 'fw': 4, 'wf': 4, 'fx': 4, 'xf': 4, 'fy': 2, 'yf': 2, 'fz': 4, 'zf': 4, 'gh': 4, 'hg': 4, 'gi': 2, 'ig': 2, 'gj': 4, 'jg': 4, 'gk': 4, 'kg': 4, 'gl': 4, 'lg': 4, 'gm': 4, 'mg': 4, 'gn': 4, 'ng': 4, 'go': 2, 'og': 2, 'gp': 4, 'pg': 4, 'gq': 4, 'qg': 4, 'gr': 4, 'rg': 4, 'gs': 4, 'sg': 4, 'gt': 4, 'tg': 4, 'gu': 2, 'ug': 2, 'gv': 4, 'vg': 4, 'gw': 4, 'wg': 4, 'gx': 4, 'xg': 4, 'gy': 2, 'yg': 2, 'gz': 4, 'zg': 4, 'hi': 2, 'ih': 2, 'hj': 4, 'jh': 4, 'hk': 4, 'kh': 4, 'hl': 4, 'lh': 4, 'hm': 4, 'mh': 4, 'hn': 4, 'nh': 4, 'ho': 2, 'oh': 2, 'hp': 4, 'ph': 4, 'hq': 4, 'qh': 4, 'hr': 4, 'rh': 4, 'hs': 4, 'sh': 4, 'ht': 4, 'th': 4, 'hu': 2, 'uh': 2, 'hv': 4, 'vh': 4, 'hw': 4, 'wh': 4, 'hx': 4, 'xh': 4, 'hy': 2, 'yh': 2, 'hz': 4, 'zh': 4, 'ij': 2, 'ji': 2, 'ik': 2, 'ki': 2, 'il': 2, 'li': 2, 'im': 2, 'mi': 2, 'in': 2, 'ni': 2, 'io': 4, 'oi': 4, 'ip': 2, 'pi': 2, 'iq': 2, 'qi': 2, 'ir': 2, 'ri': 2, 'is': 2, 'si': 2, 'it': 2, 'ti': 2, 'iu': 4, 'ui': 4, 'iv': 2, 'vi': 2, 'iw': 2, 'wi': 2, 'ix': 2, 'xi': 2, 'iy': 4, 'yi': 4, 'iz': 2, 'zi': 2, 'jk': 4, 'kj': 4, 'jl': 4, 'lj': 4, 'jm': 4, 'mj': 4, 'jn': 4, 'nj': 4, 'jo': 2, 'oj': 2, 'jp': 4, 'pj': 4, 'jq': 4, 'qj': 4, 'jr': 4, 'rj': 4, 'js': 4, 'sj': 4, 'jt': 4, 'tj': 4, 'ju': 2, 'uj': 2, 'jv': 4, 'vj': 4, 'jw': 4, 'wj': 4, 'jx': 4, 'xj': 4, 'jy': 2, 'yj': 2, 'jz': 4, 'zj': 4, 'kl': 4, 'lk': 4, 'km': 4, 'mk': 4, 'kn': 4, 'nk': 4, 'ko': 2, 'ok': 2, 'kp': 4, 'pk': 4, 'kq': 4, 'qk': 4, 'kr': 4, 'rk': 4, 'ks': 4, 'sk': 4, 'kt': 4, 'tk': 4, 'ku': 2, 'uk': 2, 'kv': 4, 'vk': 4, 'kw': 4, 'wk': 4, 'kx': 4, 'xk': 4, 'ky': 2, 'yk': 2, 'kz': 4, 'zk': 4, 'lm': 4, 'ml': 4, 'ln': 4, 'nl': 4, 'lo': 2, 'ol': 2, 'lp': 4, 'pl': 4, 'lq': 4, 'ql': 4, 'lr': 4, 'rl': 4, 'ls': 4, 'sl': 4, 'lt': 4, 'tl': 4, 'lu': 2, 'ul': 2, 'lv': 4, 'vl': 4, 'lw': 4, 'wl': 4, 'lx': 4, 'xl': 4, 'ly': 2, 'yl': 2, 'lz': 4, 'zl': 4, 'mn': 4, 'nm': 4, 'mo': 2, 'om': 2, 'mp': 4, 'pm': 4, 'mq': 4, 'qm': 4, 'mr': 4, 'rm': 4, 'ms': 4, 'sm': 4, 'mt': 4, 'tm': 4, 'mu': 2, 'um': 2, 'mv': 4, 'vm': 4, 'mw': 4, 'wm': 4, 'mx': 4, 'xm': 4, 'my': 2, 'ym': 2, 'mz': 4, 'zm': 4, 'no': 2, 'on': 2, 'np': 4, 'pn': 4, 'nq': 4, 'qn': 4, 'nr': 4, 'rn': 4, 'ns': 4, 'sn': 4, 'nt': 4, 'tn': 4, 'nu': 2, 'un': 2, 'nv': 4, 'vn': 4, 'nw': 4, 'wn': 4, 'nx': 4, 'xn': 4, 'ny': 2, 'yn': 2, 'nz': 4, 'zn': 4, 'op': 2, 'po': 2, 'oq': 2, 'qo': 2, 'or': 2, 'ro': 2, 'os': 2, 'so': 2, 'ot': 2, 'to': 2, 'ou': 4, 'uo': 4, 'ov': 2, 'vo': 2, 'ow': 2, 'wo': 2, 'ox': 2, 'xo': 2, 'oy': 4, 'yo': 4, 'oz': 2, 'zo': 2, 'pq': 4, 'qp': 4, 'pr': 4, 'rp': 4, 'ps': 4, 'sp': 4, 'pt': 4, 'tp': 4, 'pu': 2, 'up': 2, 'pv': 4, 'vp': 4, 'pw': 4, 'wp': 4, 'px': 4, 'xp': 4, 'py': 2, 'yp': 2, 'pz': 4, 'zp': 4, 'qr': 4, 'rq': 4, 'qs': 4, 'sq': 4, 'qt': 4, 'tq': 4, 'qu': 2, 'uq': 2, 'qv': 4, 'vq': 4, 'qw': 4, 'wq': 4, 'qx': 4, 'xq': 4, 'qy': 2, 'yq': 2, 'qz': 4, 'zq': 4, 'rs': 4, 'sr': 4, 'rt': 4, 'tr': 4, 'ru': 2, 'ur': 2, 'rv': 4, 'vr': 4, 'rw': 4, 'wr': 4, 'rx': 4, 'xr': 4, 'ry': 2, 'yr': 2, 'rz': 4, 'zr': 4, 'st': 4, 'ts': 4, 'su': 2, 'us': 2, 'sv': 4, 'vs': 4, 'sw': 4, 'ws': 4, 'sx': 4, 'xs': 4, 'sy': 2, 'ys': 2, 'sz': 4, 'zs': 4, 'tu': 2, 'ut': 2, 'tv': 4, 'vt': 4, 'tw': 4, 'wt': 4, 'tx': 4, 'xt': 4, 'ty': 2, 'yt': 2, 'tz': 4, 'zt': 4, 'uv': 2, 'vu': 2, 'uw': 2, 'wu': 2, 'ux': 2, 'xu': 2, 'uy': 4, 'yu': 4, 'uz': 2, 'zu': 2, 'vw': 4, 'wv': 4, 'vx': 4, 'xv': 4, 'vy': 2, 'yv': 2, 'vz': 4, 'zv': 4, 'wx': 4, 'xw': 4, 'wy': 2, 'yw': 2, 'wz': 4, 'zw': 4, 'xy': 2, 'yx': 2, 'xz': 4, 'zx': 4, 'yz': 2, 'zy': 2, ' \t': 2, '\t ': 2, ' \n': 2, '\n ': 2, '\t\n': 2, '\n\t': 2, '01': 2, '10': 2, '02': 2, '20': 2, '03': 2, '30': 2, '04': 2, '40': 2, '05': 2, '50': 2, '06': 2, '60': 2, '07': 2, '70': 2, '08': 2, '80': 2, '09': 2, '90': 2, '12': 2, '21': 2, '13': 2, '31': 2, '14': 2, '41': 2, '15': 2, '51': 2, '16': 2, '61': 2, '17': 2, '71': 2, '18': 2, '81': 2, '19': 2, '91': 2, '23': 2, '32': 2, '24': 2, '42': 2, '25': 2, '52': 2, '26': 2, '62': 2, '27': 2, '72': 2, '28': 2, '82': 2, '29': 2, '92': 2, '34': 2, '43': 2, '35': 2, '53': 2, '36': 2, '63': 2, '37': 2, '73': 2, '38': 2, '83': 2, '39': 2, '93': 2, '45': 2, '54': 2, '46': 2, '64': 2, '47': 2, '74': 2, '48': 2, '84': 2, '49': 2, '94': 2, '56': 2, '65': 2, '57': 2, '75': 2, '58': 2, '85': 2, '59': 2, '95': 2, '67': 2, '76': 2, '68': 2, '86': 2, '69': 2, '96': 2, '78': 2, '87': 2, '79': 2, '97': 2, '89': 2, '98': 2, '"\'': 2, '\'"': 2, '\\/': 2, '/\\': 2, '_-': 2, '-_': 2, '.?': 2, '?.': 2, '.!': 2, '!.': 2, '.:': 2, ':.': 2, '.;': 2, ';.': 2, '.,': 2, ',.': 2, '?!': 2, '!?': 2, '?:': 2, ':?': 2, '?;': 2, ';?': 2, '?,': 2, ',?': 2, '!:': 2, ':!': 2, '!;': 2, ';!': 2, '!,': 2, ',!': 2, ':;': 2, ';:': 2, ':,': 2, ',:': 2, ';,': 2, ',;': 2, '{}': 2, '}{': 2, '{(': 2, '({': 2, '{)': 2, '){': 2, '{[': 2, '[{': 2, '{]': 2, ']{': 2, '}(': 2, '(}': 2, '})': 2, ')}': 2, '}[': 2, '[}': 2, '}]': 2, ']}': 2, '()': 2, ')(': 2, '([': 2, '[(': 2, '(]': 2, '](': 2, ')[': 2, '[)': 2, ')]': 2, '])': 2, '[]': 2, '][': 2}


def groomForAlignment (self):
	self.clean()
	self.replace ('\n', ' ')
	self.replace ('\t', ' ')
	self.text =' '+ self.text

def toListForAlignment (self):
	listObj = ListPerso()
#	listObj.addList (self.text.split())
	listObj.addList (list (self.text))
	return listObj

setattr (Text, 'groom', groomForAlignment)
setattr (Text, 'toList', toListForAlignment)

def alignment (self, newText):
	self.groom()
	newText.groom()
	if self.text == newText.text:
		print ('les textes sont identiques')
		return 'pareil'
	# aller
	listA = self.toList();		ranA = listA.range()
	listB = newText.toList();	ranB = listB.range()
	scoreTab =[]
	pathTab =[]
	for a in ranA:
		scoreTab.append ([])
		pathTab.append ([])
		for b in ranB:
			scoreTab[-1].append (scoreGap)
			pathTab[-1].append (0)
	ranA = listA.range (1)
	ranB = listB.range (1)
	for a in ranA:
		for b in ranB:
			scoreApp =0
			if listA[a] == listB[b]: scoreApp =6
			elif listA[a] + listB[b] in scoreMatrix.keys(): scoreApp = scoreMatrix[listA[a] + listB[b]]
			scoreTmp =[
				scoreTab[a-1][b-1] + scoreApp,
				scoreTab[a-1][b] + scoreGap,
				scoreTab[a][b-1] + scoreGap
			]
			scoreTab[a][b] = max (scoreTmp)
			pathTab[a][b] = scoreTmp.index (scoreTab[a][b])
	# retour
	textA ="";	lenA = self.length() -1
	textB ="";	lenB = newText.length() -1
	while lenA >0 or lenB >0:
		if pathTab[lenA][lenB] ==0:
			textA = self[lenA] + textA
			textB = newText[lenB] + textB
			lenA -=1
			lenB -=1
		elif pathTab[lenA][lenB] ==1:
			textA = self[lenA] + textA
			textB = ' '+ textB
			lenA -=1
		else:
			textA = ' '+ textA
			textB = newText[lenB] + textB
			lenB -=1
	textA = textA +'\n'+ textB
	return textA

setattr (Text, 'comparScore', alignment)

def alignment_va (self, newText):
	self.clean()
	newText.clean()
	self = self.replace ('\n', ' ')
	self = self.replace ('\t', ' ')
	newText = newText.replace ('\n', ' ')
	newText = newText.replace ('\t', ' ')
	if self == newText:
		print ('les textes sont identiques')
		return 'pareil'
	# aller
	self = self.preppend (' ')
	newText = newText.preppend (' ')
	lenA = self.length();		ranA = range (lenA)
	lenB = newText.length();	ranB = range (lenB)
	scoreTab =[]
	pathTab =[]
	scoreGap =1
	for a in ranA:
		scoreTab.append ([])
		pathTab.append ([])
		for b in ranB:
			scoreTab[-1].append (scoreGap)
			pathTab[-1].append (0)
	ranA = range (1, lenA)
	ranB = range (1, lenB)
	for a in ranA:
		for b in ranB:
			scoreApp =0
			if self[a] == newText[b]: scoreApp =6
			elif self[a] + newText[b] in scoreMatrix.keys(): scoreApp = scoreMatrix[self[a] + newText[b]]
			scoreTmp =[
				scoreTab[a-1][b-1] + scoreApp,
				scoreTab[a-1][b] + scoreGap,
				scoreTab[a][b-1] + scoreGap
			]
			scoreTab[a][b] = max (scoreTmp)
			pathTab[a][b] = scoreTmp.index (scoreTab[a][b])
	# retour
	textA ="";	lenA -=1
	textB ="";	lenB -=1
	while lenA >0 or lenB >0:
		if pathTab[lenA][lenB] ==0:
			textA = self[lenA] + textA
			textB = newText[lenB] + textB
			lenA -=1
			lenB -=1
		elif pathTab[lenA][lenB] ==1:
			textA = self[lenA] + textA
			textB = ' '+ textB
			lenA -=1
		else:
			textA = ' '+ textA
			textB = newText[lenB] + textB
			lenB -=1
	textA = textA +'\n'+ textB
	return textA

def createScoreMatrix():
	all = 'abcdefghijklmnopqrstuvwxyz \t\n0123456789"\'\\/*°_-.?!:;,%$@&#{}()[]'
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	voyels = 'aeiouy'; consomns = 'bcdfghjklmnpqrstvwxz'
	numbers = '0123456789'
	spaces = ' \t\n'; quotes = '"\''; brackets = '{}()[]'; slashs = '\\/'; tirets = '_-'; points = '.?!:;,'
	scoreMatrix = {}
	for la in all:
		for lb in all:
		#	if la==lb: scoreMatrix[la+la] =6
			if la==lb: continue
			elif (la in consomns and lb in consomns) or (la in voyels and lb in voyels):
				scoreMatrix[la+lb] =4
				scoreMatrix[lb+la] =4
			elif (la in points and lb in points) or (la in tirets and lb in tirets) or (la in slashs and lb in slashs) or (la in brackets and lb in brackets) or (la in quotes and lb in quotes) or (la in spaces and lb in spaces) or (la in numbers and lb in numbers) or (la in numbers and lb in numbers) or (la in alphabet and lb in alphabet):
				scoreMatrix[la+lb] =2
				scoreMatrix[lb+la] =2
			"""
			else:
				scoreMatrix[la+lb] =0
				scoreMatrix[lb+la] =0
			"""
	print (scoreMatrix)

