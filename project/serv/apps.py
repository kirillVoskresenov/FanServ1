from django.apps import AppConfig


class ServConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serv'

    def ready(self):
        import serv.signals