import os

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CustomUserCreationForm(UserCreationForm):
    field_order = [
        "username",
        "password1",
        "password2",
        "email",
        "first_name",
        "last_name",
        "is_company",
        "avatar",
    ]

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "is_company",
            "first_name",
            "last_name",
            "avatar",
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
            "first_name",
            "last_name",
            "avatar",
        )
        field_classes = {"username": UsernameField}

    def clean_avatar(self):
        arg_as_str = "avatar"
        if arg_as_str in self.changed_data and self.instance.avatar:
            if os.path.exists(self.instance.avatar.path):
                os.remove(self.instance.avatar.path)
        return self.cleaned_data.get(arg_as_str)

    def clean_login(self):
        return str.lower(self.cleaned_data.get("username"))
