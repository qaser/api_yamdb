from django.contrib import admin
from importlib import import_module
from django.apps import apps


def model_register(*app_list):
    # проходим циклом по зарегистрированным приложениям
    for i in app_list:
        module_path = f'{i}.admin'
        module = import_module(module_path)
        app_config = apps.get_app_config(i)
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


model_register('api',)