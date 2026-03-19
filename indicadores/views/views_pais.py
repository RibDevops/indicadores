from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Pais
from ..forms import PaisForm


def pais_list(request):
    return render(request, 'pais/list.html', {'objetos': Pais.objects.all()})


def pais_create(request):
    form = PaisForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'País criado.')
        return redirect('ind:pais_list')
    return render(request, 'pais/form.html', {'form': form, 'titulo': 'Novo País'})


def pais_update(request, pk):
    obj = get_object_or_404(Pais, pk=pk)
    form = PaisForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'País atualizado.')
        return redirect('ind:pais_list')
    return render(request, 'pais/form.html', {'form': form, 'titulo': 'Editar País'})


def pais_delete(request, pk):
    obj = get_object_or_404(Pais, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'País excluído.')
        return redirect('ind:pais_list')
    return render(request, 'pais/confirm_delete.html', {'objeto': obj, 'titulo': 'País'})
