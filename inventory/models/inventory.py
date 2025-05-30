from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import MyUser
from inventory.models.helpers import VehicleType, default_start_time, default_end_time
from locations.models import Location
from main.models import TimeStampActiveMixin, Days


class FloorPlan(TimeStampActiveMixin):
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    location = models.ForeignKey(
        Location,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="location_floors",
    )
    floor_name = models.CharField(max_length=16, null=True, blank=True, db_index=True)
    floor_name_long = models.CharField(
        max_length=32, null=True, blank=True, db_index=True
    )
    floor_num = models.PositiveIntegerField(
        default=0, null=False, blank=False, db_index=True
    )
    gate_location = models.CharField(max_length=64, null=True, blank=True)
    gate_num = models.PositiveIntegerField(null=True, blank=True)
    num_rows = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=[MinValueValidator(1)],
    )
    num_columns = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=[MinValueValidator(1)],
    )
    max_slots = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        db_index=True,
        validators=[MinValueValidator(1)],
    )

    is_parking_paid = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    has_toilet = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    is_parking_available = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    is_divyang_friendly = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    is_elevated = models.BooleanField(
        default=False, blank=False, null=False, db_index=True
    )
    valid_from = models.TimeField(
        null=True, blank=False, db_index=True, default=default_start_time
    )
    valid_till = models.TimeField(
        null=True, blank=False, db_index=True, default=default_end_time
    )

    def save(self, *args, **kwargs):
        if not self.floor_name:
            self.floor_name = str(self.floor_num)
        if not self.floor_name_long:
            self.floor_name_long = self.floor_name
        if not self.latitude and self.location and self.location.latitude:
            self.latitude = self.location.latitude
        if not self.longitude and self.location and self.location.longitude:
            self.longitude = self.location.longitude
        super(FloorPlan, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.location.name) + "-" + str(self.floor_name)

    class Meta:
        ordering = ("location", "floor_name", "-created_at")
        unique_together = ("location", "floor_name")
        verbose_name = "Floor Plan"
        verbose_name_plural = "Floor Plans"


class ParkingSpot(TimeStampActiveMixin):
    floor = models.ForeignKey(
        FloorPlan,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="parking_spot_floor",
    )
    spot_code = models.CharField(max_length=8, null=False, blank=False, db_index=True)
    is_elevated = models.BooleanField(
        default=False, blank=False, null=False, db_index=True
    )
    is_available = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    row_num = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    column_num = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    vehicle_types = models.ManyToManyField(
        VehicleType, blank=True, related_name="spot_vehicle_types", db_index=True
    )

    def is_vehicle_type_allowed(self, vehicle_type: VehicleType):
        return self.vehicle_types.contains(vehicle_type)

    class Meta:
        unique_together = (("floor", "spot_code"),)
        verbose_name = "Parking Spot"
        verbose_name_plural = "Parking Spots"

    def clean(self):
        if self.row_num and self.floor.num_rows and self.row_num > self.floor.num_rows:
            raise ValidationError(
                {"row_num": "Row number can not exceed max number of rows."}
            )
        if (
            self.column_num
            and self.floor.num_columns
            and self.column_num > self.floor.num_columns
        ):
            raise ValidationError(
                {"column_num": "Column number can not exceed max number of columns."}
            )


class ParkingSpotAvailability(TimeStampActiveMixin):
    floor = models.ForeignKey(
        FloorPlan,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="floor_parking_availability",
    )
    vehicle_type = models.ForeignKey(
        VehicleType, null=False, blank=False, on_delete=models.CASCADE
    )
    total = models.PositiveIntegerField(
        default=0, null=False, blank=False, db_index=True
    )
    available = models.PositiveIntegerField(
        default=0, null=False, blank=False, db_index=True
    )
    added_by = models.ForeignKey(
        MyUser, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Parking Spot Availability"
        verbose_name_plural = "Parking Spot Availabilities"
        unique_together = ("floor", "vehicle_type")

    def __str__(self):
        return self.floor.floor_name + "-" + str(self.vehicle_type.name)


class FloorPlanPrediction(TimeStampActiveMixin):
    floor = models.ForeignKey(
        FloorPlan, null=False, blank=False, on_delete=models.CASCADE
    )
    day = models.ForeignKey(Days, null=False, blank=False, on_delete=models.CASCADE)
    time = models.TimeField(null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "Floor Plan Prediction"
        verbose_name_plural = "Floor Plan Predictions"
        unique_together = ("floor", "day", "time", "is_active")
        ordering = ("day", "time", "created_at")


class FloorPlanPredictionVehicleWise(TimeStampActiveMixin):
    prediction = models.ForeignKey(
        FloorPlanPrediction, null=False, blank=False, on_delete=models.CASCADE
    )
    vehicle_type = models.ForeignKey(
        VehicleType, null=False, blank=False, on_delete=models.CASCADE
    )
    value = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        null=False,
        blank=False,
        db_index=True,
    )

    class Meta:
        verbose_name = "Vehicle-Type Floor Plan Prediction"
        verbose_name_plural = "Vehicle-Type Floor Plan Predictions"
        unique_together = ("prediction", "vehicle_type", "is_active")
        ordering = ("vehicle_type", "created_at")
