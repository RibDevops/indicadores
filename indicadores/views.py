from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Status, TipoAcesso, TipoElo, Pais, Estado, RegiaoCidade,
    Comar, OM, Servidor, DataCompra, DataVisita,
)
from .forms import (
    StatusForm, TipoAcessoForm, TipoEloForm, PaisForm, EstadoForm,
    RegiaoCidadeForm, ComarForm, OMForm, ServidorForm,
    DataCompraForm, DataVisitaForm,
)


# ── Home ──────────────────────────────────────────────────────────────────────

def home(request):
    context = {
        'total_servidores': Servidor.objects.count(),
        'total_om': OM.objects.count(),
        'total_comar': Comar.objects.count(),
    }
    return render(request, 'home.html', context)


# ── Status ────────────────────────────────────────────────────────────────────

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


# ── TipoAcesso ────────────────────────────────────────────────────────────────

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


# ── TipoElo ───────────────────────────────────────────────────────────────────

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


# ── Pais ──────────────────────────────────────────────────────────────────────

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


# ── Estado ────────────────────────────────────────────────────────────────────

def estado_list(request):
    return render(request, 'estado/list.html', {'objetos': Estado.objects.select_related('pais').all()})

def estado_create(request):
    form = EstadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estado criado.')
        return redirect('ind:estado_list')
    return render(request, 'estado/form.html', {'form': form, 'titulo': 'Novo Estado'})

def estado_update(request, pk):
    obj = get_object_or_404(Estado, pk=pk)
    form = EstadoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Estado atualizado.')
        return redirect('ind:estado_list')
    return render(request, 'estado/form.html', {'form': form, 'titulo': 'Editar Estado'})

def estado_delete(request, pk):
    obj = get_object_or_404(Estado, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Estado excluído.')
        return redirect('ind:estado_list')
    return render(request, 'estado/confirm_delete.html', {'objeto': obj, 'titulo': 'Estado'})


# ── RegiaoCidade ──────────────────────────────────────────────────────────────

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


# ── Comar ─────────────────────────────────────────────────────────────────────

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


# ── OM ────────────────────────────────────────────────────────────────────────

def om_list(request):
    return render(request, 'om/list.html', {'objetos': OM.objects.select_related('comar', 'pais', 'tipo_elo').all()})

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


# ── Servidor ──────────────────────────────────────────────────────────────────

def servidor_list(request):
    servidores = Servidor.objects.select_related('om', 'status', 'tipo_acesso').all()
    return render(request, 'servidor/list.html', {'objetos': servidores})

def servidor_detail(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    compras = DataCompra.objects.filter(servidor=obj).order_by('-data_compra')
    visitas = DataVisita.objects.filter(servidor=obj).order_by('-data_visita')
    return render(request, 'servidor/detail.html', {
        'objeto': obj,
        'compras': compras,
        'visitas': visitas,
    })

def servidor_create(request):
    form = ServidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Servidor criado.')
        return redirect('ind:servidor_list')
    return render(request, 'servidor/form.html', {'form': form, 'titulo': 'Novo Servidor'})

def servidor_update(request, pk):
    obj = get_object_or_404(Servidor, pk=pk)
    form = ServidorForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
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


# ── DataCompra ────────────────────────────────────────────────────────────────

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


# ── DataVisita ────────────────────────────────────────────────────────────────

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
