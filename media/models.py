from typing import Dict

from django.db import models, transaction, IntegrityError
from django.db.models import Q

BBFC_RATINGS = [
    ('TBC', "Not yet rated"),
    ('U', "Universal"),
    ('PG', "Parental guidance"),
    ('12A', "Cinema release suitable for 12 years and over"),
    ('12', "Video release suitable for 12 years and over"),
    ('15', "Suitable only for 15 years and over"),
    ('18', "Suitable only for adults"),
    ('R18', "Adults works for licensed premises only")
]


class Media(models.Model):
    FILM = 'F'
    SERIES = 'S'
    BOOK = 'B'
    MEDIA_TYPES = [
        (FILM, "Film"),
        (SERIES, "Series"),
        (BOOK, "Book")
    ]
    SEQUEL = 'S'
    RELATED = 'R'

    media_type = models.CharField(max_length=1, choices=MEDIA_TYPES, blank=False, default=None)
    title = models.CharField(max_length=250, default=None)
    local_title = models.CharField(max_length=250, null=True, blank=True,
                                   help_text="The title of the film in its original language, blank if english")
    description = models.TextField(null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    members = models.IntegerField(default=0)
    related_media = models.ManyToManyField('self', blank=True,
                                           through='RelatedMedia', through_fields=('media1', 'media2'),
                                           help_text="Any media related to this but not before or after it")

    @staticmethod
    def create_film(**kwargs):
        return Media._create_media(Film, **kwargs)

    @staticmethod
    def create_series(**kwargs):
        return Media._create_media(Series, **kwargs)

    @staticmethod
    def create_book(**kwargs):
        return Media._create_media(Book, **kwargs)

    def add_sequel(self, sequel):
        self.add_related_media(sequel, relationship=Media.SEQUEL)

    def add_prequel(self, prequel):
        self.add_related_media(media1=self, media2=prequel, relationship=Media.SEQUEL)

    def add_related_media(self, media1, *, relationship=RELATED, media2=None):
        if media2 is None:
            media2 = self
        if RelatedMedia.objects.filter(Q(media1=media1) & Q(media2=media2) | Q(media2=media1) & Q(media1=media2)):
            raise IntegrityError(f"Key pair ({media1.pk}, {media2.pk}) already exists, remove it first")
        RelatedMedia.objects.create(media1=media1, media2=media2, relationship=relationship)

    def delete_related_media(self, media):
        RelatedMedia.objects.get(Q(media1=self) & Q(media2=media) | Q(media2=self) & Q(media1=media)).delete()

    def get_sequels(self):
        """Gets a QuerySet of Media objects to which self is a prequel, or which are sequel to self"""
        qs = RelatedMedia.objects.filter((Q(media2=self) & Q(relationship=Media.SEQUEL)))
        return self._get_related_from_qs(qs)

    def get_prequels(self):
        """Gets a QuerySet of Media objects to which self is a sequel, or which are prequel to self"""
        qs = RelatedMedia.objects.filter((Q(media1=self) & Q(relationship=Media.SEQUEL)))
        return self._get_related_from_qs(qs)

    def get_related_media(self):
        """Gets a QuerySet of Media objects to which self is related"""
        qs = RelatedMedia.objects.filter(
            (Q(media1=self) | Q(media2=self)) & Q(relationship=Media.RELATED))
        return self._get_related_from_qs(qs)

    def _get_related_from_qs(self, qs):
        """Gets a QuerySet of Media objects from a QuerySet of RelatedMedia objects, excluding the current object"""
        ids = set(qs.values_list('media1', flat=True)).union(set(qs.values_list('media2', flat=True)))
        return Media.objects.filter(pk__in=ids).exclude(pk=self.pk)

    @staticmethod
    @transaction.atomic
    def _create_media(model, **kwargs):
        types = {Film: Media.FILM, Series: Media.SERIES, Book: Media.BOOK}
        media_args, model_args = Media._split_args(model, **kwargs)
        media = Media.objects.create(media_type=types[model], **media_args)
        model.objects.create(media=media, **model_args)
        return media

    @staticmethod
    def _split_args(model, **kwargs) -> (Dict, Dict):
        media_args, type_args = dict(), dict()
        type_fields = [field.name for field in model._meta.fields]
        for arg, value in kwargs.items():
            if arg in type_fields:
                type_args[arg] = value
            else:
                media_args[arg] = value
        return media_args, type_args

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, type={self.get_media_type_display()!r})"

    def __str__(self):
        return self.title


class RelatedMedia(models.Model):
    RELATIONSHIPS = [
        (Media.SEQUEL, "Sequel"),
        (Media.RELATED, "Related")
    ]

    media1 = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="media1")
    media2 = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="media2")
    relationship = models.CharField(default=None, choices=RELATIONSHIPS, max_length=1,
                                    help_text="The relationship from media1 to media2, "
                                              "i.e. SEQUEL if media1 is the SEQUEL to media2")

    class Meta:
        unique_together = ['media1', 'media2']

    def __repr__(self):
        return f"{self.__class__.__name__}(media1={self.media1.title!r}" \
               f" {self.get_relationship_display().upper()} to " \
               f"media2={self.media2.title!r})"

    def __str__(self):
        return repr(self)


class Film(models.Model):
    RATINGS = BBFC_RATINGS
    NOT_YET_RELEASED = 'N'
    CURRENTLY_IN_CINEMAS = 'C'
    RELEASED = 'F'
    RELEASE_STATUSES = [
        (NOT_YET_RELEASED, "Not yet released"),
        (CURRENTLY_IN_CINEMAS, "Currently in cinemas"),
        (RELEASED, "Released")
    ]

    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    runtime = models.IntegerField(help_text="The total runtime of the film in minutes", null=True)
    rating = models.CharField(max_length=3, choices=RATINGS, blank=True, null=True,
                              help_text="The BBFC age rating of this series, rounded down from local age rating if "
                                        "none exists")
    release_status = models.CharField(max_length=1, choices=RELEASE_STATUSES, default=None)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.media=}, {self.get_release_status_display()})"

    def __str__(self):
        return self.media


class Series(models.Model):
    RATINGS = BBFC_RATINGS
    NOT_AIRED = 'N'
    CURRENTLY_AIRING = 'C'
    FINISHED_AIRING = 'F'
    AIRING_STATUSES = [
        (NOT_AIRED, "Not yet aired"),
        (CURRENTLY_AIRING, "Currently airing"),
        (FINISHED_AIRING, "Finished airing")
    ]

    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    episodes = models.IntegerField(help_text="The number of episodes in this TV series", null=True, blank=True)
    rating = models.CharField(max_length=3, choices=RATINGS, blank=True, null=True,
                              help_text="The BBFC age rating of this series, rounded down from local age rating if "
                                        "none exists")
    airing_status = models.CharField(max_length=1, choices=AIRING_STATUSES, default=None)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.media=}, {self.get_airing_status_display()})"

    def __str__(self):
        return self.media


class Book(models.Model):
    NOT_PUBLISHED = 'N'
    PUBLISHED = 'P'
    RELEASE_STATUSES = [
        (NOT_PUBLISHED, "Not yet published"),
        (PUBLISHED, "Published")
    ]

    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    chapters = models.IntegerField(help_text="The number of chapters in this book", null=True, blank=True)
    release_status = models.CharField(max_length=1, choices=RELEASE_STATUSES, default=None)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.media=}, {self.get_release_status_display()})"

    def __str__(self):
        return self.media
