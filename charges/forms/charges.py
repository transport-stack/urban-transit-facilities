from django import forms
from django.core.exceptions import ValidationError

from charges.models import ParkingSpotRate, ParkingSpotHourlyRate


class ParkingSpotRateForm(forms.ModelForm):
    class Meta:
        model = ParkingSpotRate
        fields = "__all__"

    def clean(self):
        if self.cleaned_data["valid_from"] > self.cleaned_data["valid_till"]:
            raise ValidationError(
                {
                    "valid_from": "Valid From can't be greater than Valid Till",
                    "valid_till": "Valid Till can't be less than Valid From",
                }
            )

        parking_spot_master = ParkingSpotRate.objects.filter(
            floor=self.cleaned_data["floor"],
            offer=self.cleaned_data["offer"],
        ).exclude(pk=self.instance.pk)

        for day in self.cleaned_data["days"].all():
            parking_spot = parking_spot_master.filter(
                days__exact=day, vehicle_type=self.cleaned_data["vehicle_type"]
            )
            if parking_spot.filter(
                valid_from__lt=self.cleaned_data["valid_from"],
                valid_till__gt=self.cleaned_data["valid_from"],
            ).exists():
                raise ValidationError(
                    {
                        "valid_from": f"Rate already exists for this time range for this day on {day}."
                    }
                )
            if parking_spot.filter(
                valid_from__lt=self.cleaned_data["valid_till"],
                valid_till__gt=self.cleaned_data["valid_till"],
            ).exists():
                raise ValidationError(
                    {
                        "valid_till": f"Rate already exists for this time range for this day on {day}."
                    }
                )
            return self.cleaned_data


class ParkingSpotHourlyRateForm(forms.ModelForm):
    class Meta:
        model = ParkingSpotHourlyRate
        fields = "__all__"

    def clean(self):
        if self.cleaned_data["valid_from"] > self.cleaned_data["valid_till"]:
            raise ValidationError(
                {
                    "valid_from": "Valid From can't be greater than Valid Till",
                    "valid_till": "Valid Till can't be less than Valid From",
                }
            )

        parking_spot = ParkingSpotHourlyRate.objects.filter(
            parking_spot_rate=self.cleaned_data["parking_spot_rate"],
        ).exclude(pk=self.instance.pk)

        if parking_spot.filter(
            valid_from__lt=self.cleaned_data["valid_from"],
            valid_till__gt=self.cleaned_data["valid_from"],
        ).exists():
            raise ValidationError(
                {
                    "valid_from": f"Rate already exists for this time range for this rate."
                }
            )
        if parking_spot.filter(
            valid_from__lt=self.cleaned_data["valid_till"],
            valid_till__gt=self.cleaned_data["valid_till"],
        ).exists():
            raise ValidationError(
                {
                    "valid_till": f"Rate already exists for this time range for this rate."
                }
            )
        return self.cleaned_data
