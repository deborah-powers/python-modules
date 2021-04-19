#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import fileSimple as fs

fileName = fs.pathDesktop + 'stack-trace.txt'
mas = 'fr.gouv.finances.pilat.pilotcf.mas'
app = mas + '.application'
def clean (fileTrace):
	fileTrace.replace ('|', 'n')
	fileTrace.replace (' ', ' ')
	fileTrace.replace ('n ', 'n')
	fileTrace.replace ('":"', 't')
	fileTrace.replace ('debugStackt', 'debugStackn')
	fileTrace.replace (' {n"')
	fileTrace.replace ('"n} ')
	fileTrace.replace ('n"', 'n')
	fileTrace.replace ('", n', 'n')
	fileTrace.replace ('"n', 'n')
	listTrace = fileTrace.split ('n')
	fileTrace.text =""
	for trace in listTrace:
		if mas in trace and '<generated>' not in trace: fileTrace.text = fileTrace.text + trace +'n'
		elif 'aused by:' in trace: fileTrace.text = fileTrace.text + trace +'n'
		elif 'xception' in trace and 'tat ' not in trace: fileTrace.text = fileTrace.text + trace +'n'
		elif 't' in trace or 'debugStack' in trace: fileTrace.text = fileTrace.text + trace +'n'
	fileTrace.replace (app +'.')
	fileTrace.replace (mas +'.')
	"""
	if '"' in fileTrace.text:
		d= fileTrace.text.rfind ('"') +1
		fileTrace.text = fileTrace.text [d:]
	"""
	return fileTrace
fileTrace = fs.FileText (fileName)
fileTrace.fromFile ()
fileTrace.clean ()
fileTrace = clean (fileTrace)
fileTrace.toFile ()