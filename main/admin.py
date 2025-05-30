from django.contrib import admin

from .models import Settings, Days


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Settings.objects.count() == 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        (
            "Data",
            {"fields": ("title", "is_active", "starting_of_the_week", "base_url")},
        ),
        (
            "Important Dates",
            {"fields": ("created_at", "updated_at")},
        ),
        (
            "Occupancy",
            {
                "fields": (
                    "occupancy_level_1",
                    "occupancy_level_1_threshold",
                    "occupancy_level_1_color_primary",
                    "occupancy_level_1_color_secondary",
                    "occupancy_level_2",
                    "occupancy_level_2_threshold",
                    "occupancy_level_2_color_primary",
                    "occupancy_level_2_color_secondary",
                    "occupancy_level_3",
                    "occupancy_level_3_color_primary",
                    "occupancy_level_3_color_secondary",
                )
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    class Meta:
        model = Settings


@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ("day", "is_active", "order")
    search_fields = ("day",)
    list_filter = ("is_active",)
    readonly_fields = ("day", "master_order")

    class Meta:
        model = Days
