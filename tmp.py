#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires
from listClass import ListPerso
from fileList import FileList, FileTable
from fileClass import FilePerso
from listFile import ListFile

directory = 'C:\\Users\\deborah.powers\\Desktop\\mantis 30211\\%s-%s.log'
files =( 'bth-11-16', 'bth-11-18', 'edi-09-04', 'edi-09-11', 'ord-09', 'ord-10')
tmpFile = FileLog()


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

