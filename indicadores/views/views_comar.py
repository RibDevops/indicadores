from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Comar
from ..forms import ComarForm


def comar_list(request):
    return render(request, 'comar/list.html', {'objetos': Comar.objects.select_related('regiao_cidade').all()})


def comar_create(request):
    form = ComarForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'COMAR criado.')
        return redirect('ind:comar_list')
    return render(request, 'comar/form.html', {'form': form, 'titulo': 'Novo COMAR'})


def comar_update(request, pk):
    obj = get_object_or_404(Comar, pk=pk)
    form = ComarForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'COMAR atualizado.')
        return redirect('ind:comar_list')
    return render(request, 'comar/form.html', {'form': form, 'titulo': 'Editar COMAR'})


def comar_delete(request, pk):
    obj = get_object_or_404(Comar, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'COMAR excluído.')
        return redirect('ind:comar_list')
    return render(request, 'comar/confirm_delete.html', {'objeto': obj, 'titulo': 'COMAR'})
