'''
Created on 10/04/2010

@author: alexandre
'''
from django import forms
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRPhoneNumberField,\
    BRStateChoiceField

class NotifyForm(forms.Form):
    
    subject = ''
    user_list = []

    def notify(self):
        """
        Sends an email to all members of the staff with ordered list of fields
        and values for any form that subclasses FormMail
        """
        site_name = Site.objects.get_current().name
        subject = self.subject or '%s Contato' % (site_name)
        
        if not self.user_list:
            self.user_list = [u.email for u in User.objects.filter(is_staff=True).exclude(email="").order_by('id')]
        
        message = ""
        for k in self.base_fields.keyOrder:
            message = message + '%s: %s\n\n' % (self[k].label, self.cleaned_data[k])
        send_mail(subject, message, self.cleaned_data['email'], self.user_list)

class ContatoForm(NotifyForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))
    assunto = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))
    telefone = BRPhoneNumberField(required=False)
    estado = BRStateChoiceField(initial='AL')
    cidade = forms.CharField()
    email = forms.EmailField()
    mensagem = forms.CharField(widget=forms.Textarea)