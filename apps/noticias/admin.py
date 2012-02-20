# -*- coding: utf-8 -*-
"""
admin.py

Created by Alexandre Marinho on 2009-10-22.
"""

from django.contrib import admin
from django import forms

from cuboweb.apps.cms.admin import BaseAdmin

from models import Noticia

class NoticiaAdmin(BaseAdmin):
	list_display = ['has_image']
	fieldsets = [
		('Dados', {'fields' : ('titulo', 'texto','imagem','legenda')}),
	]

	class Media():
		js = ['grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', 'grappelli/tinymce_setup/tinymce_setup.js']


admin.site.register(Noticia, NoticiaAdmin)