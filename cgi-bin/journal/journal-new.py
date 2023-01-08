#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os, sys, codecs, json, cgi, cgitb

# les cors
cgitb.enable()
print ('Content-type: text/html; charset=utf-8')
print ('Access-Control-Allow-Origin: *')
print ('Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS')
print ('Access-Control-Allow-Headers: Content-Type')
print ("")

# récupérer les champs du formulaire
dayDict ={
	"date": "",
	"place": "",
	"title": "",
	"tags": [],
	"peoples": [],
	"content": []
}
contentText =""
form = cgi.FieldStorage()
if form.getvalue ('date'): dayDict['date'] = form.getvalue ('date').replace ('-', '/')
if form.getvalue ('place'): dayDict['place'] = form.getvalue ('place')
if form.getvalue ('peoples'): dayDict['peoples'] = form.getvalue ('peoples').split (', ')
if form.getvalue ('tags'): dayDict['tags'] = form.getvalue ('tags').split (', ')
if form.getvalue ('title'): dayDict['title'] = form.getvalue ('title')
if form.getvalue ('message'): contentText = form.getvalue ('message')

# mots speciaux devant debuter par une majuscule
wordsUpp = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre', 'deborah', 'powers', 'maman', 'mamie', 'papa', 'victo', 'tony', 'simplon', 'loïc')
pointsEnd = '\n\t .?!,;:'	# liste des symboles suivant les mots spéciaux
# "dictionnaire" des majuscule prenant en compte les accents
charUnicode =( ('\\u00c2', 'Â'), ('\\u00e2', 'â'), ('\\u00e0', 'à'), ('\\u00e7', 'ç'),
		('\\u00e9', 'é'), ('\\u00ca', 'Ê'), ('\\u00ea', 'ê'), ('\\u00e8', 'è'), ('\\u00cb', 'Ë'), ('\\u00eb', 'ë'),
		('\\u00ce', 'Î'), ('\\u00ee', 'î'), ('\\u00cf', 'Ï'), ('\\u00ef', 'ï'),
		('\\u00d4', 'Ô'), ('\\u00f4', 'ô'), ('\\u00d6', 'Ö'), ('\\u00f6', 'ö'),
		('\\u00db', 'Û'), ('\\u00fb', 'û'), ('\\u00f9', 'ù')
	)
accents =( ('a','A'), ('à','A'), ('b','B'), ('c','C'), ('\xe7','\xc7'), ('d','D'), ('e','E'), ('é','E'), ('è','E'), ('ê','E'), ('ë','E'), ('f','F'), ('g','G'), ('h','H'), ('i','I'), ('î','I'), ('ï','I'), ('j','J'), ('k','K'), ('l','L'), ('m','M'), ('n','N'), ('o','O'), ('\xf4', '\xe4'), ('p','P'), ('q','Q'), ('r','R'), ('s','S'), ('t','T'), ('u','U'), ('v','V'), ('w','W'), ('x','X'), ('y','Y'), ('z','Z') )
# liste des points, des chaines de caracteres suivies par une majuscule
points =( '\n', '. ', '! ', '? ', ': ', '\n_ ', '\n\t')
pointsShape =( '\n\t- ', '______ ', '\n------ ' )
artefacts =( ('> ','>'), ('Deborah.powers', 'deborah.powers'), ('Http','http'), ('\n ','\n'), (' \n','\n'), ('\n______ ', '\n\n______ '), ('\n______\n\n______ ', '\n\n________________________\n______ '), (' ______\n', ' ______\n\n'), ('------ ', '\n------ '), (' ------', ' ------\n'), ('\n\n\n', '\n\n') )

def shapeText (string):
	string = string.capitalize()
	for p in points:
		for old, new in accents: string = string.replace (p+old, p+new)
	for old, new in artefacts: string = string.replace (old, new)
	for word in wordsUpp:
		for p in pointsEnd:
			string = string.replace (' '+ word +p, ' '+ word.capitalize() +p)
			string = string.replace ('\t'+ word +p, '\t'+ word.capitalize() +p)
			string = string.replace ('\n'+ word +p, '\n'+ word.capitalize() +p)
	return string

dayDict['peoples'].sort()
dayDict['tags'].sort()
dayDict['date'] = dayDict['date'].replace ('-','/')
dayDict['title'] = shapeText (dayDict['title'])
contentText = contentText.replace (' $ ','\n')
contentText = shapeText (contentText)
dayDict['content'] = contentText.split ('\n')

dayJson = json.dumps (dayDict)
print (dayJson)

# écrire l'article dans le json temporaire
jsonName = os.path.dirname (os.path.abspath (__file__)) + os.sep + 'journal-new.json'

def readFile (fileName):
	text =""
	if os.path.exists (fileName):
		textBrut = open (fileName, 'rb')
		tmpByte = textBrut.read()
		encodingList =('utf-8', 'ISO-8859-1', 'ascii')
		for encoding in encodingList:
			try: text = codecs.decode (tmpByte, encoding=encoding)
			except UnicodeDecodeError: pass
			else: break;
		textBrut.close()
	return text

def writeFile (fileName, text):
	textBrut = open (fileName, 'w')
	textBrut.write (text)
	textBrut.close()

def shapeJson (jsonObj):
	dayString = str (jsonObj).replace ('], "', '],\n\t"')
	dayString = dayString.replace ('{"', '{\n\t"')
	dayString = dayString.replace (', "place', ',\n\t"place')
	dayString = dayString.replace (', "title', ',\n\t"title')
	dayString = dayString.replace (', "peoples', ',\n\t"peoples')
	dayString = dayString.replace (', "tags', ',\n\t"tags')
	dayString = dayString.replace (', "content', ',\n\t"content')
	dayString = dayString.replace ('["', '[ "')
	dayString = dayString.replace ('"]', '" ]')
	dayString = dayString.replace ('content": [ "', 'content": [\n\t\t"')
	dayString = dayString.replace ('" ]}', '"\n\t]\n}')
	dayString = dayString.replace (']}', ']\n}')
	dayString = dayString.replace ('}', '},\n')
	for old, new in charUnicode: dayString = dayString.replace (old, new)
	return dayString

articleList = readFile (jsonName)
articleList = articleList[1:]
dayString = shapeJson (dayJson);
articleList ='['+ dayString + articleList
writeFile (jsonName, articleList)
