from django.db import IntegrityError, transaction
from django.test import TestCase

from media.models import Media, Series


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
        Series.objects.create(media=self.media, airing_status=Series.FINISHED_AIRING)

        self.media.delete()

        items = Series.objects.all()

        self.assertQuerysetEqual(items, [])
