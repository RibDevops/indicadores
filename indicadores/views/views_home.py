from django.shortcuts import render

from ..models import Comar, OM, Servidor
from .views_indicadores import _compute_indicadores


def home(request):
    context = {
        'total_servidores': Servidor.objects.count(),
        'total_om': OM.objects.count(),
        'total_comar': Comar.objects.count(),
        **_compute_indicadores(),
    }
    return render(request, 'home.html', context)
