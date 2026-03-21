"""
Views de gerenciamento de usuários locais.

O sistema usa autenticação LDAP (core/backend.py): o LDAP valida a senha,
mas o usuário precisa existir localmente no banco para ter acesso.
Estas views permitem cadastrar, listar, editar e excluir esses usuários locais.

Fluxo de autenticação:
  1. Usuário envia username + password no login.
  2. CustomLDAPBackend verifica se o username existe localmente (User.objects.get).
  3. Se existir, autentica contra o servidor LDAP.
  4. Se não existir localmente, o acesso é negado mesmo com credenciais LDAP válidas.

Portanto, para liberar acesso a um novo usuário:
  - Cadastre o username aqui (sem senha — a senha é gerenciada pelo LDAP).
  - Para revogar acesso, exclua o usuário desta lista.
"""

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

User = get_user_model()


def usuario_list(request):
    """Lista todos os usuários locais com todos os campos disponíveis."""
    usuarios = User.objects.all().order_by('username')
    return render(request, 'usuario/list.html', {'objetos': usuarios})


def usuario_create(request):
    """
    Cadastra um novo usuário local (somente username, sem senha).
    A senha é gerenciada pelo LDAP — não é necessário defini-la aqui.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()

        if not username:
            messages.error(request, 'O username não pode ser vazio.')
            return render(request, 'usuario/form.html', {'titulo': 'Novo Usuário', 'username': username})

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Usuário "{username}" já existe.')
            return render(request, 'usuario/form.html', {'titulo': 'Novo Usuário', 'username': username})

        # Cria sem senha — autenticação é delegada ao LDAP
        User.objects.create_user(username=username)
        messages.success(request, f'Usuário "{username}" cadastrado com sucesso.')
        return redirect('ind:usuario_list')

    return render(request, 'usuario/form.html', {'titulo': 'Novo Usuário'})


def usuario_update(request, pk):
    """
    Edita somente o username do usuário.
    Outros campos (senha, permissões) são gerenciados pelo LDAP ou pelo admin Django.
    """
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        novo_username = request.POST.get('username', '').strip()

        if not novo_username:
            messages.error(request, 'O username não pode ser vazio.')
            return render(request, 'usuario/form.html', {
                'titulo': 'Editar Usuário',
                'usuario': usuario,
                'username': novo_username,
            })

        if User.objects.filter(username=novo_username).exclude(pk=pk).exists():
            messages.error(request, f'Username "{novo_username}" já está em uso.')
            return render(request, 'usuario/form.html', {
                'titulo': 'Editar Usuário',
                'usuario': usuario,
                'username': novo_username,
            })

        usuario.username = novo_username
        usuario.save(update_fields=['username'])
        # update_fields=['username'] evita disparar o signal de DataStatus
        # (que só observa Servidor, mas é boa prática ser explícito)
        messages.success(request, f'Username atualizado para "{novo_username}".')
        return redirect('ind:usuario_list')

    return render(request, 'usuario/form.html', {
        'titulo': 'Editar Usuário',
        'usuario': usuario,
        'username': usuario.username,
    })


def usuario_delete(request, pk):
    """
    Exclui o usuário local. Após a exclusão, o usuário não consegue mais
    fazer login mesmo que possua credenciais LDAP válidas.
    """
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuário "{username}" excluído.')
        return redirect('ind:usuario_list')

    return render(request, 'usuario/confirm_delete.html', {
        'objeto': usuario,
        'titulo': 'Usuário',
    })
