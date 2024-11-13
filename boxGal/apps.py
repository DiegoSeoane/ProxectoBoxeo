from django.apps import AppConfig


class BoxgalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boxGal'

    def ready(self):
        import boxGal.signals