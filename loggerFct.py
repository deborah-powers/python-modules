#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
from inspect import stack
from fileLocal import pathRoot, pathDesktop

logDate = False

def traceLine():
	stackList = stack()
	stackLen = len (stackList)
	i=0
	while i< stackLen and __file__ in stackList[i].filename: i+=1
	strNum = str (stackList[i].lineno)
	while len (strNum) <3: strNum = strNum +' '
	strFile = stackList[i].filename
	strFile = strFile.replace ('AppData\\Local\\Programs\\Python\\Python38\\lib\\site-packages\\', "")
	strFile = strFile.replace ('\\__init__.py', "")
	strFile = strFile.replace (pathDesktop + 'python\\', "")
	strFile = strFile.replace (pathDesktop, "")
	strFile = strFile.replace (pathRoot, "")
	return '%s\t%s %s' % (strFile, strNum, stackList[i].function)

def computeTrace():
	# date est un objet datetime.datetime
	now = datetime.today()
	strDate = '%02d:%02d:%02d:%02d'% (now.hour, now.minute, now.second, now.microsecond)
	strDate = strDate[:12]
	while len (strDate) <13: strDate = strDate +' '
	return strDate

def objToStr (message):
	if type (message) == int and message ==0: return 'O'
	elif type (message) == bool:
		if message: return 'oui'
		else: return 'non'
	elif not message: return ""
	elif type (message) == dict:
		messageKeys = list (message.keys())
		res = "dictionnaire à "+ objToStr (len (messageKeys)) + " entrées\n"
		nbkeys = len (messageKeys)
		if nbkeys >10: nbkeys =10
		rkeys = range (nbkeys)
		for k in rkeys: res = res + objToStr (messageKeys[k]) +"\t"+ objToStr (message[messageKeys[k]]) +"\n"
		return res
	elif type (message) == list:
		res = "liste à "+ objToStr (len (message)) + " éléments\n"
		for line in message[:10]: res = res + objToStr (line) +"\n"
		return res
	elif type (message) == str: return message[:100]
	else: return str (message)

def logInfo():
	trace = traceLine()
	if logDate: trace = computeTrace() + trace
	print (trace)

def message (message):
	trace = traceLine()
	if logDate: trace = computeTrace() + trace
	res = objToStr (message)
	trace = trace +'\t'+ res
	print (trace)

def coucou ():
	message ('coucou')

def log (*messages):
	trace = traceLine()
	if logDate: trace = computeTrace() + trace
	for message in messages:
		res = objToStr (message)
		if '\n' in res or len (res) >300: trace = trace +'\n'+ res
		else: trace = trace +'\t'+ res
	print (trace)

def exists (obj):
	if (obj): message (obj)
	else: message ('objet null')

alphabet = 'abcdefghijklmnopqrstuvwxyz'
letterPos =0

def letter():
	log (alphabet [letterPos])
	letterPos = letterPos +1
	if letterPos >25: letterPos =0

# afficher l'aide basique pour un objet. conçu pour mes classes perso

def findParentsClass (classObj):
	name = classObj.__name__
	methods =[]
	for item in classObj.__dict__:
		if classObj.__dict__[item] and 'function' == type (classObj.__dict__[item]).__name__: methods.append (item)
	if 'object' != classObj.__bases__[0].__name__:
		for parent in classObj.__bases__:
			parentName, parentMethods = findParentsClass (parent)
			name = name +", "+ parentName
			for parentMethod in parentMethods:
				if parentMethod not in methods: methods.append (parentMethod)
	return name, methods

def objectManual (item):
	text = 'object of class %s, in module %s\nfields: ' % (item.__class__.__name__, item.__class__.__module__)
	for field in item.__dict__: text = text + field +", "
	text = text[:-2]
	name, methods = findParentsClass (item.__class__)
	eraseInit = methods.pop (0)
	text = text +'\nmethods: '+ ", ".join (methods)
	posClassName =1+ name.find (', ')
	name = name[posClassName:]
	text = text +'\nparents:' + name
	return text
