from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.IntegerChoices):
    ADMIN = 100, _("Admin")
    SERVICE_PROVIDER = 200, _("Service Provider")
    SERVICE_CONSUMER = 300, _("Service Consumer")
    CUSTOMER = 400, _("Customer")
    NONE = 0, _("None")
