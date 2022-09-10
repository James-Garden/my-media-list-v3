from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class ProfileTests(TestCase):
    url = reverse("profiles:profile")

    def setUp(self):
        self.user = User.objects.create_user(username="john_smith", email="john_smith@example.com", password="password")

    def test_own_profile_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:login")+"?next=/profile/")

    def test_own_profile_logged_in(self):
        self.client.login(username="john_smith", password="password")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['profiles/profile.html'])
        self.assertContains(response, "john_smith")

    def test_other_profile(self):
        other_user = User.objects.create_user(username="jane_smith", email="jane_smith@example.com", password="password")
        url = reverse("profiles:profile", kwargs={'username': other_user.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['profiles/profile.html'])
        self.assertContains(response, other_user.username)

    def test_other_profile_not_found(self):
        url = reverse("profiles:profile", kwargs={'username': "not existing user"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
