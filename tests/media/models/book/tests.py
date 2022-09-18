from django.db import IntegrityError, transaction
from django.test import TestCase

from media.models import Media, Book


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
