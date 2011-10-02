# -*- coding: utf-8 -*-
"""
models.py

Created by Alexandre Marinho on 2009-10-13.
"""
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from cuboweb.apps.cms.models import Base
from cuboweb.apps.cms.fields import RemovableImageField

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    publico = models.BooleanField(default=True,help_text=u'Marque essa opção se deseja que a categoria apareca no formulário de cadastro')
    
    def __unicode__(self):
        return self.nome

class Preco(models.Model):
    categoria = models.ForeignKey(Categoria)
    valor = models.CommaSeparatedIntegerField(max_length=20,help_text='Ex.: 120,00')
    vencimento = models.DateField(help_text='Escolha uma data para a vencimento desse preço')
    
    def __unicode__(self):
        return '%s' % self.valor
    
    class Meta():
        ordering = ('vencimento','categoria')
        verbose_name_plural = u'Preços'

class Palestrante(Base):
    '''Palestrante do evento
    '''
    descricao = models.TextField('Descrição')
    foto = RemovableImageField(upload_to='palestrantes', null=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('palestrantes_view', [])
    
    class Meta():
        ordering = ('titulo',)

class Programacao(Base):
    '''Programação do evento
    '''
    instrucoes = models.TextField('Instruções')
    
    @models.permalink
    def get_absolute_url(self):
        return ('programacao_view', [])
    
    def itens(self):
        return self.itemprogramacao_set.order_by('dia','inicio', 'termino')
    
    class Meta():
        verbose_name = u'Programação'
        verbose_name_plural = u'Programações'

class ItemProgramacao(models.Model):
    '''O ítem relacionado a programação do evento
    '''
    programacao = models.ForeignKey(Programacao)
    titulo = models.CharField('Título', max_length=150)
    dia = models.DateField()
    inicio = models.TimeField('Início')
    termino = models.TimeField('Término')
    palestrante = models.ForeignKey(Palestrante, null=True, blank=True)
    
    def __unicode__(self):
        return self.titulo
    
    class Meta():
        verbose_name = u'Ítem Programação'
        verbose_name_plural = u'Ítens da Programação'
        ordering = ('dia','inicio','termino')

class Patrocinio(models.Model):
    '''Imagens de patrocinio do congresso
    '''
    nome = models.CharField(max_length='200')
    imagem = models.ImageField(upload_to='patrocinio')
    url = models.URLField(blank=True,null=True)
    
    def __unicode__(self):
        return self.nome

class InscricaoBase(models.Model):
    '''Modelo abstrato para inscricao em eventos
    '''
    nome = models.CharField(max_length=200)
    rg = models.CharField('RG',max_length=20,unique=True)
    cpf = models.CharField('CPF', max_length=20,unique=True)
    endereco = models.CharField('Endereço', max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=22)
    celular = models.CharField(max_length=22, blank=True, null=True)
    email = models.EmailField(max_length=100)
    data_inscricao = models.DateTimeField(default=datetime.now)
    numero_boleto = models.CharField(max_length=30, blank=True, null=True,editable=False)
    data_pagamento = models.DateField(blank=True,null=True,help_text='Utilize o ícone para selecionar a data.')
    confirmado = models.BooleanField()
    categoria = models.ForeignKey(Categoria)
    
    def attrs(self):
        for field in self._meta.local_fields:
            yield field.verbose_name, getattr(self,field.name)
        yield 'valor', self.valor()
    
    def __unicode__(self):
        return self.nome
    
    def numero_inscricao(self):
        ''' Número de Inscricao formatado 
        '''
        return '%04d' % self.id
    
    def data_vencimento(self):
        ''' Calculo da data do vencimento
		'''
        precos = Preco.objects.filter(categoria=self.categoria,vencimento__gte=self.data_inscricao).order_by('vencimento')
        if len(precos) > 0:
            return precos[0].vencimento.strftime('%d/%m/%Y')
        return precos
    data_vencimento.short_description = u'Data de Vencimento'
    
    def valor(self):
        ''' Valor da inscricao
		'''
        precos = Preco.objects.filter(categoria=self.categoria,vencimento__gte=self.data_inscricao).order_by('vencimento')
        if len(precos) > 0:
            return float(precos[0].valor.replace(',','.'))
        return 0
    
    def nosso_numero(self):
        ''' Padrão unico do nosso numero
		'''
        return '%09d' % self.id
    nosso_numero.short_description = u'Nosso Número'
    
    def boleto_link(self):
        ''' Retorna o link do boleto
        '''
        return u'<a href="%s" target="_blank">Gerar Boleto</a>' % reverse('boleto',args=[self.id])
    boleto_link.allow_tags = True
    boleto_link.short_descrition = u'Gerar Boleto'
    
    class Meta():
        abstract = True
        ordering = ('-data_inscricao')
        verbose_name_plural = u'Inscrições'

inscricao_model = models.get_model('congresso','Inscricao')

if inscricao_model:
    
    def email_handler(sender,instance,**kwargs):
        try:
            confirmado = inscricao_model.objects.get(pk=instance.pk).confirmado
            if confirmado == False and instance.confirmado == True:
                from_email = getattr(settings,'DEFAULT_FROM_EMAIL')
                nome_congresso = getattr(settings,'NOME_CONGRESSO')
                mensagem = render_to_string('congresso/email_confirmacao.html', locals())
                send_mail('Inscrição Confirmada', mensagem, from_email, [instance.email])
        except inscricao_model.DoesNotExist:
            pass
    pre_save.connect(email_handler, sender=inscricao_model)
    
    def numero_boleto_handler(sender,instance,created,**kwargs):
        if created:
            instance.numero_boleto = instance.nosso_numero()
            instance.save()
    post_save.connect(numero_boleto_handler, sender=inscricao_model)