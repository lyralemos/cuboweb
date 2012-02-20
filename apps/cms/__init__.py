# -*- coding: utf-8 -*-
"""
__init__.py

Created by Alexandre Marinho on 2009-10-22.
"""
VERSION = 1.2

from django.conf import settings

#settings.FILEBROWSER_URL_WWW = settings.MEDIA_URL+'/uploads/'
#settings.FILEBROWSER_URL_FILEBROWSER_MEDIA = settings.MEDIA_URL + "filebrowser/"
settings.FORMAT_MODULE_PATH = 'cuboweb.apps.cms.formats'
