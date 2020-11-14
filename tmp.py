#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires
from listClass import ListPerso
from fileList import FileList
from fileClass import FilePerso
from listFile import TableFile

fileCsvName = '/home/lenovo/Bureau/divers/perso/depenses.tsv'

def getCol():
	fileCsv = TableFile ('\n','\t', fileCsvName)
	fileCsv.fromFile()
	listNames = fileCsv.getCol (2)
	listNames.delDuplicates()
	listNames.sort()
	print (listNames)

getCol()

def lower():
	fileCsv = FilePerso (fileCsvName)
	fileCsv.fromFile()
	fileCsv.text = fileCsv.text.lower()
	print (fileCsv.text)
	fileCsv.toFile()

jsDomVariables =[ 'addEventListener', 'alert', 'atob', 'blur', 'btoa', 'cancelAnimationFrame', 'cancelIdleCallback', 'captureEvents', 'chrome', 'clearInterval', 'clearTimeout', 'clientInformation', 'close', 'closed', 'confirm', 'createImageBitmap', 'crypto', 'customElements', 'defaultStatus', 'defaultstatus', 'devicePixelRatio', 'dispatchEvent', 'document', 'external', 'fetch', 'find', 'focus', 'frameElement', 'frames', 'getComputedStyle', 'getSelection', 'history', 'indexedDB', 'innerHeight', 'innerWidth', 'isSecureContext', 'length', 'localStorage', 'location', 'locationbar', 'matchMedia', 'menubar', 'moveBy', 'moveTo', 'name', 'navigator', 'onabort', 'onafterprint', 'onanimationend', 'onanimationiteration', 'onanimationstart', 'onappinstalled', 'onauxclick', 'onbeforeinstallprompt', 'onbeforeprint', 'onbeforeunload', 'onblur', 'oncancel', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'onclose', 'oncontextmenu', 'oncuechange', 'ondblclick', 'ondevicemotion', 'ondeviceorientation', 'ondeviceorientationabsolute', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'ongotpointercapture', 'onhashchange', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onlanguagechange', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onlostpointercapture', 'onmessage', 'onmessageerror', 'onmousedown', 'onmouseenter', 'onmouseleave', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpause', 'onplay', 'onplaying', 'onpointercancel', 'onpointerdown', 'onpointerenter', 'onpointerleave', 'onpointermove', 'onpointerout', 'onpointerover', 'onpointerup', 'onpopstate', 'onprogress', 'onratechange', 'onrejectionhandled', 'onreset', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onseeking', 'onselect', 'onstalled', 'onstorage', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'ontransitionend', 'onunhandledrejection', 'onunload', 'onvolumechange', 'onwaiting', 'onwebkitanimationend', 'onwebkitanimationiteration', 'onwebkitanimationstart', 'onwebkittransitionend', 'onwheel', 'open', 'openDatabase', 'opener', 'origin', 'outerHeight', 'outerWidth', 'pageXOffset', 'pageYOffset', 'parent', 'performance', 'personalbar', 'postMessage', 'print', 'prompt', 'releaseEvents', 'removeEventListener', 'requestAnimationFrame', 'requestIdleCallback', 'resizeBy', 'resizeTo', 'screen', 'screenLeft', 'screenTop', 'screenX', 'screenY', 'scroll', 'scrollBy', 'scrollTo', 'scrollX', 'scrollY', 'scrollbars', 'self', 'sessionStorage', 'setInterval', 'setTimeout', 'speechSynthesis', 'status', 'statusbar', 'stop', 'styleMedia', 'toolbar', 'top', 'visualViewport', 'webkitCancelAnimationFrame', 'webkitRequestAnimationFrame', 'webkitRequestFileSystem', 'webkitResolveLocalFileSystemURL', 'webkitStorageInfo', 'window']
def comparaison():
	fileNameA = 'b/python/textClass.py'
	fileNameB = 'b/python b/textClass.py'
	fpA = FilePerso (fileNameA)
	fpB = FilePerso (fileNameB)
	fpA.compare (fpB, 'lsort')

def changeCss():
	fllst = FileList ('b/localhost/site-dp/')
	fllst.get ('.html')
	fllst.replace ('library-js/debby-play/debbyPlay.css', 'library-css/debbyPlay.css')
	fllst.replace ('library-js/debby-play/debbyPlay.js', 'library-js/debbyPlay.js')

