from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from ..models import Servidor, DataStatus, DataVisita
from ..forms import ServidorForm


def servidor_list(request):
    # om foi removido de Servidor — a relação agora é inversa (OM.servidor FK)
    # prefetch_related('oms') carrega as OMs vinculadas sem N+1 queries
    servidores = (
        Servidor.objects
        .select_related('status', 'tipo_acesso')
        .prefetch_related('oms')
        .all()
    )
    return render(request, 'servidor/list.html', {'objetos': servidores})


def servidor_detail(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    # OMs vinculadas a este servidor (relação inversa via OM.servidor FK)
    # Acesso via related_name='oms' definido em OM.servidor
    oms = obj.oms.select_related('comar', 'pais', 'tipo_elo').all()
    # Histórico de mudanças de status — usado para exibir linha do tempo
    # e para calcular dias por status via obj.dias_por_status()
    historico_status = DataStatus.objects.filter(servidor=obj).order_by('-data_status')
    visitas = DataVisita.objects.filter(servidor=obj).order_by('-data_visita')
    return render(request, 'servidor/detail.html', {
        'objeto': obj,
        'oms': oms,
        'historico_status': historico_status,
        'dias_por_status': obj.dias_por_status(),
        'visitas': visitas,
    })


def servidor_create(request):
    form = ServidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        # O signal post_save em indicadores/signals.py registra automaticamente
        # o status inicial em DataStatus após o save.
        messages.success(request, 'Servidor criado.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/form.html', {'form': form, 'titulo': 'Novo Servidor'})


def servidor_update(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    form = ServidorForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        # O signal post_save em indicadores/signals.py detecta se o status mudou
        # e, se sim, cria um novo registro em DataStatus automaticamente.
        messages.success(request, 'Servidor atualizado.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/form.html', {'form': form, 'titulo': 'Editar Servidor'})


def servidor_delete(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Servidor excluído.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/confirm_delete.html', {'objeto': obj, 'titulo': 'Servidor'})
