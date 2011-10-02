# -*- coding: utf-8 -*-
"""
urls.py

Created by Alexandre Marinho on 2009-10-19.
"""
from django.conf.urls.defaults import *

from models import Palestrante

palestrantes_dict = {
    'queryset' : Palestrante.objects.publicados().order_by('titulo'),
    'extra_context' : {'css_class':'palestrantes'}
}

urlpatterns = patterns('',
	url(r'^palestrantes/?$', 'django.views.generic.list_detail.object_list', palestrantes_dict,name='palestrantes_view'),
	url(r'^convidados/?$', 'django.views.generic.list_detail.object_list', palestrantes_dict,name='convidados_view'),
	url(r'^programacao/?$', 'cuboweb.apps.congresso.views.programacao', name='programacao_view'),
    url(r'^inscricao/?$', 'cuboweb.apps.congresso.views.inscricao', name='inscricao_view'),
    url(r'^boleto/(?P<cod_inscrito>\d+)/$','cuboweb.apps.congresso.views.boleto',name='boleto'),
	url(r'^boleto/cef_sigcb/(?P<cod_inscrito>\d+)/$','cuboweb.apps.congresso.views.cef_sigcb',name='boleto_cef_sigcb'),
	url(r'^boleto/codigodebarra/?$','cuboweb.apps.congresso.views.codigobarra',name='codigo_de_barra'),
)