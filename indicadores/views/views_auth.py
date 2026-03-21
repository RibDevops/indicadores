"""
Views de autenticação do sistema.

Fluxo:
  1. Usuário não autenticado acessa qualquer URL → redirecionado para /login/
  2. Login bem-sucedido → redirecionado para / (home)
  3. Logout → redirecionado para /boas-vindas/

Autenticação:
  - O backend CustomLDAPBackend (core/backend.py) exige que o username
    exista localmente antes de validar a senha no servidor LDAP.
  - Cadastro de usuários locais: menu Administração → Usuários.
"""

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect


def boas_vindas(request):
    """
    Tela pública de apresentação do sistema — acessível em /.
    Usuários já autenticados são redirecionados direto para o home.
    """
    if request.user.is_authenticated:
        return redirect('ind:home')
    return render(request, 'boas_vindas.html')



def login(request):
    """
    Tela de login.
    - GET:  exibe o formulário.
    - POST: autentica via CustomLDAPBackend → ModelBackend (settings.AUTHENTICATION_BACKENDS).
            Sucesso → redireciona para home.
            Falha   → exibe mensagem de erro.
    """
    # Usuário já logado não precisa ver o login
    if request.user.is_authenticated:
        return redirect('ind:home')

    erro = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            erro = 'Preencha o usuário e a senha.'
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redireciona para a URL solicitada originalmente (se houver) ou para home
                next_url = request.GET.get('next') or '/home/'
                return redirect(next_url)
            else:
                # Pode ser: usuário não cadastrado localmente OU senha LDAP incorreta
                erro = 'Usuário ou senha inválidos.'

    return render(request, 'login.html', {'erro': erro})


def logout(request):
    """
    Encerra a sessão e redireciona para a tela de boas-vindas.
    Aceita GET e POST para compatibilidade com botão simples de link.
    """
    auth_logout(request)
    return redirect('ind:boas_vindas')
