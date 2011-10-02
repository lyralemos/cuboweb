# -*- coding: utf-8

from datetime import date

class bancoreal:
    def __init__(self):
        pass
        
    

    def getboletodados(self,dados):        
        
        dados['codigobanco'] = '356'
        dados['codigobancodv'] = self.geraCodigoBanco(dados['codigobanco'])
        dados['nummoeda'] = '9'
        
        fator_vencimento = self.fator_vencimento(dados['data_vencimento'])
        
        boleto = dict()
        boleto = dados
        
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = self.formata_numero(str(vtotal),10,0,'valor')

        boleto['valor'] = vtotal.replace('.',',')
        
        agencia = self.formata_numero(dados['agencia'],4,0)   
        conta = self.formata_numero(dados['conta'],7,0)
        nossonumero = self.formata_numero(dados['nosso_numero'],13,0)
        # Digitao - Digito de Cobranca do banco Real
        digitao_cobranca = self.modulo_10("%s%s%s" %(nossonumero,agencia,conta))
        
        linha = "%s%s0%s%s%s%s%s%s" %(dados['codigobanco'],
                                      dados['nummoeda'],
                                      fator_vencimento,
                                      valor,
                                      agencia,
                                      conta,
                                      digitao_cobranca,
                                      nossonumero)
        linha = self.dvBarra(linha)
        
        
        agencia_codigo = "%s/%s/%s" %(agencia,conta,digitao_cobranca)


        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = self.monta_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero
        
        
        return boleto
        
        
    def dvBarra(self,numero):
        pesos = '43290876543298765432987654329876543298765432'
        if len(numero) == 44:
            soma = 0
            for i in range(len(numero)):
                soma=soma+(int(numero[i]) * int(pesos[i]))
                
            num_temp = 11 - (soma % 11)
            if num_temp >= 10:
                num_temp = 1
            
            l = list(numero)    
            l[4] = str(num_temp)
            numero = str()
            for c in l:
                numero = numero+"%s" %c
                
        return numero
        
    
    def fator_vencimento(self,data):

        data = data.split("/")

        ano = data[2]
        mes = data[1]
        dia = data[0]

        tempo = abs(date(1997,10,07) - date(int(ano),int(mes),int(dia)))

        return tempo.days


    def formata_numero(self,numero,loop,insert,tipo="geral"):
        if tipo == "geral":
            numero = numero.replace(",","").replace('.','')
            while len(numero) < loop:
                numero="%s%s" %(insert,numero)
        if tipo == "valor":
            numero = numero.replace(",","").replace('.','')
            while len(numero) < loop:
                numero = "%s%s" %(insert,numero)
        if tipo == "convenio":
            while len(numero) < loop:
                numero = "%s%s" %(numero,insert)
        return numero
            
             
    
    def modulo_10(self,num):
        numtotal10=str()
        fator = 2
        for i in range(len(str(num))).__reversed__():
            numeros = int(num[i])
            parcial10 = numeros * fator
            numtotal10 = numtotal10+ "%s" %parcial10
            if fator == 2:
                fator = 1
            else:
                fator = 2
        soma = 0
        for i in range(len(numtotal10)).__reversed__():
            numeros = int(numtotal10[i])
            soma=soma+numeros
        resto = soma % 10
        digito = 10 - resto
        if resto == 0:
            digito = 0
        return digito
        
    
    def modulo_11(self,num,base=9,r=0):
        soma=0
        fator=2
        for i in range(len(str(num))).__reversed__():
            numeros = int(num[i])
            parcial10 = numeros * fator
            soma = soma+parcial10
            if fator == base:
                fator = 1
            fator=fator+1
        if r == 0:
            soma = soma * 10
            digito = soma % 11
            if digito == 10:
                digito = 0
            return digito     
        if r == 1:
            resto = soma % 11
            return resto
    
    
    def monta_linha_digitavel(self,linha):

        """
         Posição    Conteúdo
         1 a 3    Número do banco
         4        Código da Moeda - 9 para Real
         5        Digito verificador do Código de Barras
         6 a 19   Valor (12 inteiros e 2 decimais)
         20 a 44  Campo Livre definido por cada banco

         """

        p1 = linha[0:4]
        p2 = linha[19:24]        
        p3 = self.modulo_10("%s%s"%(p1,p2))
        p4 = "%s%s%s" %(p1,p2,p3)
        p5 = p4[0:5]
        p6 = p4[5:]
        campo1 = "%s.%s" %(p5,p6)

        p1 = linha[24:34]
        p2 = self.modulo_10(p1)
        p3 = "%s%s" %(p1,p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo2 = "%s.%s" %(p4,p5)

        p1 = linha[34:44]
        p2 = self.modulo_10(p1)
        p3 = "%s%s" %(p1,p2)
        p4 = p3[0:5]
        p5 = p3[5:]
        campo3 = "%s.%s" %(p4,p5)
        campo4 = linha[4]        
        campo5 = linha[5:19]

        return "%s %s %s %s %s" %(campo1,campo2,campo3,campo4,campo5)
            
    def geraCodigoBanco(self,numero):
        parte1 = numero[0:4]
        parte2 = self.modulo_11(parte1)
        return "%s-%s" %(parte1,parte2)
            
            