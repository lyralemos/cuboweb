# -*- coding: utf-8 -*-
"""
forms.py

Created by Alexandre Marinho on 2009-10-13.
"""
from django import forms
from django.contrib.localflavor.br.forms import BRStateChoiceField, BRPhoneNumberField, BRCPFField, BRZipCodeField
from django.db.models import get_model

from models import Palestrante, Categoria

class PalestranteAdminForm(forms.ModelForm):
    '''Formulario para o palestrante 
    '''
    titulo = forms.CharField(label='Nome',max_length=200)
    
    class Meta():
        model = Palestrante

class InscricaoForm(forms.ModelForm):
    
    cpf = BRCPFField(label='CPF')
    estado = BRStateChoiceField(initial='AL')
    cep = BRZipCodeField()
    telefone = BRPhoneNumberField()
    celular = BRPhoneNumberField(required=False)
    
    def __init__(self,*args,**kwargs):
        super(InscricaoForm,self).__init__(*args,**kwargs)
        total = Categoria.objects.count()
        if total == 1:
            self.fields['categoria'] = forms.CharField(widget=forms.HiddenInput,initial=1)
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        total = Categoria.objects.count()
        if total == 1:
            return Categoria.objects.all()[0]
        return categoria
    
    class Meta():
        exclude = ('confirmado','data_inscricao','data_pagamento')
        model = get_model('congresso','Inscricao')