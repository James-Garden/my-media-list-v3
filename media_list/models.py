from django.db import models
from django.db.models import Q

from accounts.models import User
from media.models import Media


class ListEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    score = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    progress = models.IntegerField(default=0, blank=True)

    class Meta:
        unique_together = ['user', 'media']

    @classmethod
    def get_user_film_list(cls, user: User):
        return cls._get_user_list_entries(user, media_type=Media.FILM)

    @classmethod
    def get_user_series_list(cls, user: User):
        return cls._get_user_list_entries(user, media_type=Media.SERIES)

    @classmethod
    def get_user_book_list(cls, user: User):
        return cls._get_user_list_entries(user, media_type=Media.BOOK)

    def __str__(self):
        return f"<{self.__class__}: [{self.user}: [{self.media}]>"

    @classmethod
    def _get_user_list_entries(cls, user: User, media_type=None):
        query = Q(user=user)
        if media_type is not None:
            query = Q(media__media_type=media_type) & query

        return cls.objects.filter(query)
