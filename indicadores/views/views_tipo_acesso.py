from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import TipoAcesso
from ..forms import TipoAcessoForm


def tipo_acesso_list(request):
    return render(request, 'tipo_acesso/list.html', {'objetos': TipoAcesso.objects.all()})


def tipo_acesso_create(request):
    form = TipoAcessoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tipo de Acesso criado.')
        return redirect('ind:tipo_acesso_list')
    return render(request, 'tipo_acesso/form.html', {'form': form, 'titulo': 'Novo Tipo de Acesso'})


def tipo_acesso_update(request, pk):
    obj = get_object_or_404(TipoAcesso, pk=pk)
    form = TipoAcessoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tipo de Acesso atualizado.')
        return redirect('ind:tipo_acesso_list')
    return render(request, 'tipo_acesso/form.html', {'form': form, 'titulo': 'Editar Tipo de Acesso'})


def tipo_acesso_delete(request, pk):
    obj = get_object_or_404(TipoAcesso, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tipo de Acesso excluído.')
        return redirect('ind:tipo_acesso_list')
    return render(request, 'tipo_acesso/confirm_delete.html', {'objeto': obj, 'titulo': 'Tipo de Acesso'})
