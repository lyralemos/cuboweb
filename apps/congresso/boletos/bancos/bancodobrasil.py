# -*- coding: utf-8
from datetime import date

class bancodobrasil():
    
    def __init__(self):
        pass
        
    
    def getdadosboleto(self,formatconvenio,formatnnumero,dados):
        
        """
         Retorna dados do boleto 
         
        """
        dados['codigobanco']= '001'
        dados['nummoeda'] = '9'
         
        dados['livre_zeros'] = '000000'

        fator_vencimento = self.fator_vencimento(dados["data_vencimento"])  
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = self.formata_numero(str(vtotal),10,0,'valor')
        agencia = self.formata_numero(dados["agencia"],4,0)   
        conta = self.formata_numero(dados["conta"],8,0)


        boleto = dict()
        boleto = dados
        
        
        
        boleto['codigobancodv'] = self.geraCodigoBanco(dados['codigobanco'])
        boleto['agenciaconta'] = "%s-%s / %s-%s" %(agencia,self.modulo_11(agencia),conta,self.modulo_11(conta))
        boleto['valor'] = vtotal.replace('.',',')
        
        
        

        
        
        # Carteira 18 com Convênio de 8 dígitos
        if formatconvenio == 8:            
            convenio = self.formata_numero(dados['convenio'],8,0,'convenio')
            
            # Nossó numero de até 9 dígitos 
            nossonumero = self.formata_numero(dados['nosso_numero'],9,0)
            boleto['nossonumero'] = nossonumero
            boleto['convenio'] = convenio
        
               
            dv = self.modulo_11("%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                    dados['nummoeda'],
                                                    fator_vencimento,
                                                    valor,
                                                    dados['livre_zeros'],
                                                    convenio,
                                                    nossonumero,
                                                    dados['carteira']))
                                                    
            linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                           dados['nummoeda'],
                                           dv,
                                           fator_vencimento,
                                           valor,
                                           dados['livre_zeros'],
                                           convenio,
                                           nossonumero,
                                           dados['carteira'])
            boleto['codigobarra'] = linha 
            boleto['linhadigitavel'] = self.monta_linha_digitavel(linha)
              
            # Montando o nosso numero que aparecerá no boleto
            nossonumero = "%s%s-%s" %(convenio,nossonumero, self.modulo_11("%s%s"%(convenio,nossonumero)))
            boleto['nossonumeroformatado'] = nossonumero
            return  boleto                                   
            
            
        # Carteira 18 com Convênio de 7 dígitos
        if formatconvenio == 7:            
            convenio = self.formata_numero(dados['convenio'],7,0,'convenio')
            
            # Nossó numero de até 10 dígitos 
            nossonumero = self.formata_numero(dados['nosso_numero'],10,0)
            boleto['convenio'] = convenio
            boleto['nossonumero'] = nossonumero
            
            dv = self.modulo_11("%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                      dados['nummoeda'],
                                                      fator_vencimento,
                                                      valor,
                                                      dados['livre_zeros'],
                                                      convenio,
                                                      nossonumero,
                                                      dados['carteira']))
          
            
            linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                           dados['nummoeda'],
                                           dv,
                                           fator_vencimento,
                                           valor,
                                           dados['livre_zeros'],
                                           convenio,
                                           nossonumero,
                                           dados['carteira'])

            boleto['codigobarra'] = linha 
            boleto['linhadigitavel'] = self.monta_linha_digitavel(linha)            
            # Montando o nosso numero que aparecerá no boleto
            nossonumero = "%s%s" %(convenio,nossonumero)
            boleto['nossonumeroformatado'] = nossonumero
                                    
            return boleto     
        
        # Carteira 18 com Convênio de 6 dígitos 
        if formatconvenio == 6:            
            convenio = self.formata_numero(dados['convenio'],6,0,'convenio')
            
            if formatnnumero == 1:
                
                # Nossó numero de até 5 dígitos 
                nossonumero = self.formata_numero(dados['nosso_numero'],5,0)   
                boleto['nossonumero'] = nossonumero             
                dv = self.modulo_11("%s%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                          dados['nummoeda'],
                                                          fator_vencimento,
                                                          valor,
                                                          convenio,
                                                          nossonumero,
                                                          agencia,
                                                          conta,                                                          
                                                          dados['carteira']))

                linha = "%s%s%s%s%s%s%s%s%s%s" %( dados['codigobanco'],
                                                  dados['nummoeda'],
                                                  dv,
                                                  fator_vencimento,
                                                  valor,
                                                  convenio,                                                 
                                                  nossonumero,
                                                  agencia,
                                                  conta,
                                                  dados['carteira'])
                boleto['codigobarra'] = linha 
                boleto['linhadigitavel'] = self.monta_linha_digitavel(linha)   
                # montando o nosso numero que aparecerá no boleto
                nossonumero = "%s%s-%s" %(convenio,
                                          nossonumero,
                                          self.modulo_11("%s%s" %(convenio,
                                                                  nossonumero))) 
                boleto['nossonumeroformatado'] = nossonumero
                
                return  boleto
                                                                                  
                
            if formatnnumero == 2:
                
                # Nosso número de até 17 dígitos
                
                nservico = '21'
                nossonumero = self.formata_numero(dados['nosso_numero'],17,0)
                boleto['nossonumero'] = nossonumero  
                
                dv = self.modulo_11("%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                          dados['nummoeda'],
                                                          fator_vencimento,
                                                          valor,
                                                          convenio,
                                                          nossonumero,
                                                          nservico))
                
                linha = "%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                             dados['nummoeda'],
                                             dv,
                                             fator_vencimento,
                                             valor,
                                             convenio,                                                 
                                             nossonumero,
                                             nservico)
                boleto['codigobarra'] = linha                
                boleto['linhadigitavel'] = self.monta_linha_digitavel(linha)   
                boleto['nossonumeroformatado'] = nossonumero
                return boleto
                
                
                                                             
                                                             
         
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
                digito = 'X'
            
            if len(num) == 43:
                if digito == 0 or digito == 'X' or digito > 9:
                    digito = 1
            
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
    

