#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

author = 'deborah powers'
email = 'deborah.powers@orange.fr'
name = 'pp-test'
description = "package test pour comprendre la création et l'installation  des packages"
version = '0.1'

setup (
	name = name, version = version, description = description,
	author = author, author_email = email,
	# list folders, not files
	# packages =[ 'pptest'],
	packages = find_packages(),
	# additional packages that needs to be installed along with your package
	install_requires =[],
	keywords =[ 'python', 'first package', 'test'],
	classifiers= [
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Education",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)