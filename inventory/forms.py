from django import forms
from django.core.exceptions import ValidationError

from inventory.models import FloorPlan


class FloorPlanForm(forms.ModelForm):
    class Meta:
        model = FloorPlan
        fields = "__all__"

    def clean(self):
        if self.cleaned_data["valid_from"] > self.cleaned_data["valid_till"]:
            raise ValidationError(
                {
                    "valid_from": "Valid From can't be greater than Valid Till",
                    "valid_till": "Valid Till can't be less than Valid From",
                }
            )

        parking_spot_master = FloorPlan.objects.filter(
            location=self.cleaned_data["location"]
        ).exclude(pk=self.instance.pk)

        if parking_spot_master.filter(
            valid_from__lt=self.cleaned_data["valid_from"],
            valid_till__gt=self.cleaned_data["valid_from"],
        ).exists():
            raise ValidationError(
                {"valid_from": f"Floor Plan already exists for this time range."}
            )
        if parking_spot_master.filter(
            valid_from__lt=self.cleaned_data["valid_till"],
            valid_till__gt=self.cleaned_data["valid_till"],
        ).exists():
            raise ValidationError(
                {"valid_till": f"Floor Plan already exists for this time range."}
            )
        return self.cleaned_data
