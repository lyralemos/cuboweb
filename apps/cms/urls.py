'''
Created on 10/04/2010

@author: alexandre
'''
from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('',
    url(r'^contato/$','cuboweb.apps.cms.views.contato',name='contato_view')
)