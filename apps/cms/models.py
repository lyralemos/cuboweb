# -*- coding: utf-8 -*-
"""
models.py

Created by Alexandre Marinho on 2009-10-22.
"""
from datetime import datetime
from django.db import models

WORKFLOW = (
	('privado','Privado'),
	('publicado','Publicado'),
)

class ManagerPublicado(models.Manager):
	'''Manager para itens publicados 
	'''
	def publicados(self):
		return self.get_query_set().filter(estado='publicado')
	
	def get_or_none(self, **kwargs):
		try:
			return self.get(**kwargs)
		except self.model.DoesNotExist:
			return None


class Base(models.Model):
	'''Classe abstrata básica para os modelos dessa aplicação 
	'''
	titulo = models.CharField(max_length=200)
	slug = models.SlugField('URL',max_length=200)
	data_criacao = models.DateTimeField('Data de Criação',auto_now_add=True,editable=False)
	ultima_modificacao = models.DateTimeField('Última Modificação',auto_now=True,editable=False)
	data_publicacao = models.DateTimeField('Data de Publicação',null=True,blank=True)
	estado = models.CharField(max_length=30,choices=WORKFLOW,default='publicado',
		help_text='Privado - Não disponível para os visitantes<br />Publicado - Disponível para todos')

	objects = ManagerPublicado()
	
	def __unicode__(self):
		return self.titulo
	
	def publicado(self):
		return self.estado == 'publicado'
	publicado.short_name = 'Publicado?'
	publicado.boolean = True
	
	def save(self,*args,**kwargs):
		if self.estado == 'publicado' and self.data_publicacao is None:
			self.data_publicacao = datetime.now()
		super(Base,self).save(*args, **kwargs)
	
	class Meta():
		abstract = True
		get_latest_by = '-data_publicacao'