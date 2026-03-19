from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import DataCompra
from ..forms import DataCompraForm


def data_compra_list(request):
    return render(request, 'data_compra/list.html', {'objetos': DataCompra.objects.select_related('servidor').all()})


def data_compra_create(request):
    form = DataCompraForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Data de Compra registrada.')
        return redirect('ind:data_compra_list')
    return render(request, 'data_compra/form.html', {'form': form, 'titulo': 'Nova Data de Compra'})


def data_compra_update(request, pk):
    obj = get_object_or_404(DataCompra, pk=pk)
    form = DataCompraForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Data de Compra atualizada.')
        return redirect('ind:data_compra_list')
    return render(request, 'data_compra/form.html', {'form': form, 'titulo': 'Editar Data de Compra'})


def data_compra_delete(request, pk):
    obj = get_object_or_404(DataCompra, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Data de Compra excluída.')
        return redirect('ind:data_compra_list')
    return render(request, 'data_compra/confirm_delete.html', {'objeto': obj, 'titulo': 'Data de Compra'})
