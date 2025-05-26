#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
from fileLocal import shortcut
from fileCls import File
from htmlCls import Html

templateStyle ="""div {
	float: right;
	clear: right;
}
br {
	height: 4em;
	line-height: 4em;
}
p { margin: 1em 0; }"""

templateLetter ="""<div><p>Deborah Powers</p><p>06 22 39 55 25</p><p>deborah.powers89@gmail.com</p><p>$infosMoi</p></div>
<p>$infosDestinataire</p>
<br/>
<p>Objet: $objet</p>
<br/>
<p>Bonjour,</p>
$text
<br/>
<p>Merci,</p><p>Deborah Powers</p>"""

def toParagraph (text):
	while '\n\n' in text: text = text.replace ('\n\n', '\n')
	text = text.strip()
	text = text.replace ('\n', '</p><p>')
#	text = '<p>' + text + '</p>'
	return text

class Letter (Html):
	def __init__ (self):
		Html.__init__(self)
		self.infosDestinataire =""
		self.infosMoi =""
		self.objet =""
		self.meta['style'] = templateStyle
		self.path = 'b/\t.html'

	def read (self, path):
		path = shortcut (path)
		fileTxt = File (path)
		fileTxt.read()
		self.title = fileTxt.title
		d= fileTxt.text.find ('\n')
		self.objet = fileTxt.text[:d]
		fileTxt.text = fileTxt.text[d+1:]
		textList = fileTxt.text.split ('\n==\n')
		self.text = textList[0]
		self.infosDestinataire = textList[1]
		self.infosMoi = textList[2]

	def write (self):
		self.infosMoi = toParagraph (self.infosMoi)
		self.infosDestinataire = toParagraph (self.infosDestinataire)
		self.text = toParagraph (self.text)
		self.text = '<p>' + self.text + '</p>'
		self.text = templateLetter.replace ('$text', self.text)
		self.text = self.text.replace ('$objet', self.objet)
		self.text = self.text.replace ('$infosMoi', self.infosMoi)
		self.text = self.text.replace ('$infosDestinataire', self.infosDestinataire)
		Html.write (self)


pathTxt = 'b/lettre resilliation ah.txt'
letter = Letter()
letter.read (pathTxt)
letter.write()
