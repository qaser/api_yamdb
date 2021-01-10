from importlib import import_module

from django.apps import apps
from django.contrib import admin

from api.apps import ApiConfig


def model_register(*app_list):
    # проходим циклом по зарегистрированным приложениям
    for app in app_list:
        module_path = f'{app}.admin'
        module = import_module(module_path)
        app_config = apps.get_app_config(app)
        # проходим циклом по всем моделям приложения
        for model in app_config.get_models():
            model_admin = getattr(module, f'{model.__name__}Admin', None)
            try:
                if model_admin:
                    # аналог admin.site.register(User, UserAdmin)
                    admin.site.register(model, model_admin)
                else:
                    admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass


model_register(ApiConfig.name)
