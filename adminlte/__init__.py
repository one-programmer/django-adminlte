from django.utils.module_loading import autodiscover_modules

default_app_config = 'adminlte.apps.AdminlteConfig'


def autodiscover():
    autodiscover_modules('adminlte')
