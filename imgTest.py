#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from PIL import Image, ImageOps
from io import BytesIO
from imgModif import openImage
from PIL.ExifTags import TAGS, GPSTAGS, GPS, IFD, Base, Interop
import loggerFct as log
import win32com.client as wclient

imgName = 'C:\\Users\\LENOVO\\Desktop\\articles\\informatique\\test-css\\img-bmp.bmp'
imgNameBis, imageOriginal = openImage (imgName)
imgNameBis = imgNameBis + '-bis.bmp'

# récupérer les métadonnées de windows
fileFolder = 'C:\\Users\\LENOVO\\Desktop\\articles\\informatique\\test-css'
fileName = 'img-bmp.bmp'
sh = wclient.gencache.EnsureDispatch ('Shell.Application',0)
ns = sh.NameSpace (fileFolder)
item = ns.ParseName (fileName)
metadata =[ 'Name', 'Size', 'Item type', 'Date modified', 'Date created' ]
metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected', 'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords', 'Masters keywords']

file_metadata = dict()
for ind, attribute in enumerate (metadata):
	attr_value = ns.GetDetailsOf (item, ind)
	print (ind, attribute, attr_value)
	if attr_value: file_metadata[attribute] = attr_value
"""
exifData = imageOriginal.getexif()
exifData[36867] = '2024-06-21'
imageOriginal.save (imgNameBis, exif=exifData)
36867	DateTimeOriginal	2008:11:15 19:36:24
36868	DateTimeDigitized	2008:11:15 19:36:24
306	DateTime				2008:11:15 19:36:24
315	Artist
40091	XPTitle
40092	XPComment
40093	XPAuthor
40094	XPKeywords
40095	XPSubject
37500	MakerNote
37510	UserComment
34377	ImageResources
33432	Copyright
269	DocumentName
270	ImageDescription
1	GPSLatitudeRef
2	GPSLatitude
3	GPSLongitudeRef
4	GPSLongitude
5	GPSAltitudeRef
6	GPSAltitude
7	GPSTimeStamp
28	GPSAreaInformation
29	GPSDateStamp
"""

"""
imageExif = imageOriginal.getexif()
print (imageExif)
log.logMsg (Interop.__dict__)
log.logMsg (Base.__dict__)
log.logMsg (GPS.__dict__)
log.logMsg (GPSTAGS)
------
imageNew = imageFromBase64 (img_b64)
imageNew.show()

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
""
imageOriginal = imageOriginal.convert ('P', palette=Image.ADAPTIVE, colors=10)
imageOriginal = ImageOps.grayscale (imageOriginal)
imageArray = numpy.array (imageOriginal)
imageArray = eraseLonelyPixel (imageArray)
imageOriginal = Image.fromarray (imageArray)
imageOriginal.save (imgNameBis)
"""

