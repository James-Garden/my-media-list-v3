from django.test import TestCase

from accounts.models import User
from media.models import Media, Film, Book, Series
from media_list.models import ListEntry


class ListEntryModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="TestUser", email="test@example.com")
        self.user2 = User.objects.create_user(username="TestUser2", email="test2@example.com")
        self.book = Media.create_book(title="Book 1", release_status=Book.PUBLISHED)
        self.film = Media.create_film(title="Film 1", release_status=Film.RELEASED)
        self.series = Media.create_series(title="Series 1", airing_status=Series.FINISHED_AIRING)

    def test_create_list_entry(self):
        list_entry = ListEntry.objects.create(user=self.user, media=self.film)

        self.assertQuerysetEqual(ListEntry.objects.all(), [list_entry])

    def test_get_user_book_list(self):
        book_list_entry = ListEntry.objects.create(user=self.user, media=self.book)
        ListEntry.objects.create(user=self.user, media=self.film)
        ListEntry.objects.create(user=self.user, media=self.series)
        ListEntry.objects.create(user=self.user2, media=self.book)

        self.assertQuerysetEqual(ListEntry.get_user_book_list(self.user), [book_list_entry])

    def test_get_user_film_list(self):
        film_list_entry = ListEntry.objects.create(user=self.user, media=self.film)
        ListEntry.objects.create(user=self.user, media=self.book)
        ListEntry.objects.create(user=self.user, media=self.series)
        ListEntry.objects.create(user=self.user2, media=self.film)

        self.assertQuerysetEqual(ListEntry.get_user_film_list(self.user), [film_list_entry])

    def test_get_user_series_list(self):
        series_list_entry = ListEntry.objects.create(user=self.user, media=self.series)
        ListEntry.objects.create(user=self.user, media=self.film)
        ListEntry.objects.create(user=self.user, media=self.book)
        ListEntry.objects.create(user=self.user2, media=self.series)

        self.assertQuerysetEqual(ListEntry.get_user_series_list(self.user), [series_list_entry])
