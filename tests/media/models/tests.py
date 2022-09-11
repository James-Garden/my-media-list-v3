from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from media.models import Media, Film, Series, Book, RelatedMedia


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


class RelatedMediaTests(TestCase):
    def setUp(self):
        self.media1 = Media.create_film(title='2001: A Space Odyssey', release_status=Film.RELEASED)
        self.media2 = Media.create_book(title='The Martian', release_status=Book.PUBLISHED)
        self.media3 = Media.create_series(title='The Expanse Season 1', airing_status=Series.FINISHED_AIRING)
        self.media4 = Media.create_series(title='The Expanse Season 2', airing_status=Series.FINISHED_AIRING)

    def test_add_sequel(self):
        self.media1.add_sequel(self.media2)
        relation = RelatedMedia.objects.get()

        self.assertEqual(relation.media1, self.media2)
        self.assertEqual(relation.media2, self.media1)
        self.assertEqual(relation.relationship, Media.SEQUEL)

    def test_add_prequel(self):
        self.media1.add_prequel(self.media2)
        relation = RelatedMedia.objects.get()

        self.assertEqual(relation.media1, self.media2)
        self.assertEqual(relation.media2, self.media1)
        self.assertEqual(relation.relationship, Media.PREQUEL)

    def test_add_related_media(self):
        self.media1.add_related_media(self.media2)
        relation = RelatedMedia.objects.get()

        self.assertEqual(relation.media1, self.media2)
        self.assertEqual(relation.media2, self.media1)
        self.assertEqual(relation.relationship, Media.RELATED)

    def test_get_sequels(self):
        RelatedMedia.objects.create(media1=self.media2, media2=self.media1, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media1, media2=self.media3, relationship=Media.PREQUEL)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.RELATED)
        self.assertQuerysetEqual(self.media1.get_sequels(), [self.media2, self.media3], ordered=False)

    def test_get_prequels(self):
        RelatedMedia.objects.create(media1=self.media2, media2=self.media1, relationship=Media.PREQUEL)
        RelatedMedia.objects.create(media1=self.media1, media2=self.media3, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.RELATED)
        self.assertQuerysetEqual(self.media1.get_prequels(), [self.media2, self.media3], ordered=False)

    def test_get_related_media(self):
        RelatedMedia.objects.create(media1=self.media2, media2=self.media1, relationship=Media.RELATED)
        RelatedMedia.objects.create(media1=self.media1, media2=self.media3, relationship=Media.RELATED)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.SEQUEL)
        self.assertQuerysetEqual(self.media1.get_related_media(), [self.media2, self.media3], ordered=False)


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
