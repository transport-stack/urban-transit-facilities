import django_filters
from locations.models import PinCode, State, Location


class PinCodeFilter(django_filters.FilterSet):
    class Meta:
        model = PinCode
        fields = {
            "district": ["icontains"],
            "city": ["icontains"],
            "code": ["exact"],
        }


class StateFilter(django_filters.FilterSet):
    class Meta:
        model = State
        fields = {"name": ["icontains"]}


class LocationFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(field_name="address", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_parking_available = django_filters.BooleanFilter(
        field_name="is_parking_available"
    )

    class Meta:
        model = Location
        fields = ["address", "name", "is_parking_available"]
