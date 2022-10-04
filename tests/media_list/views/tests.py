from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from media.models import Media, Book, Film, Series
from media_list.models import ListEntry


class MediaListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="john_smith", email="john.smith@test.com", password="password")
        book = Media.create_book(title="Book", release_status=Book.PUBLISHED)
        film = Media.create_film(title="Film", release_status=Film.RELEASED)
        series = Media.create_series(title="Series", airing_status=Series.FINISHED_AIRING)
        self.book_list_entry = ListEntry.objects.create(media=book, user=self.user)
        self.film_list_entry = ListEntry.objects.create(media=film, user=self.user)
        self.series_list_entry = ListEntry.objects.create(media=series, user=self.user)

    def test_own_lists_not_logged_in(self):
        list_urls = [
            reverse('media_list:book-list'),
            reverse('media_list:film-list'),
            reverse('media_list:series-list'),
        ]

        for list_url in list_urls:
            expected_redirect_url = f"{reverse('accounts:login')}?next={list_url}"

            response = self.client.get(list_url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, expected_redirect_url)

    def test_own_book_list(self):
        book_list_url = reverse('media_list:book-list')

        self.client.login(username="john_smith", password="password")
        response = self.client.get(book_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.book_list_entry])

    def test_other_user_book_list(self):
        book_list_url = reverse('media_list:book-list', kwargs={'username': self.user.username})

        response = self.client.get(book_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.book_list_entry])

    def test_own_film_list(self):
        film_list_url = reverse('media_list:film-list')

        self.client.login(username="john_smith", password="password")
        response = self.client.get(film_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.film_list_entry])

    def test_other_user_film_list(self):
        film_list_url = reverse('media_list:film-list', kwargs={'username': self.user.username})

        response = self.client.get(film_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.film_list_entry])

    def test_own_series_list(self):
        series_list_url = reverse('media_list:series-list')

        self.client.login(username="john_smith", password="password")
        response = self.client.get(series_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.series_list_entry])

    def test_other_user_series_list(self):
        series_list_url = reverse('media_list:series-list', kwargs={'username': self.user.username})

        response = self.client.get(series_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['media_list/list.html'])
        self.assertQuerysetEqual(response.context_data['list_objects'], [self.series_list_entry])
