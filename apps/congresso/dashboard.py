# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'maceiodonto.dashboard.CustomIndexDashboard'
"""
from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models import get_model

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name

from cuboweb.apps.congresso.models import Preco, Categoria



class DiasModule(DashboardModule):
    title = 'Término das inscrições'
    template = 'congresso/dashboard/dias.html'

    def init_with_context(self, context):
        try:
            self.ultimo_dia = Preco.objects.latest('vencimento').vencimento
            self.dias = self.ultimo_dia - date.today()
        except Preco.DoesNotExist:
            pass

    def is_empty(self):
        if not Preco.objects.count():
            return True
        if self.dias.days < 0:
            return True
        return False

class CategoriasModule(DashboardModule):
    title = 'Categorias'
    template = 'congresso/dashboard/categorias.html'

    def init_with_context(self,context):
        self.categorias = Categoria.objects.all()
    
    def is_empty(self):
        return not bool(len(self.categorias))

class InscricoesModule(DashboardModule):
    title = 'Inscrições'
    template = 'congresso/dashboard/inscricoes.html'

    def init_with_context(self,context):
        Inscricao = get_model('congresso','Inscricao')
        self.total = Inscricao.objects.count()
    
    def is_empty(self):
        return False

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            'Administração',
            column=1,
            collapsible=True,
            css_classes=('collapse closed',),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.ModelList(
            'Conteúdo',
            column=1,
            collapsible=False,
            models=('cuboweb.apps.congresso.*','cuboweb.apps.paginas.*','cuboweb.apps.noticias.*','apps.*'),
        ))

        self.children.append(DiasModule(
            column=2,
            collapsible=False,
        ))

        self.children.append(InscricoesModule(
            column=2,
            collapsible=False,
        ))

        self.children.append(CategoriasModule(
            column=2,
            collapsible=False,
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            u'Links Úteis',
            column=2,
            collapsible=False,
            children=[
                {
                    'title': 'Gerenciador de Arquivos',
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
                {
                    'title': 'Cubo Estúdio Web',
                    'url': 'http://cuboestudioweb.com/',
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


