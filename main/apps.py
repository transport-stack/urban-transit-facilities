from django.apps import AppConfig
from django.db.models.signals import post_save


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        from main.signals import post_settings
        from main.models import Settings

        post_save.connect(post_settings, sender="main.Settings")
