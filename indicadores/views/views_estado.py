from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Estado
from ..forms import EstadoForm


def estado_list(request):
    return render(request, 'estado/list.html', {'objetos': Estado.objects.select_related('pais').all()})


def estado_create(request):
    form = EstadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estado criado.')
        return redirect('ind:estado_list')
    return render(request, 'estado/form.html', {'form': form, 'titulo': 'Novo Estado'})


def estado_update(request, pk):
    obj = get_object_or_404(Estado, pk=pk)
    form = EstadoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estado atualizado.')
        return redirect('ind:estado_list')
    return render(request, 'estado/form.html', {'form': form, 'titulo': 'Editar Estado'})


def estado_delete(request, pk):
    obj = get_object_or_404(Estado, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Estado excluído.')
        return redirect('ind:estado_list')
    return render(request, 'estado/confirm_delete.html', {'objeto': obj, 'titulo': 'Estado'})
