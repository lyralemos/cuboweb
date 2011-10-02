# -*- coding: utf-8 -*-

from django.db import models

from cuboweb.apps.cms.models import Base

class Noticia(Base):
	'''O tipo notícia serve como objeto para as noticias do site
	'''
	texto = models.TextField()
	imagem = models.ImageField(upload_to='imagens_noticias',null=True,blank=True)
	legenda = models.CharField(max_length=50,null=True,blank=True)
	
	def has_image(self):
		return bool(self.imagem)
	has_image.short_description = 'Possui Imagem?'
	has_image.boolean = True
	
	@models.permalink
	def get_absolute_url(self):
		return ('noticia_view', [str(self.slug)])
	
	class Meta(Base.Meta):
		verbose_name = 'Notícia'
		verbose_name_plural = 'Notícias'
		app_label = 'cms'