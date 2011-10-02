# -*- coding: utf-8 -*-
"""
__init__.py

Created by Alexandre Marinho on 2009-10-22.
"""
VERSION = 1.1

from django.conf import settings

settings.TINYMCE_DEFAULT_CONFIG = {
    'theme' : 'advanced',
    'skin' : "o2k7",
    'plugins' : 'table',
    'plugins' : "table,searchreplace,insertdatetime,fullscreen",
    'theme_advanced_buttons1' : "bold,italic,underline,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,|,image,link,unlink,anchor,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,undo,redo",
    'theme_advanced_buttons2' : "charmap,removeformat,|,tablecontrols,|,code,fullscreen,help",
    'theme_advanced_buttons3' : "",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : 'true',
    'table_styles' : "Tabela 1=tabela1;Tabela 2=tabela2;Tabela 3=tabela3",
    'table_cell_styles' : "Celula 1=celula1;Celula 2=celula2;Celula 3=celula3",
    'table_row_styles' : "Cabeﾍalho=cabecalho;Linha 1=linha1;Linha 2=linha2",
    'height' : '400',
    'extended_valid_elements' : 'iframe[src|width|height|name|align]',
}

settings.FILEBROWSER_URL_WWW = settings.MEDIA_URL+'/uploads/'
settings.FILEBROWSER_URL_FILEBROWSER_MEDIA = settings.MEDIA_URL + "filebrowser/"
settings.FORMAT_MODULE_PATH = 'cuboweb.apps.cms.formats'
