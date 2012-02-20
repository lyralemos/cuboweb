# -*- coding: utf-8 -*-
"""
admin.py

Created by Alexandre Marinho on 2009-10-22.
"""

from django.contrib import admin
from django import forms

from cuboweb.apps.cms.admin import BaseAdmin

from models import Pagina

class PaginaAdmin(BaseAdmin):
    #form = PaginaAdminForm
    search_fields = ['texto']
    fieldsets = [
        ('Dados', {'fields' : ('titulo', 'texto')}),
    ]

    class Media:
        js = ['grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', 'grappelli/tinymce_setup/tinymce_setup.js']


admin.site.register(Pagina, PaginaAdmin)