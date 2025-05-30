import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings

from accounts.constants import UserType
from main.models import TimeStampActiveMixin
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser, TimeStampActiveMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True, db_index=True)
    language_preferred = models.CharField(
        max_length=7, choices=settings.LANGUAGES, default="en", blank=True, null=True
    )
    email = models.EmailField(
        _("email address"), blank=True, null=True, unique=True, db_index=True
    )
    type = models.IntegerField(
        choices=UserType.choices,
        default=UserType.NONE,
        null=False,
        blank=False,
        db_index=True,
    )
    service_provider = models.ForeignKey(
        "providers.ServiceProvider", null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-is_active", "-created_at")

    @property
    def render_sbadmin2_ui(self):
        # TODO: TEMPLATE write this logic
        return True

    @property
    def name(self):
        string = self.first_name + " " + self.last_name
        return string.strip()
