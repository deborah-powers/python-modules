#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

author = 'deborah powers'
email = 'deborah.powers@orange.fr'
name = 'listPerso'
description = "classes et methodes pour traites les liste et les tables"
version = '0.1'

setup (
	name = name, version = version, description = description,
	author = author, author_email = email,
	# list folders, not files
	# packages =[ 'pptest'],
	packages = find_packages()
)