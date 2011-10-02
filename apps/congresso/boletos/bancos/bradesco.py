# -*- coding: utf-8

from datetime import date

class bradesco:    
    def __init__(self):
        pass    
    
    
    def getdadosboleto(self,dados):
        
        dados['codigobanco'] = '237'
        dados['nummoeda'] = '9'
        
        boleto = dict()
        boleto = dados
        
        boleto['codigobancodv'] = self.geraCodigoBanco(dados['codigobanco'])
        fator_vencimento = self.fator_vencimento(dados['data_vencimento'])
        
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = self.formata_numero(str(vtotal),10,0,'valor')

        boleto['valor'] = vtotal.replace('.',',')        
        agencia = self.formata_numero(dados['agencia'],4,0)   
        conta = self.formata_numero(dados['conta'],6,0)
        conta_dv = self.formata_numero(dados['conta_dv'],1,0)
        
        # nosso número (sem dv) é 11 digitos
        nnum = "%s%s" %(self.formata_numero(dados['carteira'],2,0),self.formata_numero(dados['nosso_numero'],11,0))
        
        # dv do nosso número
        dv_nosso_numero = self.digitoVerificador_nossonumero(nnum)
        
        # conta cedente (sem dv) é 7 digitos        
        boleto['conta_cedente'] = self.formata_numero(dados['conta_cedente'],7,0)
        boleto['conta_devente_dv'] = self.formata_numero(dados['conta_cedente_dv'],1,0)
        
        boleto['nossonumero'] = nnum
        boleto['dvnossonumero'] = dv_nosso_numero
        
        # 43 numeros para o calculo do digito verificador do codigo de barras
        dv = self.digitoVerificador_barra("%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                                                   dados['nummoeda'],
                                                                   fator_vencimento,
                                                                   valor,
                                                                   agencia,
                                                                   nnum,
                                                                   boleto['conta_cedente'],
                                                                   '0'))
                                                                   

          # Numero para o codigo de barras com 44 digitos
        linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                     dados['nummoeda'],
                                     dv,
                                     fator_vencimento,
                                     valor,
                                     agencia,
                                     nnum,
                                     boleto['conta_cedente'],'0')

        nossonumero = "%s/%s-%s" %(nnum[0:2],nnum[2:],dv_nosso_numero)
        agencia_codigo = "%s-%s / %s-%s" %(agencia,dados['agencia_dv'],boleto['conta_cedente'],boleto['conta_devente_dv'])

        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = self.monta_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero

        
        
        return boleto
        
        
        
        
        
        
        
        
    
    def digitoVerificador_nossonumero(self,numero):
        resto2 = self.modulo_11(numero,7,1)
        digito = 11 - resto2
        if digito == 10:
            dv = 'P'
        elif digito == 11:
            dv = 0
        else:
            dv = digito
         
        return dv
       
       
    def digitoVerificador_barra(self,numero):
        resto2 = self.modulo_11(numero,9,1)
        if resto2 == 0 or resto2 == 1 or resto2 == 10:
            dv = 1
        else:
            dv = 11 - resto2
        return dv
            
            
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
                          
                