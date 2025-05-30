from copy import deepcopy

from charges.models import ParkingSpotRate, ParkingSpotHourlyRate
from inventory.models import FloorPlan


def set_values():
    base_floor = FloorPlan.objects.get(pk=112)
    floors = FloorPlan.objects.filter(is_active=True)

    if floors.exists():
        for floor in floors:
            if not ParkingSpotRate.objects.filter(floor=floor).exists():
                print(floor)
                rates = ParkingSpotRate.objects.filter(floor=base_floor)
                print(rates)
                if rates.exists():
                    for rate in rates:
                        new_rate = deepcopy(rate)
                        new_rate.pk = None
                        new_rate.floor = floor
                        new_rate.save()

                        related_manager = getattr(rate, "days")
                        new_related_manager = getattr(new_rate, "days")
                        new_related_manager.set(related_manager.all())
                        hours = ParkingSpotHourlyRate.objects.filter(
                            parking_spot_rate=rate
                        )
                        if hours.exists():
                            for hour in hours:
                                print(hours)
                                new_hour = deepcopy(hour)
                                new_hour.pk = None
                                new_hour.parking_spot_rate = new_rate
                                new_hour.save()
                break
