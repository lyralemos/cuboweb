# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'procuradores.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'procuradores.dashboard.CustomAppIndexDashboard'
"""
from datetime import date

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from cuboweb.apps.congresso.models import Preco

class DiasModule(modules.DashboardModule):
    title = 'Dias para o evento'
    template = 'congresso/dias.html'

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

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for congresso.
    """
    def init_with_context(self, context):
        
        self.children.append(modules.ModelList('Gerenciador de Conteúdo', ['cuboweb.apps.*','*.Inscricao','website.*']))
        
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))
        
        self.children.append(DiasModule())
        
        self.children.append(modules.LinkList(
            
            layout='inline',
            children=(
                {
                    'title': 'Exportar Inscritos',
                    'url': 'congresso/inscricao/inscritos/',
                    'external': False,
                    'description': 'Exportar inscritos em XLS',
                },
                ['Gerenciador de arquivos','filebrowser/browse/']
            )
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for procuradores.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
