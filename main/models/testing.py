from django.db import models

from .helpers import TimeStampActiveMixin


class TestModel(TimeStampActiveMixin):
    name = models.CharField(max_length=127, help_text="Some test field")

    class Meta:
        verbose_name = "Test Model"
        verbose_name_plural = "Test Model"
        ordering = ("-is_active", "-created_at")
