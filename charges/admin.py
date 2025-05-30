from admin_numeric_filter.admin import (
    RangeNumericFilter,
    SliderNumericFilter,
    NumericFilterModelAdmin,
)
from django.contrib import admin

from charges.forms import ParkingSpotRateForm, ParkingSpotHourlyRateForm
from charges.models import Offer, PaymentMode, ParkingSpotRate, ParkingSpotHourlyRate


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)
    list_display = ("name", "is_active")
    readonly_fields = ("created_at", "updated_at")

    class Meta:
        model = Offer


@admin.register(PaymentMode)
class PaymentModeAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)
    list_display = ("name", "is_active", "is_online")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("is_active", "is_online")

    class Meta:
        model = PaymentMode


class ParkingSpotHourlyRateInline(admin.TabularInline):
    form = ParkingSpotHourlyRateForm
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("parking_spot_rate",)
    fields = (
        "is_active",
        "fixed_rate",
        "max_rate",
        "hourly_rate",
        "valid_from",
        "valid_till",
    )
    model = ParkingSpotHourlyRate
    extra = 0


@admin.register(ParkingSpotRate)
class ParkingSpotRateAdmin(admin.ModelAdmin):
    form = ParkingSpotRateForm
    inlines = [ParkingSpotHourlyRateInline]
    search_fields = ("floor__location__name__icontains",)
    list_display = (
        "pk",
        "floor",
        "valid_from",
        "valid_till",
        "get_days",
        "vehicle_type",
    )
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("floor",)
    list_filter = ("is_active", "is_parking_allowed", "days", "vehicle_type")

    def get_days(self, obj: ParkingSpotRate):
        return ", ".join([p.day for p in obj.days.all()])

    class Meta:
        model = ParkingSpotRate


@admin.register(ParkingSpotHourlyRate)
class ParkingSpotHourlyRateAdmin(NumericFilterModelAdmin):
    form = ParkingSpotHourlyRateForm
    search_fields = ("parking_spot_rate__floor__location__name__icontains",)
    list_display = (
        "pk",
        "parking_spot_rate",
        "valid_from",
        "valid_till",
        "fixed_rate",
        "hourly_rate",
    )
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("parking_spot_rate",)
    list_filter = (
        "is_active",
        ("valid_from", SliderNumericFilter),
        ("valid_till", SliderNumericFilter),
    )

    class Meta:
        model = ParkingSpotHourlyRate
