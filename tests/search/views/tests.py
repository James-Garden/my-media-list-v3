from django.contrib.messages import get_messages
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class InvalidSearchTestCase(TestCase):
    def test_search_no_params(self):
        response = self.client.get(reverse("search:index"))
        messages = [message_obj.message for message_obj in list(get_messages(response.wsgi_request))]

        self.assertEqual(response.status_code, 302)
        self.assertIn("!warning Search query must be at least 3 characters.", messages)

    def test_search_too_short(self):
        response = self.client.get(reverse("search:index"), {
            'query': 'ab'
        })
        messages = [message_obj.message for message_obj in list(get_messages(response.wsgi_request))]

        self.assertEqual(response.status_code, 302)
        self.assertIn("!warning Search query must be at least 3 characters.", messages)

    def test_search_no_type(self):
        response = self.client.get(reverse("search:index"), {
            'query': 'abc'
        })
        messages = [message_obj.message for message_obj in list(get_messages(response.wsgi_request))]

        self.assertEqual(response.status_code, 302)
        self.assertIn("!danger Invalid search type.", messages)

    def test_search_invalid_type(self):
        response = self.client.get(reverse("search:index"), {
            'query': 'abc',
            'type': 'invalid_type'
        })
        messages = [message_obj.message for message_obj in list(get_messages(response.wsgi_request))]

        self.assertEqual(response.status_code, 302)
        self.assertIn("!danger Invalid search type.", messages)

    def test_search_invalid_with_referer(self):
        response = self.client.get(reverse("search:index"), {
            'referer': '/home/'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')


class UserSearchTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testUser1",
                                              email="test1@test.com",
                                              first_name="John")
        self.user2 = User.objects.create_user(username="testUser2",
                                              email="test2@test.com",
                                              last_name="Smith")

    def test_user_search_redirect(self):
        response = self.client.get(reverse("search:index"), {
            'query': 'abc',
            'type': 'users'
        })

        url = reverse("search:users") + "?query=abc"

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

    def test_user_search_has_results(self):
        response = self.client.get(reverse("search:users"), {
            'query': 'test'
        })

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['object_list'], [self.user1, self.user2])

    def test_user_search_by_first_name(self):
        response = self.client.get(reverse("search:users"), {
            'query': 'john'
        })

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['object_list'], [self.user1])

    def test_user_search_by_last_name(self):
        response = self.client.get(reverse("search:users"), {
            'query': 'smith'
        })

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['object_list'], [self.user2])

    def test_user_search_no_results(self):
        response = self.client.get(reverse("search:users"), {
            'query': 'query with no response'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found for 'query with no response'")
        self.assertQuerysetEqual(response.context_data['object_list'], [])
