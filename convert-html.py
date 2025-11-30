#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import pypandoc
from fileCls import File

fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\rgaa-certif\\rgaa diaporama.html'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\rgaa présentation conv.pptx'

fileSrcEpsiloon = 'C:\\Users\\LENOVO\\Desktop\\magasine epsiloon 54.pdf'
fileSrc = 'C:\\Users\\LENOVO\\Desktop\\okilele tapuscrit.pdf'
fileDst = 'C:\\Users\\LENOVO\\Desktop\\okilele tapuscrit.html'

fileTxt = File (fileSrc)
fileTxt.fromPdf()

def pdfToHtmlWex():
	import subprocess
	subprocess.call ('pdf2htmlEX '+ fileSrc, shell=True)

def pdfToHtmlWspirePdf():
	"""
	from spire.filePdf.common import *
	from spire.pdf import *
	"""
	doc = PdfDocument()
	doc.LoadFromFile(fileSrc)
	# Set the conversion options to 
	convertOptions = doc.ConvertOptions
	# Specify convert options
	convertOptions.SetPdfToHtmlOptions (True, True, 1, False)
	doc.SaveToFile(fileDst, FileFormat.HTML)
	doc.Dispose()
	"""
convertOptions.SetPdfToHtmlOptions
	useEmbeddedSvg(boolean) : Specifies whether to convert the PDF to an SVG image file and embed it in the HTML code.
	useEmbededImg(boolean): Specifies whether to embed image data in the HTML file. This option is only effective when useEmbeddedSvg is set to false.
	maxPageOneFile(boolean): Specifies the maximum number of pages in one HTML file. This option is only effective when useEmbeddedSvg is set to false.
	useHighQualityEmbeddedSvg(boolean): Specifies whether to use high-quality SVG image embedding in the HTML. This option is only effective when useEmbeddedSvg is set to true.
	"""

def pdfToTextWcodecs():
	import codecs
	textBrut = open (pdfPath, 'rb')
	tmpByte = textBrut.read()
	encodingList = ('ISO-8859-1', 'ISO8859-1')
	text =""
	for encoding in encodingList:
		try:
			text = codecs.decode (tmpByte, encoding='ISO8859-1')
			text = text.encode('utf-8', errors='ignore')
		except UnicodeDecodeError: pass
		else: break
	if not text:
		for encoding in encodingList:
			try:
				text = codecs.decode (tmpByte, encoding=encoding, errors='ignore')
				text = text.encode('utf-8', errors='ignore')
			except UnicodeDecodeError: pass
			else: break
	textBrut.close()
	print (text[:200])

"""
output = pypandoc.convert_file (fileSrc, 'pptx', outputfile=fileDst)
output = pypandoc.convert_file (fileSrc, 'plain', outputfile=fileDst)
fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\bdc.pdf'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\fichier.html'
output = pypandoc.convert_file (fileSrc, 'html', outputfile=fileDst)
fileSrc = 'C:\\Users\\deborah.powers\\Desktop\\Portail Outils de gestion de projet avec ANCT.odt'
fileDst = 'C:\\Users\\deborah.powers\\Desktop\\gestion de projet.html'
output = pypandoc.convert_file (fileSrc, 'html', outputfile=fileDst)
"""