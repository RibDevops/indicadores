"""
Signals do app indicadores.

Responsabilidade principal:
  - Toda vez que um Servidor é criado ou tem seu campo `status` alterado,
    um registro em DataStatus é criado automaticamente com a data atual.

Como funciona:
  - O signal `post_save` do Servidor é capturado pela função
    `registrar_data_status` abaixo.
  - Na criação (created=True): registra o status inicial.
  - Na atualização: compara o status atual com o último registro em DataStatus;
    só cria um novo registro se o status mudou.

Para desabilitar o registro automático em um save específico (ex.: fixtures),
passe `update_fields` sem incluir 'status':
    servidor.save(update_fields=['obs'])  # não dispara novo DataStatus

Para registrar manualmente uma mudança retroativa:
    from indicadores.models import DataStatus
    from datetime import date
    DataStatus.objects.create(
        servidor=meu_servidor,
        status=novo_status,
        data_status=date(2024, 1, 15),
    )
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Servidor, DataStatus


@receiver(post_save, sender=Servidor)
def registrar_data_status(sender, instance, created, **kwargs):
    """
    Cria um registro em DataStatus sempre que o status do Servidor mudar.

    - Na criação do Servidor: registra o status inicial.
    - Na edição: verifica se o status mudou comparando com o último registro;
      evita duplicatas se o status for o mesmo.
    """
    hoje = timezone.now().date()

    if created:
        # Servidor novo: registra o status inicial
        DataStatus.objects.create(
            servidor=instance,
            status=instance.status,
            data_status=hoje,
        )
        return

    # Servidor existente: verifica se o status mudou em relação ao último registro
    ultimo = (
        DataStatus.objects
        .filter(servidor=instance)
        .order_by('-data_status', '-id')
        .first()
    )

    # Se não há histórico ou o status mudou, cria novo registro
    if ultimo is None or ultimo.status_id != instance.status_id:
        DataStatus.objects.create(
            servidor=instance,
            status=instance.status,
            data_status=hoje,
        )
