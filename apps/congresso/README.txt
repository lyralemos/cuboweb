#INSTALAÇÃO

Dependencias:

 - cuboweb.apps.cms
 - cuboweb.apps.paginas
 - sorl.thumbnail
 - pagination
 

1. Para usar o modulo de congresso coloque-o (e suas dependências) no INSTALLED_APPS

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

3. Configuração da Inscricao

Para habilitar a inscricao é necessário criar um model baseado no InscricaoBase, ex.:

from cuboweb.apps.congresso.models import InscricaoBase

class InscricaoEventoX(InscricaoBase):
	''' Defina aqui os atributos a mais que você deseja
	'''
	campo_extra1 = models.CharField(max_lenght=100)
	...
	# É necessário definir os metodos abaixo:
	
	def data_vencimento(self):
		''' Calculo da data do vencimento
		'''
		return datetime.now().strftime('%d/%m/%Y')
	
	def valor(self):
		''' Valor da inscricao
		'''
		return 30.00
	
	def nosso_numero(self):
		''' Padrão unico do nosso numero
		'''
		return '%09d' % self.id

Depois é preciso configurar o settings.py com:

INSCRICAO_MODEL = 'nome_da_app.InscricaoEventoX' #Modelo que você criou para a inscricao
NOME_CONGRESSO = 'Evento X' #Nome do congresso

#Dados para gerar o boleto
AGENCIA = '0000' #numero da agencia
CONTA = '0000' #numero da conta, sem o digito
DV_CONTA = '0' #digito verificador da conta
CONTA_CEDENTE = '00000' #codigo do cendente (somente CEF)

CPF_CNPJ = '' #CPF/CNPJ do recebedor do dinheiro
ENDERECO_REALIZADOR = '' #Endereco do recebedor do dinheiro
CIDADE_UF = '' #Cidade e Estado do recebedor
RAZAO_SOCIAL = '' #Razão social do recebedor 