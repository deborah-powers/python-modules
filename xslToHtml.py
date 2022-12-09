#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

fileName = 'b/exemple.xsl'
fileObj = File (fileName)

tagNames =( 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button', 'a', 'img', 'form', 'input', 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body' )
attrNames =( 'id', 'class', 'type' )

def cleanCode (self):
	self.text = self.text.strip()
	self.replace ('\t', "")
	self.replace ('\r', "")
	self.replace ('\n', " ")
	while '  ' in self.text: self.replace ('  ', ' ')
	self.replace ('> <', '><')
	self.replace (' >', '>')
	self.replace (' />', '/>')
	self.replace ('"', "'")
	self.replace ('<!--', '\n<!--')
	self.replace ('-->', '-->\n')

def convert (self):
	for tag in tagNames: self.replace ("<xsl:element name='" + tag +"'>", '<'+ tag +'>')
	for attr in attrNames: self.replace ("><xsl:attribute name='" + attr +"'>", " "+ attr + "='")

	self.replace ("</xsl:attribute>", "'")
"""
	self.replace ("<xsl:attribute name='")
	self.replace ("xsl:element name='")
	self.replace ("xsl:variable name='")
	self.replace ("'> ", ' ')
	self.replace ("'>", "='")
"""
setattr (File, 'cleanXsl', cleanCode)
setattr (File, 'toHtml', convert)

fileObj.read()
fileObj.cleanXsl()
fileObj.toHtml()
fileObj.title = 'exemple bis'
fileObj.write()



