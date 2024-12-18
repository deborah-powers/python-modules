#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from PIL import Image, IptcImagePlugin
from imgModif import openImage
import loggerFct as log

imgName = 'C:\\Users\\LENOVO\\Pictures\\11132024143654.jpg'
imgNameBis, imageOriginal = openImage (imgName)
imgNameBis = imgNameBis + '-bis.bmp'

iptc = IptcImagePlugin.getiptcinfo (imageOriginal)
print (iptc)


"""
https://stackoverflow.com/questions/64113710/extracting-gps-coordinates-from-image-using-python
https://sylvaindurand.org/gps-data-from-photos-with-python/

exifData = imageOriginal.getexif()
{
	256: 800,	# largeur
	257: 800,	# hauteur
	274: 0,		# ?
	306: '2024:11:17 16:40:00',	# date
	271: 'vivo',	# téléphone marque
	272: 'V2110'	# téléphone modèle
	305: 'MediaTek Camera Application'	# appli de photo
	# ?
	34853: 194,
	34665: 106
}
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
imageExif = imageOriginal.getexif()
print (imageExif)
log.logMsg (Interop.__dict__)
log.logMsg (Base.__dict__)
log.logMsg (GPS.__dict__)
log.logMsg (GPSTAGS)
"""

def getMetadataWindow():
	import win32com.client as wclient
	fileFolder = 'C:\\Users\\LENOVO\\Pictures'
	fileName = '11132024143654.jpg'

	sh = wclient.gencache.EnsureDispatch ('Shell.Application',0)
	ns = sh.NameSpace (fileFolder)
	item = ns.ParseName (fileName)

	metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected', 'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords']

	file_metadata = dict()
	for ind, attribute in enumerate (metadata):
		attr_value = ns.GetDetailsOf (item, ind)
		if attr_value:
			print (ind, attribute, ':', attr_value)
			file_metadata[attribute] = attr_value
