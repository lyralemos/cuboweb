# -*- coding: utf-8 -*-
"""
admin.py

Created by Alexandre Marinho on 2009-10-22.
"""

from django.contrib import admin

def make_published(modeladmin, request, queryset):
    #queryset.update(estado='publicado')
    for obj in queryset:
        obj.estado = 'publicado'
        obj.save()
make_published.short_description = u'Publicar os ítens selecionados'

def make_private(modeladmin, request, queryset):
    queryset.update(estado='privado')
make_private.short_description = u'Retirar os ítens selecionados'

class BaseAdmin(admin.ModelAdmin):
    pre_list_display = ['titulo', 'data_criacao', 'ultima_modificacao', 'data_publicacao']
    pos_list_display = ['publicado']
    default_fields = ('slug', 'estado', 'data_publicacao')
    pre_fieldsets = [
    	('Propriedades', {'fields': ('slug', 'estado', 'data_publicacao'), 'classes' : ('properties',)}),
    ]
    pre_list_filter = ['estado', 'data_criacao', 'ultima_modificacao', 'data_publicacao']
    pre_search_fields = ['titulo']
    prepopulated_fields = {'slug' : ('titulo',)}
    date_hierarchy = 'data_publicacao'
    
    combine_display = True

    actions = [make_published, make_private]

    def __init__(self, *args, **kwargs):
        if self.combine_display:
            if self.list_display == ('__str__',):
                self.list_display = list(self.pre_list_display) + list(self.pos_list_display)
            else:
                self.list_display = list(self.pre_list_display) + list(self.list_display) + list(self.pos_list_display)
        if self.fieldsets:
            self.fieldsets = list(self.pre_fieldsets) + list(self.fieldsets)
        if self.list_filter == None:
            self.list_filter = list(self.pre_list_filter)
        else:
            self.list_filter = list(self.pre_list_filter) + list(self.list_filter)
        if self.search_fields == None:
            self.search_fields = list(self.pre_search_fields)
        else:
            self.search_fields = list(self.pre_search_fields) + list(self.search_fields)
        super(BaseAdmin, self).__init__(*args, **kwargs)

    class Media():
        css = {"all": ("cms/css/cmsadmin.css",)}
        #js = ['/media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/tinymce_setup/tinymce_setup.js',]

