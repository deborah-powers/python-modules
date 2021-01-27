#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from articleHtml import ArticleHtml
from fileHtml import FileHtml
import urllib as ul
from urllib import request as urlRequest

links =(
	'https://www.reddit.com/r/femaledatingstrategy/comments/hmjaqh/thread_on_detecting_lies_and_infidelity/',
	'https://www.therealfemaledatingstrategy.com/post/how-to-vet-for-sexual-compatibility',
	'https://www.therealfemaledatingstrategy.com/post/dick-size-matters',
	'https://www.therealfemaledatingstrategy.com/forum/handbook-posts/males-monogamy-and-mate-guarding/',
	'https://www.reddit.com/r/femaledatingstrategy/comments/fgmqcm/women_have_the_trump_card_and_men_know_it/',
	'https://www.therealfemaledatingstrategy.com/post/women-are-not-responsible-for-mens-behavior',
	'https://www.reddit.com/r/femaledatingstrategy/comments/izylyt/protect_your_womb_like_its_the_last_thing_you_do/',
	'https://www.reddit.com/r/femaledatingstrategy/comments/fbdes8/the_real_reason_why_lvm_want_to_go_dutch_and_why/',
	'https://www.reddit.com/r/femaledatingstrategy/comments/iwfi5z/the_myth_of_the_modern_housewife/',
	'https://www.reddit.com/r/femaledatingstrategy/comments/imkv32/fds_is_so_judgemental_yes_and_we_are_proud_of_it/'
)
article = ArticleHtml()
article.path = 'b/fds/'

def getFiles():
	for link in links: article.fromWeb (link, 'feminisme')

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

