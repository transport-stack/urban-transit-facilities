from django.contrib import admin

from inventory.forms import FloorPlanForm
from inventory.models import (
    FloorPlan,
    ParkingSpot,
    VehicleType,
    ParkingSpotAvailability,
    FloorPlanPrediction,
    FloorPlanPredictionVehicleWise,
)


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)
    list_display = ("name", "is_active")
    readonly_fields = ("created_at", "updated_at")

    class Meta:
        model = VehicleType


@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    form = FloorPlanForm
    search_fields = ("location__name__icontains",)
    list_display = (
        "pk",
        "location",
        "floor_name",
        "valid_from",
        "valid_till",
    )
    autocomplete_fields = ("location",)

    class Meta:
        model = FloorPlan


@admin.register(ParkingSpotAvailability)
class ParkingSpotAvailabilityAdmin(admin.ModelAdmin):
    search_fields = (
        "vehicle_type__name__icontains",
        "floor__location__name__icontains",
        "floor__floor_name__icontains",
    )
    list_display = ("pk", "floor", "vehicle_type", "total")
    list_filter = ("vehicle_type", "is_active")
    autocomplete_fields = ("floor", "vehicle_type")

    class Meta:
        model = ParkingSpotAvailability


class FloorPlanPredictionVehicleWiseInline(admin.TabularInline):
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("vehicle_type",)
    fields = (
        "vehicle_type",
        "value",
    )
    model = FloorPlanPredictionVehicleWise
    extra = 0


@admin.register(FloorPlanPrediction)
class FloorPlanPredictionAdmin(admin.ModelAdmin):
    inlines = [FloorPlanPredictionVehicleWiseInline]

    search_fields = (
        "floor__location__name__icontains",
        "floor__floor_name__icontains",
    )
    list_display = ("pk", "floor", "day", "time")
    list_filter = ("time", "day")
    autocomplete_fields = ("floor",)

    class Meta:
        model = FloorPlanPrediction


# @admin.register(ParkingSpot)
# class ParkingSpotAdmin(admin.ModelAdmin):
#     search_fields = ("spot_code__icontains",)
#     list_display = (
#         "pk",
#         "spot_code",
#         "floor",
#         "is_available",
#         "is_active",
#     )
#     autocomplete_fields = ("floor",)
#     list_filter = ("is_available", "is_active", "vehicle_types",)
#
#     class Meta:
#         model = ParkingSpot
