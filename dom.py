#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""
je veux recréer le dom d'un document,
pour retrouver l'emplacement d'un élément, extraire sa valeur, la modifier...
"""

text = """<div class='a' id='body' style='b' value='c'>
	d
	<div id='divA'>
		<p id='pA'>e</p>
		<ul id='ul'>
			<li id='li'>f</li>
			<li>g</li>
			<li>h</li>
		</ul>
	</div>
	<div id='divB'>
		<p id='pB'>i</p>
		<input id='input' value='j'/>
	</div>
	k
</div>"""
text2 = """
<div id='body'>
	d
	<div id='divA'>
		<p id='pA'>e</p>
	</div>
	k
</div>

<div id='body'>
	d
	<div id='divA'>
		<p id='pA'>
			<ul id='ul'>
				<li id='li'>f</li>
				<//li><li>hi></li</li>g</li>
			</ul>
			e
		</p>
		<div id='divB'>
		<p id='pB'>
			<input id='input'/>
			i
		</p>
		</div>
	</div>
	k
</div>
"""

closedTags =( 'br', 'hr', 'img', 'input')

def clean (text):
	text = text.replace ('\r', "")
	text = text.replace ('\n', "")
	text = text.replace ('\t', "")
	while '  ' in text: text = text.replace ('  ', ' ')
	text = text.replace ('> <', '><')
	text = text.strip()
	return text

class Node():
	def __init__ (self, tag=""):
		self.tag = tag
		self.id =""
		self.clazz =""
		self.style =""
		self.attributes ={}
		self.content =[]

	def fill (self, tag, content=[], id="", clazz="", attributes={}, style=""):
			self.tag = tag
			self.id = id
			self.clazz = clazz
			self.style = style
			self.content = content
			self.attributes = attributes

	def show (self):
		print ('%s\t%s\t' %( self.tag, self.id), len (self.content))
		for subNode in self.content: print ('\t', subNode.tag, subNode.id)

	def __str__ (self):
		if not self.tag: return ""
		elif self.tag == 'text': return self.id
		text = '<' + self.tag
		if self.id: text = text +" id='" + self.id +"'"
		"""
		if self.clazz: text = text +" class='" + self.clazz +"'"
		if self.style: text = text +" style='" + self.style +"'"
		attributeList = self.attributes.keys()
		for attr in attributeList:
			text = text +' '+ attr +"='"+ self.attributes[attr] +"'"
		"""
		if self.tag in closedTags: text = text + '/>'
		else:
			text = text +'>'
			for node in self.content:
				if node.tag == 'text': text = text + node.id
				else: text = text + node.__str__()
			text = text + '</' + self.tag +'>'
		return text

	def drapeau (self, text, letter):
		print (letter)
		self.show()
	#	print (text)

	def parse (self, text):
		drapeau = False
		# trouver les limites du noeud
		if '<' not in text:
			self.tag = 'text'
			self.id = text
			return ""
		# récupérer le tag et les attributs
		text = text[1:]
		f= text.find ('>')
		if ' ' in text[:f]:
			attributeList = text[:f].split (' ')
			self.tag = attributeList.pop(0)
			for attr in attributeList:
				attrList = attr.split ('=')
				if attrList[0] == 'id': self.id = attrList[1][1:-1]
				"""
				elif attrList[0] == 'class': self.clazz = attrList[1][1:-1]
				elif attrList[0] == 'style': self.style = attrList[1][1:-1]
				else: self.attributes [attrList[0]] = attrList[1][1:-1]
				"""
		else: self.tag = text[:f]
		# récupérer le contenu
		if text[0] =='/': return ""
		text = text[f+1:]
		# récupérer le contenu
		while text[:f].count ('</'+ self.tag) != text[:f].count ('<'+ self.tag): f= text.find ('</'+ self.tag, f+1)
		f= text.find ('</'+ self.tag, f)
		textNext = text [3+f+ len (self.tag):]
		text = text[:f]
		while text:
			if text[0] !='<':
				fin = Node ('text')
				f= text.find ('<')
				fin.id = text[:f]
				self.content.append (fin)
				text = text[f:]
			fin = Node ('text')
			if text[-1] !='>':
				f= text.rfind ('>') +1
				fin.id = text[f:]
			#	self.content.append (fin)
				text = text[:f]
			subNode = Node ('coucou')
			text = subNode.parse (text)
			self.content.append (subNode)
			subNodeNext = Node ('coucou')
			subNodeNext.parse (textNext)
			self.content.append (subNodeNext)
			self.content.append (fin)
		return text



text = clean (text)
body = Node()
body.parse (text)
print ('\nend\n', body)



"""
	def parseOne (self, text):
		subNode = Node()
		subNode.tag = 'text'
		if '<' not in text:
			subNode.id = text
			self.content.append (subNode)
			return ""
		else:
			if text[0] !='<':
				d= text.find ('<')
				subNode.id = text[:d]
				self.content.append (subNode)
				text = text[d:]
			if text[-1] !='>':
				endNode = Node()
				endNode.tag = 'text'
				d= text.rfind ('>') +1
				endNode.id = text[d:]
			#	self.content.append (endNode)
				text = text[:d]
			return self.parse (text)

	def parseOld (self, text):
		if '<' not in text:
			subNode = Node()
			subNode.tag = 'text'
			subNode.id = text
			self.content.append (subNode)
			return ""
		if self.tag in closedTags:
			f= text.find ('/>') +2
			textLast = textLast + text[f:]
		else:
		#	print (self.tag, self.id, text)
			text = text[f+1:]
			f= text.find ('</'+ self.tag)
			while text[:f].count ('</'+ self.tag) != text[:f].count ('<'+ self.tag):
				f= text.find ('</'+ self.tag, f+1)
			print ('f', self.tag, self.id, text[:f])
			d=3+f+ len (self.tag)
			textLast = textLast + text[:d]
			text = text[:f]
			if '<' not in text:
				print ('coucou', self.tag, self.id)
				subNode = Node()
				subNode.tag = 'text'
				subNode.id = text
				self.content.append (subNode)
			else:
				while text: text = self.parseOne (text)
		return textLast

def old():
			d=0
			nb=1+ text.count ('<'+ self.tag)
			while nb>0:
				d= text.find ('</'+ self.tag, d+1)
				nb-=1
			f=3+d+ len (self.tag)
			textLast = textLast + text[f:]
			text = text[:d]
			print (self.tag, self.id, text)
			subNode = Node()
			if '<' not in text:
				subNode.tag = 'text'
				subNode.id = text
				self.content.append (subNode)
			else:
				while text and '<' in text:
					text = subNode.parse (text)
					if text:
						subNodeA = Node()
						subNodeA.tag = 'text'
						if '§' not in text:
							subNodeA.id = text
							self.content.append (subNode)
							self.content.append (subNodeA)
						elif text[-1] =='§':
							subNodeA.id = text[:-1]
							self.content.append (subNodeA)
							self.content.append (subNode)
						else:
							d= text.find ('§')
							subNodeA.id = text[:d]
							self.content.append (subNodeA)
							self.content.append (subNode)
							subNodeB = Node()
							subNodeB.tag = 'text'
							subNodeB.id = text[d+1:]
							self.content.append (subNodeB)
					else: self.content.append (subNode)
	#	self.show()
		return textLast
"""


