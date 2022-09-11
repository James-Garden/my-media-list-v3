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


class FilmModelTests(TestCase):
    def setUp(self):
        self.media = Media.objects.create(media_type=Media.FILM, title="The Martian")

    def test_create_film(self):
        film = Film.objects.create(media=self.media, release_status=Film.RELEASED)
        films = Film.objects.all()

        self.assertQuerysetEqual(films, [film])

    def test_create_film_no_media(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Film.objects.create(release_status=Film.RELEASED)

        items = Film.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_create_film_no_status(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Film.objects.create(media=self.media)

        items = Film.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_delete_media_cascade(self):
        Film.objects.create(media=self.media, release_status=Film.RELEASED)

        self.media.delete()

        films = Film.objects.all()

        self.assertQuerysetEqual(films, [])


class SeriesModelTests(TestCase):
    def setUp(self):
        self.media = Media.objects.create(media_type=Media.SERIES, title="The Expanse")

    def test_create_series(self):
        series = Series.objects.create(media=self.media, airing_status=Series.FINISHED_AIRING)
        series_qs = Series.objects.all()

        self.assertQuerysetEqual(series_qs, [series])

    def test_create_series_no_media(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Series.objects.create(airing_status=Series.FINISHED_AIRING)

        items = Series.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_create_film_no_status(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Series.objects.create(media=self.media)

        items = Series.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_delete_media_cascade(self):
        Series.objects.create(media=self.media, airing_status=Film.RELEASED)

        self.media.delete()

        items = Series.objects.all()

        self.assertQuerysetEqual(items, [])


class BookModelTests(TestCase):
    def setUp(self):
        self.media = Media.objects.create(media_type=Media.BOOK, title="Permanent Record")

    def test_create_book(self):
        book = Book.objects.create(media=self.media, release_status=Book.PUBLISHED)
        items = Book.objects.all()

        self.assertQuerysetEqual(items, [book])

    def test_create_book_no_media(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Book.objects.create(release_status=Book.PUBLISHED)

        items = Book.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_create_book_no_status(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Book.objects.create(media=self.media)

        items = Book.objects.all()
        self.assertQuerysetEqual(items, [])

    def test_delete_media_cascade(self):
        Book.objects.create(media=self.media, release_status=Book.PUBLISHED)

        self.media.delete()

        items = Book.objects.all()

        self.assertQuerysetEqual(items, [])
