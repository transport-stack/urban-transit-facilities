import datetime

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from charges.models import ParkingSpotRate
from charges.serializers import ParkingSpotRateSerializer
from inventory.models import (
    FloorPlan,
    ParkingSpot,
    VehicleType,
    ParkingSpotAvailability,
    FloorPlanPrediction,
)
from locations.serializers import LocationSerializer
from main.models.site import Days, Settings


class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        exclude = ["created_at", "updated_at"]


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        exclude = ["created_at", "updated_at", "is_active"]


class ParkingSpotAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpotAvailability
        fields = ["vehicle_type", "available"]


class FloorPlanSerializer(serializers.ModelSerializer):
    parking_spot_availability = serializers.SerializerMethodField(
        method_name="get_parking_spot_availability", read_only=True
    )

    location = LocationSerializer(many=False, read_only=True)

    rate = serializers.SerializerMethodField(method_name="get_rate", read_only=True)

    def get_parking_spot_availability(self, obj: FloorPlan):
        availability = obj.floor_parking_availability.filter(
            vehicle_type__is_active=True, total__gt=0
        )
        return ParkingSpotAvailabilitySerializer(availability, many=True).data

    def get_rate(self, obj: FloorPlan):
        # TODO: Check for vehicle type
        cur_time = datetime.datetime.now().time()
        cur_day = datetime.datetime.now().weekday()

        availability = obj.floor_parking_availability.filter(
            vehicle_type__is_active=True, total__gt=0
        )

        spot_rates = ParkingSpotRate.objects.filter(
            floor=obj,
            valid_from__lte=cur_time,
            valid_till__gte=cur_time,
            vehicle_type__in=[a.vehicle_type for a in availability],
            days__in=[Days.objects.get(master_order=cur_day + 1)],
        ).order_by("-id")

        if spot_rates.exists():
            return ParkingSpotRateSerializer(spot_rates, many=True).data
        else:
            return None

    class Meta:
        model = FloorPlan
        exclude = ["created_at", "updated_at"]


class FloorPlanPredictionSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField(method_name="get_values", read_only=True)

    class Meta:
        model = FloorPlanPrediction
        fields = ["floor", "day", "time", "values"]

    def get_values(self, obj: FloorPlanPrediction):
        vehicles = obj.floorplanpredictionvehiclewise_set.all()
        value = {}
        settings = Settings.load()

        for vehicle in vehicles:
            occupancy_data = {}
            if vehicle.value >= settings.occupancy_level_1_threshold:
                occupancy_data["level"] = settings.occupancy_level_1
                occupancy_data[
                    "color_primary"
                ] = settings.occupancy_level_1_color_primary
                occupancy_data[
                    "color_secondary"
                ] = settings.occupancy_level_1_color_secondary
            elif vehicle.value >= settings.occupancy_level_2_threshold:
                occupancy_data["level"] = settings.occupancy_level_2
                occupancy_data[
                    "color_primary"
                ] = settings.occupancy_level_2_color_primary
                occupancy_data[
                    "color_secondary"
                ] = settings.occupancy_level_2_color_secondary
            else:
                occupancy_data["level"] = settings.occupancy_level_3
                occupancy_data[
                    "color_primary"
                ] = settings.occupancy_level_3_color_primary
                occupancy_data[
                    "color_secondary"
                ] = settings.occupancy_level_3_color_secondary

            value[vehicle.vehicle_type.name] = occupancy_data

        return value
