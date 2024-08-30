#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from sys import argv
import numpy
numpy.seterr (all='warn')
from PIL import Image, ImageOps
import colorsys
from imgModif import openImage, imGtoHsv, hsVtoImg
from imgDetour import eraseLonelyPixel, unifyClosesColors
import loggerFct as log

imgName = 'b/test.bmp'
imgNameBis, imageOriginal = openImage (imgName)
imgNameBis = imgNameBis + '-bis.bmp'
imageOriginal = ImageOps.grayscale (imageOriginal)
imageArray = unifyClosesColors (imageOriginal)
imageOriginal = Image.fromarray (imageArray)
hue, saturation, value = imGtoHsv (imageOriginal)

rangeHeight = range (len (saturation))
rangeWidth = range (len (saturation[0]))

for h in rangeHeight:
	colorArea = numpy.logical_and (hue == hue[h][0], value == value[h][0])
	saturation[colorArea] = 0.5
	value[colorArea] =100
	hue[colorArea] = 0.4
	colorArea = numpy.logical_and (hue == hue[h][-1], value == value[h][-1])
	saturation[colorArea] = 0.5
	value[colorArea] =100
	hue[colorArea] = 0.4
for w in rangeWidth:
	colorArea = numpy.logical_and (hue == hue[0][w], value == value[0][w])
	saturation[colorArea] = 0.5
	value[colorArea] =100
	hue[colorArea] = 0.4
	colorArea = numpy.logical_and (hue == hue[-1][w], value == value[-1][w])
	saturation[colorArea] = 0.5
	value[colorArea] =100
	hue[colorArea] = 0.4
imageArray = hsVtoImg (hue, saturation, value)
imageOriginal = Image.fromarray (imageArray)
"""
imageOriginal = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=10)
imageOriginal = ImageOps.grayscale (imageOriginal)
imageArray = numpy.array (imageOriginal)
imageArray = eraseLonelyPixel (imageArray)
imageOriginal = Image.fromarray (imageArray)
"""
imageOriginal.save (imgNameBis)

