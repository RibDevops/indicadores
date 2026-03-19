from django.db import models
from django.utils import timezone

# =========================
# TABELAS BASE
# =========================

class Status(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class TipoAcesso(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo


class TipoElo(models.Model):
    tipo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipo


class Pais(models.Model):
    sigla = models.CharField(max_length=5, primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Estado(models.Model):
    sigla = models.CharField(max_length=5, primary_key=True)
    nome = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class RegiaoCidade(models.Model):
    sigla = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Comar(models.Model):
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    regiao_cidade = models.ForeignKey(RegiaoCidade, on_delete=models.CASCADE)
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome



class OM(models.Model):
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    comar = models.ForeignKey(Comar, on_delete=models.CASCADE)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    tipo_elo = models.ForeignKey(TipoElo, on_delete=models.CASCADE)
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Servidor(models.Model):  # 🔥 nome mais semântico
    om = models.ForeignKey(
        OM,
        on_delete=models.CASCADE,
        related_name='servidores'  # 🔥 agora faz sentido
    )

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    tipo_acesso = models.ForeignKey(TipoAcesso, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    data_aquisicao = models.DateField()

    sistema_operacional = models.CharField(max_length=100)
    versao_so = models.CharField(max_length=50)

    obs = models.TextField(blank=True, null=True)

    def idade_anos(self):
        return (timezone.now().date() - self.data_aquisicao).days / 365

    def __str__(self):
        return self.nome


class DataCompra(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    data_compra = models.DateField()

    def __str__(self):
        return f"{self.servidor} - {self.data_compra}"


class DataVisita(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    data_visita = models.DateField()

    def __str__(self):
        return f"{self.servidor} - {self.data_visita}"