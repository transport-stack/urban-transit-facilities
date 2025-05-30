from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from main.models import TimeStampActiveMixin
from accounts.models import MyUser


class ServiceProvider(TimeStampActiveMixin):
    name = models.CharField(max_length=128, null=False, blank=False, db_index=True)
    phone_num = PhoneNumberField(null=True, blank=True, db_index=True)

    added_by = models.ForeignKey(
        MyUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="provider_added_by",
    )

    def __str__(self):
        return str(self.name) + " | " + str(self.phone_num)

    class Meta:
        unique_together = ("name", "phone_num")
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
