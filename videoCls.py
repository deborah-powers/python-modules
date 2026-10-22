#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
import numpy
import cv2
from imageCls import MediaFile
import loggerFct as log

videoExtensions =( 'avi', 'mp4', 'mov' )

class VideoFile (MediaFile):
	def __init__ (self, video=None):
		MediaFile.__init__ (self)
		self.frames =[]
		self.nbFrames =0
		self.rangeFrames =[]
		self.width =0
		self.height =0
		if video:
			self.path = video
			self.fromPath()

	def test (self):
		self.extension = 'avi'

	def toNb (self):
		for f in self.rangeFrames: self.frames[f] = cv2.cvtColor (self.frames[f], cv2.COLOR_BGR2GRAY)
		self.title = self.title +' nb'
		self.toPath()

	def open (self):
		self.toPath()
		if not os.path.exists (self.path): return
		videoCap = cv2.VideoCapture (self.path)
		if not videoCap.isOpened():
			print ("impossible d'ouvrir la vidéo", self.path)
			return
		self.width = int (videoCap.get (cv2.CAP_PROP_FRAME_WIDTH))
		self.height = int (videoCap.get (cv2.CAP_PROP_FRAME_HEIGHT))
		# Capture frame-by-frame
		ret, frame = videoCap.read()
		while ret:
			# if frame is read correctly ret is True
			self.frames.append (frame)
			ret, frame = videoCap.read()
		self.nbFrames = len (self.frames)
		self.rangeFrames = range (self.nbFrames)

	def draw (self):
		isDrawable = MediaFile.draw (self)
		if isDrawable:
			"""
			fourcc = None
			if self.extension == 'avi': fourcc = cv2.VideoWriter_fourcc (*'DIVX')
			else: fourcc = cv2.VideoWriter_fourcc (*'avc1')
			fourcc = cv2.VideoWriter_fourcc (*'DIVX')
			"""
			fourcc = cv2.VideoWriter_fourcc ('M', 'J', 'P', 'G')
			log.logMsg (self.path)
			video = cv2.VideoWriter (self.path, fourcc, 30, (self.width, self.height))
			for frame in self.frames: video.write (frame)
			cv2.destroyAllWindows()
			video.release()

if len (argv) <2: print ('veuillez entrer un fichier vidéo')
else:
	video = VideoFile (argv[1])
	video.open()
	video.test()
	video.draw()

