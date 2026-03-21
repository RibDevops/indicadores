from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'ind'

# login_required aplicado diretamente na view dentro do path().
# Usuários não autenticados são redirecionados para settings.LOGIN_URL (/login/).
lr = login_required

urlpatterns = [
    # ── Públicas (sem autenticação) ──────────────────────────────────────────
    # / é a tela de boas-vindas para usuários não autenticados
    # e redireciona para o home para usuários autenticados
    path('',       views.boas_vindas, name='boas_vindas'),
    path('login/', views.login,       name='login'),
    path('logout/',views.logout,      name='logout'),

    # ── Home (protegido) ─────────────────────────────────────────────────────
    path('home/', lr(views.home), name='home'),

    # ── Indicadores ──────────────────────────────────────────────────────────
    path('indicadores/', lr(views.indicadores), name='indicadores'),

    # ── Status ───────────────────────────────────────────────────────────────
    path('status/',                       lr(views.status_list),   name='status_list'),
    path('status/novo/',                  lr(views.status_create), name='status_create'),
    path('status/<int:pk>/editar/',       lr(views.status_update), name='status_update'),
    path('status/<int:pk>/excluir/',      lr(views.status_delete), name='status_delete'),

    # ── TipoAcesso ───────────────────────────────────────────────────────────
    path('tipo-acesso/',                  lr(views.tipo_acesso_list),   name='tipo_acesso_list'),
    path('tipo-acesso/novo/',             lr(views.tipo_acesso_create), name='tipo_acesso_create'),
    path('tipo-acesso/<int:pk>/editar/',  lr(views.tipo_acesso_update), name='tipo_acesso_update'),
    path('tipo-acesso/<int:pk>/excluir/', lr(views.tipo_acesso_delete), name='tipo_acesso_delete'),

    # ── TipoElo ──────────────────────────────────────────────────────────────
    path('tipo-elo/',                     lr(views.tipo_elo_list),   name='tipo_elo_list'),
    path('tipo-elo/novo/',                lr(views.tipo_elo_create), name='tipo_elo_create'),
    path('tipo-elo/<int:pk>/editar/',     lr(views.tipo_elo_update), name='tipo_elo_update'),
    path('tipo-elo/<int:pk>/excluir/',    lr(views.tipo_elo_delete), name='tipo_elo_delete'),

    # ── Pais ─────────────────────────────────────────────────────────────────
    path('pais/',                         lr(views.pais_list),   name='pais_list'),
    path('pais/novo/',                    lr(views.pais_create), name='pais_create'),
    path('pais/<str:pk>/editar/',         lr(views.pais_update), name='pais_update'),
    path('pais/<str:pk>/excluir/',        lr(views.pais_delete), name='pais_delete'),

    # ── Estado ───────────────────────────────────────────────────────────────
    path('estado/',                       lr(views.estado_list),   name='estado_list'),
    path('estado/novo/',                  lr(views.estado_create), name='estado_create'),
    path('estado/<str:pk>/editar/',       lr(views.estado_update), name='estado_update'),
    path('estado/<str:pk>/excluir/',      lr(views.estado_delete), name='estado_delete'),

    # ── RegiaoCidade ─────────────────────────────────────────────────────────
    path('regiao/',                       lr(views.regiao_list),   name='regiao_list'),
    path('regiao/novo/',                  lr(views.regiao_create), name='regiao_create'),
    path('regiao/<str:pk>/editar/',       lr(views.regiao_update), name='regiao_update'),
    path('regiao/<str:pk>/excluir/',      lr(views.regiao_delete), name='regiao_delete'),

    # ── Comar ────────────────────────────────────────────────────────────────
    path('comar/',                        lr(views.comar_list),   name='comar_list'),
    path('comar/novo/',                   lr(views.comar_create), name='comar_create'),
    path('comar/<int:pk>/editar/',        lr(views.comar_update), name='comar_update'),
    path('comar/<int:pk>/excluir/',       lr(views.comar_delete), name='comar_delete'),

    # ── OM ───────────────────────────────────────────────────────────────────
    path('om/',                           lr(views.om_list),   name='om_list'),
    path('om/novo/',                      lr(views.om_create), name='om_create'),
    path('om/<int:pk>/editar/',           lr(views.om_update), name='om_update'),
    path('om/<int:pk>/excluir/',          lr(views.om_delete), name='om_delete'),

    # ── Servidor ─────────────────────────────────────────────────────────────
    path('servidor/',                     lr(views.servidor_list),   name='servidor_list'),
    path('servidor/novo/',                lr(views.servidor_create), name='servidor_create'),
    path('servidor/<int:pk>/',            lr(views.servidor_detail), name='servidor_detail'),
    path('servidor/<int:pk>/editar/',     lr(views.servidor_update), name='servidor_update'),
    path('servidor/<int:pk>/excluir/',    lr(views.servidor_delete), name='servidor_delete'),

    # ── DataCompra (redirecionamentos — model removido) ───────────────────────
    path('data-compra/',                  lr(views.data_compra_list),   name='data_compra_list'),
    path('data-compra/novo/',             lr(views.data_compra_create), name='data_compra_create'),
    path('data-compra/<int:pk>/editar/',  lr(views.data_compra_update), name='data_compra_update'),
    path('data-compra/<int:pk>/excluir/', lr(views.data_compra_delete), name='data_compra_delete'),

    # ── DataVisita ───────────────────────────────────────────────────────────
    path('data-visita/',                  lr(views.data_visita_list),   name='data_visita_list'),
    path('data-visita/novo/',             lr(views.data_visita_create), name='data_visita_create'),
    path('data-visita/<int:pk>/editar/',  lr(views.data_visita_update), name='data_visita_update'),
    path('data-visita/<int:pk>/excluir/', lr(views.data_visita_delete), name='data_visita_delete'),

    # ── Usuários locais (autenticação via LDAP) ───────────────────────────────
    path('usuarios/',                     lr(views.usuario_list),   name='usuario_list'),
    path('usuarios/novo/',                lr(views.usuario_create), name='usuario_create'),
    path('usuarios/<int:pk>/editar/',     lr(views.usuario_update), name='usuario_update'),
    path('usuarios/<int:pk>/excluir/',    lr(views.usuario_delete), name='usuario_delete'),
]
