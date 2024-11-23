from contextlib import nullcontext
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tango.models import Member, Occupation, Activity, Category, Place, Opinion


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
    phone_number = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone_number: only numbers, "
                               "not spaces and chars",
                "class": "form-control"
            }
        )
    )
    occupations = forms.ModelMultipleChoiceField(
        queryset=Occupation.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "selected_occupation": "Tanguero",
                "class": "form-control-check"
            }
        ),
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
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "occupations",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Occupation.objects.exists():
            self.fields["occupations"].initial = Occupation.objects.filter(
                name="Tanguero"
            )
        else:
            self.fields["occupations"].initial = None


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
        required=False,
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
        choices=[
            (0, "MONDAY"),
            (1, "TUESDAY"),
            (2, "WEDNESDAY"),
            (3, "THURSDAY"),
            (4, "FRIDAY"),
            (5, "SATURDAY"),
            (6, "SUNDAY"),
        ],
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
        required=False,
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


class OccupationCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Occupation's name "
                               "in one word with a capital letter",
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Brief description "
                               "of this role in the Tango community",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Occupation
        fields = ("name", "description")


class CategoryCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tango activity category's name",
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Brief description of this category in Tango",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Category
        fields = ("name", "description")


class PlaceCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Place name",
                "class": "form-control"
            }
        )
    )
    city = forms.CharField(
        required=False,
        widget=forms.Select(
            attrs={
                "placeholder": "Select city",
                "class": "form-control",
            }
        )
    )
    new_city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter new city if not listed",
                "class": "form-control",
            }
        )
    )
    direction = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Direction: street, number...",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Place
        fields = ("name", "city", "new_city", "direction")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Place.objects.exists():
            self.fields["city"].widget.choices = (
                    [("", "--no selected city--")]
                    +
                    [
                        (city["city"], city["city"])
                        for city in Place.objects.values("city")
                        .distinct().order_by("city")
                    ]
            )
        else:
            self.fields["city"].widget.choices = [("", "--no selected city--")]


class MemberSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=180,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by member's Last Name...",
                "class": "form-control",
            },
        ),
    )


class ActivitySearchForm(forms.Form):
    day_of_week = forms.ChoiceField(
        required=False,
        label="",
        choices=[
            ("", "--no selected day--"),
            (0, "MONDAY"),
            (1, "TUESDAY"),
            (2, "WEDNESDAY"),
            (3, "THURSDAY"),
            (4, "FRIDAY"),
            (5, "SATURDAY"),
            (6, "SUNDAY"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )


class OpinionForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "cols": "80",
                "rows": "2",
                "placeholder": "Add your opinion here...",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = Opinion
        fields = ("content", )


class MemberUpdateForm(UserChangeForm):
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
    phone_number = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone_number: "
                               "only numbers, not spaces and chars",
                "class": "form-control"
            }
        )
    )
    occupations = forms.ModelMultipleChoiceField(
        queryset=Occupation.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "selected_occupation": "Tanguero",
                "class": "form-control-check"
            }
        ),
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
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "occupations",
            "password1",
            "password2",
        )
