from django import forms
from accounts.models import MyUser


class MyUserForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False, label="Password", help_text="Enter new Password for the user"
    )

    def save(self, commit=True):
        new_password = self.cleaned_data.get("new_password", None)
        obj = super(MyUserForm, self).save(commit=False)
        if new_password:
            obj.set_password(new_password)
        if commit:
            obj.save()
        return obj

    class Meta:
        model = MyUser
        fields = ["new_password"]
        widgets = {"new_password": forms.PasswordInput()}
