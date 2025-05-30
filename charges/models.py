from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from inventory.models import (
    FloorPlan,
    VehicleType,
    default_start_time,
    default_end_time,
)
from main.models import TimeStampActiveMixin, Days


class Offer(TimeStampActiveMixin):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.description

    @classmethod
    def get_default_pk(cls):
        exam, created = cls.objects.get_or_create(
            name="GENERAL",
        )
        return exam.pk

    @classmethod
    def get_default(cls):
        exam, created = cls.objects.get_or_create(
            name="GENERAL",
        )
        return exam

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.name.replace(" ", "_")
            self.name = self.name.upper()
        if not self.description:
            self.description = self.name
        super(Offer, self).save(*args, **kwargs)


class PaymentMode(TimeStampActiveMixin):
    name = models.CharField(max_length=64, primary_key=True)
    is_online = models.BooleanField(
        default=True, null=False, blank=False, db_index=True
    )

    class Meta:
        verbose_name = "Payment Mode"
        verbose_name_plural = "Payment Modes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.name.replace(" ", "_")
            self.name = self.name.upper()
        if not self.description:
            self.description = self.name
        super(PaymentMode, self).save(*args, **kwargs)


class ParkingSpotRate(TimeStampActiveMixin):
    floor = models.ForeignKey(
        FloorPlan, null=False, blank=False, on_delete=models.CASCADE
    )
    offer = models.ForeignKey(
        Offer,
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        default=Offer.get_default_pk,
    )
    vehicle_type = models.ForeignKey(
        VehicleType,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="parking_spot_rate_vehicle",
    )
    days = models.ManyToManyField(Days, blank=False, db_index=True)
    is_parking_allowed = models.BooleanField(
        default=True, null=False, blank=False, db_index=True
    )
    valid_from = models.TimeField(
        null=True, blank=True, db_index=True, default=default_start_time
    )
    valid_till = models.TimeField(
        null=True, blank=True, db_index=True, default=default_end_time
    )
    night_charge_per_hour = models.FloatField(
        null=False,
        blank=False,
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
    )
    night_charge_fixed = models.FloatField(
        null=False,
        blank=False,
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"Parking Spot Rate {self.pk}"

    @property
    def long_description(self):
        hourly_rates = self.parking_spot_hourly_rate.all()
        string = ""
        for rate in hourly_rates:
            temp = ""
            if rate.fixed_rate > 0:
                temp += f"₹{rate.fixed_rate} + "
            if rate.valid_from > 0:
                temp += f"₹{rate.hourly_rate}/hr from {rate.valid_from} hrs till {rate.valid_till} hrs upto ₹{rate.max_rate}"
            else:
                temp += f"₹{rate.hourly_rate}/hr till {rate.valid_till} hrs upto ₹{rate.max_rate}"
            string += temp + "\n"
        if self.night_charge_fixed > 0 or self.night_charge_per_hour > 0:
            string += "Night Charges: "
            if self.night_charge_fixed > 0:
                string += f"₹{self.night_charge_fixed}"
                if self.night_charge_per_hour > 0:
                    string += " + "
            if self.night_charge_fixed > 0:
                string += f"₹{self.night_charge_per_hour}/hr"
            string += " extra"
        string = string.strip("\n")
        return string

    class Meta:
        verbose_name = "Parking Spot Rate"
        verbose_name_plural = "Parking Spot Rates"

    def save(self, *args, **kwargs):
        if not self.valid_from:
            self.valid_from = self.floor.valid_from
        if not self.valid_till:
            self.valid_till = self.floor.valid_till
        super(ParkingSpotRate, self).save(*args, **kwargs)


class ParkingSpotHourlyRate(TimeStampActiveMixin):
    parking_spot_rate = models.ForeignKey(
        ParkingSpotRate,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="parking_spot_hourly_rate",
    )
    fixed_rate = models.FloatField(
        null=False,
        blank=False,
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
    )
    max_rate = models.FloatField(
        null=False,
        blank=False,
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
    )
    hourly_rate = models.FloatField(
        null=False,
        blank=False,
        default=0,
        db_index=True,
        validators=[MinValueValidator(0)],
    )
    valid_from = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        db_index=True,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        help_text="Value between 0 and 24",
    )
    valid_till = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        db_index=True,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        help_text="Value between 0 and 24",
    )

    def calculate_charge(self, num_hours):
        return min(self.max_rate, self.fixed_rate + self.hourly_rate * num_hours)

    def __str__(self):
        return f"Parking Spot Hourly Rate for {self.parking_spot_rate.pk}"

    class Meta:
        verbose_name = "Parking Spot Hourly Rate"
        verbose_name_plural = "Parking Spot Hourly Rates"

    def save(self, *args, **kwargs):
        if not self.parking_spot_rate.floor.is_parking_paid:
            self.fixed_rate = 0
            self.hourly_rate = 0
            self.max_rate = 0
        super(ParkingSpotHourlyRate, self).save(*args, **kwargs)
