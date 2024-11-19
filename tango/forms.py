from contextlib import nullcontext

from django import forms

from django.contrib.auth.forms import UserCreationForm


from tango.models import Member, Occupation, Activity, Category, Place

"""
Copyright (c) 2019 - present AppSeed.us
"""
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


"""
Copyright (c) 2019 - present AppSeed.us
--changed--
"""
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Contact phone number",
                "class": "form-control"
            }
        ))
    occupations = forms.ModelMultipleChoiceField(
        queryset=Occupation.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Member
        fields = ("username", "first_name", "last_name", "email", "phone_number", "occupations", "password1", "password2")


class ActivityCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Activity's name",
                "class": "form-control placeholder-lg"
            }
        ))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="--no category selected--",
        widget=forms.Select(
            attrs={
                "placeholder": "Select category",
                "class": "text-muted form-control",
            }
        ),
        required=True,
    )
    location = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        empty_label="--no location selected--",
        widget=forms.Select(
            attrs={
                "placeholder": "Select location",
                "class": "text-muted form-control",
            }
        ),
    )
    day_of_week = forms.ChoiceField(
        choices=[(0, "MONDAY"), (1, "TUESDAY"), (2, "WEDNESDAY"), (3, "THURSDAY"), (4, "FRIDAY"), (5, "SATURDAY"),
                 (6, "SUNDAY"), ],
        widget=forms.Select(
            attrs={
                "placeholder": "Select day of the week",
                "class": "form-control form-control-sm",
            }
        )
    )
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={
            "type": "time",
            "placeholder": "Start time",
            "class": "form-control form-control-sm",
        }
    ))
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={
            "type": "time",
            "placeholder": "End time",
            "class": "form-control form-control-sm",
        }
    ))
    price = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "placeholder": "Price in dollars",
                "class": "form-control",
            },
        )
    )
    additional_notes = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Additional information here...",
                "class": "form-control",
            }
        )
    )
    class Meta:
        model = Activity
        possessor = nullcontext
        fields = ("name", "category", "possessor", "location",
                  "day_of_week", "start_time", "end_time", "price",
                  "additional_notes")



class PlaceCreationForm(forms.ModelForm):
    pass
    # name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Place name",
    #             "class": "form-control"
    #         }
    #     )
    # )
    # city = forms.CharField(
    #     widget=forms.Select(
    #         choices=[(city["city"], city["city"]) for city in Place.objects.values("city").distinct()],
    #         attrs={
    #             "placeholder": "Select city",
    #             "class": "form-control",
    #         }
    #     )
    # )
    # new_city = forms.CharField(
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Enter new city if not listed",
    #             "class": "form-control",
    #         }
    #     )
    # )
    # direction = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Direction: street, number...",
    #             "class": "form-control"
    #         }
    #     )
    # )
    #
    # class Meta:
    #     model = Place
    #     fields = ("name", "city", "new_city", )
    #
