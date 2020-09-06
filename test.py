#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
from fileClass import FileText

help = """pour tester mes classes.
utilisation: l'appeler dans un autre fichier.
fileTest = Test (objetTesté, fichierTesté)
	fichierTesté	le fichier contenant la classe (string)
	objetTesté		une instance de la clase
"""

class TestFunc():
	def __init__ (self, func, res, *args):
		self.function = func
		self.resPredicted = res
		self.resComputed =None
		self.arguments =None
		if args: self.arguments = args
		self.succes =False

	def __str__ (self):
		txt = '____________ fonction %s ____________' % self.function.__name__
		if self.arguments !=None: txt = txt + '\narguments:\t\t' + str (self.arguments)
		txt = txt + '\nrésultat attendu:\t' + str (self.resPredicted)
		if self.resComputed !=None:
			txt = txt + '\nrésultat obtenu:\t' + str (self.resComputed)
			if self.succes: txt = txt + '\nla fonction donne le résultat attendu'
			else: txt = txt + '\nla fonction donne un résultat érroné'
		return txt

	def launch (self):
		if (self.arguments): self.resComputed = self.function (*self.arguments)
		else: self.resComputed = self.function()
		if self.resComputed == self.resPredicted: self.succes = True
		else: self.succes = False
		print (self)


class TestClass():
	def __init__ (self, clazz, *args):
		self.clazz = clazz
		self.object = clazz (*args)
		self.funcs =[]
		for func in dir (clazz):
			if func[:2] != '__': self.funcs.append (func)

	def __str__ (self):
		txt = '____________ class %s ____________' % self.clazz.__name__
		txt = txt +'\nles fonctions: ' + ', '.join (self.funcs)
		txt = txt +'\n'+ str (self.object)
		return txt
"""
	def __init__(self, objTested, fileTested):
		FileText.__init__ (self)
		self.clazz = objTested.__class__.__name__
		self.object = objTested
		self.title = 'test ' + self.clazz
		self.text = 'test de la classe %s, fichier: %s\nliste des fonctions: %s' %( self.clazz, fileTested, ', '.join (self.funcs))
		print (self.text)
"""

def coucou (prenom, nom):
	print ('coucou', prenom, nom)
	return 1

def coucouNoargs():
	print ('coucou toi')
	return 1

tfunc = TestFunc (coucou, 1, 'Deborah', 'Caroussi')
tfunc.resPredicted =2
tfunc.launch()

tclass = TestClass (TestFunc, coucou, 2)
# print (tclass)
tclass.launch()





class Test (FileText):
	def __init__(self, objTested, fileTested):
		FileText.__init__ (self)
		self.clazz = objTested.__class__.__name__
		self.object = objTested
		self.funcs =[]
		for func in dir (objTested.__class__):
			if func[:2] != '__': self.funcs.append (func)
		self.title = 'test ' + self.clazz
		self.text = 'test de la classe %s, fichier: %s\nliste des fonctions: %s' %( self.clazz, fileTested, ', '.join (self.funcs))
		print (self.text)

	def oneFunc (self, funcTest, funcRes=None, messageRes=None):
		message = 'test de '+ funcTest.__name__
		print (message)
		self.text = self.text +'\n'+ message
		if funcRes != None and messageRes:
			message = messageRes % funcRes
			print (message)
			self.text = self.text +': '+ message

	def toFile (self):
		self.shape()
		FileText.toFile (self)

	def testFileText (self):
		self.oneFunc (self.object.count, self.object.count ('test'), '%d occurences du mot "test".')
		self.oneFunc (self.object.find, self.object.find ('test'), '"test" apparaît pour la première fois à la position %d.')
		self.oneFunc (self.object.find, self.object.find ('coucou'), '"coucou" apparaît pour la première fois à la position %d.')
		self.oneFunc (self.object.contain, self.object.contain ('chocolat'), 'le mot "chocolat" est retrouvé dans le texte: %r')
		self.oneFunc (self.object.contain, self.object.contain ('coucou'), 'le mot "coucou" est retrouvé dans le texte: %r')
		self.oneFunc (self.object.replace, self.object.replace ('coucou', 'salut'))
		self.oneFunc (self.object.toFile, self.object.toFile())
		self.oneFunc (self.object.fromFile, self.object.fromFile())
		self.oneFunc (self.object.clean, self.object.clean())
		self.oneFunc (self.object.shape, self.object.shape())
		self.oneFunc (self.object.toFile, self.object.toFile ('a'))


"""
# on appele ce script dans un autre script
if __name__ != '__main__': pass
# le nom du fichier n'a pas ete donne
else: print (help)
"""