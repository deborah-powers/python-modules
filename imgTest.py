#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import win32com.client as wclient
from PIL import Image, IptcImagePlugin
from pillow_heif import register_heif_opener
from imgModif import openImage
import loggerFct as log

register_heif_opener()
metadataWindow =[
	'Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes', 'Offline status', 'Availability', 'Perceived type',
	'Owner', 'Kind', 'Date taken', 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating',
	'Authors', 'Title', 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
	'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords'
]
def getMetadataWindow (nameSpace):
	fileName = '20241102_160437.heic'
	item = nameSpace.ParseName (fileName)
	print (nameSpace.GetDetailsOf (item, 12))
	"""
	for ind, attribute in enumerate (metadataWindow):
		attr_value = nameSpace.GetDetailsOf (item, ind)
		print (ind, attribute, ':', attr_value)
	"""
fileFolder = 'C:\\Users\\LENOVO\\Pictures'
shellApp = wclient.gencache.EnsureDispatch ('Shell.Application', 0)
nameSpace = shellApp.NameSpace (fileFolder)
getMetadataWindow (nameSpace)

"""
https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python
pip install pillow-heif

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

