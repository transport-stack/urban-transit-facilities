from django.apps import AppConfig
from django.db.models.signals import post_save


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"

    def ready(self):
        from inventory.signals import post_floor_plan_creation
        from inventory.models import FloorPlan

        post_save.connect(post_floor_plan_creation, sender="inventory.FloorPlan")
