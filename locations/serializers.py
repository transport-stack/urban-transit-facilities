from rest_framework import serializers

from locations.models import State, PinCode, Location, Coordinates
from providers.serializers import ServiceProviderSerializer


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["name", "country"]


class PinCodeSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True, many=False)

    class Meta:
        model = PinCode
        fields = ["state", "code", "city", "district"]


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    area = PinCodeSerializer(read_only=True)
    type = serializers.CharField(source="get_type_display", read_only=True)
    provider = ServiceProviderSerializer(read_only=True)
    # payment_mode = PaymentModeSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
