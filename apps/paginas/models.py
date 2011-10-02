# -*- coding: utf-8 -*-
"""
models.py

Created by Alexandre Marinho on 2009-10-13.
"""
from django.db import models

from cuboweb.apps.cms.models import Base

class Pagina(Base):
    '''Uma pagina eh o tipo mais simples de conteudo
    '''
    texto = models.TextField()
    
    @models.permalink
    def get_absolute_url(self):
        return ('pagina_view', [str(self.slug)])
    
    class Meta(Base.Meta):
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'
        app_label = 'cms'