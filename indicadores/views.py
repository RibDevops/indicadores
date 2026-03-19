from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Max
from django.utils import timezone

from .models import (
    Status, TipoAcesso, TipoElo, Pais, Estado, RegiaoCidade,
    Comar, OM, Servidor, DataCompra, DataVisita,
)
from .forms import (
    StatusForm, TipoAcessoForm, TipoEloForm, PaisForm, EstadoForm,
    RegiaoCidadeForm, ComarForm, OMForm, ServidorForm,
    DataCompraForm, DataVisitaForm,
)

# ---------------------------------------------------------------------------
# Indicator helpers
# ---------------------------------------------------------------------------

# Status descriptions that mean "inoperante" (case-insensitive match)
_STATUS_INOPERANTE = ('inoperante', 'inativo', 'desativado', 'offline')

# Sigla do Brasil no cadastro de países
_SIGLA_BRASIL = 'BR'


def _score_vis_tec(ultima_visita):
    """
    Score for time since last technical visit (in months).
    ≤48 → 1.0 | 49-72 → 0.5 | 73-96 → 0.25 | >96 → 0.0 | never → 0.0
    """
    if ultima_visita is None:
        return 0.0
    meses = (timezone.now().date() - ultima_visita).days / 30.44
    if meses <= 48:
        return 1.0
    elif meses <= 72:
        return 0.5
    elif meses <= 96:
        return 0.25
    return 0.0


def _compute_indicadores():
    """
    Compute all three indicator groups (REDE_M, I_BR, I_EXT) and return
    a dict ready to be passed as template context.
    """
    today = timezone.now().date()

    # ── REDE_M ────────────────────────────────────────────────────────────────
    # OMs that have at least one server
    om_com_rede = OM.objects.filter(servidores__isnull=False).distinct()
    qnt_unid_total = om_com_rede.count()

    # Count per TipoAcesso (only OMs that have servers)
    tipos_acesso = (
        TipoAcesso.objects
        .filter(servidor__isnull=False)
        .annotate(total=Count('servidor', distinct=True))
        .values('tipo', 'total')
        .order_by('-total')
    )

    # OMs inoperantes: all servers of that OM have an "inoperante" status
    om_inoperantes = 0
    for om in om_com_rede:
        todos_inop = all(
            any(kw in s.status.descricao.lower() for kw in _STATUS_INOPERANTE)
            for s in om.servidores.select_related('status').all()
        )
        if todos_inop:
            om_inoperantes += 1

    # ── I_BR ──────────────────────────────────────────────────────────────────
    servidores_br = (
        Servidor.objects
        .filter(om__pais__sigla=_SIGLA_BRASIL)
        .select_related('om__pais', 'status', 'tipo_acesso')
        .prefetch_related('datavisita_set')
    )
    qnt_br = servidores_br.count()

    ciclo_br = sum(s.score_ciclo_vida() for s in servidores_br)
    sup_so_br = sum(s.score_suporte_so() for s in servidores_br)
    vis_tec_br = sum(
        _score_vis_tec(
            s.datavisita_set.aggregate(m=Max('data_visita'))['m']
        )
        for s in servidores_br
    )

    # ── I_EXT ─────────────────────────────────────────────────────────────────
    servidores_ext = (
        Servidor.objects
        .exclude(om__pais__sigla=_SIGLA_BRASIL)
        .select_related('om__pais', 'status', 'tipo_acesso')
        .prefetch_related('datavisita_set')
    )
    qnt_ext = servidores_ext.count()

    ciclo_ext = sum(s.score_ciclo_vida() for s in servidores_ext)
    sup_so_ext = sum(s.score_suporte_so() for s in servidores_ext)
    vis_tec_ext = sum(
        _score_vis_tec(
            s.datavisita_set.aggregate(m=Max('data_visita'))['m']
        )
        for s in servidores_ext
    )

    return {
        # REDE_M
        'rede_qnt_unid_total': qnt_unid_total,
        'rede_tipos_acesso': list(tipos_acesso),
        'rede_om_inoperantes': om_inoperantes,
        # I_BR
        'ibr_qnt_total': qnt_br,
        'ibr_ciclo_vida': round(ciclo_br, 2),
        'ibr_sup_so': round(sup_so_br, 2),
        'ibr_vis_tec': round(vis_tec_br, 2),
        # I_EXT
        'iext_qnt_total': qnt_ext,
        'iext_ciclo_vida': round(ciclo_ext, 2),
        'iext_sup_so': round(sup_so_ext, 2),
        'iext_vis_tec': round(vis_tec_ext, 2),
    }


# ── Home ──────────────────────────────────────────────────────────────────────

def home(request):
    context = {
        'total_servidores': Servidor.objects.count(),
        'total_om': OM.objects.count(),
        'total_comar': Comar.objects.count(),
        **_compute_indicadores(),
    }
    return render(request, 'home.html', context)


# ── Indicadores ───────────────────────────────────────────────────────────────

def indicadores(request):
    context = _compute_indicadores()
    return render(request, 'indicadores.html', context)


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
