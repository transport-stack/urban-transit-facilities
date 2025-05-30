from django.contrib import admin

from locations.models import State, Country, PinCode, Location, Coordinates


# Register your models here.
@admin.register(State)
class StateListAdmin(admin.ModelAdmin):
    search_fields = ("name__icontains",)
    autocomplete_fields = ("country",)
    list_display = ("pk", "name", "country")
    list_filter = ("country",)

    class Meta:
        model = State


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_filter = ("is_active",)
    list_display = ("name", "code", "is_active")
    search_fields = ("name__icontains",)

    class Meta:
        model = Country


@admin.register(Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ("latitude", "longitude")
    search_fields = ("latitude__exact", "longitude__exact")

    class Meta:
        model = Coordinates


@admin.register(PinCode)
class PinCodeAdmin(admin.ModelAdmin):
    list_filter = ("state", "is_active")
    list_display = ("id", "code", "state")
    search_fields = ("code",)

    class Meta:
        model = PinCode


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_filter = ("type",)
    list_display = ("name", "type", "is_active")
    autocomplete_fields = ("area", "provider")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name__icontains", "address__icontains", "code__icontains")

    class Meta:
        model = Location
