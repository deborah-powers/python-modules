#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

author = 'deborah powers'
email = 'deborah.powers@cgi.com'
name = 'mantis'
description = "traiter les fiches mantis chez moi"
version = '0.1'

setup (
	name = name, version = version, description = description,
	author = author, author_email = email,
	# list folders, not files
	packages = find_packages()
)