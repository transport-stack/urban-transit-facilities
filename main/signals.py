from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Settings, Days


@receiver(post_save, sender=Settings)
def post_settings(sender, instance: Settings, created, **kwargs):
    if instance.starting_of_the_week:
        if Days.objects.count() == 7:
            starting_of_the_week_order = instance.starting_of_the_week.master_order
            Days.objects.filter(pk="Monday").update(
                order=(1 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Tuesday").update(
                order=(2 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Wednesday").update(
                order=(3 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Thursday").update(
                order=(4 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Friday").update(
                order=(5 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Saturday").update(
                order=(6 - starting_of_the_week_order) % 7 + 1
            )
            Days.objects.filter(pk="Sunday").update(
                order=(7 - starting_of_the_week_order) % 7 + 1
            )
