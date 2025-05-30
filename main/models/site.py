import datetime

from django.core.validators import MinValueValidator
from django.db import models

from .helpers import SingletonModel
from django.core.validators import MinValueValidator, RegexValidator


class Days(models.Model):
    day = models.CharField(max_length=9, primary_key=True)
    is_active = models.BooleanField(
        default=True, blank=False, null=False, db_index=True
    )
    order = models.IntegerField(
        default=0, null=False, blank=False, db_index=True, unique=True
    )
    master_order = models.IntegerField(
        default=0, null=False, blank=False, db_index=True, unique=True
    )

    def __str__(self):
        return self.day

    class Meta:
        ordering = ("order", "day")
        verbose_name = "Day"
        verbose_name_plural = "Days"


hex_color_validator = RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Invalid hex color.')

class Settings(SingletonModel):
    # Existing fields
    title = models.CharField(max_length=127, help_text="Title for the site")
    starting_of_the_week = models.ForeignKey(
        Days, null=True, blank=False, on_delete=models.PROTECT
    )
    base_url = models.URLField(null=True, blank=True)

    occupancy_level_1 = models.CharField(max_length=16, null=True, blank=True, help_text="This level represents low occupancy.")
    occupancy_level_1_threshold = models.FloatField(
        validators=[MinValueValidator(0)], default=0, null=False, blank=False
    )
    occupancy_level_1_color_primary = models.CharField(
        max_length=7, default='#CCFFCC', validators=[hex_color_validator]
    )
    occupancy_level_1_color_secondary = models.CharField(
        max_length=7, default='#99FF99', validators=[hex_color_validator]
    )

    occupancy_level_2 = models.CharField(max_length=16, null=True, blank=True, help_text="This level represents medium occupancy.")
    occupancy_level_2_threshold = models.FloatField(
        validators=[MinValueValidator(0)], default=0, null=False, blank=False
    )
    occupancy_level_2_color_primary = models.CharField(
        max_length=7, default='#FFFFCC', validators=[hex_color_validator]
    )
    occupancy_level_2_color_secondary = models.CharField(
        max_length=7, default='#FFFF99', validators=[hex_color_validator]
    )

    occupancy_level_3 = models.CharField(max_length=16, null=True, blank=True, help_text="This level represents high occupancy.")
    occupancy_level_3_color_primary = models.CharField(
        max_length=7, default='#FFCCCC', validators=[hex_color_validator]
    )
    occupancy_level_3_color_secondary = models.CharField(
        max_length=7, default='#FF9999', validators=[hex_color_validator]
    )


    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
        ordering = ("-created_at",)
