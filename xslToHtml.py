#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

fileName = 'b/exemple.xsl'
fileObj = File (fileName)

tagNames =[ 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ul', 'ol', 'td', 'th', 'label', 'button', 'a', 'img', 'form', 'input', 'hr', 'br', 'tr', 'table', 'figure', 'figcaption', 'form', 'fieldset', 'code', 'nav', 'article', 'section', 'body' ]
attrNames =[ 'id', 'class', 'type', 'style', 'href', 'alt', 'src', 'name', 'value' ]

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
	while '\n\n' in self.text: self.replace ('\n\n', '\n')

def convert (self):
	self.replace ("<xsl:text>")
	self.replace ("</xsl:text>")
	# les templates
	self.replace ("<xsl:template", '<template')
	self.replace ("</xsl:template>", '</template>')
	tmpList = self.text.split ("<xsl:apply-templates select='")
	tmpRange = range (1, len (tmpList))
	for t in tmpRange:
		f= tmpList[t].find ('mode=')
		tmpList[t] = tmpList[t][f:]
	self.text = "<apply-templates ".join (tmpList)
	# les variables
	tmpList = self.text.split ("<xsl:value-of select='")
	tmpRange = range (1, len (tmpList))
	for t in tmpRange: tmpList[t] = tmpList[t].replace ("'/>", "", 1)
	self.text = "".join (tmpList)
	# les les attributs
	tmpList = self.text.split ("<xsl:attribute name='")
	for line in tmpList:
		f= line.find ("'")
		if line[:f] not in attrNames: attrNames.append (line[:f])
	for attr in attrNames: self.replace ("><xsl:attribute name='" + attr +"'>", " "+ attr + "='")
	self.replace ("</xsl:attribute>", "'")
	# les les balises
	tmpList = self.text.split ("<xsl:element name='")
	for line in tmpList:
		f= line.find ("'")
		if line[:f] not in tagNames: tagNames.append (line[:f])
	for tag in tagNames:
		self.replace ("<xsl:element name='" + tag +"'", '<'+ tag +'>')
		self.replace ("<xsl:element name='" + tag +"'/>", '<'+ tag +'/>')
		self.replace ('<'+ tag +'> ', '<'+ tag +' ')
#	self.replace ("'<", "'><")


setattr (File, 'cleanXsl', cleanCode)
setattr (File, 'toHtml', convert)

fileObj.read()
fileObj.cleanXsl()
fileObj.toHtml()
fileObj.title = 'exemple bis'
fileObj.write()



