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

from models import Noticia

class NoticiaAdminForm(forms.ModelForm):
	'''Formuário para o tipo noticia do admin
	'''
	texto = forms.CharField(widget=Text(attrs={'cols': 80, 'rows': 30}))
	
	class Meta():
		model = Noticia

class NoticiaAdmin(BaseAdmin):
	form = NoticiaAdminForm
	list_display = ['has_image']
	fieldsets = [
		('Dados', {'fields' : ('titulo', 'texto','imagem','legenda')}),
	]


admin.site.register(Noticia, NoticiaAdmin)