#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

toDeleteLines =[ 'at java.base/', 'at jdk.', 'at org.', 'at io.', 'at com.', 'at jakarta.', ' INFO ', ' DEBUG ', '.war//org.' ]
toDeleteLen = len (toDeleteLines)
toErasePattern = [ 'fr.gouv.dila.psl.']

errorName = 'b/error-log.txt'
errorFile = File (errorName)
errorFile.read()

errorList = errorFile.text.split ('\n');
errorRange = reversed (range (0, len (errorList)))
for e in errorRange:
	l=0
	while l< toDeleteLen:
		if toDeleteLines[l] in errorList[e]:
			trash = errorList.pop (e)
			l= toDeleteLen
		l+=1

errorFile.text = '\n'.join (errorList)

for eraPattern in toErasePattern: errorFile.replace (eraPattern)
errorFile.write()