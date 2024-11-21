from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase


from tango.forms import (
    SignUpForm, ActivityCreationForm, OccupationCreationForm, CategoryCreationForm,
    PlaceCreationForm, MemberSearchForm, ActivitySearchForm, OpinionForm
)
from tango.models import Occupation, Category, Place, Activity


class SignUpFormTest(TestCase):
    def setUp(self):
        self.occupation = Occupation.objects.create(name="Test occupation")

    def test_valid_form(self):
        form_data = {
            "username": "testmember",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "email": "testmember@test.com",
            "phone_number": "1234567890",
            "occupations": [self.occupation.id],
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        member = form.save()
        self.assertIn(self.occupation, member.occupations.all())

    def test_phone_number_field(self):
        form_data = {
            "username": "testmember",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "email": "testmember@test.com",
            "phone_number": "12345abc",
            "occupations": [self.occupation.id],
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_occupations_field(self):
        form_data = {
            "username": "testmember",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "email": "testmember@test.com",
            "phone_number": "1234567890",
            "occupations": [],
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("occupations", form.errors)

    def test_form_widget(self):
        form = SignUpForm()
        self.assertIsInstance(
            form.fields["occupations"].widget,
            forms.CheckboxSelectMultiple
        )


class FormsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test category")
        self.location = Place.objects.create(name="Test location", city="Test city", direction="Test direction")
        self.occupation = Occupation.objects.create(name="Test occupation")
        self.member = get_user_model().objects.create_user(
            username="testmember",
            first_name="TestFirst",
            last_name="TestLast",
            email="testmember@test.com",
            phone_number="1234567890",
            password="testpassword",
        )
        self.activity = Activity.objects.create(
            name="Test Activity1",
            category=self.category,
            possessor=self.member,
            day_of_week="0",
            start_time="15:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes",
        )
        self.client.force_login(self.member)

    def test_new_occupation(self):
        form_data = {
            "name": "occupation_name",
            "description": "occupation_description",
        }
        form = OccupationCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_category(self):
        form_data = {
            "name": "category_name",
            "description": "category_description",
        }
        form = CategoryCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_place(self):
        form_data = {
            "name": "place_name",
            "city": "place_city",
            "direction": "place_direction",
        }
        form = PlaceCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_activity(self):
        form_data = {
            "name": "activity_name",
            "category": self.category.id,
            "possessor": self.member.id,
            "location": self.location.id,
            "day_of_week": 0,
            "start_time": "10:00",
            "end_time": "11:00",
            "price": "7.50",
            "additional_notes": "Test additional notes"
        }

        form = ActivityCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_opinion(self):
        form_data = {
            "user": self.member.id,
            "activity": self.activity.id,
            "content": "Opinion about this activity",
        }
        form = OpinionForm(data=form_data)
        self.assertTrue(form.is_valid())


class SearchFormTest(TestCase):
    def test_activity_search_form(self):
        form_data = {"day_of_week": "0"}
        form = ActivitySearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"day_of_week": ""}
        form = ActivitySearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertIsInstance(form.fields["day_of_week"].widget, forms.Select)

    def test_member_search_form(self):
        form_data = {"last_name": "Test"}
        form = MemberSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"last_name": ""}
        form = MemberSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertIsInstance(form.fields["last_name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["last_name"].widget.attrs["placeholder"],
            "Search by member's Last Name..."
        )
        self.assertEqual(form.fields["last_name"].max_length, 180)
