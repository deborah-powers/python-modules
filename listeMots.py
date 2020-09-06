#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileClass import FileText
from tableClass import ListPerso

nameTxt = "a/opinions/curiosites.html"
alphabet = 'abcdefghijklmnopqrstuvwxyz'
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \t\n'
suffix1 = 'aestxz'
suffix2 = 'ai au as er es le on te ux'
suffix3 = 'ait ain ais ant aux ble eau ent eux ion les lle nes ont ons que sme sse tes tte'
suffix4 = 'able ains aire asme bles eaux esse euse mant ment eons ible ique ions isme lles ques smes ttes'
suffix5 = 'ables aires asmes amant elles ement esses ettes euses ibles iques ismes ments ssent'
forbidden2old = 'cb bc db bd dc cd fb bf fc cf fd df gb bg gc cg gd dg gf fg hb bh hc hd dh hf fh hg gh nh jb bj jc cj cm jd dj jf fj jg gj jh hj kb bk kc ck kd dk kf fk kg gk kh hk kj jk lh hl lj jl lk kl bm mc md dm mf fm mg mh hm mj jm mk km nb bn dn fn jn kn pb bp pc cp pd dp pf fp pg gp hp pj jp pk kp pm np qa qb bq qc cq qd dq qe qf fq qg gq qh hq qi qj jq qk kq ql qm mq qn qo qp pq hr rj jr rk kr qr sb sd ds sf fs sg gs sh hs sj js sk ks qs tb bt tc td dt tf ft tg gt th ht tj jt tk kt tm mt tn tp tq qt vb bv vc cv vd dv vf fv vg gv vh hv vj jv vk kv vl lv vm mv vn vp pv vq qv vs sv vt tv wb bw wc cw wd dw wf fw wg gw wh hw wj jw wk kw wl lw wm mw wn nw wp pw wq qw wr rw cs ws sw wt tw wu uw wv vw xb bx xc cx xd dx xf fx xg gx xh hx xj jx xk kx xl lx xm mx xn xp px xq qx xr rx xs sx xt tx xv vx xw wx yi iy yj jy yq qy yw wy zb bz zc cz zd dz zf fz zg gz zh hz zj jz zk kz zl lz zm mz zn nz zp pz zq qz zr rz zs sz zt uz zv vz zw wz zx xz yz'
forbidden2 =( 'cb', 'bc', 'db', 'bd', 'dc', 'cd', 'fb', 'bf', 'fc', 'cf', 'fd', 'df', 'gb', 'bg', 'gc', 'cg', 'gd', 'dg', 'gf', 'fg', 'hb', 'bh', 'hc', 'hd', 'dh', 'hf', 'fh', 'hg', 'gh', 'nh', 'jb', 'bj', 'jc', 'cj', 'cm', 'jd', 'dj', 'jf', 'fj', 'jg', 'gj', 'jh', 'hj', 'kb', 'bk', 'kc', 'ck', 'kd', 'dk', 'kf', 'fk', 'kg', 'gk', 'kh', 'hk', 'kj', 'jk', 'lh', 'hl', 'lj', 'jl', 'lk', 'kl', 'bm', 'mc', 'md', 'dm', 'mf', 'fm', 'mg', 'mh', 'hm', 'mj', 'jm', 'mk', 'km', 'nb', 'bn', 'dn', 'fn', 'jn', 'kn', 'pb', 'bp', 'pc', 'cp', 'pd', 'dp', 'pf', 'fp', 'pg', 'gp', 'hp', 'pj', 'jp', 'pk', 'kp', 'pm', 'np', 'qa', 'qb', 'bq', 'qc', 'cq', 'qd', 'dq', 'qe', 'qf', 'fq', 'qg', 'gq', 'qh', 'hq', 'qi', 'qj', 'jq', 'qk', 'kq', 'ql', 'qm', 'mq', 'qn', 'qo', 'qp', 'pq', 'hr', 'rj', 'jr', 'rk', 'kr', 'qr', 'sb', 'sd', 'ds', 'sf', 'fs', 'sg', 'gs', 'sh', 'hs', 'sj', 'js', 'sk', 'ks', 'qs', 'tb', 'bt', 'tc', 'td', 'dt', 'tf', 'ft', 'tg', 'gt', 'th', 'ht', 'tj', 'jt', 'tk', 'kt', 'tm', 'mt', 'tn', 'tp', 'tq', 'qt', 'vb', 'bv', 'vc', 'cv', 'vd', 'dv', 'vf', 'fv', 'vg', 'gv', 'vh', 'hv', 'vj', 'jv', 'vk', 'kv', 'vl', 'lv', 'vm', 'mv', 'vn', 'vp', 'pv', 'vq', 'qv', 'vs', 'sv', 'vt', 'tv', 'wb', 'bw', 'wc', 'cw', 'wd', 'dw', 'wf', 'fw', 'wg', 'gw', 'wh', 'hw', 'wj', 'jw', 'wk', 'kw', 'wl', 'lw', 'wm', 'mw', 'wn', 'nw', 'wp', 'pw', 'wq', 'qw', 'wr', 'rw', 'cs', 'ws', 'sw', 'wt', 'tw', 'wu', 'uw', 'wv', 'vw', 'xb', 'bx', 'xc', 'cx', 'xd', 'dx', 'xf', 'fx', 'xg', 'gx', 'xh', 'hx', 'xj', 'jx', 'xk', 'kx', 'xl', 'lx', 'xm', 'mx', 'xn', 'xp', 'px', 'xq', 'qx', 'xr', 'rx', 'xs', 'sx', 'xt', 'tx', 'xv', 'vx', 'xw', 'wx', 'yi', 'iy', 'yj', 'jy', 'yq', 'qy', 'yw', 'wy', 'zb', 'bz', 'zc', 'cz', 'zd', 'dz', 'zf', 'fz', 'zg', 'gz', 'zh', 'hz', 'zj', 'jz', 'zk', 'kz', 'zl', 'lz', 'zm', 'mz', 'zn', 'nz', 'zp', 'pz', 'zq', 'qz', 'zr', 'rz', 'zs', 'sz', 'zt', 'uz', 'zv', 'vz', 'zw', 'wz', 'zx', 'xz', 'yz')

fileWords = FileText ('b/liste-mots.txt')

def fromText (nameTxt):
	# préparer les fichiers
	fileWords.fromFile()
	fileWords.dataFromFile()
	fileTxt = FileText (nameTxt)
	fileTxt.fromFile()
	# préparer les mots
	for c in fileTxt.text:
		if c not in letters: fileTxt.replace (c, ' ')
	fileTxt.replace ('\n',' ')
	fileTxt.replace ('\t',' ')
	while fileTxt.contain ('  '): fileTxt.replace ('  ',' ')
	fileTxt.text = fileTxt.text.lower()
	listTxt = ListPerso()
	listTxt.fromList (fileTxt.text.split (' '))
	# analyser les mots
	rangeTxt = listTxt.range()
	rangeTxt.reverse()
	for w in rangeTxt:
		if listTxt.count (listTxt[w]) >1: listTxt.pop(w)
		elif len (listTxt[w]) >5 and listTxt[w][-5:] in suffix5 and listTxt[w][:-5] in listTxt: listTxt.pop(w)
		elif len (listTxt[w]) >4 and listTxt[w][-4:] in suffix4 and listTxt[w][:-4] in listTxt: listTxt.pop(w)
		elif len (listTxt[w]) >3 and listTxt[w][-3:] in suffix3 and listTxt[w][:-3] in listTxt: listTxt.pop(w)
		elif len (listTxt[w]) >2 and listTxt[w][-2:] in suffix2 and listTxt[w][:-2] in listTxt: listTxt.pop(w)
		elif len (listTxt[w]) >1 and listTxt[w][-1] in suffix1 and listTxt[w][:-1] in listTxt: listTxt.pop(w)
	rangeTxt = listTxt.range()
	rangeTxt.reverse()
	for w in rangeTxt:
		for pair in forbidden2:
			if pair in listTxt[w]:
				print (listTxt[w])
				listTxt.pop(w)
				break
	listTxt.sort()
	for word in listTxt:
		if not fileWords.contain (word):
			if word[-5:] in suffix5 and fileWords.contain (word[:-5]): continue
			elif word[-4:] in suffix4 and fileWords.contain (word[:-4]): continue
			elif word[-3:] in suffix3 and fileWords.contain (word[:-3]): continue
			elif word[-2:] in suffix2 and fileWords.contain (word[:-2]): continue
			elif word[-1] in suffix1 and fileWords.contain (word[:-1]): continue
			else: fileWords.text = fileWords.text +' '+ word


def duo():
	txt =""
	rangeAlphabet = range (26)
	for a in rangeAlphabet:
		for b in rangeAlphabet[:a]:
			if alphabet[a] + alphabet[b] not in forbidden2: txt = txt + alphabet[a] + alphabet[b] +' '
			if alphabet[b] + alphabet[a] not in forbidden2: txt = txt + alphabet[b] + alphabet[a] +' '
	fileWords.text = txt

def addLetter (txt):
	if (len (txt)) >5: return []
	lst = ListPerso()
	lstTmp =[]
	for l in alphabet:
		if txt:
			if txt[-1] ==l: continue
			elif txt[-1] +l in forbidden2: continue
		lstTmp.append (txt +l)
		if len (txt) >2: lst.append (txt +l)
	if len (lstTmp[-1]) <6:
		for w in lstTmp: lst.extend (addLetter (w))
	return lst

def recapLetter():
	lst = addLetter ('a')
	lst.sort()
	fileWords.text = ' '.join (lst)

fromText (nameTxt)
fileWords.dataFromFile()
fileWords.toFile()

