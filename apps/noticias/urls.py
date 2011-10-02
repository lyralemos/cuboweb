# -*- coding: utf-8 -*-
"""
urls.py

Created by Alexandre Marinho on 2009-10-22.
"""
from django.conf.urls.defaults import patterns,url
from django.contrib.sitemaps import GenericSitemap

from cuboweb.apps.noticias.models import Noticia
from feeds import LatestEntries

queryset = Noticia.objects.publicados().order_by('-data_publicacao')

noticias_list = {
    'queryset' : queryset,
    'template_name' : 'noticias/noticia_list.html',
}

noticia = {
    'queryset' : queryset,
    'template_name' : 'noticias/noticia_detail.html',
    'extra_context': {'css_class':'noticia'}
}

noticias_sitemap_dict = {
    'queryset' : queryset,
    'date_field' : 'data_publicacao',
}

NoticiaSitemap = GenericSitemap(noticias_sitemap_dict, priority=0.6)

urlpatterns = patterns('',
    url(r'^rss/$', LatestEntries(),name='noticias_feed'),
    url(r'^(?P<slug>[\w_-]+)/$', 'django.views.generic.list_detail.object_detail', noticia, name='noticia_view'),
    url(r'^$', 'django.views.generic.list_detail.object_list', noticias_list,name='noticias_view'),
)