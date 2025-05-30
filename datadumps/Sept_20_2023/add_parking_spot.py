from inventory.models import FloorPlan, VehicleType
from charges.models import ParkingSpotRate, ParkingSpotHourlyRate, Offer
from main.models import Days

offer = Offer.get_default()
BICYCLE = VehicleType.objects.get(name="BICYCLE")
PERSONAL_2 = VehicleType.objects.get(name="TWO_WHEELER")
PERSONAL_4 = VehicleType.objects.get(name="CAR_JEEP_VAN")


def set_spot_rate():
    floors = FloorPlan.objects.filter(is_active=True)
    for floor in floors:
        bicycle_spot_rate = ParkingSpotRate.objects.create(
            floor=floor,
            offer=offer,
            is_parking_allowed=True,
            vehicle_type=BICYCLE,
        )
        personal_2_spot_rate = ParkingSpotRate.objects.create(
            floor=floor,
            offer=offer,
            is_parking_allowed=True,
            vehicle_type=PERSONAL_2,
        )
        personal_4_spot_rate = ParkingSpotRate.objects.create(
            floor=floor,
            offer=offer,
            is_parking_allowed=True,
            vehicle_type=PERSONAL_4,
        )
        for day in Days.objects.all():
            bicycle_spot_rate.days.add(day)
            personal_2_spot_rate.days.add(day)
            personal_4_spot_rate.days.add(day)

        rates = [
            ParkingSpotHourlyRate(
                parking_spot_rate=bicycle_spot_rate,
                fixed_rate=0,
                hourly_rate=5,
                max_rate=30,
                valid_from=0,
                valid_till=6,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=bicycle_spot_rate,
                fixed_rate=30,
                hourly_rate=5,
                max_rate=60,
                valid_from=6,
                valid_till=12,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=bicycle_spot_rate,
                fixed_rate=60,
                hourly_rate=10,
                max_rate=180,
                valid_from=12,
                valid_till=24,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_2_spot_rate,
                fixed_rate=0,
                hourly_rate=15,
                max_rate=90,
                valid_from=0,
                valid_till=6,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_2_spot_rate,
                fixed_rate=90,
                hourly_rate=25,
                max_rate=240,
                valid_from=6,
                valid_till=12,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_2_spot_rate,
                fixed_rate=240,
                hourly_rate=60,
                max_rate=960,
                valid_from=12,
                valid_till=24,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_4_spot_rate,
                fixed_rate=0,
                hourly_rate=30,
                max_rate=180,
                valid_from=0,
                valid_till=6,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_4_spot_rate,
                fixed_rate=180,
                hourly_rate=50,
                max_rate=480,
                valid_from=6,
                valid_till=12,
            ),
            ParkingSpotHourlyRate(
                parking_spot_rate=personal_4_spot_rate,
                fixed_rate=480,
                hourly_rate=60,
                max_rate=1200,
                valid_from=12,
                valid_till=24,
            ),
        ]

        ParkingSpotHourlyRate.objects.bulk_create(rates)
