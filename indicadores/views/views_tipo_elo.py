from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import TipoElo
from ..forms import TipoEloForm


def tipo_elo_list(request):
    return render(request, 'tipo_elo/list.html', {'objetos': TipoElo.objects.all()})


def tipo_elo_create(request):
    form = TipoEloForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tipo de Elo criado.')
        return redirect('ind:tipo_elo_list')
    return render(request, 'tipo_elo/form.html', {'form': form, 'titulo': 'Novo Tipo de Elo'})


def tipo_elo_update(request, pk):
    obj = get_object_or_404(TipoElo, pk=pk)
    form = TipoEloForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tipo de Elo atualizado.')
        return redirect('ind:tipo_elo_list')
    return render(request, 'tipo_elo/form.html', {'form': form, 'titulo': 'Editar Tipo de Elo'})


def tipo_elo_delete(request, pk):
    obj = get_object_or_404(TipoElo, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tipo de Elo excluído.')
        return redirect('ind:tipo_elo_list')
    return render(request, 'tipo_elo/confirm_delete.html', {'objeto': obj, 'titulo': 'Tipo de Elo'})
