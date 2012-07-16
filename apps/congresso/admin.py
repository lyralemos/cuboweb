# -*- coding: utf-8 -*-
"""
admin.py

Created by Alexandre Marinho on 2009-10-13.
"""
import xlwt
from datetime import datetime

from django.contrib import admin
from django.conf import settings
from django.db.models import get_model
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

from cuboweb.apps.cms.admin import BaseAdmin

from models import ItemProgramacao, Programacao, Palestrante, Patrocinio, Categoria, Preco
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail

class ItemProgramacaoInline(admin.TabularInline):
    model = ItemProgramacao
    extra = 10

class ProgramacaoAdmin(BaseAdmin):
    fieldsets = [
        ('Dados', {'fields' : ('titulo', 'instrucoes')}),
    ]
    inlines = [ItemProgramacaoInline]

class PalestranteAdmin(BaseAdmin):
    fieldsets = [
        ('Dados', {'fields' : ('titulo', 'descricao', 'foto')}),
    ]

inscricao_model = get_model('congresso','Inscricao')

def confirmar(modeladmin, request, queryset):
    queryset.update(confirmado=True)
confirmar.short_description = u'Confirmar Inscrição'

def atualizar_data_inscricao(modeladmin, request, queryset):
    queryset.update(data_inscricao=datetime.now())
atualizar_data_inscricao.short_description = u'Atualizar data de inscrição'

def reenviar_boletos(modeladmin, request, queryset):
    for inscrito in queryset:
        nome_congresso = getattr(settings, 'NOME_CONGRESSO')
        default_from = getattr(settings, 'DEFAULT_FROM_EMAIL')
        site_domain = Site.objects.get_current().domain
        mensagem = render_to_string('congresso/email_inscricao.html', {
            'instance':inscrito,
            'domain':site_domain,
            'NOME_CONGRESSO':settings.NOME_CONGRESSO
        })
        send_mail('[%s] Inscrição recebida' % nome_congresso, mensagem,default_from,[inscrito.email])
reenviar_boletos.short_description = u'Reenviar Boleto'

custom_list_filter = getattr(settings,'CUSTOM_LIST_FILTER',('estado','confirmado','categoria'))

class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('nome','estado','numero_boleto','data_inscricao','data_vencimento','boleto_link','confirmado','valor')
    list_filter = custom_list_filter
    search_fields = ('nome','numero_boleto')
    actions = [confirmar,atualizar_data_inscricao,reenviar_boletos]
    
    def get_urls(self):
        urls = super(InscricaoAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^inscritos/$', self.admin_site.admin_view(self.inscritos),name='exportar_inscritos')
        )
        return my_urls + urls
    
    def inscritos(self,request):
        inscritos = inscricao_model.objects.order_by('confirmado')
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Inscritos")
        linha = 1
        for inscricao in inscritos:
            coluna = 0
            for attr,value in inscricao.attrs():
                if linha == 1:
                    try:
                        ws.write(0,coluna,attr.decode('utf-8'))
                    except UnicodeEncodeError:
                        ws.write(0,coluna,attr)
                try:
                    ws.write(linha,coluna,value)
                except:
                    ws.write(linha,coluna,value.__unicode__())
                coluna += 1
            linha += 1 
        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=inscritos.xls'
        wb.save(response)
        return response

class PrecoAdmin(admin.ModelAdmin):
    list_display = ('categoria','valor','vencimento')
    list_filter = ('categoria','vencimento')

admin.site.register(Categoria)
admin.site.register(Preco,PrecoAdmin)
admin.site.register(Programacao, ProgramacaoAdmin)
admin.site.register(Palestrante, PalestranteAdmin)
admin.site.register(Patrocinio)
admin.site.register(inscricao_model,InscricaoAdmin)
