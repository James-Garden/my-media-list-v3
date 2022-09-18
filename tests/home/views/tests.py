from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['home/index.html'])
