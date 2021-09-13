from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs["class"] = "form-control"
