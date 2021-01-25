#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from fileHtml import FileHtml
import urllib as ul
from urllib import request as urlRequest

urlF = 'https://mantis2.axyus.com/view.php?id=660'
urlD = 'https://mantis2.axyus.com/login_password_page.php'
urlE = 'https://mantis2.axyus.com/login.php'
params ={
	'username': 'deborah.powers',
	'password': 'DePoS2020**'
}

def fillForm (url):
	paramsUrl = ul.parse.urlencode (params).encode ('utf-8')
	myRequest = urlRequest.Request (url, method='POST')
	response = urlRequest.urlopen (myRequest, paramsUrl)
"""
fillForm (urlD)
fillForm (urlE)
"""
file = FileHtml()
file.link = urlE
file.fromUrlVa (params)
file.title = 'tmp'
file.fileFromData()
file.toFile()

