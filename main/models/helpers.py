from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

BOOLEAN_CHOICES = ((True, "Yes"), (False, "No"))


class TimeStampActiveMixin(models.Model):
    """TimeStampActiveMixin acts as parent class to model for adding creation and update time fields

    Attributes
    ----------
    created_at : models.DateTimeField
        Auto adds the now value of datetime, and is not affected by further updates
    updated_at : models.DateTimeField
        Auto adds the now value of datetime, and is updated to new value when further updates happen
    is_active : models.BooleanField
        Whether object is active or not (soft delete)
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Created date & time"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last Updated date & time"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether is active or not?",
        db_index=True,
    )
    description = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = (
            "-is_active",
            "-created_at",
        )

    def update_object(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


class SingletonModel(TimeStampActiveMixin):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)
