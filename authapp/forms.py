from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CustomUserCreationForm(UserCreationForm):
    field_order = [
        "username",
        "password1",
        "password2",
        "email",
        "is_company",
    ]

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "is_company",
        )
        field_classes = {"username": UsernameField}

    def clean_login(self):
        return str.lower(self.cleaned_data.get("username"))


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )
        field_classes = {"username": UsernameField}

    def clean_login(self):
        return str.lower(self.cleaned_data.get("username"))
