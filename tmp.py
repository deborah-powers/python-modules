#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires
from listClass import ListPerso
from fileList import FileList
from fileClass import FilePerso
from listFile import TableFile, ListFile

directory = 'C:\\Users\\deborah.powers\\Desktop\\mantis 30211\\%s-%s.log'
files =( 'bth-11-16', 'bth-11-18', 'edi-09-04', 'edi-09-11', 'ord-09', 'ord-10')
tmpFile = FilePerso()

dateStart = '2020-11-24'
dateEnd = '2020-11-25'

def findHour (self, hour):
	hourFound = False
	hourText = '%s %s:' %(dateStart, hour)
	if self.contain (hourText):
		d= self.index (hourText)
		d= self.text[:d].rfind ('\n')
		if d<0: d=0
		self.text = self.text[d:]
		hourFound = True
	return hourFound

def findDate (self):
	# repérer le jour
	if self.contain (dateStart):
		d= self.index (dateStart)
		d= self.text[:d].rfind ('\n')
		if d<0: d=0
		self.text = self.text[d:]
		if self.contain (dateEnd):
			d= self.index (dateEnd)
			d= self.text[:d].rfind ('\n')
			if d>0: self.text = self.text[:d]
		# repérer l'heure
		hourFound = self.findHour ('07')
		if not hourFound: hourFound = self.findHour ('08')
		if not hourFound: hourFound = self.findHour ('09')
		if not hourFound: hourFound = self.findHour ('10')
		if not hourFound: hourFound = self.findHour ('11')
		if self.contain ('[ERROR]'): print (self.countWord ('[ERROR]'), 'erreurs dans', self.title)
		else: print ("pas d'erreur dans", self.title, self.length(), self.text[:200])
		self.clean()
		self.replace ('\n<label>Voir</label>\n</xmlResult>]) sur la Queue queue://ord-com-out .....')
		self.toFile()
	else: print (self.title, 'ne contient pas la date recherchée')

def extractErrors (self):
	errorNb =0
	tmpList = ListFile()
	tmpList.copyFile (self)
	tmpList.fromFile()
	tmpRang = tmpList.range()
	tmpRang.reverse()
	trash =0
	for i in tmpRang:
		# if '[INFO]' in tmpList[i]: trash = tmpList.pop (i)
		elif '\tat ' in tmpList[i] and '\tat fr.asp.synergie' not in tmpList[i]: trash = tmpList.pop (i)
	i=0
	tmpLen = tmpList.length()
	while i< tmpLen:
		if '\tat fr.asp.synergie' not in tmpList[i]:
			errorNb =0
			i+=1
		elif errorNb <5:
			errorNb +=1
			i+=1
		else:
			trash = tmpList.pop (i)
			tmpLen -=1
	tmpList.toFile()

setattr (FilePerso, 'findDate', findDate)
setattr (FilePerso, 'findHour', findHour)
setattr (FilePerso, 'extractErrors', extractErrors)

def reviewLogs (funcRes, trace=False):
	directory = 'C:\\Users\\deborah.powers\\Desktop\\mantis 30211\\%s-%s.log'
	# files =( 'bth-11-16', 'bth-11-18', 'edi-09-04', 'edi-09-11', 'ord-09', 'ord-10')
	files =( 'bth-11-16', 'bth-11-18', 'edi-09-04')
	tmpFile = FilePerso()
	for name in files:
		tmpName = directory %( name, 'log')
		tmpFile.file = tmpName
		tmpFile.dataFromFile()
		tmpFile.fromFile()
		funcRes (tmpFile)
	if trace:
		for name in files:
			tmpName = directory %( name, 'tra')
			tmpFile.file = tmpName
			tmpFile.dataFromFile()
			tmpFile.fromFile()
			funcRes (tmpFile)

reviewLogs (findDate)
reviewLogs (extractErrors)





def getCol():
	fileCsv = TableFile ('\n','\t', fileCsvName)
	fileCsv.fromFile()
	listNames = fileCsv.getCol (2)
	listNames.delDuplicates()
	listNames.sort()
	print (listNames)

def lower():
	fileCsv = FilePerso (fileCsvName)
	fileCsv.fromFile()
	fileCsv.text = fileCsv.text.lower()
	print (fileCsv.text)
	fileCsv.toFile()

def compare():
	fileNameA = 'b/html\\utils\\color.css'
	fileNameB = 'b/html\\library-perso\\color.css'
	fpA = FilePerso (fileNameA)
	fpB = FilePerso (fileNameB)
	fpA.compare (fpB, 'lsort')

jsDomVariables =[ 'addEventListener', 'alert', 'atob', 'blur', 'btoa', 'cancelAnimationFrame', 'cancelIdleCallback', 'captureEvents', 'chrome', 'clearInterval', 'clearTimeout', 'clientInformation', 'close', 'closed', 'confirm', 'createImageBitmap', 'crypto', 'customElements', 'defaultStatus', 'defaultstatus', 'devicePixelRatio', 'dispatchEvent', 'document', 'external', 'fetch', 'find', 'focus', 'frameElement', 'frames', 'getComputedStyle', 'getSelection', 'history', 'indexedDB', 'innerHeight', 'innerWidth', 'isSecureContext', 'length', 'localStorage', 'location', 'locationbar', 'matchMedia', 'menubar', 'moveBy', 'moveTo', 'name', 'navigator', 'onabort', 'onafterprint', 'onanimationend', 'onanimationiteration', 'onanimationstart', 'onappinstalled', 'onauxclick', 'onbeforeinstallprompt', 'onbeforeprint', 'onbeforeunload', 'onblur', 'oncancel', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'onclose', 'oncontextmenu', 'oncuechange', 'ondblclick', 'ondevicemotion', 'ondeviceorientation', 'ondeviceorientationabsolute', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'ongotpointercapture', 'onhashchange', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onlanguagechange', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onlostpointercapture', 'onmessage', 'onmessageerror', 'onmousedown', 'onmouseenter', 'onmouseleave', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpause', 'onplay', 'onplaying', 'onpointercancel', 'onpointerdown', 'onpointerenter', 'onpointerleave', 'onpointermove', 'onpointerout', 'onpointerover', 'onpointerup', 'onpopstate', 'onprogress', 'onratechange', 'onrejectionhandled', 'onreset', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onseeking', 'onselect', 'onstalled', 'onstorage', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'ontransitionend', 'onunhandledrejection', 'onunload', 'onvolumechange', 'onwaiting', 'onwebkitanimationend', 'onwebkitanimationiteration', 'onwebkitanimationstart', 'onwebkittransitionend', 'onwheel', 'open', 'openDatabase', 'opener', 'origin', 'outerHeight', 'outerWidth', 'pageXOffset', 'pageYOffset', 'parent', 'performance', 'personalbar', 'postMessage', 'print', 'prompt', 'releaseEvents', 'removeEventListener', 'requestAnimationFrame', 'requestIdleCallback', 'resizeBy', 'resizeTo', 'screen', 'screenLeft', 'screenTop', 'screenX', 'screenY', 'scroll', 'scrollBy', 'scrollTo', 'scrollX', 'scrollY', 'scrollbars', 'self', 'sessionStorage', 'setInterval', 'setTimeout', 'speechSynthesis', 'status', 'statusbar', 'stop', 'styleMedia', 'toolbar', 'top', 'visualViewport', 'webkitCancelAnimationFrame', 'webkitRequestAnimationFrame', 'webkitRequestFileSystem', 'webkitResolveLocalFileSystemURL', 'webkitStorageInfo', 'window']

def changeCss():
	fllst = FileList ('b/localhost/site-dp/')
	fllst.get ('.html')
	fllst.replace ('library-js/debby-play/debbyPlay.css', 'library-css/debbyPlay.css')
	fllst.replace ('library-js/debby-play/debbyPlay.js', 'library-js/debbyPlay.js')

