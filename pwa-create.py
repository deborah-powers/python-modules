#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os
from sys import argv
from shutil import copyfile
from fileLocal import *
import fileClass as fc
# les fichiers modèles
filesScript = ('text', 'debbyPlay')
filesStyles = ('structure', 'color', 'debbyPlay')
iconsNb = ('144', '192', '512')
# créer l'architecture d'une pwa perso
fc.extensions = fc.extensions +' webmanifest'
folder = shortcut ('s/')
name = argv [1]
desc = argv [2]
subFolder =""
if len (argv) >3:
	subFolder = argv [3] +'/'
	folder = folder + argv [3] +'/'
# les dossiers
folder = folder + name +'/'
fc.createFolder (folder)
fc.createFolder (folder + 'utils')
def createFile (self, title, extension, text):
	self.title = title
	self.extension = extension
	self.fileFromData ()
	self.text = text
	self.toFile ()
setattr (fc.File, 'createFilePwa', createFile)
# les fichiers communs
fileTmp = fc.File (folder + 'manifest.webmanifest')
fileTmp.text = """ {
	"name":"%s",
	"short_name":"%s",
	"description":"%s",
	"icons": [
		{	"src":"utils/icone-192.png","sizes":"192x192","type":"image/png"	},
		{	"src":"utils/icone-512.png","sizes":"512x512","type":"image/png"	}
	],
	"version":"1",
	"lang":"fr",
	"start_url":"/%s/index.html",
	"display":"standalone",
	"background_color":"ivory",
	"theme_color":"#C29FC2"
} """ % (name, name, desc, subFolder + name)
fileTmp.toFile ()
text = """<!doctype html><html><head>
	<title>%s</title>
	<meta name='viewport' content='width=device-width, initial-scale=1'/>
	<meta charset='utf-8'/>
	<base target='_blank'>
	<link rel='manifest' href='manifest.webmanifest'/>
	<link rel='icon' type='image/png' href='utils/icone-192.png'/>
	<link rel='apple-touch-icon' type='image/png' href='utils/icone-192.png'/>
	<meta name='msapplication-TileImage' content='utils/icone-192.png'>
	<meta name='theme-color' content='ivory'/>
	<meta name='msapplication-TileColor' content='ivory'>
	<meta name='apple-mobile-web-app-capable' content='yes'>
	<meta name='apple-mobile-web-app-status-bar-style' content='black'>
	<meta name='apple-mobile-web-app-title' content='%s'>
	<link rel='stylesheet' type='text/css' href='utils/structure.css'/>
	<link rel='stylesheet' type='text/css' href='utils/debbyPlay.css'/>
	<link rel='stylesheet' type='text/css' href='utils/color.css' media='screen'/>
	<script type='text/javascript' src='utils/text.js'></script>
	<script type='text/javascript' src='utils/debbyPlay.js'></script>
<style type='text/css'></style></head><body>
	<h1>mon appli</h1>
	<button id='install-pwa'>installer l'application</button>
	<script type='text/javascript' src='service-launcher.js'></script>
</body></html>""" % (name, name)
fileTmp.createFilePwa ('index', 'html', text)
text = """const messageAppInstalled = "app installée";
// vérifier si le service-worker est installable
window.onload = function () {
	'use strict';
	if ('serviceWorker' in navigator) navigator.serviceWorker.register ('./service-worker.js');
}
// rendre mon application installable
var installButton = document.getElementById ('install-pwa');
var deferredPrompt;
window.addEventListener ('beforeinstallprompt', function (event) {
	// empêcher l'affichage de la popup d'installation
	event.preventDefault ();
	deferredPrompt = event;
	if (! deferredPrompt) installButton.innerHTML = messageAppInstalled;
	else installButton.innerHTML = "installez l'application";
});
installButton.addEventListener ('click', function () {
	if (! deferredPrompt) installButton.innerHTML = messageAppInstalled;
	else {
		deferredPrompt.prompt ();
		deferredPrompt.userChoice.then (function (choiceResult) {
			if (choiceResult.outcome === 'accepted') installButton.innerHTML = messageAppInstalled;
			else installButton.innerHTML = 'installation ratée';
});} });
// vérifier si l'appli est installée
window.addEventListener ('appinstalled', function (event) {
	var installButton = document.getElementById ('install-pwa');
	installButton.innerHTML = messageAppInstalled;
});"""
fileTmp.createFilePwa ('service-launcher', 'js', text)
text = """// gérer le cache
const cacheName = 'pwa-base';
const filesToCache = [
	'/pwa-base/index.html',
	'/pwa-base/utils/structure.css',
	'/pwa-base/utils/color.css',
	'/pwa-base/utils/debbyPlay.css',
	'/pwa-base/utils/debbyPlay.js',
	'/pwa-base/utils/text.js',
	'/pwa-base/service-launcher.js'
];
// mettre en cache le contenu de l'app
self.addEventListener ('install', function (event) {
	event.waitUntil (caches.open (cacheName).then (function (cache) {
		return cache.addAll (filesToCache);
}));});
// rendre le contenu de l'app hors-ligne
self.addEventListener ('fetch', function (event) {
	event.respondWith (
	caches.match (event.request).then (function (response) {
		return response || fetch (event.request);
}));});
"""
text = text.replace ('pwa-base', subFolder + name)
fileTmp.createFilePwa ('service-worker', 'js', text)
# les fichiers de style
folder = folder + 'utils/'
filePathSrc = shortcut ('s/library-css/%s.css')
filePathDst = folder + '%s.css'
for nb in filesStyles: copyfile (filePathSrc %nb, filePathDst %nb)
filePathSrc = shortcut ('s/library-js/%s.js')
filePathDst = folder + '%s.js'
for nb in filesScript: copyfile (filePathSrc %nb, filePathDst %nb)
filePathSrc = shortcut ('s/data/icone-%s.png')
filePathDst = folder + 'icone-%s.png'
for nb in iconsNb: copyfile (filePathSrc %nb, filePathDst %nb)