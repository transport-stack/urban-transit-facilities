from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from locations.models import PinCode
from locations.models.constants import LocationType
from main.models import TimeStampActiveMixin
from providers.models import ServiceProvider


class Coordinates(models.Model):
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    def __str__(self):
        return str(self.latitude) + "-" + str(self.longitude)

    class Meta:
        verbose_name = "Coordinate"
        verbose_name_plural = "Coordinates"


class Location(TimeStampActiveMixin, Coordinates):
    name = models.CharField(max_length=256, blank=False, null=False, db_index=True)
    code = models.CharField(max_length=5, null=True, blank=True, db_index=True)
    address = models.CharField(max_length=1000, blank=True)
    type = models.IntegerField(
        choices=LocationType.choices,
        default=LocationType.BUS_DEPOT,
        blank=False,
        db_index=True,
    )
    area = models.ForeignKey(PinCode, null=True, blank=True, on_delete=models.PROTECT)
    is_parking_available = models.BooleanField(
        default=True, null=False, blank=False, db_index=True
    )
    num_gates = models.PositiveIntegerField(
        null=True, blank=True, db_index=True, default=0
    )
    num_floors = models.PositiveIntegerField(
        null=False, blank=False, db_index=True, default=0
    )
    phone_num = PhoneNumberField(null=True, blank=True, db_index=True)

    # Flags
    is_underground = models.BooleanField(
        default=False, null=False, blank=False, db_index=True
    )
    is_junction = models.BooleanField(
        default=False, null=False, blank=False, db_index=True
    )

    payment_mode = models.ManyToManyField(
        "charges.PaymentMode", blank=True, db_index=True
    )

    # Electric Charger
    has_electric_charger = models.BooleanField(
        default=False, null=False, blank=False, db_index=True
    )
    electric_charger_capacity = models.FloatField(
        default=0, null=False, blank=False, db_index=True
    )
    num_electric_charger = models.PositiveIntegerField(
        default=0, null=False, blank=False, db_index=True
    )

    provider = models.ForeignKey(
        ServiceProvider, null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    @property
    def name_long(self):
        return str(self.__str__()) + f", {self.get_type_display()}"

    class Meta:
        unique_together = ("code", "area")
        verbose_name = "Location"
        verbose_name_plural = "Locations"
