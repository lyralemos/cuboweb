# This Python file uses the following encoding: utf-8
"""
Grupo SELCO
Programa para emissão de boleto bancário via PDF
Dependência: reportlab, rlbarcode, python-devel
Por: Armando Roque Ferreira Pinto
Inicio: 22/09/2006 Término 25/09/2006

Medidas expressas em mm (milimetros)

Agradecimentos ao Luciano Pacheco da lista Python-Brasil por ter visto o erro do método image no Canvas.

Para inscrever na lista envie um e-mail para
python-br-subscribe@yahoogroups.com.br
e confirme a inscrição com o e-mail

Atualizações
Autor    Data       Descrição
Armando  25/09/2006 

"""

# imports
from reportlab.graphics import renderPDF
from reportlab.graphics import shapes
from reportlab.graphics.shapes import *
from reportlab.graphics.shapes import Image, Drawing
from reportlab.graphics.barcode.common import *

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from reportlab.pdfgen.canvas import Canvas

from reportlab.platypus import Paragraph, Frame

import string

import os

from datetime import datetime,date

from django.conf import settings

# Constantes
MEDIA_URL = getattr(settings,'MEDIA_ROOT')

# Formulário
FONTE_FORM='Helvetica'
FONTE_FORM_TAM=6

FONTE_FORM_TAM_ID=10

FONTE_DADOS='Helvetica'
FONTE_DADOS_TAM=9

class Boleto():
    banco = ''
    local_pagamento = ''
    cedente = ''
    telefone = ''
    documento = ''
    emissao = ''
    aceite = ''
    especie_doc = ''
    especie_mon = 'R$'
    
    agenci = ''
    conta_sem_dv = ''
    digito_verificador = ''
    carteira = ''
    nosso_numero = ''
    
    valor = ''
    juros = ''
    observacao1 = ''
    observacao2 = ''
    observacao3 = ''
    linha_digitavel = ''
    codigo_de_barra = ''
    
    uso_banco = ''
    
    def verifier_digit(self, field):
        """ Esse metodo utiliza a formula do MODULO 10 para verificar o digito
    	"""
        mult = 2
        sum = 0
        for i in range(len(field)-1, -1, -1):
            x = (int(field[i]) * mult)
            if(x >= 10):
                x = (x % 10) + 1
            sum += x
            if(mult == 2):
                mult = 1
            else:
                mult = 2
        if(not (sum % 10)):
            sum = 0
        else:
            sum = 10 - (sum % 10)
        return sum
    
    def diff_date(self, date_comp):
        """ Calculo do fator do vencimento
        """
        date_def = date(1997,10,7)
        return (str(date_comp - date_def))[0:4]
    
    def calc_our_number(self, our_number):
        """ Calculo do nosso numero usando a formula do MODULO 11
    	"""
        mult = 2
        sum = 0
        for i in range(len(our_number) - 1, -1, -1):
            sum += (int(our_number[i]) * mult)
            if(mult >= 9):
                mult = 2
            else:
                mult += 1
        sum = 11 - (sum % 11)
        if(sum > 9):
            sum = 0
        return str(sum)
    
    def general_digit(self, line):
        """ Calculo do digito verificador geral
        """
        mult = 2
        sum = 0
        tots = ''
        for i in range(len(line) - 1, -1, -1):
            sum += (int(line[i]) * mult)
            tots += str(sum)+' + '
            if(mult >= 9):
                mult = 2
            else:
                mult += 1
        sum = 11 - (sum % 11)
        if(sum > 9 or sum==1 or not sum):
            sum = 1
        return sum

#Global Banco, empresa e cedente (Default Banco do Brasil)
banco='341'
localpagamento='Pague este título preferencialmente nas agências do Banco Itaú'
cedente='PAULA G. SARMENTO DE BRITO'
telefone_empresa='(82) 3231-8238'

#Boleto
documento=''
emissao = datetime.now().strftime('%d/%m/%Y')

aceite='N'
especiedoc='DP'
especiemon='R$'

ag = '1598'
conta = '18087'
dv_conta = '3'
agencia = ag + '/' +conta + '-' + dv_conta
carteira='109'
nossonumero='123321'

valorexpresso=''
juros=''
observacao1='Não receber após vencimento'
observacao2=''
observacao3=''
linhadigitavel = '2379.264712 90600.000336 23007.514005 5 33070000011402'
codigobarra = '23795330700000114022647190600000332300751400'

usobanco=''

def verifier_digit(field):
    mult = 2
    sum = 0
    for i in range(len(field)-1, -1, -1):
        x = (int(field[i]) * mult)
        if(x >= 10):
            x = (x % 10) + 1
        sum += x
        if(mult == 2):
            mult = 1
        else:
            mult = 2
    if(not (sum % 10)):
        sum = 0
    else:
        sum = 10 - (sum % 10)
    return sum

def diff_date(date_comp):
    date_def = date(1997,10,7)
    return (str(date_comp - date_def))[0:4]

def calc_our_number(our_number):
    mult = 2
    sum = 0
    for i in range(len(our_number) - 1, -1, -1):
        sum += (int(our_number[i]) * mult)
        if(mult >= 9):
            mult = 2
        else:
            mult += 1
    sum = 11 - (sum % 11)
    if(sum > 9):
        sum = 0
    return str(sum)

def general_digit(line):
    mult = 2
    sum = 0
    tots = ''
    for i in range(len(line) - 1, -1, -1):
        sum += (int(line[i]) * mult)
        tots += str(sum)+' + '
        if(mult >= 9):
            mult = 2
        else:
            mult += 1
    sum = 11 - (sum % 11)
    if(sum > 9 or sum==1 or not sum):
        sum = 1
    return sum

def mount_line(bank, currency, carteira, code_transf, our_number, factor, value):
    global codigobarra
    diff = 10 - len(str(value))
    dv_nossonumero = calc_our_number(ag+conta+carteira+our_number)
    campo_1 = bank + currency + carteira + our_number[:2]
    campo_1_dv = str(verifier_digit(campo_1))
    
    campo_2 = our_number[2:8] + dv_nossonumero + ag[:3]
    campo_2_dv = str(verifier_digit(campo_2))
    
    campo_3 = ag[3:4] + conta + dv_conta + '000'
    campo_3_dv = str(verifier_digit(campo_3))
    
    campo_4 = factor + ('0' * diff) + value
    
    codigobarra = bank + currency + campo_4 + carteira + our_number + dv_nossonumero + ag + conta + dv_conta + '000'
    g_digit = general_digit(codigobarra)
    codigobarra = codigobarra[:4] + str(g_digit) + codigobarra[4:]
    
    return '%s.%s %s.%s %s.%s %s %s' %\
    (campo_1[:5],campo_1[5:]+campo_1_dv,
     campo_2[:5],campo_2[5:]+campo_2_dv,
     campo_3[:5],campo_3[5:]+campo_3_dv,
     g_digit,campo_4)


def formboleto(response,sacado,endereco,endereco1,valor,vencimento_date,nossonumero,observacao2):
    #temporarios
    #nossonumero = '99999998'
    #valor = '1,00'
    vencimento = vencimento_date.strftime('%d/%m/%Y')
    v = valor.replace(',','')
    fator = diff_date(vencimento_date)
    linhadigitavel = mount_line(banco,'9',carteira,agencia,nossonumero,fator,v)
    nossonumero += '-'+str(calc_our_number(ag+conta+carteira+nossonumero))
    boleto=Canvas(response)
    
    # Logomarca da empresa
    boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/empresa.jpg', x=7*mm, y=280*mm, width=30*mm, height=11*mm)
    
    boleto.setStrokeColor(colors.black)
    boleto.setLineWidth(0.1)
    boleto.setFont('Helvetica-Bold',14)
    global localpagamento, usobanco
  
  
    if banco=='237':
# bradesco
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancobradesco.jpg',x=160*mm, y=280*mm, width=25*mm, height=8*mm)
        
        # imagem do recido do sacado
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancobradesco.jpg',x=7*mm, y=229*mm, width=25*mm, height=8*mm)
        
        # imagem do banco na ficha de compensação
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancobradesco.jpg',x=7*mm, y=112*mm, width=25*mm, height=8*mm)
        
        # codigo do banco
        boleto.drawString(43*mm, 229*mm, '237-9')
        boleto.drawString(43*mm, 112*mm, '237-9')
        
        localpagamento+='Banco BRADESCO S/A'
        
        usobanco='269'
        #LINHADIGITAVEL='2379.264712 90600.000336 23007.514005 5 33070000011402'
        #CODIGOBARRA='23795330700000114022647190600000332300751400'
  
    elif banco=='422':
        # safra
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancosafra.jpg',x=160*mm, y=275*mm, width=32*mm, height=7*mm)
        
        # imagem do recido do sacado
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancosafra.jpg',x=7*mm, y=229*mm, width=30*mm, height=6*mm)
        
        # imagem do banco na ficha de compensação
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancosafra.jpg',x=7*mm, y=112*mm, width=30*mm, height=6*mm)
        
        # codigo do banco
        boleto.drawString(43*mm, 229*mm, '422-7')
        boleto.drawString(43*mm, 112*mm, '422-7')
          
        localpagamento+='Banco SAFRA'

    elif banco=='341':
        # itau
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancoitau.jpg',x=160*mm, y=275*mm, width=32*mm, height=7*mm)
        
        # imagem do recido do sacado
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancoitau.jpg',x=7*mm, y=229*mm, width=30*mm, height=6*mm)
        
        # imagem do banco na ficha de compensação
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancoitau.jpg',x=7*mm, y=112*mm, width=30*mm, height=6*mm)
        
        # codigo do banco
        boleto.drawString(43*mm, 229*mm, '341-7')
        boleto.drawString(43*mm, 112*mm, '341-7')
        
        #localpagamento+='Banco ITAU'
      
    else:
        # banco do brasil para default
        # imagem do canhoto
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancodobrasil.jpg',x=160*mm, y=280*mm, width=30*mm, height=5*mm)
        
        # imagem do recido do sacado
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancodobrasil.jpg',x=7*mm, y=229*mm, width=30*mm, height=5*mm)
        
        # imagem do banco na ficha de compensação
        boleto.drawImage(image=MEDIA_URL+'/alagoasdigital/logos/bancodobrasil.jpg',x=7*mm, y=112*mm, width=30*mm, height=5*mm)
        
        # codigo do banco
        boleto.drawString(43*mm, 229*mm, '001-9')
        boleto.drawString(43*mm, 112*mm, '001-9')
        localpagamento+='Banco do BRASIL S/A'
        
        
        # telefone da empresa
        boleto.setFont('Helvetica-Bold', 12)
        boleto.drawString(7*mm, 275*mm, telefone_empresa)
    
    
    ###############
    #RETICULAS DO VENCIMENTO E DO VALOR 
    #           (NÃO RETIRAR DAQUI SENÃO SOBREPORÁ O VALOR E O VENCIMENTO)
    
    # Recibo do sacado
    # retícula com cinza (Vencimento)
    boleto.setFillColor(colors.lightgrey)
    boleto.setStrokeColor(colors.white)
    boleto.rect(158*mm, 220*mm, 42*mm, 8*mm, stroke=1, fill=1)
    # retícula com cinza (Valor do documento)
    boleto.rect(158*mm, 196*mm, 42*mm, 8*mm, stroke=1, fill=1)
    
    # Ficha de compensação
    # retícula com cinza (Vencimento)
    boleto.setFillColor(colors.lightgrey)
    boleto.setStrokeColor(colors.lightgrey)
    boleto.rect(158*mm, 103*mm, 42*mm, 8*mm, stroke=1, fill=1)
    # retícula com cinza (Valor do documento)
    boleto.rect(158*mm, 79*mm, 42*mm, 8*mm, stroke=1, fill=1)
    
    # Término das retículas cinza
    ################
    
    boleto.setStrokeColor(colors.black)
    boleto.setFillColor(colors.black)
    
    # Recibo de entrega
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
    boleto.drawString(7*mm, 270*mm, 'Sacado:')
    boleto.drawString(7*mm, 266*mm, 'Endereço:')
    boleto.drawString(7*mm, 258*mm, 'Documento:')
    boleto.drawString(7*mm, 254*mm, 'Emissão:')
    boleto.drawString(7*mm, 250*mm, 'Data:')
    boleto.drawString(80*mm, 258*mm, 'Valor:')
    boleto.drawString(80*mm, 254*mm, 'Vencimento:')
    boleto.drawString(80*mm, 250*mm, 'Assinatura: _______________________________')
    
    boleto.drawString(7*mm, 217*mm, 'Data do documento')
    boleto.drawString(41*mm, 217*mm, 'No. do documento')
    boleto.drawString(71*mm, 217*mm, 'Espécie doc')
    boleto.drawString(91*mm, 217*mm, 'Aceite')
    boleto.drawString(114*mm, 217*mm, 'Data do processamento')
    boleto.drawString(160*mm, 217*mm, 'Agência/Código do cedente')
    boleto.drawString(7*mm, 209*mm, 'Uso do banco')
    boleto.drawString(7*mm, 201*mm, 'Instruções (Todas informações deste BOLETO são de exclusiva responsabilidade do cedente)')
    boleto.drawString(7*mm, 225*mm, 'Cedente')
    boleto.drawString(160*mm, 225*mm, 'Vencimento')
    boleto.drawString(41*mm, 209*mm, 'Carteira')
    boleto.drawString(56*mm, 209*mm, 'Espécie')
    boleto.drawString(71*mm, 209*mm, 'Quantidade')
    boleto.drawString(71*mm, 205*mm, '')
    
    boleto.drawString(123*mm, 206*mm, 'x')
    
    boleto.drawString(124*mm, 209*mm, 'Valor')
    boleto.drawString(124*mm, 205*mm, '')
    boleto.drawString(160*mm, 209*mm, 'Nosso número')
    boleto.drawString(160*mm, 201*mm, '(=) Valor do documento')
    boleto.drawString(160*mm, 193*mm, '(-) Desconto/Abatimento')
    boleto.drawString(160*mm, 185*mm, '(-) Outras deduções')
    boleto.drawString(160*mm, 177*mm, '(+) Mora/Multa')
    boleto.drawString(160*mm, 169*mm, '(+) Outros acréscimos')
    boleto.drawString(160*mm, 161*mm, '(=) Valor cobrado')
    boleto.drawString(7*mm, 154*mm, 'Sacado')
    boleto.drawString(7*mm, 140*mm, 'Sacador/avalista')
    boleto.drawString(135*mm, 140*mm, 'Código de baixa')
    boleto.drawString(161*mm, 134*mm, 'Autenticação mecânica')
    
    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(20*mm, 270*mm, sacado)
    boleto.drawString(20*mm, 266*mm, endereco)
    boleto.drawString(20*mm, 262*mm, endereco1)
    boleto.drawString(20*mm, 258*mm, documento)
    boleto.drawString(20*mm, 254*mm, emissao)
    boleto.drawString(96*mm, 258*mm, valor)
    boleto.drawString(96*mm, 254*mm, vencimento)
    
    boleto.drawString(7*mm, 221*mm, cedente)
    boleto.drawString(180*mm, 221*mm, vencimento)
    boleto.drawString(7*mm, 213*mm, emissao)
    boleto.drawString(41*mm, 213*mm, documento)
    boleto.drawString(71*mm, 213*mm, especiedoc)
    boleto.drawString(91*mm, 213*mm, aceite)
    boleto.drawString(114*mm, 213*mm, emissao)
    boleto.drawString(160*mm, 213*mm, agencia)
    boleto.drawString(7*mm, 205*mm, usobanco)
    boleto.drawString(41*mm, 205*mm, carteira)
    boleto.drawString(56*mm, 205*mm, especiemon)
    boleto.drawString(160*mm, 189*mm, '')
    boleto.drawString(160*mm, 205*mm, nossonumero)
    boleto.drawString(7*mm, 197*mm, valorexpresso)
    boleto.drawString(177*mm, 197*mm, valor)
    boleto.drawString(20*mm, 185*mm, juros)
    boleto.drawString(160*mm, 181*mm, '')
    boleto.drawString(7*mm, 177*mm, observacao1)
    boleto.drawString(7*mm, 171*mm, observacao2)
    boleto.drawString(7*mm, 164*mm, observacao3)
    boleto.drawString(160*mm, 173*mm, '')
    boleto.drawString(160*mm, 165*mm, '')
    boleto.drawString(160*mm, 157*mm, '')
    boleto.drawString(7*mm, 151*mm, sacado)
    boleto.drawString(7*mm, 147*mm, endereco)
    boleto.drawString(7*mm, 144*mm, endereco1)
    
    # linha dividindo o canhoto
    boleto.setStrokeColor(colors.gray)
    boleto.line(0, 240*mm, 210*mm, 240*mm)
    # linha dividindo o recibo do sacado e ficha de compensação
    boleto.line(0, 122*mm, 210*mm, 122*mm)
    
    boleto.setStrokeColor(colors.black)
    boleto.setFillColor(colors.black)
    
    # abaixo da logo do banco
    boleto.line(7*mm, 228*mm, 200*mm, 228*mm)
    # separadores cedente, data do documento e uso do banco
    boleto.line(7*mm, 220*mm, 200*mm, 220*mm)
    boleto.line(7*mm, 212*mm, 200*mm, 212*mm)
    boleto.line(7*mm, 204*mm, 200*mm, 204*mm)
    # separador do número do banco
    boleto.line(42*mm, 228*mm, 42*mm, 234*mm)
    boleto.line(56*mm, 228*mm, 56*mm, 234*mm)
    
    # separador coluna cedente e vencimento
    boleto.line(158*mm, 228*mm, 158*mm, 156*mm)
    
    # separadores do bloco acima
    boleto.line(40*mm, 204*mm, 40*mm, 220*mm)
    boleto.line(55*mm, 204*mm, 55*mm, 212*mm)
    boleto.line(70*mm, 204*mm, 70*mm, 220*mm)
    boleto.line(90*mm, 212*mm, 90*mm, 220*mm)
    boleto.line(113*mm, 212*mm, 113*mm, 220*mm)
    boleto.line(123*mm, 204*mm, 123*mm, 212*mm)
    
    # separador em branco da quantidade e valor
    boleto.setStrokeColor(colors.white)
    boleto.line(123*mm, 205*mm, 123*mm, 208*mm)
    boleto.setStrokeColor(colors.black)
    
    boleto.line(158*mm, 196*mm, 200*mm, 196*mm)
    boleto.line(158*mm, 188*mm, 200*mm, 188*mm)
    boleto.line(158*mm, 180*mm, 200*mm, 180*mm)
    boleto.line(158*mm, 172*mm, 200*mm, 172*mm)
    boleto.line(158*mm, 164*mm, 200*mm, 164*mm)
    boleto.line(7*mm, 156*mm, 200*mm, 156*mm)
    
    # Divisor Recibo sacado e autenticação mecânica
    boleto.line(7*mm, 139*mm, 200*mm, 139*mm)
    boleto.line(144*mm, 126*mm, 144*mm, 133*mm)
    boleto.line(144*mm, 133*mm, 200*mm, 133*mm)
    boleto.line(200*mm, 126*mm, 200*mm, 133*mm)
    
    
    # Ficha de compensação
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
    boleto.drawString(7*mm, 108*mm, 'Local de pagamento')
    boleto.drawString(160*mm, 108*mm, 'Vencimento')
    boleto.drawString(7*mm, 100*mm, 'Cedente')
    boleto.drawString(7*mm, 92*mm, 'Data do documento')
    boleto.drawString(41*mm, 92*mm, 'No. do documento')
    boleto.drawString(71*mm, 92*mm, 'Espécie doc')
    boleto.drawString(91*mm, 92*mm, 'Aceite')
    boleto.drawString(114*mm, 92*mm, 'Data do processamento')
    boleto.drawString(160*mm, 100*mm, 'Agência/Código do cedente')
    boleto.drawString(7*mm, 84*mm, 'Uso do banco')
    boleto.drawString(41*mm, 84*mm, 'Carteira')
    boleto.drawString(56*mm, 84*mm, 'Espécie')
    boleto.drawString(71*mm, 84*mm, 'Quantidade')
    boleto.drawString(123*mm, 81*mm, 'x')
    boleto.drawString(124*mm, 84*mm, 'Valor')
    boleto.drawString(160*mm, 92*mm, 'Nosso número')
    boleto.drawString(160*mm, 84*mm, '(=) Valor do documento')
    boleto.drawString(160*mm, 76*mm, '(-) Desconto/Abatimento')
    boleto.drawString(160*mm, 68*mm, '(-) Outras deduções')
    boleto.drawString(160*mm, 60*mm, '(+) Mora/Multa')
    boleto.drawString(160*mm, 52*mm, '(+) Outros acréscimos')
    boleto.drawString(160*mm, 44*mm, '(=) Valor cobrado')
    boleto.drawString(7*mm, 36*mm, 'Sacado')
    boleto.drawString(7*mm, 23*mm, 'Sacador/avalista')
    boleto.drawString(135*mm, 23*mm, 'Código de baixa')
    boleto.drawString(161*mm, 20*mm, 'Autenticação mecânica')
    boleto.drawString(7*mm, 76*mm, 'Instruções (Todas informações deste BOLETO são de exclusiva responsabilidade do cedente)')
    
    boleto.setFont('Helvetica-Bold',14)
    boleto.drawString(58*mm, 112*mm, linhadigitavel)
    
    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(7*mm, 104*mm, localpagamento)
    boleto.drawString(180*mm, 104*mm, vencimento)
    boleto.drawString(7*mm, 96*mm, cedente)
    boleto.drawString(7*mm, 88*mm, emissao)
    boleto.drawString(41*mm, 88*mm, documento)
    boleto.drawString(71*mm, 88*mm, especiedoc)
    boleto.drawString(91*mm, 88*mm, aceite)
    boleto.drawString(114*mm, 88*mm, emissao)
    boleto.drawString(160*mm, 96*mm, agencia)
    boleto.drawString(7*mm, 80*mm, usobanco)
    boleto.drawString(41*mm, 80*mm, carteira)
    boleto.drawString(56*mm, 80*mm, especiemon)
    boleto.drawString(71*mm, 80*mm, '')
    boleto.drawString(124*mm, 80*mm, '')
    boleto.drawString(160*mm, 88*mm, nossonumero)
    
    boleto.drawString(7*mm, 72*mm, valorexpresso)
    boleto.drawString(177*mm, 80*mm, valor)
    boleto.drawString(160*mm, 72*mm, '')
    boleto.drawString(20*mm, 60*mm, juros)
    boleto.drawString(7*mm, 54*mm, observacao1)
    boleto.drawString(7*mm, 48*mm, observacao2)
    boleto.drawString(7*mm, 41*mm, observacao3)
    boleto.drawString(160*mm, 56*mm, '')
    boleto.drawString(160*mm, 48*mm, '')
    boleto.drawString(160*mm, 40*mm, '')
    boleto.drawString(160*mm, 32*mm, '')
    boleto.drawString(7*mm, 33*mm, sacado)
    boleto.drawString(7*mm, 29*mm, endereco)
    boleto.drawString(7*mm, 26*mm, endereco1)
    
    # Identificação das partes
    
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM_ID)
    boleto.drawString(165*mm, 140*mm, 'Recibo do sacado')
    boleto.drawString(163*mm, 23*mm, 'Ficha de compensação')
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
    
    # abaixo da logo do banco
    boleto.line(7*mm, 111*mm, 200*mm, 111*mm)
    
    # separador do número do banco
    boleto.line(42*mm, 111*mm, 42*mm, 116*mm)
    boleto.line(56*mm, 111*mm, 56*mm, 116*mm)
    
    # separador coluna local de pagamento e vencimento
    boleto.line(158*mm, 39*mm, 158*mm, 111*mm)
    
    # separadores local de pagamento, cedente, data do documento e uso do banco
    boleto.line(7*mm, 103*mm, 200*mm, 103*mm)
    boleto.line(7*mm, 95*mm, 200*mm, 95*mm)
    boleto.line(7*mm, 87*mm, 200*mm, 87*mm)
    boleto.line(7*mm, 79*mm, 200*mm, 79*mm)
    
    # separadores do bloco acima
    boleto.line(40*mm, 79*mm, 40*mm, 95*mm)
    boleto.line(55*mm, 79*mm, 55*mm, 87*mm)
    boleto.line(70*mm, 79*mm, 70*mm, 95*mm)
    boleto.line(90*mm, 87*mm, 90*mm, 95*mm)
    boleto.line(113*mm, 87*mm, 113*mm, 95*mm)
    boleto.line(123*mm, 79*mm, 123*mm, 87*mm)
    
    # separador em branco da quantidade e valor
    boleto.setStrokeColor(colors.white)
    boleto.line(123*mm, 80*mm, 123*mm, 83*mm)
    boleto.setStrokeColor(colors.black)
    
    # separadora valor documento, desconto abatimento
    boleto.line(158*mm, 71*mm, 200*mm, 71*mm)
    boleto.line(158*mm, 63*mm, 200*mm, 63*mm)
    boleto.line(158*mm, 55*mm, 200*mm, 55*mm)
    
    boleto.setLineWidth(0.2)
    boleto.line(158*mm, 47*mm, 200*mm, 47*mm)
    boleto.line(7*mm, 39*mm, 200*mm, 39*mm)
    
    # Divisor Ficha de compensação e autenticação mecânica
    boleto.setLineWidth(0.1)
    boleto.line(7*mm, 22*mm, 200*mm, 22*mm)
    
    boleto.line(144*mm, 12*mm, 144*mm, 19*mm)
    boleto.line(144*mm, 19*mm, 200*mm, 19*mm)
    boleto.line(200*mm, 12*mm, 200*mm, 19*mm)
    
    f = Frame(2*mm, mm, 5*mm, 20*mm, showBoundary=0)
    f.addFromList([I2of5(codigobarra,barWidth=0.89,ratio=2.2, xdim = 0.3*mm, checksum=0, bearers=0)], boleto)
    
    boleto.showPage()
    boleto.save()
    return response