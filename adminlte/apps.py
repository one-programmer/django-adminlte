from django.apps import AppConfig


class AdminlteConfig(AppConfig):
    name = 'adminlte'

    def ready(self):
        self.module.autodiscover()
