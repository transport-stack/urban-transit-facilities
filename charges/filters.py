import django_filters

from charges.models import Offer, ParkingSpotRate, PaymentMode


class OfferFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Offer
        fields = ["name"]


class ParkingSpotRateFilter(django_filters.FilterSet):
    floor = django_filters.NumberFilter(
        field_name="floor__pk", required=True, label="floor"
    )
    vehicle_type = django_filters.CharFilter(
        field_name="vehicle_type__name", lookup_expr="contains"
    )

    class Meta:
        model = ParkingSpotRate
        fields = ["floor", "vehicle_type"]


class PaymentModeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", required=False, lookup_expr="icontains", label="name"
    )

    class Meta:
        model = PaymentMode
        fields = ["name"]
