#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageOps
import colorsys
from imgModif import openImage, imGtoHsv, hsVtoImg
import loggerFct as log

imgName = 'b/test.bmp'
imgNameBis, imgObj = openImage (imgName)
hue, saturation, value = imGtoHsv (imgObj)

rangeHeight = range (len (saturation))
rangeWidth = range (len (saturation[0]))
for h in rangeHeight:
	for w in rangeWidth: saturation[h][w] = 1.0
imgNameBis = imgNameBis + '-bis.bmp'
imgArray = hsVtoImg (hue, saturation, value)
imgObj = Image.fromarray (imgArray)
imgObj.save (imgNameBis)

