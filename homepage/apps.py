from django.apps import AppConfig

class HomepageConfig(AppConfig):
    name = 'homepage'

    def ready(self):
        from . import signals
        