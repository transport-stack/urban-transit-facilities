from rest_framework import serializers

from charges.models import Offer, ParkingSpotRate, PaymentMode, ParkingSpotHourlyRate
from inventory.models import VehicleType


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ["created_at", "updated_at", "is_active"]


class ParkingSpotHourlyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpotHourlyRate
        exclude = ["created_at", "updated_at", "is_active"]


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        exclude = ["created_at", "updated_at", "is_active", "logo_image"]


class ParkingSpotRateSerializer(serializers.ModelSerializer):
    rate_card = ParkingSpotHourlyRateSerializer(
        read_only=True, many=True, source="parking_spot_hourly_rate"
    )

    class Meta:
        model = ParkingSpotRate
        exclude = ["created_at", "updated_at", "is_active"]


class ParkingSpotRateCompleteSerializer(serializers.ModelSerializer):
    rate_card = ParkingSpotHourlyRateSerializer(
        read_only=True, many=True, source="parking_spot_hourly_rate"
    )
    long_description = serializers.ReadOnlyField()

    class Meta:
        model = ParkingSpotRate
        exclude = ["created_at", "updated_at", "is_active"]


class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        exclude = ["created_at", "updated_at", "is_active"]
