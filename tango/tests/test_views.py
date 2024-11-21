from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tango.models import Occupation, Category, Place, Member, Activity

MEMBERS_URL = reverse("tango:member-list")
ACTIVITIES_URL = reverse("tango:activity-list")
PLACES_URL = reverse("tango:place-list")


class PublicTest(TestCase):   # not REGISTERED users
    def test_home_login_required(self):
        res = self.client.get(reverse("tango:index"))
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.url, "/login/?next=/")

    def test_members_login_required(self):
        res = self.client.get(MEMBERS_URL)
        self.assertNotEqual(res.status_code, 404)
        self.assertEqual(res.url, "/accounts/login/?next=/members/")

    def test_activities_login_required(self):
        res = self.client.get(ACTIVITIES_URL)
        self.assertNotEqual(res.status_code, 404)
        self.assertEqual(res.url, "/accounts/login/?next=/activities/")

    def test_places_login_required(self):
        res = self.client.get(PLACES_URL)
        self.assertNotEqual(res.status_code, 404)
        self.assertEqual(res.url, "/accounts/login/?next=/places/")


class PrivateTest(TestCase):  # REGISTERED users
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.occupation = Occupation.objects.create(
            name="Test_occupation",
            description="Description Test_occupation"
        )
        self.place = Place.objects.create(
            name="Test Place",
            city="TestCity",
            direction="TestDirection",
        )
        self.user.occupations.add(self.occupation)

        self.category = Category.objects.create(
            name="Test Category",
            description="Description Test Category",
        )
        self.activity1 = Activity.objects.create(
            name="Test Activity1",
            category=self.category,
            possessor=self.user,
            day_of_week="0",
            start_time="15:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes 1",
        )
        self.activity2 = Activity.objects.create(
            name="Test Activity2",
            category=self.category,
            possessor=self.user,
            location=self.place,
            day_of_week="3",
            start_time="10:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes 2",
        )

    def test_retrieve_members(self):
        get_user_model().objects.create_user(
            username="test1",
            first_name="BBB_FirstTest",
            last_name="AAA_LastTest",
            email="test1@test.com",
            phone_number="1112223331",
            password="testpassword1",
        )
        get_user_model().objects.create_user(
            username="test2",
            first_name="AAA_FirstTest",
            last_name="AAA_LastTest",
            email="test2@test.com",
            phone_number="1112223332",
            password="testpassword2",
        )
        get_user_model().objects.create_user(
            username="test3",
            first_name="AAA_FirstTest",
            last_name="BBB_LastTest",
            email="test3@test.com",
            phone_number="1112223333",
            password="testpassword3",
        )
        response = self.client.get(MEMBERS_URL)
        self.assertEqual(response.status_code, 200)
        members = Member.objects.all()
        self.assertEqual(
            list(response.context["member_list"]),
            list(members)
        )
        self.assertTemplateUsed(response, "tango/member_list.html")

    def test_retrieve_activity(self):
        response = self.client.get(ACTIVITIES_URL)
        self.assertEqual(response.status_code, 200)
        activities = Activity.objects.all()
        self.assertEqual(
            list(response.context["activity_list"]),
            list(activities)
        )
        self.assertTemplateUsed(response, "tango/activity_list.html")

    def test_retrieve_places(self):
        response = self.client.get(PLACES_URL)
        self.assertEqual(response.status_code, 200)
        places = Place.objects.all()
        self.assertEqual(
            list(response.context["place_list"]),
            list(places)
        )
        self.assertTemplateUsed(response, "tango/place_list.html")
