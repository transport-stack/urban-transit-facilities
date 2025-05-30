from django.db import models
from django.utils.translation import gettext_lazy as _


class LocationType(models.IntegerChoices):
    METRO_STATION = 1, _("Metro Station")
    BUS_DEPOT = 2, _("Bus Depot")
    MALL = 3, _("Mall")
    OFFICE = 4, _("Office")
    RESIDENTIAL_AREA = 5, _("Residential Area")
