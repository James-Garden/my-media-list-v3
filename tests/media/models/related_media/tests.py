from django.test import TestCase

from media.models import Media, RelatedMedia, Film, Book, Series


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

        self.assertEqual(relation.media1, self.media1)
        self.assertEqual(relation.media2, self.media2)
        self.assertEqual(relation.relationship, Media.SEQUEL)

    def test_add_related_media(self):
        self.media1.add_related_media(self.media2)
        relation = RelatedMedia.objects.get()

        self.assertEqual(relation.media1, self.media2)
        self.assertEqual(relation.media2, self.media1)
        self.assertEqual(relation.relationship, Media.RELATED)

    def test_get_sequels(self):
        RelatedMedia.objects.create(media1=self.media2, media2=self.media1, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media3, media2=self.media1, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.RELATED)
        self.assertQuerysetEqual(self.media1.get_sequels(), [self.media2, self.media3], ordered=False)

    def test_get_prequels(self):
        RelatedMedia.objects.create(media1=self.media1, media2=self.media2, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media1, media2=self.media3, relationship=Media.SEQUEL)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.RELATED)
        self.assertQuerysetEqual(self.media1.get_prequels(), [self.media2, self.media3], ordered=False)

    def test_get_related_media(self):
        RelatedMedia.objects.create(media1=self.media2, media2=self.media1, relationship=Media.RELATED)
        RelatedMedia.objects.create(media1=self.media1, media2=self.media3, relationship=Media.RELATED)
        RelatedMedia.objects.create(media1=self.media4, media2=self.media1, relationship=Media.SEQUEL)
        self.assertQuerysetEqual(self.media1.get_related_media(), [self.media2, self.media3], ordered=False)
