#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

class ListPerso (list):
	def range (self, start=0, end=0, step=1):
		# end peut valoir -1
		lenList = self.__len__()
		if lenList ==0 or step ==0: return []
		if step <0:
			tmp = start
			start = end
			end = tmp
			step *=-1
		while start <0: start += lenList
		if start > lenList: start = lenList
		while end <=0: end += lenList
		if end > lenList: end = lenList
		rangeList = None
		if start > end: rangeList = reversed (range (end, start, step))
		else: rangeList = range (start, end, step)
		return rangeList



	def length (self):
		return self.__len__()

	def __str__(self):
		listStr =""
		for item in self: listStr = listStr = str (item) +'\n'
		return listStr

