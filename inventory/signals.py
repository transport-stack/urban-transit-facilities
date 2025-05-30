from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models import (
    FloorPlan,
    ParkingSpot,
    VehicleType,
    ParkingSpotAvailability,
)


@receiver(post_save, sender=FloorPlan)
def post_floor_plan_creation(sender, instance, created, **kwargs):
    if created:
        floor_plan = FloorPlan.objects.get(pk=instance.pk)
        # for spot_num in range(floor_plan.max_slots):
        #     ParkingSpot.objects.create(
        #         floor=floor_plan,
        #         spot_code=spot_num + 1,
        #         is_available=True,
        #         is_elevated=False,
        #     )

        vehicle_types = VehicleType.objects.filter()
        if vehicle_types.exists():
            for vehicle_type in vehicle_types:
                ParkingSpotAvailability.objects.create(
                    floor=floor_plan, vehicle_type=vehicle_type
                )
