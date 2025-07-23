from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import datetime
import re


def validate_age(birth_date):
    today = datetime.date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    if age < 18:
        raise ValidationError("You must be at least 18 years old to register.")


def validate_phone_number(phone):
    phone_regex = re.compile(
        r"^0\d{9}$"
    )  # Ensures the phone number starts with 0 and is exactly 10 digits long
    if not phone_regex.match(phone):
        raise ValidationError(
            "Phone number must be entered in the format: '0XXXXXXXXX' and must have exactly 10 digits."
        )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=10)
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"onfocus": "(this.type='date')"}),
        input_formats=["%d-%m-%Y"],
        help_text="Format: DD-MM-YYYY",
        validators=[validate_age],
    )
    phone = forms.CharField(
        max_length=15,
        validators=[validate_phone_number],
    )
    city = forms.ChoiceField(choices=CustomUser.CITY_CHOICES, initial="Casablanca")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone", "city", "birth_date")


class CustomUserChangeForm(UserChangeForm):
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"onfocus": "(this.type='date')"}),
        input_formats=["%d-%m-%Y"],
        help_text="Format: DD-MM-YYYY",
        validators=[validate_age],
    )
    phone = forms.CharField(
        max_length=15,
        validators=[validate_phone_number],
    )

    class Meta:
        model = CustomUser
        fields = ("email", "phone", "city", "birth_date")
