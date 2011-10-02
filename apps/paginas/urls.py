# -*- coding: utf-8 -*-
"""
urls.py

Created by Alexandre Marinho on 2009-10-19.
"""
from django.conf.urls.defaults import *
from django.contrib.sitemaps import GenericSitemap

from models import Pagina

queryset = Pagina.objects.publicados().order_by('titulo')

paginas_list = {
    'queryset' : queryset,
    'template_name' : 'paginas/pagina_list.html',
}

pagina = {
    'queryset' : queryset,
    'template_name' : 'paginas/pagina_detail.html',
    'extra_context' : {'css_class':'pagina'}
}

paginas_sitemap_dict = {
    'queryset' : queryset,
    'date_field' : 'data_publicacao',
}

PaginaSitemap = GenericSitemap(paginas_sitemap_dict, priority=0.6)

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w_-]+)/$', 'django.views.generic.list_detail.object_detail', pagina, name='pagina_view'),
    url(r'^$', 'django.views.generic.list_detail.object_list', paginas_list, name="paginas_view"),
)