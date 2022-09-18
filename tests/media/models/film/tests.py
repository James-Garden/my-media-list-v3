from django.db import IntegrityError, transaction
from django.test import TestCase

from media.models import Media, Film


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
