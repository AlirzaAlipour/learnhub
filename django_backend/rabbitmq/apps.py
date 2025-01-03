from django.apps import AppConfig


class RabbitmqConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rabbitmq"
    def ready(self):
        import rabbitmq.signals
