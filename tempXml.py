#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File
# fileXmlNpslName = 'C:\\Users\\deborah.powers\\Desktop\\ciphyto flux\\ciphyto conseil npsl 05-12 flux.xml'
fileXmlNpslName = 'C:\\Users\\deborah.powers\\Desktop\\ciphyto flux\\9 npsl A-6-7MEJ84TT.xml'
fileXmlLegaName = 'C:\\Users\\deborah.powers\\Desktop\\ciphyto flux\\9 lega A-6-6HZO3N66.xml'

def cleanXml (xmlText):
	xmlText = xmlText.replace ('\t', " ")
	xmlText = xmlText.replace ('\n', " ")
	xmlText = xmlText.replace ('\r', " ")
	while "  " in xmlText: xmlText = xmlText.replace ("  ", " ")
	xmlText = xmlText.replace (" >", ">")
	xmlText = xmlText.replace (" <", "<")
	xmlText = xmlText.replace ("> ", ">")
	xmlText = xmlText.replace ('</', '\n</')
	xmlText = xmlText.replace ('><', '>\n<')
	xmlText = xmlText.replace ("/>", ">")
	xmlText = xmlText.strip()
	xmlList = xmlText.split ('\n')
	xmlRange = reversed (range (len (xmlList)))
	trash = 'hello'
	for l in xmlRange:
		if xmlList[l][:2] == '</': trash = xmlList.pop (l)
	xmlText = '\n'.join (xmlList)
	while '\n\n' in xmlText: xmlText = xmlText.replace ('\n\n', '\n')
	xmlText = xmlText.replace ('>\n', '>')
	xmlText = xmlText.replace ('><', '>\n<')
	return xmlText

fileXmlNpsl = File (fileXmlNpslName)
fileXmlNpsl.read()
fileXmlNpsl.text = cleanXml (fileXmlNpsl.text)

fileXmlLega = File (fileXmlLegaName)
fileXmlLega.read()
fileXmlLega.text = cleanXml (fileXmlLega.text)

fileXmlNpsl.comparer (fileXmlLega)


"""
https://www.xml.com/pub/1999/09/expat/index.html
https://stackoverflow.com/questions/1179305/expat-parsing-in-python-3
from xml.parsers import expat

parser = expat.ParserCreate()
fileXml = parser.ParseFile (open (fileXmlName, 'rb'))

print ('fichier xml\n', fileXml)
"""
