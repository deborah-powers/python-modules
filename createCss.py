#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileCls import File

nameCss = 'h/bol.css'
fileCss = File (nameCss)

cssTemplate = 'bol >*:nth-child(%d){ transform: rotateY(%0.2fdeg) rotateX(%0.2fdeg) translateZ(var(--width-half)); }\n'
nb=2
rotateX =( 11.25, 33.75, 56.25, 78.75, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75, 303.75, 326.25, 348.75 )
rangeY =( 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 )
rotateX =(350, 330, 310, 290, 270, 250, 230, 210, 190)
rangeX = range (len (rotateX))

for y in rangeY:
	for x in rangeX:
		if x==4 and y%3 !=0: continue
		elif y%2 ==1 and (x==3 or x==5): continue
		"""
		if x==4 and y%2 ==1: cssLine = cssTemplate % (nb, y*7.5, 101.25)
		elif x==10 and y%2 ==1: cssLine = cssTemplate % (nb, y*7.5, 281.25)
		else: cssLine = cssTemplate % (nb, y*7.5, rotateX[x])
		if x==3 and y%2 ==0:
			cssLine = cssTemplate % (nb, y*7.5, 281.5)
		else: cssLine = cssTemplate % (nb, y*7.5, rotateX[x])
		"""
		cssLine = cssTemplate % (nb, y*7.5, rotateX[x])
		fileCss.text = fileCss.text + cssLine
		nb+=1
fileCss.replace ('rotateY(0.00deg) ')
fileCss.replace ('0deg)', 'deg)')
fileCss.replace ('.0deg)', 'deg)')
fileCss.write()
