import datetime

from cropperjs.models import CropperImageField
from django.db import models
import urllib.parse
from main.models import TimeStampActiveMixin, Settings


class VehicleType(TimeStampActiveMixin):
    name = models.CharField(max_length=64, primary_key=True)
    logo_image = CropperImageField(
        help_text="Vehicle Type Image",
        dimensions=(256, 256),
        null=True,
        blank=True,
    )
    logo = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return str(self.description)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.name.replace(" ", "_")
            self.name = self.name.upper()
        if self.logo_image:
            settings = Settings.load()
            if settings.base_url:
                self.logo = urllib.parse.urljoin(settings.base_url, self.logo_image.url)
            else:
                self.logo = self.logo_image.url
        if not self.description:
            self.description = self.name
        super(VehicleType, self).save(*args, **kwargs)


def default_start_time():
    return datetime.time(0, 0, 0)


def default_end_time():
    return datetime.time(23, 59, 59)
