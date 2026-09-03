#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc
from textFct import cleanBasic
from fileCls import File, Article
from htmlCls import Html
from eventCls import DatePerso
import loggerFct as log

# le fichier
fileSrc = 'b/bus 2026-08 244 horaire.pdf'
# le html avec l'horaire complet
horaireCompletNom = 'b/bus $date $bus horaire complet.html'

class HorairePage():
	def __init__ (self):
		self.direction =""
		self.periode =""
		self.arrets ={}

	def melt (self, nvHoraire):
		if self.direction == nvHoraire.direction and self.periode == nvHoraire.periode:
			arrets = self.arrets.keys()
			arretsNv = nvHoraire.arrets.keys()
			for arret in arrets: self.arrets[arret].extend (nvHoraire.arrets[arret])
			return True
		else: return False

	def read (self, pdfText):
		pdfText = cleanBasic (pdfText)
		# infos de base
		d=1+ pdfText.find ('\n')
		pdfText = pdfText[d:]
		d= pdfText.find ('\n')
		self.direction = pdfText[:d]
		if 'Horaires valables' in self.direction:
			d= self.direction.find ('Horaires valables')
			self.direction = self.direction[:d-1]
		d= pdfText.find ('\n')
		pdfText = pdfText[d+1:]
		d= pdfText.find ('\n')
		self.periode = pdfText[:d]
		pdfText = pdfText[d+1:]
		d= pdfText.find ('Bon à sav') -1
		pdfText = pdfText[:d]
		# tri par arrêt, corriger les heures
		while '| |' in pdfText: pdfText = pdfText.replace ('| |','|')
		pdfText = pdfText.replace ('|','00:00')
		numbers = '0123456789'
		for nb in numbers: pdfText = pdfText.replace (" "+ str(nb) +':', " 0"+ str(nb) +':')
		for nb in numbers: pdfText = pdfText.replace (" "+ str(nb) +" ", " 0"+ str(nb) +" ")
		for nb in numbers[6:]: pdfText = pdfText.replace (" "+ str(nb), " 0"+ str(nb))
		pdfText = pdfText.replace (" 7", " 07")
		pdfText = pdfText.replace (" 8", " 08")
		pdfText = pdfText.replace (" 9", " 09")
		pdfText = pdfText.replace (": ", ':')
		pdfText = pdfText.strip()
		# tri par arrêt, identifier les noms sur deux lignes
		pdfList = pdfText.split ('\n')
		pdfRange = reversed (range (len (pdfList)))
		for p in pdfRange:
			if ':' not in pdfList[p] and ':' not in pdfList[p-1]:
				bout = pdfList.pop (p)
				pdfList[p-1] = pdfList[p-1] +" "+ bout
			elif ':' in pdfList[p] and ':' not in pdfList[p-1]:
				d= pdfList[p].find (':')
				if d==2:
					bout = pdfList.pop (p)
					pdfList[p-1] = pdfList[p-1] +" "+ bout
		pdfRange = reversed (range (len (pdfList)))
		for p in pdfRange:
			if ':' not in pdfList[p] and ':' in pdfList[p-1]:
				bout = pdfList.pop (p)
				d= pdfList[p-1].find (':') -3
				pdfList[p-1] = pdfList[p-1][:d] +" "+ bout + pdfList[p-1][d:]
		# tri par arrêt, identifier les arrêts
		for arret in pdfList:
			d= arret.find (':') -3
			self.arrets [arret[:d]] = arret[d+1:].split (" ")

def createFullHour (filePdf):
	horaireCompletNom = horaireCompletNom.replace ('$bus', filePdf.meta['bus'])
	horaireCompletNom = horaireCompletNom.replace ('$date', filePdf.meta['date'])
	horaireCompletFich = Html (horaireCompletNom)
	horaireCompletFich.author = filePdf.author
	horaireCompletFich.subject = filePdf.subject

def extractPdfData():
	filePdf = Article (fileSrc)
	filePdf.fromPdf (False)
	# les métadonnées
	filePdf.subject = 'transport, bus'
	filePdf.author = 'ratp'
	today = DatePerso (2026, 5, 12)
	today = today.today()
	filePdf.meta['date'] = today.toStrDay()
	filePdf.meta['bus'] = filePdf.title[12:15]
	# les données
	filePdf.text = '\n'+ filePdf.text
	filePdf.replace ('\n\n', '\n')
	pages = filePdf.text.split ("\n== page ")
	trash = pages.pop(0)

	horairePages =[]
	nvHoraire = HorairePage()
	nvHoraire.read (pages[0])
	horairePages.append (nvHoraire)
	trash = pages.pop(0)
	for page in pages:
		nvHoraire = HorairePage()
		nvHoraire.read (page)
		melted = horairePages[-1].melt (nvHoraire)
		if not melted: horairePages.append (nvHoraire)

	filePdf.text = "horaire du bus "+ filePdf.meta['bus'] +". le "+ filePdf.meta['date'] +'\n'
	for horaire in horairePages:
		filePdf.text = filePdf.text + "== vers "+ horaire.direction +". le "+ horaire.periode +'\n'
		arrets = horaire.arrets.keys()
		passages =""
		for arret in arrets:
			passages = " ".join (horaire.arrets[arret])
			filePdf.text = filePdf.text +"** "+ arret +'\n'+ passages +'\n'
	while '00:00 00:00' in filePdf.text: filePdf.replace ('00:00 00:00', '00:00')
	filePdf.write()

extractPdfData()

"""
for page in horairePages:
	log.log (page.direction, page.periode)
"""
