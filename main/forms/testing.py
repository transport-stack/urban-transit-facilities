from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from main.models import TestModel


class TestModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(TestModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-vertical"
        self.helper.label_class = "mb-0 mb-lg-1"
        self.helper.field_class = "mb-2 mb-lg-3"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn-primary text-white px-4 py-2 mt-1")
        )

    class Meta:
        model = TestModel
        fields = ["name"]
