from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import OM
from ..forms import OMForm


def om_list(request):
    # Carrega servidor junto para exibir na listagem sem queries extras
    objetos = OM.objects.select_related('comar', 'pais', 'tipo_elo', 'servidor').all()
    return render(request, 'om/list.html', {'objetos': objetos})


def om_create(request):
    form = OMForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'OM criada.')
        return redirect('ind:om_list')
    return render(request, 'om/form.html', {'form': form, 'titulo': 'Nova OM'})


def om_update(request, pk):
    obj = get_object_or_404(OM, pk=pk)
    form = OMForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'OM atualizada.')
        return redirect('ind:om_list')
    return render(request, 'om/form.html', {'form': form, 'titulo': 'Editar OM'})


def om_delete(request, pk):
    obj = get_object_or_404(OM, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'OM excluída.')
        return redirect('ind:om_list')
    return render(request, 'om/confirm_delete.html', {'objeto': obj, 'titulo': 'OM'})
