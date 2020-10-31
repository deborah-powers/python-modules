#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# mes actions temporaires
from fileList import FileList

fllst = FileList ('b/localhost/site-dp/')
fllst.get ('.html')
fllst.replace ('library-js/debby-play/debbyPlay.css', 'library-css/debbyPlay.css')
fllst.replace ('library-js/debby-play/debbyPlay.js', 'library-js/debbyPlay.js')

