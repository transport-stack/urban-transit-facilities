import django_filters

from inventory.models import FloorPlan, ParkingSpot, VehicleType, FloorPlanPrediction
from main.models import Days


class FloorPlanFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(
        method="location_name_search", label="location"
    )
    address = django_filters.CharFilter(method="address_search", label="address")
    vehicle_type = django_filters.CharFilter(method="vehicle_type_search")

    def address_search(self, queryset, value, *args, **kwargs):
        try:
            if args:
                queryset = queryset.filter(location__address__icontains=args[0])
        except ValueError:
            pass
        return queryset

    def location_name_search(self, queryset, value, *args, **kwargs):
        try:
            if args:
                ids = args[0].split(",")
                ids = [i.strip() for i in ids]
                location = ids[0]
                queryset = queryset.filter(location__name__icontains=location)
        except ValueError:
            pass
        return queryset

    def vehicle_type_search(self, queryset, value, *args, **kwargs):
        try:
            if args:
                ids = args[0].split(",")
                ids = [i.strip() for i in ids]
                queryset = queryset.filter(parkingspotrate__vehicle_type__name__in=ids)
        except ValueError:
            pass
        return queryset

    class Meta:
        model = FloorPlan
        fields = ["location", "vehicle_type"]


class VehicleTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", required=False, lookup_expr="icontains", label="name"
    )

    class Meta:
        model = VehicleType
        fields = ["name"]


class ParkingSpotFilter(django_filters.FilterSet):
    floor = django_filters.NumberFilter(
        field_name="floor__pk", required=False, label="floor"
    )
    vehicle_type = django_filters.CharFilter(
        field_name="vehicle_types__name", lookup_expr="contains"
    )

    class Meta:
        model = ParkingSpot
        fields = ["floor", "vehicle_type"]


class FloorPlanPredictionFilter(django_filters.FilterSet):
    floor = django_filters.NumberFilter(
        field_name="floor__pk", required=True, label="floor"
    )
    day = django_filters.ModelChoiceFilter(queryset=Days.objects.all(), required=False)
    start_time = django_filters.TimeFilter(
        field_name="time", lookup_expr="gte", required=False
    )
    end_time = django_filters.TimeFilter(
        field_name="time", lookup_expr="lte", required=False
    )

    class Meta:
        model = FloorPlanPrediction
        fields = ["floor", "day", "start_time", "end_time"]
