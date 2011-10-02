# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from cuboweb.apps.paginas.models import Pagina

class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        inscricao_texto = u" "
        inscricao = Pagina(titulo=u'Inscrição',slug='inscricao',texto=inscricao_texto)
        inscricao.save()
        
        texto_encerradas = u"""
        Lamentamos o ocorrido, mas n&atilde;o &eacute; mais poss&iacute;vel se inscrever no <b>NOME DO CONGRESSO</b>.
        <br /><br />
        Para maiores informa&ccedil;&otilde;es, <a href="/contato"><b>clique aqui</b></a> e entre em contato com a nossa equipe.
        <br /><br />
        Atenciosamente,<br />
        <b>Secretaria Executiva</b>
        """
        encerradas = Pagina(titulo=u'Inscrições Encerradas',slug='incricoes-encerradas',texto=texto_encerradas)
        encerradas.save()
        
        enviada_texto = """
        Obrigado por se inscrever no <b>NOME DO CONGRESSO</b>.
        <br /><br />
        Aguarde o nosso email com a confirma&ccedil;&atilde;o da sua inscri&ccedil;&atilde;o.
        <br /><br />  
        Para maiores informa&ccedil;&otilde;es, <a href="/contato"><b>clique aqui</b></a> e entre em contato com a nossa equipe.
        <br /><br />
        Atenciosamente,<br />
        Secretaria Executiva.
        """
        enviada = Pagina(titulo=u'Incrição Enviada',slug='inscricao-enviada',texto=enviada_texto)
        enviada.save()
        
        print u'Páginas criadas com sucesso!'