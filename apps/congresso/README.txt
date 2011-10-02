#INSTALA��O

Dependencias:

 - cuboweb.apps.cms
 - cuboweb.apps.paginas
 - sorl.thumbnail
 - pagination
 

1. Para usar o modulo de congresso coloque-o (e suas depend�ncias) no INSTALLED_APPS

INSTALLED_APPS = (
    'cuboweb.apps.cms',
  	'cuboweb.apps.paginas',
  	'sorl.thumbnail',
 	'pagination',
	...
	'cuboweb.apps.congresso'
	...
)

2. Rode comando syncdb

>> python manage.py syncdb

3. Configura��o da Inscricao

Para habilitar a inscricao � necess�rio criar um model baseado no InscricaoBase, ex.:

from cuboweb.apps.congresso.models import InscricaoBase

class InscricaoEventoX(InscricaoBase):
	''' Defina aqui os atributos a mais que voc� deseja
	'''
	campo_extra1 = models.CharField(max_lenght=100)
	...
	# � necess�rio definir os metodos abaixo:
	
	def data_vencimento(self):
		''' Calculo da data do vencimento
		'''
		return datetime.now().strftime('%d/%m/%Y')
	
	def valor(self):
		''' Valor da inscricao
		'''
		return 30.00
	
	def nosso_numero(self):
		''' Padr�o unico do nosso numero
		'''
		return '%09d' % self.id

Depois � preciso configurar o settings.py com:

INSCRICAO_MODEL = 'nome_da_app.InscricaoEventoX' #Modelo que voc� criou para a inscricao
NOME_CONGRESSO = 'Evento X' #Nome do congresso

#Dados para gerar o boleto
AGENCIA = '0000' #numero da agencia
CONTA = '0000' #numero da conta, sem o digito
DV_CONTA = '0' #digito verificador da conta
CONTA_CEDENTE = '00000' #codigo do cendente (somente CEF)

CPF_CNPJ = '' #CPF/CNPJ do recebedor do dinheiro
ENDERECO_REALIZADOR = '' #Endereco do recebedor do dinheiro
CIDADE_UF = '' #Cidade e Estado do recebedor
RAZAO_SOCIAL = '' #Raz�o social do recebedor 