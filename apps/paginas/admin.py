# -*- coding: utf-8 -*-
"""
admin.py

Created by Alexandre Marinho on 2009-10-22.
"""

from django.contrib import admin
from django import forms

try:
    from tinymce.widgets import TinyMCE
    Text = TinyMCE
except ImportError:
    Text = forms.Textarea

from cuboweb.apps.cms.admin import BaseAdmin

from models import Pagina

class PaginaAdminForm(forms.ModelForm):
    '''Formulário para o tipo pagina do admin
    '''
    texto = forms.CharField(widget=Text(attrs={'cols': 80, 'rows': 30}))
    
    class Meta():
        model = Pagina

class PaginaAdmin(BaseAdmin):
    form = PaginaAdminForm
    search_fields = ['texto']
    fieldsets = [
        ('Dados', {'fields' : ('titulo', 'texto')}),
    ]

admin.site.register(Pagina, PaginaAdmin)