# DataCompra foi removido — a data de aquisição agora está em Servidor.data_aquisicao.
# Este arquivo mantém as funções para não quebrar imports existentes,
# redirecionando para a lista de servidores.

from django.shortcuts import redirect


def data_compra_list(request):
    return redirect('ind:servidor_list')


def data_compra_create(request):
    return redirect('ind:servidor_list')


def data_compra_update(request, pk):
    return redirect('ind:servidor_list')


def data_compra_delete(request, pk):
    return redirect('ind:servidor_list')
