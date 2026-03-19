from django.shortcuts import render
from django.db.models import Count, Max
from django.utils import timezone

from ..models import TipoAcesso, OM, Servidor

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Palavras-chave que identificam um status como "inoperante" (sem distinção de maiúsculas).
# Uma OM é considerada inoperante quando TODOS os seus servidores possuem
# um status cujo texto contenha ao menos uma dessas palavras.
_STATUS_INOPERANTE = ('inoperante', 'inativo', 'desativado', 'offline')

# Sigla do país Brasil conforme cadastrado na tabela Pais.
# Usada para separar os servidores da Rede Brasil (I_BR) dos do Exterior (I_EXT).
_SIGLA_BRASIL = 'BR'


# ---------------------------------------------------------------------------
# Funções auxiliares de pontuação
# ---------------------------------------------------------------------------

def _score_vis_tec(ultima_visita):
    """
    VisTec — Pontuação pelo tempo (em meses) desde a última visita técnica.

    Regra:
        até 48 meses  → 1,0  (visita recente, situação ideal)
        49 a 72 meses → 0,5  (visita com algum atraso)
        73 a 96 meses → 0,25 (visita muito atrasada)
        acima de 96   → 0,0  (sem visita há mais de 8 anos)
        sem registro  → 0,0  (nenhuma visita cadastrada)

    Parâmetro:
        ultima_visita: date ou None — data da visita mais recente do servidor.

    Retorno:
        float com a pontuação correspondente.
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


# ---------------------------------------------------------------------------
# Função principal de cálculo dos indicadores
# ---------------------------------------------------------------------------

def _compute_indicadores():
    """
    Calcula os três grupos de indicadores (REDE_M, I_BR, I_EXT) e retorna
    um dicionário pronto para ser passado como contexto ao template.

    ═══════════════════════════════════════════════════════════════════════
    REDE_M — Indicadores gerais da Rede M
    ═══════════════════════════════════════════════════════════════════════

    QntUnidTotal
        Quantidade total de OMs que possuem ao menos um servidor cadastrado.
        OMs sem nenhum servidor não são contabilizadas.

    QntUnidTotalTiposdeAcesso
        Quantidade de servidores agrupada por Tipo de Acesso (ex.: SSH, RDP).
        Permite visualizar a distribuição dos meios de acesso na rede.

    QntUnid-INOperantes
        Quantidade de OMs consideradas inoperantes no dia atual.
        Uma OM é marcada como inoperante quando TODOS os seus servidores
        possuem um status que contenha as palavras definidas em
        _STATUS_INOPERANTE (inoperante, inativo, desativado, offline).

    ═══════════════════════════════════════════════════════════════════════
    I_BR — Índice de Confiabilidade da Rede Brasil
    ═══════════════════════════════════════════════════════════════════════

    QntUnidTotalBR
        Quantidade total de servidores vinculados a OMs cujo país é Brasil
        (sigla 'BR'). Base de cálculo dos demais sub-índices do I_BR.

    CicloVidaBR
        Soma das pontuações de ciclo de vida de cada servidor brasileiro.
        A pontuação individual é calculada pelo método score_ciclo_vida()
        do modelo Servidor, com a seguinte escala:
            até 2 anos  → 1,0
            2 a 4 anos  → 0,5
            4 a 6 anos  → 0,26
            acima de 6  → 0,0

    SupSOBR
        Soma das pontuações de suporte do sistema operacional de cada
        servidor brasileiro. Calculada pelo método score_suporte_so()
        do modelo Servidor:
            Atual         → 1,0
            Suportado     → 0,5
            Descontinuado → 0,0

    VisTecBR
        Soma das pontuações de visita técnica de cada servidor brasileiro.
        Usa a data da visita mais recente registrada em DataVisita.
        Escala definida em _score_vis_tec():
            até 48 meses  → 1,0
            49 a 72 meses → 0,5
            73 a 96 meses → 0,25
            acima de 96   → 0,0

    ═══════════════════════════════════════════════════════════════════════
    I_EXT — Índice de Confiabilidade da Rede Exterior
    ═══════════════════════════════════════════════════════════════════════

    QntUnidTotalExt
        Quantidade total de servidores vinculados a OMs cujo país NÃO é
        Brasil. Base de cálculo dos demais sub-índices do I_EXT.

    CicloVidaExt / SupSOExt / VisTecExt
        Mesmas regras de pontuação do I_BR, aplicadas aos servidores
        do Exterior.
    """

    # ── REDE_M ────────────────────────────────────────────────────────────────

    # OMs que possuem ao menos um servidor cadastrado
    om_com_rede = OM.objects.filter(servidores__isnull=False).distinct()

    # QntUnidTotal: total de OMs com rede
    qnt_unid_total = om_com_rede.count()

    # QntUnidTotalTiposdeAcesso: contagem de servidores por tipo de acesso
    tipos_acesso = (
        TipoAcesso.objects
        .filter(servidor__isnull=False)
        .annotate(total=Count('servidor', distinct=True))
        .values('tipo', 'total')
        .order_by('-total')
    )

    # QntUnid-INOperantes: OMs onde todos os servidores estão inoperantes
    om_inoperantes = 0
    for om in om_com_rede:
        todos_inop = all(
            any(kw in s.status.descricao.lower() for kw in _STATUS_INOPERANTE)
            for s in om.servidores.select_related('status').all()
        )
        if todos_inop:
            om_inoperantes += 1

    # ── I_BR — Rede Brasil ────────────────────────────────────────────────────

    # Servidores de OMs localizadas no Brasil
    servidores_br = (
        Servidor.objects
        .filter(om__pais__sigla=_SIGLA_BRASIL)
        .select_related('om__pais', 'status', 'tipo_acesso')
        .prefetch_related('datavisita_set')
    )

    # QntUnidTotalBR
    qnt_br = servidores_br.count()

    # CicloVidaBR: soma das pontuações de ciclo de vida (<=2=1; 2-4=0,5; 4-6=0,26; >6=0)
    ciclo_br = sum(s.score_ciclo_vida() for s in servidores_br)

    # SupSOBR: soma das pontuações de suporte do SO (atual=1; suportado=0,5; descontinuado=0)
    sup_so_br = sum(s.score_suporte_so() for s in servidores_br)

    # VisTecBR: soma das pontuações pela data da última visita técnica
    vis_tec_br = sum(
        _score_vis_tec(s.datavisita_set.aggregate(m=Max('data_visita'))['m'])
        for s in servidores_br
    )

    # ── I_EXT — Rede Exterior ─────────────────────────────────────────────────

    # Servidores de OMs localizadas fora do Brasil
    servidores_ext = (
        Servidor.objects
        .exclude(om__pais__sigla=_SIGLA_BRASIL)
        .select_related('om__pais', 'status', 'tipo_acesso')
        .prefetch_related('datavisita_set')
    )

    # QntUnidTotalExt
    qnt_ext = servidores_ext.count()

    # CicloVidaExt: mesma escala do I_BR
    ciclo_ext = sum(s.score_ciclo_vida() for s in servidores_ext)

    # SupSOExt: mesma escala do I_BR
    sup_so_ext = sum(s.score_suporte_so() for s in servidores_ext)

    # VisTecExt: mesma escala do I_BR
    vis_tec_ext = sum(
        _score_vis_tec(s.datavisita_set.aggregate(m=Max('data_visita'))['m'])
        for s in servidores_ext
    )

    return {
        # REDE_M
        'rede_qnt_unid_total': qnt_unid_total,       # QntUnidTotal
        'rede_tipos_acesso': list(tipos_acesso),      # QntUnidTotalTiposdeAcesso
        'rede_om_inoperantes': om_inoperantes,        # QntUnid-INOperantes

        # I_BR
        'ibr_qnt_total': qnt_br,                     # QntUnidTotalBR
        'ibr_ciclo_vida': round(ciclo_br, 2),         # CicloVidaBR
        'ibr_sup_so': round(sup_so_br, 2),            # SupSOBR
        'ibr_vis_tec': round(vis_tec_br, 2),          # VisTecBR

        # I_EXT
        'iext_qnt_total': qnt_ext,                   # QntUnidTotalExt
        'iext_ciclo_vida': round(ciclo_ext, 2),       # CicloVidaExt
        'iext_sup_so': round(sup_so_ext, 2),          # SupSOExt
        'iext_vis_tec': round(vis_tec_ext, 2),        # VisTecExt
    }


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------

def indicadores(request):
    """Renderiza o painel completo de indicadores (REDE_M, I_BR, I_EXT)."""
    return render(request, 'indicadores.html', _compute_indicadores())
