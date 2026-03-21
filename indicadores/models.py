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


class Servidor(models.Model):
    # Choices para suporte do sistema operacional
    SUPORTE_ATUAL = 'atual'
    SUPORTE_SUPORTADO = 'suportado'
    SUPORTE_DESCONTINUADO = 'descontinuado'
    SUPORTE_SO_CHOICES = [
        (SUPORTE_ATUAL, 'Atual'),
        (SUPORTE_SUPORTADO, 'Suportado'),
        (SUPORTE_DESCONTINUADO, 'Descontinuado'),
    ]

    om = models.ForeignKey(
        OM,
        on_delete=models.CASCADE,
        related_name='servidores',
    )

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    tipo_acesso = models.ForeignKey(TipoAcesso, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    data_aquisicao = models.DateField()

    sistema_operacional = models.CharField(max_length=100)
    versao_so = models.CharField(max_length=50)
    suporte_so = models.CharField(
        max_length=20,
        choices=SUPORTE_SO_CHOICES,
        default=SUPORTE_ATUAL,
    )
        
    obs = models.TextField(blank=True, null=True)

    def idade_anos(self):
        return (timezone.now().date() - self.data_aquisicao).days / 365

    def score_ciclo_vida(self):
        """Pontuação pelo ciclo de vida: ≤2=1, 2-4=0.5, 4-6=0.26, >6=0."""
        anos = self.idade_anos()
        if anos <= 2:
            return 1.0
        elif anos <= 4:
            return 0.5
        elif anos <= 6:
            return 0.26
        return 0.0

    def score_suporte_so(self):
        """Pontuação pelo suporte do SO: atual=1, suportado=0.5, descontinuado=0."""
        return {
            self.SUPORTE_ATUAL: 1.0,
            self.SUPORTE_SUPORTADO: 0.5,
            self.SUPORTE_DESCONTINUADO: 0.0,
        }.get(self.suporte_so, 0.0)

    def dias_por_status(self):
        """
        Retorna um dicionário {status_descricao: total_dias} calculado a partir
        do histórico de DataStatus.

        Lógica:
          - Os registros são ordenados por data_status (crescente).
          - Para cada registro N, o período contado vai de data_status[N]
            até data_status[N+1] (ou hoje, se for o último registro).
          - Isso permite saber quantos dias o servidor ficou em cada status.

        Exemplo de uso no template:
            {% for status, dias in objeto.dias_por_status.items %}
                {{ status }}: {{ dias }} dias
            {% endfor %}
        """
        historico = list(
            self.datastatus_set.select_related('status')
            .order_by('data_status')
        )
        totais = {}
        hoje = timezone.now().date()

        for i, registro in enumerate(historico):
            # Data de início do período é a data do registro atual
            inicio = registro.data_status
            # Data de fim é o início do próximo registro, ou hoje se for o último
            fim = historico[i + 1].data_status if i + 1 < len(historico) else hoje
            dias = (fim - inicio).days
            descricao = registro.status.descricao
            totais[descricao] = totais.get(descricao, 0) + dias

        return totais

    def __str__(self):
        return self.nome


# =========================
# HISTÓRICO DE STATUS
# =========================

class DataStatus(models.Model):
    """
    Registra cada mudança de status de um Servidor.

    Um novo registro é criado automaticamente via signal (indicadores/signals.py)
    toda vez que o campo `status` do Servidor é alterado ou criado.

    Campos:
      - servidor:    FK para o Servidor relacionado.
      - status:      FK para o Status que foi atribuído nesta data.
      - data_status: Data em que o status foi aplicado (preenchida automaticamente).

    Como usar manualmente (se necessário):
        DataStatus.objects.create(
            servidor=meu_servidor,
            status=novo_status,
            data_status=date.today(),
        )

    Para calcular dias por status, use o método `servidor.dias_por_status()`.
    """
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    # Status que estava ativo nesta data
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    # Data em que o status foi registrado (preenchida automaticamente pelo signal)
    data_status = models.DateField()

    class Meta:
        ordering = ['data_status']
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Histórico de Status'

    def __str__(self):
        return f"{self.servidor} — {self.status} em {self.data_status}"


# =========================
# HISTÓRICO DE VISITAS
# =========================

class DataVisita(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    data_visita = models.DateField()

    def __str__(self):
        return f"{self.servidor} - {self.data_visita}"