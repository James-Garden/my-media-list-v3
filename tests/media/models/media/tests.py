from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from media.models import Media, Film, Series, Book


class MediaModelTests(TestCase):
    def test_create_media(self):
        media = Media.objects.create(media_type=Media.FILM, title="Source Code")
        items = Media.objects.all()

        self.assertQuerysetEqual(items, [media])

    def test_create_media_no_params(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.objects.create()
        items = Media.objects.all()

        self.assertQuerysetEqual(items, [])

    def test_create_media_no_media_type(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.objects.create(title="Source Code")
        items = Media.objects.all()

        self.assertQuerysetEqual(items, [])

    def test_create_media_no_title(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.objects.create(media_type=Media.FILM)
        items = Media.objects.all()

        self.assertQuerysetEqual(items, [])

    def test_create_book(self):
        media = Media.create_book(title='Book 1', release_status=Book.PUBLISHED)
        book = media.book

        self.assertQuerysetEqual(Media.objects.all(), [media])
        self.assertQuerysetEqual(Book.objects.all(), [book])
        self.assertEqual(media.title, 'Book 1')
        self.assertEqual(book.media, media)
        self.assertEqual(book.release_status, Book.PUBLISHED)

    def test_create_book_missing_params(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_book(title='Book 2')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_book(release_status=Book.PUBLISHED)

        self.assertQuerysetEqual(Media.objects.all(), [])
        self.assertQuerysetEqual(Book.objects.all(), [])

    def test_create_film(self):
        media = Media.create_film(title='Film 1', release_status=Film.RELEASED)
        film = media.film

        self.assertQuerysetEqual(Media.objects.all(), [media])
        self.assertQuerysetEqual(Film.objects.all(), [film])
        self.assertEqual(media.title, 'Film 1')
        self.assertEqual(film.media, media)
        self.assertEqual(film.release_status, Film.RELEASED)

    def test_create_film_missing_params(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_film(title='Film 2')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_film(release_status=Film.RELEASED)

        self.assertQuerysetEqual(Media.objects.all(), [])
        self.assertQuerysetEqual(Book.objects.all(), [])

    def test_create_series(self):
        media = Media.create_series(title='Series 1', airing_status=Series.FINISHED_AIRING)
        series = media.series

        self.assertQuerysetEqual(Media.objects.all(), [media])
        self.assertQuerysetEqual(Series.objects.all(), [series])
        self.assertEqual(media.title, 'Series 1')
        self.assertEqual(series.media, media)
        self.assertEqual(series.airing_status, Series.FINISHED_AIRING)

    def test_create_series_missing_params(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_series(title='Series 2')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Media.create_series(airing_status=Series.FINISHED_AIRING)

        self.assertQuerysetEqual(Media.objects.all(), [])
        self.assertQuerysetEqual(Book.objects.all(), [])
