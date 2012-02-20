# -*- coding: utf-8 -*-
# Create your views here.
from datetime import date
import StringIO

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.importlib import import_module

from boletos.codigodebarra import codigodebarra

from cuboweb.apps.paginas.models import Pagina

from models import Programacao, Preco
#from forms import InscricaoForm


module = getattr(
    settings,
    'INSCRICAO_FORM',
    'cuboweb.apps.congresso.forms.InscricaoForm'
)
mod, inst = module.rsplit('.', 1)
mod = import_module(mod)
InscricaoForm = getattr(mod,inst)

def programacao(request):
    css_class = 'programacao'
    programacoes = Programacao.objects.publicados().order_by('data_publicacao')
    return render_to_response('congresso/programacao.html',locals(),context_instance=RequestContext(request))


def inscricao(request):
    css_class = 'inscricao'
    cod_cedente = getattr(settings,'CONTA_CEDENTE',None)
    datas = Preco.objects.filter(categoria__publico=True).dates('vencimento','day')
    precos = Preco.objects.filter(categoria__publico=True).order_by('categoria','vencimento')
    pagina = Pagina.objects.get_or_none(slug='inscricao')
    nome_congresso = getattr(settings, 'NOME_CONGRESSO')
    if datas:
        limite_inscricoes = Preco.objects.filter(categoria__publico=True).latest('vencimento').vencimento
        if limite_inscricoes < date.today():
            return HttpResponseRedirect(reverse('pagina_view',args=['inscricoes-encerradas']))
    if request.POST:
        form = InscricaoForm(request.POST)
        if form.is_valid():
            instance = form.save()
            default_from = getattr(settings, 'DEFAULT_FROM_EMAIL')
            site_domain = Site.objects.get_current().domain
            mensagem = render_to_string('congresso/email_inscricao.html', {
                'instance':instance,
                'domain':site_domain,
                'NOME_CONGRESSO' : settings.NOME_CONGRESSO
            })
            send_mail('[%s] Inscrição recebida' % nome_congresso, mensagem,default_from,[instance.email])
            return HttpResponseRedirect(reverse('pagina_view',args=['inscricao-enviada']))
    else:
        form = InscricaoForm()
    return render_to_response('congresso/inscricao.html',locals(),context_instance=RequestContext(request))

def cef_sigcb(request,cod_inscrito):
    """
    Boleto CAIXA ECONOMICA FEDERAL (SIGCB)
    """
    from boletos.bancos.caixaeconomicasigcb import caixaeconomicasigcb
    caixa = caixaeconomicasigcb()

    dados = dict()
    inscricao_model = models.get_model('congresso','Inscricao')
    
    inscricao = inscricao_model.objects.get(pk=cod_inscrito)

    dados['taxa_boleto'] = 0.0
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = inscricao.data_vencimento()       # data vencimento demonstracao, data atual + 5 dias   
    
    dados["data_documento"] = date.today().strftime("%d/%m/%Y")
    dados["data_processamento"] = date.today().strftime("%d/%m/%Y")

    #dados['valor_boleto'] = float(inscricao.valor().replace(',','.'))
    dados['valor_boleto'] = inscricao.valor()
  
    dados['numero_documento'] = ''	# Num do pedido ou do documento
    
    # Composicao Nosso Numero - CEF SIGCB
    dados['nosso_numero1'] = '000'       # tamanho 3
    dados['nosso_numero_const1'] = '2'   # constanto 1 , 1=registrada , 2=sem registro
    dados['nosso_numero2'] = '000'       # tamanho 3
    dados['nosso_numero_const2'] = '4'   # constanto 2 , 4=emitido pelo proprio cliente
    dados['nosso_numero3'] = inscricao.nosso_numero() # tamanho 9
    

    # Dados do seu cliente 
    dados['sacado'] = inscricao.nome
    dados['endereco1'] = inscricao.endereco
    dados['endereco2'] = '%s - %s -  CEP: %s' % (inscricao.cidade,inscricao.estado,inscricao.cep)


    # Informacoes para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Inscrição - %s' % getattr(settings,'NOME_CONGRESSO')
    dados['demonstrativo2'] = ''
    dados['demonstrativo3'] = ''


    # Instrucoes para o caixa 
    dados['instrucoes1'] = '- Não receber após o vencimento'
    dados['instrucoes2'] = ''
    dados['instrucoes3'] = ''
    dados['instrucoes4'] = ''


    # Dados opcionais de acordo com o Banco ou cliente 
    dados['quantidade'] = ''
    dados['valor_unitario'] = ''
    dados['aceite'] = ''		
    dados['especie'] = 'R$'
    dados['especie_doc'] = ''


    # Dados da sua conta - CAIXA ECONOMICA FEDERAL 
    dados['agencia'] = getattr(settings,'AGENCIA')  # Num da agencia, sem digito
    dados['conta'] = getattr(settings,'CONTA')     # Num da conta, sem digito
    dados['conta_dv'] = getattr(settings,'DV_CONTA')    # Digito do Num da conta

    # Dados personalizados - CAIXA ECONOMICA FEDERAL 
    dados['conta_cedente'] = getattr(settings,'CONTA_CEDENTE')  # ContaCedente do Cliente, sem digito (Somente Numeros)
    dados['carteira'] = 'SR'                # C??digo da Carteira: pode ser SR (Sem Registro) ou CR (Com Registro) 
                                            #                                - (Confirmar com gerente qual usar)

    # Seus Dados 
    dados['identificacao'] = 'Boleto %s' % getattr(settings,'NOME_CONGRESSO')
    dados['cpf_cnpj'] = getattr(settings,'CPF_CNPJ')
    dados['endereco'] = getattr(settings,'ENDERECO_REALIZADOR')
    dados['cidade_uf'] = getattr(settings,'CIDADE_UF')
    dados['cedente'] = getattr(settings,'RAZAO_SOCIAL')



    dados = caixa.getdadosboleto(dados)

    return render_to_response('congresso/boletos/caixaeconomica.html',locals(),context_instance=RequestContext(request))

def bb(request,cod_inscrito):
    from boletos.bancos.bancodobrasil import bancodobrasil 
    bb = bancodobrasil()        
    dados = dict()
    
    inscricao_model = models.get_model('congresso','Inscricao')
    inscricao = inscricao_model.objects.get(pk=cod_inscrito)
    
    dados['nosso_numero'] = inscricao.nosso_numero()
    dados['numero_documento'] = ''
    
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = inscricao.data_vencimento()       # data vencimento demonstra√ß√£o, data atual + 5 dias
    
    dados['data_documento'] = date.today().strftime("%d/%m/%Y")
    dados['data_processamento'] = date.today().strftime("%d/%m/%Y")
    dados['valor_boleto'] = inscricao.valor()
    dados['taxa_boleto'] = 0.0
    
    # Dados da sua conta - BANCO DO BRASIL 
    dados['agencia'] = getattr(settings,'AGENCIA')
    dados['conta'] = getattr(settings,'CONTA')
    
    # Dados personalizados - BANCO DO BRASIL 
    dados['convenio'] = getattr(settings,'CONVENIO')
    dados['contrato'] = getattr(settings,'CONTRATO')
    dados['carteira'] = '18'
    dados['variacao_carteira'] = '-019'
    
    
    
    # Informa√ß√µes do seu cliente 
    dados['sacado'] = inscricao.nome
    dados['endereco1'] = inscricao.endereco
    dados['endereco2'] = '%s - %s -  CEP: %s' % (inscricao.cidade,inscricao.estado,inscricao.cep)
    
    # Informa√ß√µes para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Inscrição - %s' % getattr(settings,'NOME_CONGRESSO')
    dados['demonstrativo2'] = ""
    dados['demonstrativo3'] = ''
    
    # Instru√ß√µes para o Caixa 
    dados['instrucoes1'] = '- Não receber após o vencimento'
    dados['instrucoes2'] = ''
    dados['instrucoes3'] = ''
    dados['instrucoes4'] = ''
    
    
    # Dados opcionais de acordo com o banco ou cliente 
    dados['quantidade'] = '10'
    dados['valor_unitario'] = '10'
    dados['aceite'] = "N";        
    dados['especie'] = 'R$'
    dados['especie_doc'] = 'DM'
    
    
    # Deus Dados     
    dados['identificacao'] = 'Boleto %s' % getattr(settings,'NOME_CONGRESSO')
    dados['cpf_cnpj'] = getattr(settings,'CPF_CNPJ')
    dados['endereco'] = getattr(settings,'ENDERECO_REALIZADOR')
    dados['cidade_uf'] = getattr(settings,'CIDADE_UF')
    dados['cedente'] = getattr(settings,'RAZAO_SOCIAL')
    
    dados = bb.getdadosboleto(7,2,dados)

    return render_to_response('congresso/boletos/bancodobrasil.html',locals(),context_instance=RequestContext(request))


def boleto(request,cod_inscrito):
    banco = getattr(settings,'BANCO')
    if banco == 'CEF':
        return cef_sigcb(request,cod_inscrito)
    elif banco == 'BB':
        return bb(request,cod_inscrito)
    elif banco == 'BRADESCO':
        pass
    elif banco == 'REAL':
        pass
    return cef_sigcb(request,cod_inscrito)

def codigobarra(request):
        
    codigo = request.GET.get('codigo')
    barra = codigodebarra()
    # codigo de barra completo em d√≠gitos
    # formato que deseja salvar a imagem (PNG,GIF)
    tipo='GIF'

    # retornando uma imagem a partir do c√≥digo de barra
    image = barra.getcodbarra(codigo)

    buffer = StringIO.StringIO()        
    image.save(buffer, tipo)        
    conteudo = buffer.getvalue()
    buffer.close()
    
    return HttpResponse(conteudo,mimetype="image/gif")