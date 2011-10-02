from cuboweb.apps.congresso.models import Patrocinio

def patrocinios(request):
    return {
        'patrocinios' : Patrocinio.objects.all()
    }