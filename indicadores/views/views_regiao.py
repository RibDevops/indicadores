from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import RegiaoCidade
from ..forms import RegiaoCidadeForm


def regiao_list(request):
    return render(request, 'regiao/list.html', {'objetos': RegiaoCidade.objects.select_related('estado').all()})


def regiao_create(request):
    form = RegiaoCidadeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Região criada.')
        return redirect('ind:regiao_list')
    return render(request, 'regiao/form.html', {'form': form, 'titulo': 'Nova Região'})


def regiao_update(request, pk):
    obj = get_object_or_404(RegiaoCidade, pk=pk)
    form = RegiaoCidadeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Região atualizada.')
        return redirect('ind:regiao_list')
    return render(request, 'regiao/form.html', {'form': form, 'titulo': 'Editar Região'})


def regiao_delete(request, pk):
    obj = get_object_or_404(RegiaoCidade, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Região excluída.')
        return redirect('ind:regiao_list')
    return render(request, 'regiao/confirm_delete.html', {'objeto': obj, 'titulo': 'Região'})
