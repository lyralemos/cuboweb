README
======

Sobre
----------

Esse projeto possui a base para os projetos desenvolvidos pela cuboestudioweb.com
Provavelmente não será de grande utilidade para outras pessoas.
Atualmente consiste de 4 apps:
- cuboweb.apps.cms -> app básica que define o model Base, RemovableFileField, RemovableImageField 
- cuboweb.apps.noticias -> app de notícias que inclui feed rss e integração com tinymce(django-tinymce) no admin
- cuboweb.apps.paginas -> app de páginas similar as flatpages do django, porém mais simples.
- cuboweb.apps.congresso -> app para gerenciar congressos simples (inclui geração de boletos do bb e caixa).

Dependencias
------------
django 1.3

Instalação
----------

Baixe o codigo do repositorio::

   git clone https://github.com/lyralemos/cuboweb.git cuboweb

em seguida copie para uma pasta que esteja no pythonpath

TODO
====

- Deixar o app 'instalável';
- Migrar o restante dos bancos;