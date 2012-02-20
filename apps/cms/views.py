from django.template import Context, loader
from django.http import HttpResponseServerError
from django.conf import settings

from cuboweb.apps.cms.forms import ContatoForm
from django.views.generic.simple import direct_to_template
from cuboweb.apps.paginas.models import Pagina

def server_error(request, template_name='cms/500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL
    })))

def not_found(request, template_name='cms/400.html'):
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL
    })))

def contato(request):
    css_class = 'contato'
    try:
        pagina = Pagina.objects.get(slug='contato')
    except Pagina.DoesNotExist:
        pagina = None
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.notify()
            return direct_to_template(request,'cms/contato_enviado.html',locals())
    else:
        form = ContatoForm()
    return direct_to_template(request,'cms/contato.html',locals())