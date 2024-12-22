#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import numpy
from imageCls import ImageFile

image = ImageFile ('p/passé\\1996 taie des parents.jpg')
image.open()
image.correctContrast()
image.title = image.title + ' ctrst'
image.draw()