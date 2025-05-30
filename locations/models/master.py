from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=64, null=False, blank=False, db_index=True, unique=True
    )
    code = models.CharField(max_length=3, primary_key=True)
    is_active = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.code


class State(models.Model):
    name = models.CharField(max_length=40, null=False, db_index=True, blank=False)
    country = models.ForeignKey(
        Country, null=False, blank=False, on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

    class Meta:
        unique_together = ("country", "name")
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["name"]


class PinCode(models.Model):
    state = models.ForeignKey(State, null=False, blank=False, on_delete=models.PROTECT)
    district = models.CharField(max_length=64, null=False, blank=False)
    city = models.CharField(max_length=64, null=False, blank=False)
    code = models.IntegerField(
        blank=False,
        null=False,
        db_index=True,
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
    )
    is_active = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    def __str__(self):
        return f"{self.code}-{self.district}"
