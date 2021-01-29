#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from articleHtml import ArticleHtml
from fileHtml import FileHtml
import urllib as ul
from urllib import request as urlRequest

file = 'b/cv-2021-01/CV deborah powers.html'
html = FileHtml()
html.file = file
html.fromFile()
html.cleanWeb()
html.title = 'tmp'
html.fileFromData()
html.toFile()

links =(
	'https://www.therealfemaledatingstrategy.com/post/fucking-ain-t-fair-act-accordingly',
	'https://www.therealfemaledatingstrategy.com/post/why-are-one-night-stands-being-sold-to-women-as-strong-empowering-instead-of-risky-reckless',
	'https://www.reddit.com/r/femaledatingstrategy/comments/jbtke6/ladies_lets_talk_about_money_whether_youre_single/',
	'https://www.reddit.com/r/femaledatingstrategy/comments/exmc2u/to_the_men_that_call_us_entitled_princesses/',
	'https://www.therealfemaledatingstrategy.com/post/testing-post-3',
	'https://www.reddit.com/r/femaledatingstrategy/comments/f3datu/does_she_expect_you_to_read_her_mind_yep_next/',
	'https://www.reddit.com/r/femaledatingstrategy/wiki/index',
	'https://www.reddit.com/r/femaledatingstrategy/wiki/faqs',
	'https://www.reddit.com/r/femaledatingstrategy/comments/exmc2u/to_the_men_that_call_us_entitled_princesses/'
)
article = ArticleHtml()
article.path = 'b/fds/'

def getFiles():
	for link in links: article.fromWeb (link, 'feminisme')

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

