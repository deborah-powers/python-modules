#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from imageCls import ImageFolder
import loggerFct as log

imgFolderName = 'i/merge mansion'
imgFolder = ImageFolder (imgFolderName)
imgFolder.get()
imgFolder.open()
imgFolder.ratio()
