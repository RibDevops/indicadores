from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Servidor, DataCompra, DataVisita
from ..forms import ServidorForm


def servidor_list(request):
    servidores = Servidor.objects.select_related('om', 'status', 'tipo_acesso').all()
    return render(request, 'servidor/list.html', {'objetos': servidores})


def servidor_detail(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    compras = DataCompra.objects.filter(servidor=obj).order_by('-data_compra')
    visitas = DataVisita.objects.filter(servidor=obj).order_by('-data_visita')
    return render(request, 'servidor/detail.html', {
        'objeto': obj,
        'compras': compras,
        'visitas': visitas,
    })


def servidor_create(request):
    form = ServidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Servidor criado.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/form.html', {'form': form, 'titulo': 'Novo Servidor'})


def servidor_update(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    form = ServidorForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Servidor atualizado.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/form.html', {'form': form, 'titulo': 'Editar Servidor'})


def servidor_delete(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Servidor excluído.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/confirm_delete.html', {'objeto': obj, 'titulo': 'Servidor'})
