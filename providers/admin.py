from django.contrib import admin

from providers.models import ServiceProvider


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_num")
    search_fields = ("name__icontains",)
    autocomplete_fields = ("added_by",)
    readonly_fields = ("created_at", "updated_at")

    class Meta:
        model = ServiceProvider
