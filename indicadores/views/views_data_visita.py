from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import DataVisita
from ..forms import DataVisitaForm


def data_visita_list(request):
    return render(request, 'data_visita/list.html', {'objetos': DataVisita.objects.select_related('servidor').all()})


def data_visita_create(request):
    form = DataVisitaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Data de Visita registrada.')
        return redirect('ind:data_visita_list')
    return render(request, 'data_visita/form.html', {'form': form, 'titulo': 'Nova Data de Visita'})


def data_visita_update(request, pk):
    obj = get_object_or_404(DataVisita, pk=pk)
    form = DataVisitaForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Data de Visita atualizada.')
        return redirect('ind:data_visita_list')
    return render(request, 'data_visita/form.html', {'form': form, 'titulo': 'Editar Data de Visita'})


def data_visita_delete(request, pk):
    obj = get_object_or_404(DataVisita, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Data de Visita excluída.')
        return redirect('ind:data_visita_list')
    return render(request, 'data_visita/confirm_delete.html', {'objeto': obj, 'titulo': 'Data de Visita'})
