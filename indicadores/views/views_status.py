from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Status
from ..forms import StatusForm


def status_list(request):
    return render(request, 'status/list.html', {'objetos': Status.objects.all()})


def status_create(request):
    form = StatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Status criado com sucesso.')
        return redirect('ind:status_list')
    return render(request, 'status/form.html', {'form': form, 'titulo': 'Novo Status'})


def status_update(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    form = StatusForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Status atualizado.')
        return redirect('ind:status_list')
    return render(request, 'status/form.html', {'form': form, 'titulo': 'Editar Status'})


def status_delete(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Status excluído.')
        return redirect('ind:status_list')
    return render(request, 'status/confirm_delete.html', {'objeto': obj, 'titulo': 'Status'})
