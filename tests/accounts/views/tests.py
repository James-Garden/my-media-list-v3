from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class LoginTests(TestCase):
    url = reverse("accounts:login")

    def setUp(self):
        self.user = User.objects.create_user(username="john_smith", email="john_smith@email.com", password="password")

    def test_login_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/login.html')
        self.assertIsInstance(response.context_data['form'], AuthenticationForm)

    def test_login_invalid_details(self):
        response = self.client.post(self.url, {
            'username': "wrong username",
            'password': "wrong password"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data['form'].errors) == 1)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_valid_details(self):
        response = self.client.post(self.url, {
            'username': "john_smith",
            'password': "password"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profiles:profile'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))
