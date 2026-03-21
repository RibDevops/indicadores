from django.apps import AppConfig


class IndicadoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indicadores'

    def ready(self):
        # Registra os signals definidos em indicadores/signals.py.
        # Sem este import, o signal post_save do Servidor não seria conectado
        # e o histórico de DataStatus não seria criado automaticamente.
        import indicadores.signals  # noqa: F401
