from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from tango.models import Occupation, Place, Activity, Category, Opinion


class ModelTests(TestCase):
    def setUp(self):
        self.member1 = get_user_model().objects.create_user(
            username="test1",
            first_name="BBB_FirstTest",
            last_name="AAA_LastTest",
            email="test1@test.com",
            phone_number="1112223331",
            password="testpassword1",
        )
        self.member2 = get_user_model().objects.create_user(
            username="test2",
            first_name="AAA_FirstTest",
            last_name="AAA_LastTest",
            email="test2@test.com",
            phone_number="1112223332",
            password="testpassword2",
        )
        self.member3 = get_user_model().objects.create_user(
            username="test3",
            first_name="AAA_FirstTest",
            last_name="BBB_LastTest",
            email="test3@test.com",
            phone_number="1112223333",
            password="testpassword3",
        )
        self.occupation1 = Occupation.objects.create(
            name="BBB Test_occupation",
            description="Description Test_occupation BBB"
        )
        self.occupation2 = Occupation.objects.create(
            name="AAA Test_occupation",
            description="Description Test_occupation AAA"
        )
        self.place1 = Place.objects.create(
            name="BBB Test Place",
            city="TestCity",
            direction="TestDirection1",
        )
        self.place2 = Place.objects.create(
            name="AAA Test Place",
            city="TestCity",
            direction="TestDirection2",
        )
        self.member1.occupations.add(self.occupation1)

        self.category1 = Category.objects.create(
            name="BBB Test Category",
            description="Description Test Category BBB",
        )
        self.category2 = Category.objects.create(
            name="AAA Test Category",
            description="Description Test Category AAA",
        )
        self.activity = Activity.objects.create(
            name="Test Activity",
            category=self.category1,
            possessor=self.member1,
            location=self.place1,
            day_of_week="0",
            start_time="21:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes",
        )
        self.activity1 = Activity.objects.create(
            name="Test Activity1",
            category=self.category1,
            possessor=self.member1,
            day_of_week="0",
            start_time="15:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes 1",
        )
        self.activity2 = Activity.objects.create(
            name="Test Activity2",
            category=self.category1,
            possessor=self.member1,
            location=self.place1,
            day_of_week="3",
            start_time="10:00",
            end_time="23:00",
            price="1",
            additional_notes="Test Additional Notes 2",
        )
        self.opinion1 = Opinion.objects.create(
            user=self.member1,
            activity=self.activity1,
            content="Test Opinion 1",
        )

    def test_category_ordering_by_name(self):
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "AAA Test Category")
        self.assertEqual(categories[1].name, "BBB Test Category")

    def test_category_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="AAA Test Category",
                description="Description Test Category CCC",
            )

    def test_occupation_ordering_by_name(self):
        occupations = Occupation.objects.all()
        self.assertEqual(occupations[0].name, "AAA Test_occupation")
        self.assertEqual(occupations[1].name, "BBB Test_occupation")

    def test_occupation_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Occupation.objects.create(
                name="AAA Test_occupation",
                description="Description Test occupation CCC",
            )

    def test_place_ordering_by_name(self):
        places = Place.objects.all()
        self.assertEqual(places[0].name, "AAA Test Place")
        self.assertEqual(places[1].name, "BBB Test Place")

    def test_member_ordering_by_last_name_first_name_and_str_test(self):
        members = get_user_model().objects.all()
        self.assertEqual(str(members[0]), "AAA_LastTest AAA_FirstTest")
        self.assertEqual(str(members[1]), "AAA_LastTest BBB_FirstTest")
        self.assertEqual(str(members[2]), "BBB_LastTest AAA_FirstTest")

    def test_member_phone_number_is_unique(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="test4",
                first_name="BBB_FirstTest",
                last_name="CCC_LastTest",
                email="test4@test.com",
                phone_number="1112223331",
                password="testpassword4",
            )

    def test_activity_verbose_name_plural(self):
        self.assertEqual(
            str(self.activity._meta.verbose_name_plural),
            "activities"
        )

    def test_activity_ordering_by_day_of_week_to_start_time(self):
        activities = Activity.objects.all()
        self.assertEqual(activities[0].day_of_week, 0)
        self.assertEqual(str(activities[0].start_time), "15:00:00")
        self.assertEqual(activities[1].day_of_week, 0)
        self.assertEqual(str(activities[1].start_time), "21:00:00")
        self.assertEqual(activities[2].day_of_week, 3)
        self.assertEqual(str(activities[2].start_time), "10:00:00")

    def test_activity_str(self):
        self.assertEqual(
            str(self.activity),
            f"{self.activity.name} ({self.activity.location.name})"
        )
        self.assertEqual(
            str(self.activity1),
            f"{self.activity1.name} (No location)"
        )

    def test_opinion_ordering_by_created_time_reverse(self):
        Opinion.objects.create(
            user=self.member2,
            activity=self.activity1,
            content="Test Opinion 2",
        )
        opinions = Opinion.objects.all()
        self.assertEqual(opinions[0].content, "Test Opinion 1")
        self.assertEqual(opinions[1].content, "Test Opinion 2")
