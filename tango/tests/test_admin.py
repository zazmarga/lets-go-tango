from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.member = get_user_model().objects.create_user(
            username="member1",
            password="testmember1",
            phone_number="11-2299-0133"
        )

    def test_member_phone_number_listed(self):
        """
        Test that member's phone number is in display-list of admin page
        """
        url = reverse("admin:tango_member_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.member.phone_number)

    def test_member_phone_number_change(self):
        """
        Test that member's phone number is in detail member's admin page
        """
        url = reverse("admin:tango_member_change", args=[self.member.pk])
        res = self.client.get(url)
        self.assertContains(res, self.member.phone_number)
