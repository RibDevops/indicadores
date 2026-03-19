from django.urls import path
from . import views

app_name = 'ind'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Indicadores
    path('indicadores/', views.indicadores, name='indicadores'),

    # Status
    path('status/', views.status_list, name='status_list'),
    path('status/novo/', views.status_create, name='status_create'),
    path('status/<int:pk>/editar/', views.status_update, name='status_update'),
    path('status/<int:pk>/excluir/', views.status_delete, name='status_delete'),

    # TipoAcesso
    path('tipo-acesso/', views.tipo_acesso_list, name='tipo_acesso_list'),
    path('tipo-acesso/novo/', views.tipo_acesso_create, name='tipo_acesso_create'),
    path('tipo-acesso/<int:pk>/editar/', views.tipo_acesso_update, name='tipo_acesso_update'),
    path('tipo-acesso/<int:pk>/excluir/', views.tipo_acesso_delete, name='tipo_acesso_delete'),

    # TipoElo
    path('tipo-elo/', views.tipo_elo_list, name='tipo_elo_list'),
    path('tipo-elo/novo/', views.tipo_elo_create, name='tipo_elo_create'),
    path('tipo-elo/<int:pk>/editar/', views.tipo_elo_update, name='tipo_elo_update'),
    path('tipo-elo/<int:pk>/excluir/', views.tipo_elo_delete, name='tipo_elo_delete'),

    # Pais
    path('pais/', views.pais_list, name='pais_list'),
    path('pais/novo/', views.pais_create, name='pais_create'),
    path('pais/<str:pk>/editar/', views.pais_update, name='pais_update'),
    path('pais/<str:pk>/excluir/', views.pais_delete, name='pais_delete'),

    # Estado
    path('estado/', views.estado_list, name='estado_list'),
    path('estado/novo/', views.estado_create, name='estado_create'),
    path('estado/<str:pk>/editar/', views.estado_update, name='estado_update'),
    path('estado/<str:pk>/excluir/', views.estado_delete, name='estado_delete'),

    # RegiaoCidade
    path('regiao/', views.regiao_list, name='regiao_list'),
    path('regiao/novo/', views.regiao_create, name='regiao_create'),
    path('regiao/<str:pk>/editar/', views.regiao_update, name='regiao_update'),
    path('regiao/<str:pk>/excluir/', views.regiao_delete, name='regiao_delete'),

    # Comar
    path('comar/', views.comar_list, name='comar_list'),
    path('comar/novo/', views.comar_create, name='comar_create'),
    path('comar/<int:pk>/editar/', views.comar_update, name='comar_update'),
    path('comar/<int:pk>/excluir/', views.comar_delete, name='comar_delete'),

    # OM
    path('om/', views.om_list, name='om_list'),
    path('om/novo/', views.om_create, name='om_create'),
    path('om/<int:pk>/editar/', views.om_update, name='om_update'),
    path('om/<int:pk>/excluir/', views.om_delete, name='om_delete'),

    # Servidor
    path('servidor/', views.servidor_list, name='servidor_list'),
    path('servidor/novo/', views.servidor_create, name='servidor_create'),
    path('servidor/<int:pk>/', views.servidor_detail, name='servidor_detail'),
    path('servidor/<int:pk>/editar/', views.servidor_update, name='servidor_update'),
    path('servidor/<int:pk>/excluir/', views.servidor_delete, name='servidor_delete'),

    # DataCompra
    path('data-compra/', views.data_compra_list, name='data_compra_list'),
    path('data-compra/novo/', views.data_compra_create, name='data_compra_create'),
    path('data-compra/<int:pk>/editar/', views.data_compra_update, name='data_compra_update'),
    path('data-compra/<int:pk>/excluir/', views.data_compra_delete, name='data_compra_delete'),

    # DataVisita
    path('data-visita/', views.data_visita_list, name='data_visita_list'),
    path('data-visita/novo/', views.data_visita_create, name='data_visita_create'),
    path('data-visita/<int:pk>/editar/', views.data_visita_update, name='data_visita_update'),
    path('data-visita/<int:pk>/excluir/', views.data_visita_delete, name='data_visita_delete'),
]
