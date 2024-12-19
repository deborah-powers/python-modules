#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from datetime import datetime

class File():
	def renameDate_vb (self, addHour=False):
		alpabet = 'abcdefghijklmnopqrstuvwxyz'
		aTraiter = True
		self.fromPath()
		newPath = self.title.lower()
		if newPath[:4] not in 'img_ img- vid_' and newPath[:6] != 'video_':
			l=0
			while l<26:
				if alpabet[l] in newPath:
					aTraiter = False
					l=27
				l+=1
		if aTraiter:
			creation = self.getDateCreation (addHour)
			self.fromPath()
			l=0
			while l<26:
				newPath = self.path.replace ('\t', creation +" "+ alpabet[l])
				if not os.path.exists (newPath):
					self.toPath()
					os.rename (self.path, newPath)
					l=27
				l+=1

	def renameDate_va (self):
		months =( '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
		days =( '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
		if '2024' in self.title and '2024-' not in self.title and '2024 ' not in self.title:
			self.fromPath()
			newPath = self.title.lower()
			newPath = newPath.replace ('img_20', '20')
			newPath = newPath.replace ('img-20', '20')
			newPath = newPath.replace ('vid_20', '20')
			newPath = newPath.replace ('video_20', '20')
			newPath = newPath.replace ('20230', '2023-0')
			newPath = newPath.replace ('20231', '2023-1')
			newPath = newPath.replace ('20240', '2024-0')
			newPath = newPath.replace ('20241', '2024-1')
			for m in months: newPath = newPath.replace ('-'+m, '-'+m+'-')
			for d in days: newPath = newPath.replace ('-'+d, '-'+d+' ')
			while '--' in newPath: newPath = newPath.replace ('--', '-')
			newPath = newPath.replace ('_', ' ')
			newPath = newPath.replace ('- ', ' ')
			newPath = newPath.replace (' -', '-')
			if '2024-' in newPath and '-2024' not in newPath and ' 2024' not in newPath and newPath[:5] != '2024-':
				# images transformées avec l'appli photo resizer
				d= newPath.find (" ")
				queue = newPath[d+1:]
				newPath = newPath[:d]
				d= newPath.find ('2024-')
				hour = newPath[d+5:d+7]
				newPath = newPath[:d]
				if len (newPath) ==2: newPath = months [int (newPath[0])] +'-'+ days [int (newPath[1])]
				elif len (newPath) ==4: newPath = months [int (newPath[0:2])] +'-'+ days [int (newPath[2:4])]
				elif len (newPath) ==3 and newPath[0] == '1': newPath = months [int (newPath[0:2])] +'-'+ days [int (newPath[2])]
				elif len (newPath) ==3: newPath = months [int (newPath[0])] +'-'+ days [int (newPath[1:3])]
				newPath = '2024-' + newPath +'-'+ hour +' '+ queue
			elif '2024-' in newPath or '2024 ' in newPath: pass
			else:
				newPath = newPath.replace ('2024', '')
				newPath = self.getDateCreation() +' '+ newPath
				self.fromPath()
			while '  ' in newPath: newPath = newPath.replace ('  ', ' ')
			newPath = self.path.replace ('\t', newPath)
			self.toPath()
			os.rename (self.path, newPath)

	def getDateCreation_va (self, addHour=False):
		# self.path est bien au bon format
		self.toPath()
		dateCreation = os.path.getctime (self.path)
		dateModification = os.path.getmtime (self.path)
		dateA = os.path.getatime (self.path)
		strCreation = datetime.fromtimestamp (dateCreation).strftime (dateFormatDay)
		strM = datetime.fromtimestamp (dateModification).strftime (dateFormatDay)
		strA = datetime.fromtimestamp (dateA).strftime (dateFormatDay)
		log.logLst (self.title, strCreation, strM, strA)
		if dateModification < dateCreation:
			if addHour: strCreation = datetime.fromtimestamp (dateModification).strftime (dateFormatHour)
			else: strCreation = datetime.fromtimestamp (dateModification).strftime (dateFormatDay)
		elif addHour: strCreation = datetime.fromtimestamp (dateCreation).strftime (dateFormatHour)
		else: strCreation = datetime.fromtimestamp (dateCreation).strftime (dateFormatDay)
		return strCreation