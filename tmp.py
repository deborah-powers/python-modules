#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from articleHtml import ArticleHtml
from fileHtml import FileHtml
import urllib as ul
from urllib import request as urlRequest
import logger

file = 'b/cv-2021-01/CV deborah powers.html'
html = FileHtml()
html.file = file
html.fromFile()
html.cleanWeb()
html.title = 'tmp'
html.fileFromData()
html.toFile()

links =(
	'https://www.reddit.com/r/FemaleDatingStrategy/comments/dqnjgx/',
)
article = ArticleHtml()
article.path = 'b/fds/'

def getFiles():
	for link in links:
		article.fromWeb (link, 'feminisme')

getFiles()

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
def fillFormTest():
	file = FileHtml()
	file.link = urlE
	file.fromUrlVa (params)
	file.title = 'tmp'
	file.fileFromData()
	file.toFile()

