from django.db import models

BBFC_RATINGS = [
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

    media_type = models.CharField(max_length=1, choices=MEDIA_TYPES, blank=False, default=None)
    title = models.CharField(max_length=250, default=None)
    local_title = models.CharField(max_length=250, null=True,
                                   help_text="The title of the film in its original language, blank if english")
    description = models.TextField(null=True)
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    members = models.IntegerField(default=0)
    prequels = models.ManyToManyField('self',
                                      help_text="Any related media set before this one, with nothing else in between")
    sequels = models.ManyToManyField('self',
                                     help_text="Any related media set after this one, with nothing else in between")
    related_media = models.ManyToManyField('self',
                                           help_text="Any media related to this but not before or after it")

    def get_subclass(self):
        if self.media_type == Media.FILM:
            return self.film
        elif self.media_type == Media.SERIES:
            return self.series
        elif self.media_type == Media.BOOK:
            return self.book
        raise AttributeError(f"Media with ID [{self.pk}] has invalid media_type: <{self.media_type!r}>")


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
    rating = models.CharField(max_length=3, choices=RATINGS,
                              help_text="The BBFC age rating of this series, rounded down from local age rating if "
                                        "none exists")
    release_status = models.CharField(max_length=1, choices=RELEASE_STATUSES, default=None)


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
    episodes = models.IntegerField(help_text="The number of episodes in this TV series", null=True)
    rating = models.CharField(max_length=3, choices=RATINGS,
                              help_text="The BBFC age rating of this series, rounded down from local age rating if "
                                        "none exists")
    airing_status = models.CharField(max_length=1, choices=AIRING_STATUSES, default=None)


class Book(models.Model):
    NOT_PUBLISHED = 'N'
    PUBLISHED = 'P'
    RELEASE_STATUSES = [
        (NOT_PUBLISHED, "Not yet published"),
        (PUBLISHED, "Published")
    ]

    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    chapters = models.IntegerField(help_text="The number of chapters in this book", null=True)
    release_status = models.CharField(max_length=1, choices=RELEASE_STATUSES, default=None)
