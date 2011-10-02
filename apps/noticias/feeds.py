# -*- coding: utf-8 -*-
"""
feeds.py

Created by Alexandre Marinho on 2009-10-19.
"""
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from models import Noticia

site_name = Site.objects.get_current().name

class LatestEntries(Feed):
    title = u"Últimas notícias %s" % site_name
    link = "/noticias/rss/latest"
    description = u"Últimas notícias %s" % site_name

    def items(self):
        return Noticia.objects.publicados().order_by('-data_publicacao')[:5]
    
    def item_title(self,item):
        return item.titulo
    
    def item_description(self,item):
        return item.texto
