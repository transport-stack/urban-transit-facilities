from django.contrib import admin
from import_export.admin import ExportActionMixin

from accounts.forms import MyUserForm
from accounts.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(ExportActionMixin, admin.ModelAdmin):
    form = MyUserForm

    list_display = (
        "uuid",
        "pk",
        "username",
        "email",
        "type",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
        "updated_at",
        "last_login",
    )
    search_fields = (
        "uuid__icontains",
        "username__icontains",
        "email__icontains",
    )
    autocomplete_fields = ("service_provider",)
    list_filter = ("is_staff", "is_superuser", "is_active", "type")
    fieldsets = (
        (
            "Data",
            {
                "fields": (
                    "uuid",
                    "pk",
                    "username",
                    "new_password",
                    "email",
                    "is_active",
                    "type",
                    "service_provider",
                )
            },
        ),
        # (
        #     "Staff Permissions",
        #     {
        #         "fields": (
        #             "groups",
        #             "user_permissions",
        #         )
        #     },
        # ),
        (
            "Dates",
            {"fields": ("last_login", "date_joined", "created_at", "updated_at")},
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
        "created_at",
        "updated_at",
        "pk",
        "uuid",
    )

    class Meta:
        model = MyUser
